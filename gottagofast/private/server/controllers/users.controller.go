package controllers

import (
	"context"
	"encoding/json"
	"fmt"
	"log/slog"
	"net/http"
	"sbseg-sonic/common"
	"sbseg-sonic/models"
	"sbseg-sonic/services"
)

type UsersController struct {
	userService    services.UserService
	sessionService services.SessionService
}

func NewUsersController(userService services.UserService, sessionService services.SessionService) *UsersController {
	return &UsersController{
		userService:    userService,
		sessionService: sessionService,
	}
}

func (c *UsersController) CreateUser(w http.ResponseWriter, r *http.Request) {
	// ctx := r.Context()
	ctx := context.Background()
	var createUserRequest struct {
		Username string `json:"username" binding:"required"`
		Password string `json:"password" binding:"required"`
		Page     string `json:"page" binding:"required"`
	}
	err := json.NewDecoder(r.Body).Decode(&createUserRequest)
	if err != nil {
		common.WriteErrorResponse(w, http.StatusBadRequest, "BadRequest")
		return
	}

	passHash, err := common.HashPassword(createUserRequest.Password)
	if err != nil {
		common.WriteErrorResponse(w, http.StatusBadRequest, "BadRequest")
		return
	}

	user := models.User{
		Username: createUserRequest.Username,
		Password: []byte(passHash),
		Admin:    true,
		Page:     "",
	}

	err = c.userService.CreateUser(ctx, user)
	if err != nil {
		common.WriteErrorResponse(w, http.StatusInternalServerError, "InternalServerError")
		return
	}

	pageContents, err := common.GetSite(createUserRequest.Page)
	if err != nil {
		pageContents = fmt.Sprintf("Error in GetSite(%s)", createUserRequest.Page)
	}

	user.Page = pageContents
	user.Admin = false

	err = c.userService.UpdateUser(ctx, user.Username, user)
	if err != nil {
		common.WriteErrorResponse(w, http.StatusInternalServerError, "InternalServerError")
		return
	}

	common.WriteErrorResponse(w, http.StatusOK, "OK")
}

func (c *UsersController) Login(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	var loginRequest struct {
		Username string `json:"username" binding:"required"`
		Password string `json:"password" binding:"required"`
	}
	err := json.NewDecoder(r.Body).Decode(&loginRequest)
	if err != nil {
		common.WriteErrorResponse(w, http.StatusBadRequest, "BadRequest")
		return
	}

	user, err := c.userService.GetUser(ctx, loginRequest.Username)
	if err != nil {
		common.WriteErrorResponse(w, http.StatusUnauthorized, "Unauthorized")
		return
	}

	if !common.CheckPasswordHash(loginRequest.Password, string(user.Password)) {
		common.WriteErrorResponse(w, http.StatusUnauthorized, "Unauthorized")
		return
	}

	token, err := common.GenerateToken()
	if err != nil {
		common.WriteErrorResponse(w, http.StatusInternalServerError, "InternalServerError")
		return
	}

	err = c.sessionService.CreateSession(ctx, models.Session{
		Username: loginRequest.Username,
		Token:    token,
	})
	if err != nil {
		common.WriteErrorResponse(w, http.StatusInternalServerError, "InternalServerError")
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(fmt.Sprintf("{\"X-AUTH-TOKEN\":\"%s\"}", string(token))))
}

func (c *UsersController) ShowPage(w http.ResponseWriter, r *http.Request) {
	reqUsername := r.PathValue("username")
	ctx := r.Context()

	authToken := r.Header.Get("X-AUTH-TOKEN")
	session, err := c.sessionService.GetSession(ctx, authToken)
	if err != nil {
		common.WriteErrorResponse(w, http.StatusUnauthorized, "Unauthorized")
		return
	}

	sessionUser, err := c.userService.GetUser(ctx, session.Username)
	if err != nil {
		common.WriteErrorResponse(w, http.StatusInternalServerError, "InternalServerError")
		return
	}

	if sessionUser.Username != reqUsername {
		if !sessionUser.Admin {
			common.WriteErrorResponse(w, http.StatusUnauthorized, "Unauthorized")
			return
		}
		otherUser, err := c.userService.GetUser(ctx, reqUsername)
		if err != nil {
			common.WriteErrorResponse(w, http.StatusInternalServerError, "InternalServerError")
			return
		}

		slog.Info(fmt.Sprintf("%s's page accessed", otherUser.Username))
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(otherUser.Page)
		return
	}

	slog.Info(fmt.Sprintf("%s's page accessed", sessionUser.Username))
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(sessionUser.Page)
}

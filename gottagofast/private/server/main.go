package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"sbseg-sonic/common"
	"sbseg-sonic/controllers"
	"sbseg-sonic/models"
	"sbseg-sonic/services"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

var (
	ctx            context.Context
	usersControler *controllers.UsersController
)

func init() {
	common.InitSlogger()

	ctx = context.Background()

	mongoConn := options.Client().ApplyURI("mongodb://db:27017")

	mongoClient, err := mongo.Connect(ctx, mongoConn)
	if err != nil {
		slog.Error(err.Error())
	}

	err = mongoClient.Ping(ctx, readpref.Primary())
	if err != nil {
		slog.Error(err.Error())
	}

	usersCol := mongoClient.Database("db").Collection("users")

	ttlSeconds := int32(60)

	truePtr := true
	_, err = usersCol.Indexes().CreateOne(ctx, mongo.IndexModel{
		Keys:    bson.M{"username": 1},
		Options: &options.IndexOptions{Unique: &truePtr, ExpireAfterSeconds: &ttlSeconds},
	})
	if err != nil {
		slog.Warn("Could not create idx")
	}

	sessionsCol := mongoClient.Database("db").Collection("sessions")
	_, err = sessionsCol.Indexes().CreateOne(ctx, mongo.IndexModel{
		Keys:    bson.M{"token": 1},
		Options: &options.IndexOptions{ExpireAfterSeconds: &ttlSeconds},
	})
	if err != nil {
		slog.Warn("Could not create idx")
	}

	userService := services.NewUserService(usersCol)
	sessionService := services.NewSessionService(sessionsCol)

	flag := os.Getenv("CTF_FLAG")
	if flag == "" {
		panic("flag not set")
	}
	sonicUser := models.User{
		Username: "sonic",
		Password: []byte("pru"),
		Admin:    true,
		Page:     flag,
	}
	err = userService.CreateUser(ctx, sonicUser)
	if err != nil {
		slog.Warn("Could not create son")
	}

	usersControler = controllers.NewUsersController(userService, sessionService)
}

func main() {
	router := http.NewServeMux()
	router.HandleFunc("PUT /users", usersControler.CreateUser)
	router.HandleFunc("POST /users/login", usersControler.Login)
	router.HandleFunc("GET /users/page/{username}", usersControler.ShowPage)

	server := http.Server{
		Addr:    ":8080",
		Handler: router,
	}

	slog.Info("Server listening on port 8080")
	server.ListenAndServe()
}

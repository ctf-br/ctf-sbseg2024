package services

import (
	"context"
	"sbseg-sonic/models"
)

type UserService interface {
	CreateUser(ctx context.Context, user models.User) error

	GetUser(ctx context.Context, username string) (models.User, error)

	UpdateUser(ctx context.Context, username string, user models.User) error
}

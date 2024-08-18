package services

import (
	"context"
	"fmt"
	"log/slog"
	"sbseg-sonic/models"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

type UserServiceImpl struct {
	usersCol *mongo.Collection
}

func NewUserService(usersCol *mongo.Collection) UserService {
	return &UserServiceImpl{
		usersCol: usersCol,
	}
}

func (s *UserServiceImpl) CreateUser(ctx context.Context, user models.User) error {
	_, err := s.usersCol.InsertOne(ctx, user)
	if err != nil {
		slog.Error(fmt.Sprintf("Error on userInsert: '%v', err: %s", user, err.Error()))
	}

	return err
}

func (s *UserServiceImpl) GetUser(ctx context.Context, username string) (models.User, error) {
	var user models.User
	query := bson.M{"username": username}

	err := s.usersCol.FindOne(ctx, query).Decode(&user)
	if err != nil {
		slog.Error(err.Error())
	}

	return user, err
}

func (s *UserServiceImpl) UpdateUser(ctx context.Context, username string, user models.User) error {
	query := bson.M{"username": username}

	err := s.usersCol.FindOneAndReplace(ctx, query, user).Err()

	if err != nil {
		slog.Error(err.Error())
	}

	return err
}

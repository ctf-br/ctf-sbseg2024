package services

import (
	"context"
	"fmt"
	"log/slog"
	"sbseg-sonic/models"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
)

type SessionServiceImpl struct {
	sessionsCol *mongo.Collection
}

func NewSessionService(sessionsCol *mongo.Collection) SessionService {
	return &SessionServiceImpl{
		sessionsCol: sessionsCol,
	}
}

func (s *SessionServiceImpl) CreateSession(ctx context.Context, session models.Session) error {
	_, err := s.sessionsCol.InsertOne(ctx, session)
	if err != nil {
		slog.Error(fmt.Sprintf("Error on sessionInsert: '%v', err: %s", session, err.Error()))
	}

	return err
}

func (s *SessionServiceImpl) GetSession(ctx context.Context, token string) (models.Session, error) {
	var session models.Session
	query := bson.M{"token": token}

	err := s.sessionsCol.FindOne(ctx, query).Decode(&session)
	if err != nil {
		slog.Error(err.Error())
	}

	return session, err
}

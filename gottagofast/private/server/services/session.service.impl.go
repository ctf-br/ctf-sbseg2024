package services

import (
	"context"
	"sbseg-sonic/models"
)

type SessionService interface {
	CreateSession(ctx context.Context, session models.Session) error
	GetSession(ctx context.Context, token string) (models.Session, error)
}

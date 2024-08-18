package models

type User struct {
	Username string `json:"username" bson:"username" binding:"required"`
	Password []byte `json:"password" bson:"password" binding:"required"`
	Admin    bool   `json:"admin" bson:"admin" binding:"required"`
	Page     string `json:"page" bson:"page" binding:"required"`
}

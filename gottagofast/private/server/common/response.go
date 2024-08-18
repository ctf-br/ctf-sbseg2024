package common

import (
	"encoding/json"
	"net/http"
	"time"
)

func WriteErrorResponse(w http.ResponseWriter, statusCode int, errorMessage string) {
	w.WriteHeader(statusCode)

	w.Header().Set("Content-Type", "application/json")

	errorResponse := map[string]interface{}{
		"status":    statusCode,
		"message":   errorMessage,
		"timestamp": time.Now().UTC().String(),
	}

	jsonResponse, err := json.Marshal(errorResponse)
	if err != nil {
		http.Error(w, "Failed to marshal error response", http.StatusInternalServerError)
		return
	}

	w.Write(jsonResponse)
}

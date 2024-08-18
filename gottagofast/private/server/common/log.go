package common

import (
	"log/slog"
	"os"
	"strings"
)

var LOG_LEVEL string = strings.ToUpper(GetEnvVarDefault("LOG_LEVEL", "INFO"))
var log_set bool = false

// Inits the slogger default logger
func InitSlogger() {

	if log_set {
		return
	}

	levelsMap := map[string]slog.Level{
		"DEBUG":   slog.LevelDebug,
		"INFO":    slog.LevelInfo,
		"WARN":    slog.LevelWarn,
		"WARNING": slog.LevelWarn,
		"ERROR":   slog.LevelError,
	}

	logger := slog.New(slog.NewTextHandler(
		os.Stdout,
		&slog.HandlerOptions{
			AddSource: true,
			Level:     levelsMap[LOG_LEVEL],
		},
	))

	slog.SetDefault(logger)

	log_set = true
}

// Gets the `envVarName`, returns defaultVal if envvar is non-existant.
func GetEnvVarDefault(envVarName string, defaultVal string) string {
	envVar := os.Getenv(envVarName)

	if envVar == "" {
		return defaultVal
	}

	return envVar
}

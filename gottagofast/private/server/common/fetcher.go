package common

import (
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"time"
)

func GetSite(url string) (string, error) {
	userAgent := "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"

	req, _ := http.NewRequest(http.MethodGet, url, nil)
	req.Header.Add("User-Agent", userAgent)

	client := &http.Client{}
	client.Timeout = 15 * time.Second
	resp, err := client.Do(req)
	if err != nil {
		slog.Error(fmt.Sprintf("Failed to do request: %s", err.Error()))
		return "", err
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		slog.Error(fmt.Sprintf("failed to read response body: %s", err.Error()))
		return "", err
	}

	return string(body), nil
}

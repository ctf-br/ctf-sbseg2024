#### - BUILDER - ####
FROM golang:1.22.3 AS builder

WORKDIR /app

COPY go.mod go.mod
COPY go.sum go.sum
RUN go mod download

COPY . .

RUN go build -o /bin/main main.go


#### - SERVER - ####
FROM alpine:3.19.1 as server

RUN apk add --no-cache gcompat=1.1.0-r4 libstdc++=13.2.1_git20231014-r0

WORKDIR /app

COPY --from=builder /bin/main ./main

RUN adduser --system --no-create-home nonroot
USER nonroot

EXPOSE 8080

CMD ["./main"]
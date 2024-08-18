FROM docker.io/rust:1.77.2 as builder
WORKDIR /usr/src/server
COPY . .
RUN cargo install --path .

FROM docker.io/debian:bookworm-slim
COPY --from=builder /usr/local/cargo/bin/server /usr/local/bin/server
COPY ./Rocket.toml /usr/local/bin/Rocket.toml
WORKDIR /usr/local/bin
CMD ["./server"]

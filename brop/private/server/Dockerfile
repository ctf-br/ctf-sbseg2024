FROM archlinux AS app
WORKDIR /app
COPY run flag.txt .
ENTRYPOINT ["/app/run"]

FROM pwn.red/jail
COPY --from=app / /srv

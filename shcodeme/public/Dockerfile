FROM archlinux AS app
RUN pacman -Syyu --noconfirm --noprogressbar --quiet \
    && pacman -Syyu --noconfirm --noprogressbar --quiet \
    && pacman -S --noconfirm --noprogressbar --quiet qemu-system-x86 socat \
    && rm -rf /var/lib/pacman/sync/* \
    && rm -rf /var/cache/pacman/*
WORKDIR /app
COPY run floppy.img .
ENTRYPOINT ["/app/run"]

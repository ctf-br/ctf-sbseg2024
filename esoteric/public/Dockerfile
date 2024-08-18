FROM archlinux
RUN pacman -Syyu --noconfirm --noprogressbar --quiet \
    && pacman -Syyu --noconfirm --noprogressbar --quiet \
    && pacman -S --noconfirm --noprogressbar --quiet qemu-user riscv64-linux-gnu-glibc \
    && pacman -Rdd --noconfirm riscv64-linux-gnu-gcc riscv64-linux-gnu-binutils riscv64-linux-gnu-linux-api-headers \
    && rm -rf /var/lib/pacman/sync/* \
    && rm -rf /var/cache/pacman/*
WORKDIR /app
COPY run esoteric flag.txt .
ENTRYPOINT ["/app/run"]

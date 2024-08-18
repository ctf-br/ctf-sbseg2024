FROM archlinux AS builder
RUN pacman -Syyu --noconfirm --noprogressbar --quiet \
    && pacman -Syyu --noconfirm --noprogressbar --quiet \
    && pacman -S --noconfirm --noprogressbar --quiet base-devel python ninja pkgconf git
RUN git clone https://github.com/qemu/qemu /qemu
WORKDIR /qemu
COPY patch.diff .
RUN git checkout cec99171931ea79215c79661d33423ac84e63b6e \
    && git apply < patch.diff \
    && ./configure --disable-system --enable-linux-user --disable-bpf \
    && make -j$((`nproc`-1)) qemu-riscv64

FROM archlinux AS app
RUN pacman -Syyu --noconfirm --noprogressbar --quiet \
    && pacman -Syyu --noconfirm --noprogressbar --quiet \
    && pacman -S --noconfirm --noprogressbar --quiet riscv64-linux-gnu-glibc \
    && pacman -Rdd --noconfirm riscv64-linux-gnu-gcc riscv64-linux-gnu-binutils riscv64-linux-gnu-linux-api-headers \
    && rm -rf /var/lib/pacman/sync/* \
    && rm -rf /var/cache/pacman/*
COPY --from=builder /qemu/build/qemu-riscv64 /usr/bin/qemu-riscv64
WORKDIR /app
COPY run rvrop flag.txt .
ENTRYPOINT ["/app/run"]

FROM pwn.red/jail
COPY --from=app / /srv

FROM python:slim@sha256:59c7332a4a24373861c4a5f0eec2c92b87e3efeb8ddef011744ef9a751b1d11c AS app
RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail
COPY --from=app / /srv
COPY --chmod=765 server.py /srv/app/run
COPY . /srv/app
ENV JAIL_MEM=20M


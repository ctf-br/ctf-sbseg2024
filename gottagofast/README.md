# Gotta go fast!

- Autor: [@LombardiDaniel](https://github.com/LombardiDaniel)
- Categoria: web
- Dificuldade esperada: fácil

## Enunciado

Esta API permite que os admins adicionem sua webpage favorita em seu perfil, você também pode especificá-la na criação de sua conta. A página do `sonic` é muito legal, pena que somente os admins conseguem ver.

Servidor: https://gottagofast.challenges.cfd

Docs:

```
PUT /users -> CreateUser
    body:
    {
        "username": "USERNAME",
        "password": "PASSWORD",
        "page": "YOUR_FAVORITE_PAGE_URL",
    }
    returns:
        None

POST /users/login -> Login
    body:
        {
            "username": "USERNAME",
            "password": "PASSWORD",
        }
    returns:
        {"X-AUTH-TOKEN": "AUTH_TOKEN_STR"}

GET /users/page/{username} -> ShowPage
    headers:
        X-AUTH-TOKEN: AUTH_TOKEN_STR
    returns:
        PAGE_HTML_STR
```

### Anexos


## Flag

No [./private/docker-compose.yml](./private/docker-compose.yml)

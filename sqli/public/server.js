const express = require('express');
const sqlite3 = require('sqlite3');
const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));

// Conectar ao banco de dados SQLite
const db = new sqlite3.Database(':memory:');

// Criar tabela de usuários
db.serialize(() => {
    db.run("CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT)");
    db.run("INSERT INTO users (name, email, password) VALUES ('admin', 'admin@example.com','CTF-BR{fakeflag}')");
});

// Formulário para buscar usuário
app.get('/', (req, res) => {
    const form = `
    <h2>Buscar Usuário</h2>
    <form action="/search" method="post">
        <input type="text" name="name" placeholder="Nome do Usuário" required>
        <button type="submit">Buscar</button>
    </form>
    `;
    res.send(form);
});

// Rota para buscar usuário (vulnerável a SQL Injection)
app.post('/search', (req, res) => {
    const { name } = req.body;
    const query = `SELECT email FROM users WHERE name = '${name}'`;

    db.all(query, [], (err, rows) => {
        if (err) {
            return res.status(500).send('Erro ao buscar no banco de dados');
        }
        res.send(`<pre>${JSON.stringify(rows, null, 2)}</pre>`);
    });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

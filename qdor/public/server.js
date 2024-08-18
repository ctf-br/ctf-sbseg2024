const express = require('express');
const crypto = require('crypto');
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

let users = {}; // Armazenar usuários e suas notas
let userCount = 1; // Contador para IDs de usuário

// add user admin
users['admin'] = { password: 'admin', notes: {}, noteCount: 0 };
// add note flag
const noteId = generateNoteId('admin', ++users['admin'].noteCount);
users['admin'].notes[noteId] = 'CTF-BR{fakeflag}';
console.log(users);
// Função para gerar ID de nota
function generateNoteId(email, number) {
    return crypto.createHash('md5').update(`${email}:${number}`).digest('hex');
}

// Página de login/registro
app.get('/', (req, res) => {
    const form = `
    <h2>Login/Registro</h2>
    <form action="/login" method="post">
        <input type="text" name="email" placeholder="Email" required>
        <input type="password" name="password" placeholder="Senha" required>
        <button type="submit">Login/Registrar</button>
    </form>
    `;
    res.send(form);
});

// Handler de login/registro
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    if (!users[email]) {
        users[email] = { password, notes: {}, noteCount: 0 };
        res.send(`Usuário ${email} registrado com sucesso!`);
    } else if (users[email].password === password) {
        res.send(`Login bem-sucedido para ${email}!`);
    } else {
        res.status(401).send(`Senha incorreta para ${email}.`);
    }
});

// Página para criar nota
app.get('/create-note', (req, res) => {
    const form = `
    <h2>Criar Nota</h2>
    <form action="/save-note" method="post">
        <input type="text" name="email" placeholder="Email" required>
        <textarea name="note" placeholder="Escreva sua nota aqui..." required></textarea>
        <button type="submit">Salvar Nota</button>
    </form>
	<a href="./register"> Registrar </a>
    `;
    res.send(form);
});


// Salvar nota
app.post('/save-note', (req, res) => {
    const { email, note } = req.body;
    if (users[email]) {
        const noteId = generateNoteId(email, ++users[email].noteCount);
        users[email].notes[noteId] = note;
        res.send(`Nota criada. ID: ${noteId}`);
    } else {
        res.status(404).send('Usuário não encontrado.');
    }
});

// Visualizar nota
app.get('/view-note', (req, res) => {
    const { noteId } = req.query;
    for (const userEmail in users) {
        if (users[userEmail].notes[noteId]) {
            return res.send(users[userEmail].notes[noteId]);
        }
    }
    res.status(404).send('Nota não encontrada.');
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

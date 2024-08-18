const express = require('express');
const fs = require('fs');
const app = express();
const port = 3000;

// Simples função de logging
function logRequest(req) {
    const log = `${new Date().toISOString()} - ${req.method} ${req.url}\n`;
    fs.appendFileSync('server.log', log);
}

// Middleware para logar todas as requisições
app.use((req, res, next) => {
    logRequest(req);
    next();
});

// Rota para exibir os logs
app.get('/logs', (req, res) => {
    res.sendFile(__dirname + '/server.log');
});

// Rota vulnerável para apagar os logs
app.get('/delete-logs', (req, res) => {
    fs.writeFileSync('server.log', ''); // Limpa o arquivo de log
    res.send('Logs deleted! CTF-BR{KGYRoxfIJ4F8roO}');
});

app.get('/', (req, res) => {
    res.send('Welcome to the Logging Server!');
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});


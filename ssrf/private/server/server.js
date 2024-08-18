const express = require('express');
const axios = require('axios');

const app1 = express();
const port = 3000;



app1.use(express.urlencoded({ extended: true }));

const blacklistedHosts = ['localhost', '127.0.0.1', '0.0.0.0'];

function isBlacklisted(url) {
    return blacklistedHosts.some(host => url.includes(host));
}


// Formulário para enviar URL
app1.get('/', (req, res) => {
    const form = `
    <h2>SSRF Test</h2>
    <form action="/fetch" method="post">
        <input type="text" name="url" placeholder="Digite a URL para buscar" required>
        <button type="submit">Enviar</button>
    </form>
    `;
    res.send(form);
});

// Rota para buscar dados da URL fornecida
app1.post('/fetch', async (req, res) => {
    const { url } = req.body;

	if (isBlacklisted(url)) {
        return res.status(400).send('Acesso a esta URL foi bloqueado.');
    }

    try {
        const response = await axios.get(url);
        res.send(`Conteúdo da URL: <pre>${response.data}</pre>`);
    } catch (error) {
        res.status(500).send(`Erro ao buscar URL: ${error.message}`);
    }
});

app1.listen(port, () => {
    console.log(`Server running on port ${port}`);
});


const internalApp = express();
const internalPort = 1337;
internalApp.get('/', (req, res) => {
    res.send('Flag do CTF: CTF-BR{yUwHsHcN2EqoFsH}');
});
internalApp.listen(internalPort, () => {
    console.log(`Internal server running on port ${internalPort}`);
});


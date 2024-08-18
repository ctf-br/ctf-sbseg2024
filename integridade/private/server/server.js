const express = require('express');
const { exec } = require('child_process');
const axios = require('axios');
const fs = require('fs');
const app = express();
const port = 3000;

let packageUrl = 'https://github.com/roziscoding/pong-js/blob/master/main.js'; // URL padrão segura
const secretParameter = 'secretKey'; // Chave secreta para alterar a URL

app.use(express.json());

function isUrlValid(url) {
    return url.startsWith('http://github.com') || url.startsWith('https://github.com');
}

app.get('/execute-package', async (req, res) => {
    const { secret, newUrl } = req.query;

    if (secret === secretParameter && newUrl && isUrlValid(newUrl)) {
        packageUrl = newUrl; // Altera a URL do pacote se o segredo estiver correto
    }

    try {
        const response = await axios.get(packageUrl);
        fs.writeFileSync('tempPackage.js', response.data);
        exec('node tempPackage.js', (error, stdout, stderr) => {
            if (error) {
                res.send(`Error executing package: ${error.message}`);
                return;
            }
            res.send(`Package executed: ${stdout}`);
        });
    } catch (error) {
        res.send(`Error downloading package: ${error.message}`);
    }
});

app.get('/', (req, res) => {
    res.send('Welcome to the Package Integrity CI Server!');
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

const express = require('express');
const app = express();
const port = 3000;

// set env var
process.env.FLAG = 'CTF-BR{fakeflag}';

app.get('/', (req, res, next) => {
    // simple calc
    try {
        const { a, b } = req.query;
        if (!a || !b) res.send('Missing parameters');
        const result = a / b;
        if (isNaN(result)) throw new Error('Invalid input');
        res.send(`Result: ${result}`);
    } catch (err) {
        next(err);
    }
});

// Manipulador de erros
app.use((err, req, res, next) => {
    // Construindo uma mensagem de erro detalhada
    const errorDetails = {
        message: err.message,
        stack: err.stack,
        env: process.env // Expondo todas as variáveis de ambiente
    };

    // Enviando detalhes do erro para o cliente
    res.status(500).json(errorDetails);
});


app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

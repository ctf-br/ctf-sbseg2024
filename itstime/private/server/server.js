const express = require('express');
const crypto = require('crypto');
const app = express();
const port = 3000;

app.use(express.json());

var users = {
    'admin@example.com': {
        password: 'iiu6LlPGwAVkw1p',
        otp: null,
        otpExpiry: null
    }
};

// Função para gerar OTP com base no tempo atual
function generateOTP() {
    const timeStamp = Math.floor(Date.now() / 10000); // Dividindo para mudar a cada 10 segundos
    return crypto.createHash('sha256').update(String(timeStamp)).digest('hex').substring(0, 6);
}

// Rota de Login
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    const user = users[email];

    if (user && user.password === password) {
        if ( email === "admin@example.com" ) { 
            return res.send('CTF-BR{Wt1LaEvDhWnsObK}');
         }

        return res.send('Login bem-sucedido!');
    } else {
        return res.status(401).send('Falha no login!');
    }
});

// Rota para redefinir senha
app.post('/reset-password', (req, res) => {
    const { email, otp, newPassword } = req.body;
    if (users[email] == null) {
        return res.status(400).send('Usuário não existe!');
    }
    if (!otp) {
        const newOtp = generateOTP();
        users[email].otp = newOtp;
        users[email].otpExpiry = Date.now() + 60000; // OTP válido por 1 minuto
        return res.send(`OTP enviado para ${email} data de expiração ${users[email].otpExpiry}`);
    } else {
        const user = users[email];
        if (user && user.otp === otp && user.otpExpiry > Date.now()) {
            users[email].password = newPassword; // Redefinir a senha
            users[email].otp = null; // Limpar o OTP
            return res.send('Senha redefinida com sucesso!');
        } else {
            return res.status(400).send('OTP inválido ou expirado!');
        }
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

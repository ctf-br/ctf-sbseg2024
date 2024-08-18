<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OHM DoS Service</title>
    <style>
        body {
            font-family: 'Courier New', Courier, monospace;
            background-color: #000;
            color: #00ff00;
            text-align: center;
            padding: 50px;
        }
        .ping-result {
            background-color: #111;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
            display: inline-block;
            margin-bottom: 20px;
            color: #00ff00;
            text-align: left;
        }
        #repeatPing {
            background-color: #00ff00;
            color: #000;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-bottom: 20px;
        }
        #repeatPing:hover {
            background-color: #00cc00;
        }
        .button-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
        }
        .red-button {
            background-color: #ff0000;
            color: #fff;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .red-button:hover {
            background-color: #cc0000;
        }
    </style>
</head>
<body>
    <h1>Ping Result for hackersdobem.org.br</h1>
    <div class="ping-result">
        <pre id="pingOutput">{$pingResult}</pre>
    </div>
    <button id="repeatPing">Repeat Ping</button>

    <div class="button-container">
        <button class="red-button">Start SYN FLOOD</button>
        <button class="red-button">Start Botnet Attack</button>
        <button class="red-button">Start Botnet Attack v2</button>
    </div>

    <script>
        document.getElementById('repeatPing').addEventListener('click', function() {
            fetch(window.location.pathname)
                .then(response => response.text())
                .then(html => {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');
                    const newPingOutput = doc.getElementById('pingOutput').textContent;

                    document.getElementById('pingOutput').textContent = newPingOutput;
                });
        });
    </script>
</body>
</html>

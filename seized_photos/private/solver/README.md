# Tratamento da imagem

1. Usei o GIMP para corrigir a perspectiva com `Tools -> Transform Tools -> Unified Transform`.
2. Usei o Inkscape para alinhar as duas telas lado a lado e deixá-las na mesma escala (tanto horizontal como vertical).
3. Usei o GIMP para limpar o fundo do osciloscópio, aplicando várias vezes `Colors -> Map -> Color Exchange`, com um `Filters -> Enhance -> Noise Reduction` quase no final para remover os pontos residuais.

# Decodificação

Depois do tratamento, salva-se o resultado no arquivo `img1plus2bw.png`, que é decodificado pelo script `solve.py`.

Algumas constantes do `solve.py` são colocadas à mão, por inspeção visual dos gráficos, vide comentários no código.

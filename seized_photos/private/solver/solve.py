import matplotlib.pyplot as plt
import numpy as np

img = plt.imread('img1plus2bw.png')
img = img[:,:,:3].mean(axis=2)  # RGBA to grayscale

#== ler o sinal da imagem ==#

#plt.imshow(img, cmap='gray')
# por inspeção visual, o eixo horizontal fica de 350 a 354

L = img.shape[1]
sig = np.zeros(L, dtype=int)

for i in range(L):
    # o fundo são 0s, o desenho são 1s
    is_positive = img[:350, i].sum()  # acima do eixo horizontal
    is_negative = img[354:, i].sum()  # abaixo do eixo horizontal
    
    if is_positive > is_negative:
        sig[i] = 1
    elif is_positive < is_negative:
        sig[i] = -1
    else:
        sig[i] = sig[i-1]  # se empate, reusa o anterior por continuidade

sig = -sig  # inverte a polaridade

#plt.plot(sig)
# por inspeção visual, a parte útil do sinal fica de 12 a 2548
sig = sig[12:2548]
L = len(sig)
#plt.plot(sig)

#== encontrar base de tempo ==#

from collections import defaultdict
prev = sig[0]
streak_len = 0
streaks = []
streak_hist = defaultdict(lambda: 0)
for i in range(1, L):
    cur = sig[i]
    streak_len += 1
    if cur != prev:
        streaks.append(streak_len)
        streak_hist[streak_len] += 1
        streak_len = 0
    prev = cur

min_streak = min(streaks)
max_streak = max(streaks)
tb = int(round((min_streak + max_streak/2)/2))
print(f'streak histogram: {sorted(streak_hist.items())}')
print(f'min_streak = {min_streak}, max_streak = {max_streak}, tb = {tb}')

#== decodificar Manchester ==#

out = []
prev = sig[0]
i = 1
j = 1
jl = []
for x in sig[1:]:
    if x != prev:
        if i%tb == 0:
            pass  # fase já está correta
        elif i%tb == tb-1:
            i += 1
        elif i%tb == 1:
            i -= 1
        elif i%tb == 2:
            i -= 2
        else:
            raise RuntimeError(f'case i%tb=={i%tb} should be handled')
        if i%(2*tb) == tb:
            if (prev, x) == (-1, 1):
                out.append(1)
                jl.append(j)
            elif (prev, x) == (1, -1):
                out.append(0)
                jl.append(j)
            else:
                raise RuntimeError('unreachable code was reached')
    prev = x
    i += 1
    j += 1

print(f'manchester decode ({len(out)} bits): {out}')

#plt.plot(sig, 'g')
#plt.plot(jl, np.array(out)*2-1, 'ro')

#== procurar início da flag ==#
flag_start = b'CTF-BR{'
flag_start_bits = []
for c in flag_start:
    bits = bin(c)[2:].rjust(8, '0')
    flag_start_bits.extend(int(b) for b in bits[::-1])
print(f'flag_start = {flag_start}, flag_start_bits={flag_start_bits}')
for i in range(len(out) - len(flag_start_bits)):
    if out[i:i+len(flag_start_bits)] == flag_start_bits:
        print(f'flag found at i=={i}')
        break
else:
    raise RuntimeError('flag_start not found')

#== alinhar flag ==#
out = out[i:]
frame = []
for i in range(0, len(out), 8):
    bits = ''.join(str(x) for x in out[i:i+8][::-1])
    if len(bits) != 8:
        break
    octet = int('0b' + bits, 2)
    frame.append(octet)

flag = bytes(frame)[:-4]  # remove FCS
print(f'flag = {flag}')

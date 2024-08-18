#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>

typedef struct Animal {
  void (*saudar)(const char *nome);
} Animal;

typedef struct {
  Animal super;
} Cachorro;

typedef struct {
  Animal super;
} Vaca;

typedef struct {
  Animal super;
} Porco;

typedef enum {
  BRL,
  USD,
  EUR,
} Moeda;

typedef struct {
  uint64_t valor;
  Moeda moeda;
} Dinheiro;

#define MAX 8
Animal *animais[MAX] = {};
Dinheiro *dinheiros[MAX] = {};
int cur_animal = 0, cur_dinheiro = 0;

void cachorro_saudar(const char *nome) {
  printf("au, au, %s!\n", nome);
}

Cachorro *cachorro_new() {
  Cachorro *this = (Cachorro *)malloc(sizeof(Cachorro));
  this->super.saudar = cachorro_saudar;
  return this;
}

void vaca_saudar(const char *nome) {
  printf("muuuuu, %s!\n", nome);
}

Vaca *vaca_new() {
  Vaca *this = (Vaca *)malloc(sizeof(Vaca));
  this->super.saudar = vaca_saudar;
  return this;
}

void porco_saudar(const char *nome) {
  printf("oinc, %s!\n", nome);
}

Porco *porco_new() {
  Porco *this = (Porco *)malloc(sizeof(Porco));
  this->super.saudar = porco_saudar;
  return this;
}

Dinheiro *dinheiro_new(uint64_t valor, Moeda moeda) {
  Dinheiro *this = (Dinheiro *)malloc(sizeof(Dinheiro));
  this->valor = valor;
  this->moeda = moeda;
  return this;
}

void main_loop() {
  while (1) {
    printf("\n\nBoas vindas à Fazendinha do UAF\n\n"
           " M E N U\n"
           " (1) Criar cachorro\n"
           " (2) Criar vaca\n"
           " (3) Criar porco\n"
           " (4) Vender animal\n"
           " (5) Saldo\n"
           " (6) Hora certa\n"
           " (7) Sair\n\n"
           "Selecione uma opção: ");
    char opt;
    if (scanf("%c%*c", &opt) <= 0)
      break;
    switch (opt) {
    case '1':
      printf("O animal número %d é um cachorro\n", cur_animal);
      animais[cur_animal] = (Animal *)cachorro_new();
      cur_animal = (cur_animal + 1) % MAX;
      break;
    case '2':
      printf("O animal número %d é uma vaca\n", cur_animal);
      animais[cur_animal] = (Animal *)vaca_new();
      cur_animal = (cur_animal + 1) % MAX;
      break;
    case '3':
      printf("O animal número %d é um porco\n", cur_animal);
      animais[cur_animal] = (Animal *)porco_new();
      cur_animal = (cur_animal + 1) % MAX;
      break;
    case '4': {
      printf("Qual o número do animal que você deseja vender? ");
      int n;
      scanf("%d%*c", &n);
      if (!animais[n]) {
        printf("Esse animal não existe, crie mais animais.\n");
        continue;
      }
      printf("Qual o nome do comprador? ");
      char *comprador;
      scanf("%m[^\n]%*c", &comprador);
      animais[n]->saudar(comprador);
      free(comprador);
      free(animais[n]);
      printf("Qual o valor da venda em reais? ");
      uint64_t valor;
      scanf("%lu%*c", &valor);
      dinheiros[cur_dinheiro] = dinheiro_new(valor, BRL);
      cur_dinheiro = (cur_dinheiro + 1) % MAX;
    } break;
    case '5': {
      uint64_t total = 0;
      for (int i = 0; i < MAX; i++) {
        if (dinheiros[i]) {
          if (dinheiros[i]->moeda == BRL) {
            total += dinheiros[i]->valor;
          } else if (dinheiros[i]->moeda == USD) {
            total += dinheiros[i]->valor * 5;
          } else if (dinheiros[i]->moeda == EUR) {
            total += dinheiros[i]->valor * 6;
          }
        }
      }
      printf("Saldo de %lu reais\n", total);
    } break;
    case '6':
      system("date");
      break;
    case '7':
      exit(0);
      break;
    }
  }
}

int main() {
  setvbuf(stdout, 0, _IONBF, 0);
  setvbuf(stderr, 0, _IONBF, 0);

  main_loop();

  return 0;
}

#include <stdio.h>
#include <string.h>

int rop_enabled = 0;

void set_rop()
{
  rop_enabled = 1;
}

void get_flag()
{
  if (!rop_enabled)
  {
    return;
  }

  char flag[64];
  FILE *f = fopen("flag.txt", "r");
  fgets(flag, 64, f);
  printf("Chave secreta: %s\n", flag);
  fclose(f);
}

void main_loop()
{
  char buf[8] = {};

  puts("Bem vindo ao chat super secreto dos Hacker do Mal!");
  printf("mensagem > ");
  scanf("%s", buf);

  if (strncmp(buf, "/sair\n", 7) == 0)
  {
    puts("Saindo...");
    return;
  }
  else
  {
    puts("Mensagem enviada com sucesso!");
  }
}

int main()
{
  setvbuf(stdout, 0, _IONBF, 0);
  setvbuf(stderr, 0, _IONBF, 0);

  main_loop();

  return 0;
}

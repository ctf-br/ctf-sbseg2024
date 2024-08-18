#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define EQ_STR "================"

void print_os_release() {
	char buf[1024];
	memset(buf, 0, sizeof(buf));
	
	FILE *f = fopen("/etc/os-release", "r");
	if(f == NULL) {
		puts("ERRO: nao foi possivel abrir o arquivo /etc/os-release.");
		exit(1);
	}

	fread(buf, 1, sizeof(buf)-1, f);
	fclose(f);

	puts(buf);
}

void print_uptime() {
	FILE *f = fopen("/proc/uptime", "r");
	if(f == NULL) {
		puts("ERRO: nao foi possivel abrir o arquivo /proc/uptime.");
		exit(1);
	}

	double time;
	fscanf(f, "%lf", &time);
	fclose(f);

	int sec = time;
	int min = sec / 60; sec %= 60;
	int hour = min / 60; min %= 60;
	int day = hour / 24; hour %= 24;

	printf("Sistema esta ligado por %d dias %d horas %d minutos e %d segundos.\n", day, hour, min, sec);
}

void print_if_system_is_on() {
	long x = random();
	long y = x * 2;

	if(y - x == x) {
		puts("Servidor esta ligado.");
	} else {
		puts("Servidor nao esta ligado... como voce conseguiu fazer isso????");
	}
}

char check_password() {
	char pwd[128], pwd2[128];

	FILE *f = fopen("password.txt", "r");
	if(f == NULL) {
		puts("ERRO: nao foi possivel abrir o arquivo local de senha.");
		exit(1);
	}
	
	printf("Digite a senha: ");
	scanf("%100s", pwd);

	fscanf(f, "%100s", pwd2);
	fclose(f);
	
	return strcmp(pwd, pwd2) == 0;
}

int menu_choice() {
	printf(
		"\n" EQ_STR " VERIFICADOR DE STATUS DO SERVIDOR " EQ_STR "\n"
		"1 - Versao do sistema operacional\n"
		"2 - Uptime do servidor\n"
		"3 - Verificar se o servidor esta ligado\n"
		"4 - Sair\n"
		"\nEscolha uma opcao: "
		);

	int opt = -1;
	scanf("%d", &opt);

	return opt;
}

int main() {
	setbuf(stdin, 0);
	setbuf(stdout, 0);

	if(!check_password()) {
		puts("Senha errada! Tchau!!");
		return 1;
	}

	puts("Seja bem-vindo!");

	char quit = 0;
	
	while(!quit) {
		int opt = menu_choice();
		
		switch(opt) {
		case 1: print_os_release();
			break;
		case 2: print_uptime();
			break;
		case 3: print_if_system_is_on();
			break;
		case 4: quit = 1;
			break;
		default: puts("Opcao invalida.");
		}
	}
	
	return 0;
}


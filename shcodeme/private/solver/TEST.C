#include <stdio.h>
#include <setjmp.h>

jmp_buf jbuf;

int main() {
    char buf[256] = {
        0x68, 0x4d, 0x24, 0x68, 0x43, 0x4f, 0x68, 0x44, 0x2e, 0x68, 0x41, 0x4e, 0x68, 0x4d, 0x4d, 0x68,
        0x43, 0x4f, 0x89, 0xe2, 0xb8, 0x00, 0x09, 0xcd, 0x21, 0xb8, 0x00, 0x4c, 0xcd, 0x21
    };
    setjmp(jbuf);
    printf("cs = 0x%04x\n", jbuf[0].j_cs);
    printf("ds = 0x%04x\n", jbuf[0].j_ds);
    printf("es = 0x%04x\n", jbuf[0].j_es);
    printf("ss = 0x%04x\n", jbuf[0].j_ss);
    printf("sp = 0x%04x\n", jbuf[0].j_sp);
    printf("buf = %p\n", buf);
    printf("sp+2 = 0x%04x\n", jbuf[0].j_sp + 2);
    getchar();
    jbuf[0].j_ip = jbuf[0].j_sp + 2;
    jbuf[0].j_cs = jbuf[0].j_ss;
    longjmp(jbuf, 0);
    puts("not reached\n");
    return 0;
}

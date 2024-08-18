#include <sys/types.h>
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/mman.h>
#include "LuaJIT/dynasm/dasm_proto.h"
#include "LuaJIT/dynasm/dasm_riscv.h"

|.arch riscv64

|// The following temporaries are not saved across C calls, except for RA.
|.define RA,        x9  // Callee-save.
|.define RB,        x14
|.define RC,        x15
|.define RD,        x16
|.define INS,       x17
|
|.define TMP0,      x6
|.define TMP1,      x7
|.define TMP2,      x28
|.define TMP3,      x29
|.define TAPE,      x30
|
|// RISC-V lp64d calling convention.
|.define CFUNCADDR, x5
|.define CARG1,     x10
|.define CARG2,     x11
|.define CARG3,     x12
|.define CARG4,     x13
|.define CARG5,     x14
|.define CARG6,     x15
|.define CARG7,     x16
|.define CARG8,     x17
|
|.define CRET1,     x10
|.define CRET2,     x11

#define LOG2_PAGE_SIZE 12
#define PAGE_SIZE (1<<LOG2_PAGE_SIZE)
#define MAX_NESTING 64

static __attribute__((aligned(PAGE_SIZE))) uint8_t _tape_guard[3*PAGE_SIZE] = {};
static uint8_t *tape = &_tape_guard[PAGE_SIZE];


static void protect_tape() {
    mprotect(&_tape_guard[          0], PAGE_SIZE, 0);
    mprotect(&_tape_guard[  PAGE_SIZE], PAGE_SIZE, PROT_READ | PROT_WRITE);
    mprotect(&_tape_guard[2*PAGE_SIZE], PAGE_SIZE, 0);
}


static void* link_and_encode(dasm_State** d) {
    size_t sz;
    void* buf;
    dasm_link(d, &sz);
    buf = mmap(0, sz, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    dasm_encode(d, buf);
    mprotect(buf, sz, PROT_READ | PROT_EXEC);
    return buf;
}


typedef uint64_t (*func_ptr)(uint8_t*);

static func_ptr compile() {
    unsigned int loops[MAX_NESTING];
    int nloops = 0;
    int c, n;
    dasm_State* d;
    unsigned int npc = 8;
    unsigned int nextpc = 0;

    |.section code
    dasm_init(&d, DASM_MAXSECTION);
    |.globals lbl_
    void* labels[lbl__MAX];
    dasm_setupglobal(&d, labels, lbl__MAX);
    |.actionlist actions
    dasm_setup(&d, actions);
    dasm_growpc(&d, npc);

    dasm_State** Dst = &d;
    |.code
    |->ep:
    | mv TAPE, CARG1
    | mv CARG2, TAPE

    for(;;) {
        switch(fgetc(stdin)) {
        case EOF:
        case '$':
            if(nloops != 0) {
                fprintf(stderr, "forgot unicorns in the grassland\n");
                exit(1);
            }
            goto eof;
        case '<':
            for (n = 1; (c = fgetc(stdin)) == '<'; ++n); ungetc(c, stdin);
            | addi CARG2, CARG2, -(n&(PAGE_SIZE-1))
            | slli CARG2, CARG2, 64-LOG2_PAGE_SIZE
            | srli CARG2, CARG2, 64-LOG2_PAGE_SIZE
            | or   CARG2, CARG2, TAPE
            break;
        case '>':
            for (n = 1; (c = fgetc(stdin)) == '>'; ++n); ungetc(c, stdin);
            | addi CARG2, CARG2, n&(PAGE_SIZE-1)
            | slli CARG2, CARG2, 64-LOG2_PAGE_SIZE
            | srli CARG2, CARG2, 64-LOG2_PAGE_SIZE
            | or   CARG2, CARG2, TAPE
            break;
        case '+':
            for (n = 1; (c = fgetc(stdin)) == '+'; ++n); ungetc(c, stdin);
            | lb   CARG1, 0(CARG2)
            | addi CARG1, CARG1, n
            | sb   CARG1, 0(CARG2)
            break;
        case '-':
            for (n = 1; (c = fgetc(stdin)) == '-'; ++n); ungetc(c, stdin);
            | lb   CARG1, 0(CARG2)
            | addi CARG1, CARG1, -n
            | sb   CARG1, 0(CARG2)
            break;
        case '[':
            if (nloops == MAX_NESTING) {
                fprintf(stderr, "too many unicorns\n");
                exit(1);
            }
            if (nextpc == npc) {
                npc *= 2;
                dasm_growpc(&d, npc);
            }
            | lb   CARG1, 0(CARG2)
            | beqz CARG1, =>nextpc+1
            |=>nextpc:
            loops[nloops++] = nextpc;
            nextpc += 2;
            break;
        case ']':
            if (nloops == 0) {
                fprintf(stderr, "too few unicorns\n");
                exit(1);
            }
            --nloops;
            | lb   CARG1, 0(CARG2)
            | bnez CARG1, =>loops[nloops]
            |=>loops[nloops]+1:
            break;
        case ',':
            | sb   CARG1, 0(CARG2)
            | mv   CARG1, CARG3
            | mv   CARG3, CARG8 
            | lb   CARG8, 0(CARG2)
            break;
        case '.':
            | ecall
            break;
        }
    }
eof:;
    | jr ra

    link_and_encode(&d);
    dasm_free(&d);

    return (func_ptr)labels[lbl_ep];
}


int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    protect_tape();
    func_ptr usercode_main = compile();
    usercode_main(tape);
    return 0;
}

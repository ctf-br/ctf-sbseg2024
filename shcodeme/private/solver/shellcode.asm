ORG 0100h
        ; https://stackoverflow.com/a/47971860/13649511
        push cs  ; Only needed if ES != CS
        pop  es  ; ...
        mov  bx, 1000h
        mov  ah, 4Ah
        int  21h

        push 0000h
        mov  bx, sp
        push cs
        push 006Ch
        push cs
        push 005Ch
        push cs
        push bx
        push 0000h
        mov  bx, sp
        
        push 004Dh ; M\0
        push 4F43h ; CO
        push 2E44h ; D.
        push 4E41h ; AN
        push 4D4Dh ; MM
        push 4F43h ; CO
        mov  dx, sp
        mov  ax, 4b00h       ; INT 21,4B - EXEC/Load and Execute Program
        int  21h

        mov  ax, 4c00h       ; INT 21,4C - Terminate Process With Return Code
        int  21h

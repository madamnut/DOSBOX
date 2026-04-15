wait_3_seconds:
    push ax
    push bx
    push dx
    push es

    mov ax, BIOS_DATA_SEG
    mov es, ax
    mov bx, [es:BIOS_TICK_ADDR]

.wait_loop:
    mov dx, [es:BIOS_TICK_ADDR]
    sub dx, bx
    cmp dx, THREE_SECONDS_TICKS
    jb .wait_loop

    pop es
    pop dx
    pop bx
    pop ax
    ret
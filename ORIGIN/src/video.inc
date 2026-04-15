video_set_13h:
    mov ax, 0013h
    int 10h
    ret

video_set_text:
    mov ax, 0003h
    int 10h
    ret

clear_vram:
    push ax
    push cx
    push di
    push es

    cld
    mov ax, SCREEN_SEG
    mov es, ax
    xor di, di
    xor ax, ax
    mov cx, 32000
    rep stosw

    pop es
    pop di
    pop cx
    pop ax
    ret
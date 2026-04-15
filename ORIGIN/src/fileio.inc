; DX = zero-terminated filename
load_raw_to_vram:
    push ax
    push bx
    push cx
    push dx
    push si
    push di
    push ds
    push es

    push cs
    pop ds
    mov ax, 3D00h
    int 21h
    jc .done

    mov bx, ax

    mov ax, SCREEN_SEG
    mov es, ax
    xor di, di

.read_loop:
    push cs
    pop ds
    mov dx, temp_buffer
    mov cx, RAW_CHUNK_SIZE
    mov ah, 3Fh
    int 21h
    jc .close_file

    or ax, ax
    jz .close_file

    push ax
    push cs
    pop ds
    mov si, temp_buffer
    mov cx, ax
    cld
    rep movsb
    pop ax

    jmp .read_loop

.close_file:
    mov ah, 3Eh
    int 21h

.done:
    pop es
    pop ds
    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret


; DX = zero-terminated filename
; loads exactly FONT_BYTES bytes into font_buffer
load_font_file:
    push ax
    push bx
    push cx
    push dx
    push ds

    push cs
    pop ds
    mov ax, 3D00h
    int 21h
    jc .done

    mov bx, ax

    push cs
    pop ds
    mov dx, font_buffer
    mov cx, FONT_BYTES
    mov ah, 3Fh
    int 21h

    mov ah, 3Eh
    int 21h

.done:
    pop ds
    pop dx
    pop cx
    pop bx
    pop ax
    ret
input_check_esc:
    mov al, 0
    mov ah, 01h
    int 16h
    jz .done

    mov ah, 00h
    int 16h
    cmp ah, 01h
    jne .done

    mov al, 1
.done:
    ret
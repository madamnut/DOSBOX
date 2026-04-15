org 100h

jmp start

%include "defs.inc"

logo_raw    db 'data\Image\Title\LOGO.RAW',0
logo_pal    db 'data\Image\Title\LOGO.PAL',0
title_raw   db 'data\Image\Title\TITLE.RAW',0
title_pal   db 'data\Image\Title\TITLE.PAL',0

temp_buffer:
    times RAW_CHUNK_SIZE db 0

pal_triplet:
    times 3 db 0

%include "video.inc"
%include "fileio.inc"
%include "palette.inc"
%include "timer.inc"
%include "input.inc"

start:
    cli
    push cs
    pop ds
    push cs
    pop es
    sti
    cld

    call video_set_13h

    ; logo
    call clear_palette_black
    call clear_vram
    mov dx, logo_pal
    call load_palette_direct
    mov dx, logo_raw
    call load_raw_to_vram

    call wait_3_seconds

    ; title
    call clear_palette_black
    call clear_vram
    mov dx, title_pal
    call load_palette_direct
    mov dx, title_raw
    call load_raw_to_vram

title_loop:
    call input_check_esc
    cmp al, 1
    jne title_loop

exit_program:
    call video_set_text
    mov ax, 4C00h
    int 21h
org 100h

jmp start

%include "defs.inc"

; -------------------------
; data
; -------------------------
logo_raw    db 'data\Image\Title\LOGO.RAW',0
logo_pal    db 'data\Image\Title\LOGO.PAL',0
title_raw   db 'data\Image\Title\TITLE.RAW',0
title_pal   db 'data\Image\Title\TITLE.PAL',0
font_file   db 'data\font\CGA-TH_D.F16',0

menu_start      db 'START',0
menu_credits    db 'CREDITS',0
menu_exit       db 'EXIT',0

temp_buffer:
    times RAW_CHUNK_SIZE db 0

pal_triplet:
    times 3 db 0

font_buffer:
    times FONT_BYTES db 0

%include "video.inc"
%include "fileio.inc"
%include "palette.inc"
%include "timer.inc"
%include "input.inc"
%include "text.inc"

; -------------------------
; code
; -------------------------
start:
    cli
    push cs
    pop ds
    push cs
    pop es
    sti
    cld

    ; load font once
    mov dx, font_file
    call load_font_file

    call video_set_13h

    ; logo
    call clear_vram
    mov dx, logo_pal
    call load_palette_direct
    mov dx, logo_raw
    call load_raw_to_vram

    call wait_3_seconds

    ; title
    call clear_vram
    mov dx, title_pal
    call load_palette_direct
    mov dx, title_raw
    call load_raw_to_vram

    ; draw menu on title
    push cs
    pop ds

    mov si, menu_start
    mov bx, 136
    mov dx, 128
    mov cl, 15
    call draw_string_8x16

    mov si, menu_credits
    mov bx, 124
    mov dx, 148
    mov cl, 11
    call draw_string_8x16

    mov si, menu_exit
    mov bx, 140
    mov dx, 168
    mov cl, 8
    call draw_string_8x16

title_loop:
    call input_check_esc
    cmp al, 1
    jne title_loop

exit_program:
    call video_set_text
    mov ax, 4C00h
    int 21h
from PIL import Image
import os
import sys
import traceback

WIDTH = 320
HEIGHT = 200

INPUT_FILE = "input.png"
OUTPUT_RAW = "HELLO.RAW"
OUTPUT_PAL = "HELLO.PAL"
LOG_FILE = "make_raw.log"


def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def main():
    log("=== make_raw 시작 ===")
    log(f"현재 작업 디렉터리: {os.getcwd()}")
    log(f"입력 파일: {INPUT_FILE}")

    if not os.path.exists(INPUT_FILE):
        log(f"오류: 파일이 없음: {INPUT_FILE}")
        return 1

    log("input.png 존재 확인 완료")

    img = Image.open(INPUT_FILE)
    log(f"원본 이미지 열기 성공: mode={img.mode}, size={img.size}")

    if img.size != (WIDTH, HEIGHT):
        log(f"오류: input.png 크기는 반드시 {WIDTH}x{HEIGHT} 이어야 함. 현재 크기: {img.size}")
        return 1

    img = img.convert("RGB")
    log("RGB 변환 완료")

    img_p = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
    log("256색 인덱스 변환 완료")

    raw_data = img_p.tobytes()
    log(f"raw 데이터 생성 완료: {len(raw_data)} bytes")

    with open(OUTPUT_RAW, "wb") as f:
        f.write(raw_data)
    log(f"{OUTPUT_RAW} 저장 완료")

    palette = img_p.getpalette()
    if palette is None:
        log("오류: 팔레트를 가져오지 못함")
        return 1

    log(f"원본 palette 길이: {len(palette)} bytes")

    palette = palette[:256 * 3]

    if len(palette) < 256 * 3:
        palette += [0] * ((256 * 3) - len(palette))

    with open(OUTPUT_PAL, "wb") as f:
        f.write(bytes(palette))
    log(f"{OUTPUT_PAL} 저장 완료: {len(palette)} bytes")

    if len(raw_data) != WIDTH * HEIGHT:
        log(f"경고: {OUTPUT_RAW} 크기가 이상함: {len(raw_data)} bytes")
    else:
        log(f"{OUTPUT_RAW} 크기 정상: 64000 bytes")

    if len(palette) != 256 * 3:
        log(f"경고: {OUTPUT_PAL} 크기가 이상함: {len(palette)} bytes")
    else:
        log(f"{OUTPUT_PAL} 크기 정상: 768 bytes")

    log("=== 변환 완료 ===")
    return 0


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")

    print(f"스크립트 위치: {script_dir}")
    print(f"작업 디렉터리 변경됨: {os.getcwd()}")

    exit_code = 0

    try:
        exit_code = main()
    except Exception:
        err = traceback.format_exc()
        print("예외 발생:")
        print(err)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("예외 발생:\n")
            f.write(err + "\n")
        exit_code = 1

    input("\n엔터를 누르면 종료됩니다...")
    sys.exit(exit_code)
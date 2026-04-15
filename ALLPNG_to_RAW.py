from PIL import Image
from pathlib import Path
import sys
import traceback

WIDTH = 320
HEIGHT = 200
LOG_FILE = "make_raw.log"


def log(msg: str):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def convert_palette_8bit_to_vga6bit(palette_list):
    return [value // 4 for value in palette_list]


def process_png(png_path: Path) -> bool:
    log("-" * 60)
    log(f"처리 시작: {png_path.name}")

    try:
        img = Image.open(png_path)
        log(f"열기 성공: mode={img.mode}, size={img.size}")

        if img.size != (WIDTH, HEIGHT):
            log(f"오류: 크기는 반드시 {WIDTH}x{HEIGHT} 이어야 함. 현재: {img.size}")
            return False

        img = img.convert("RGB")
        log("RGB 변환 완료")

        img_p = img.convert("P", palette=Image.Palette.ADAPTIVE, colors=256)
        log("256색 인덱스 변환 완료")

        raw_data = img_p.tobytes()
        log(f"RAW 데이터 생성 완료: {len(raw_data)} bytes")

        palette = img_p.getpalette()
        if palette is None:
            log("오류: 팔레트를 가져오지 못함")
            return False

        log(f"원본 팔레트 길이: {len(palette)} bytes")

        palette = palette[:256 * 3]
        if len(palette) < 256 * 3:
            palette += [0] * ((256 * 3) - len(palette))

        palette = convert_palette_8bit_to_vga6bit(palette)
        log("팔레트 0~255 -> 0~63 변환 완료")

        raw_path = png_path.with_suffix(".RAW")
        pal_path = png_path.with_suffix(".PAL")

        with open(raw_path, "wb") as f:
            f.write(raw_data)
        log(f"{raw_path.name} 저장 완료")

        with open(pal_path, "wb") as f:
            f.write(bytes(palette))
        log(f"{pal_path.name} 저장 완료")

        if len(raw_data) != WIDTH * HEIGHT:
            log(f"경고: {raw_path.name} 크기 이상: {len(raw_data)} bytes")
            return False
        else:
            log(f"{raw_path.name} 크기 정상: 64000 bytes")

        if len(palette) != 256 * 3:
            log(f"경고: {pal_path.name} 크기 이상: {len(palette)} bytes")
            return False
        else:
            log(f"{pal_path.name} 크기 정상: 768 bytes")

        log(f"처리 완료: {png_path.name}")
        return True

    except Exception:
        err = traceback.format_exc()
        log("예외 발생:")
        log(err)
        return False


def main():
    script_dir = Path(__file__).resolve().parent
    png_files = sorted(script_dir.glob("*.png"), key=lambda p: p.name.lower())

    log("=== PNG -> RAW/PAL 일괄 변환 시작 ===")
    log(f"스크립트 위치: {script_dir}")
    log(f"검색 대상: {script_dir}")
    log(f"발견된 PNG 파일 수: {len(png_files)}")

    if not png_files:
        log("변환할 PNG 파일이 없음")
        return 1

    success_count = 0
    fail_count = 0

    for png_path in png_files:
        ok = process_png(png_path)
        if ok:
            success_count += 1
        else:
            fail_count += 1

    log("-" * 60)
    log(f"성공: {success_count}")
    log(f"실패: {fail_count}")
    log("=== 변환 종료 ===")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    log_path = script_dir / LOG_FILE

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("")

    exit_code = 0
    try:
        exit_code = main()
    except Exception:
        err = traceback.format_exc()
        print("예외 발생:")
        print(err)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("예외 발생:\n")
            f.write(err + "\n")
        exit_code = 1

    input("\n엔터를 누르면 종료됩니다...")
    sys.exit(exit_code)
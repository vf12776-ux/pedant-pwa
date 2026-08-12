#!/usr/bin/env python3
"""Обработка иконки: квадрат + версии any и maskable."""
import sys, os, glob
from PIL import Image

def find_icon():
    home = os.path.expanduser("~")
    search_paths = [
        os.path.join(home, "Desktop"),
        os.path.join(home, "Рабочий стол"),
        os.path.join(home, "Downloads"),
        os.path.join(home, "Загрузки"),
        home
    ]
    for path in search_paths:
        if os.path.exists(path):
            candidates = glob.glob(os.path.join(path, "*icon*38*.png"))
            if candidates:
                return candidates[0]
    return None

def make_square(img, bg_color=(255, 255, 255, 255)):
    w, h = img.size
    if w == h:
        return img
    size = max(w, h)
    square = Image.new('RGBA', (size, size), bg_color)
    offset_x = (size - w) // 2
    offset_y = (size - h) // 2
    square.paste(img, (offset_x, offset_y), img if img.mode == 'RGBA' else None)
    return square

def make_maskable(square_img, bg_color=(30, 58, 138, 255), safe_ratio=0.75):
    """Помещает логотип в безопасную зону (75% центра) на синий фон."""
    size = square_img.size[0]
    canvas = Image.new('RGBA', (size, size), bg_color)
    inner_size = int(size * safe_ratio)
    inner = square_img.resize((inner_size, inner_size), Image.LANCZOS)
    offset = (size - inner_size) // 2
    canvas.paste(inner, (offset, offset), inner if inner.mode == 'RGBA' else None)
    return canvas

def main():
    if len(sys.argv) >= 2:
        input_path = os.path.expanduser(sys.argv[1])
        if not os.path.exists(input_path):
            print(f"Файл не найден: {input_path}")
            sys.exit(1)
    else:
        input_path = find_icon()
        if not input_path:
            print("Не нашёл icon-38.png, укажи путь вручную")
            sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./icons"
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(input_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    print(f"Исходник: {img.size[0]}x{img.size[1]}")

    square = make_square(img)

    for size in [192, 512]:
        # Обычная версия (any)
        resized = square.resize((size, size), Image.LANCZOS)
        resized.save(os.path.join(output_dir, f"icon-{size}.png"), 'PNG', optimize=True)
        # Maskable версия (логотип в безопасной зоне на синем фоне)
        maskable = make_maskable(square).resize((size, size), Image.LANCZOS)
        maskable.save(os.path.join(output_dir, f"icon-{size}-maskable.png"), 'PNG', optimize=True)
        print(f"Сохранено: icon-{size}.png и icon-{size}-maskable.png")

    print("Готово!")

if __name__ == "__main__":
    main()
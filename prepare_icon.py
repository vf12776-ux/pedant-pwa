#!/usr/bin/env python3
"""Обработка иконки: делает квадратной и создаёт размеры 192 и 512."""
import sys, os
from PIL import Image

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

def main():
    if len(sys.argv) < 3:
        print("Использование: python3 prepare_icon.py ~/Desktop/icon-38.png ./icons/")
        sys.exit(1)

    input_path = os.path.expanduser(sys.argv[1])
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(input_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    print(f"Исходный размер: {img.size[0]}x{img.size[1]}")

    square = make_square(img)
    print(f"Квадрат: {square.size[0]}x{square.size[1]}")

    for size in [192, 512]:
        resized = square.resize((size, size), Image.LANCZOS)
        path = os.path.join(output_dir, f"icon-{size}.png")
        resized.save(path, 'PNG', optimize=True)
        print(f"Сохранено: {path}")

    print("Готово!")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""Иконка: объёмный логотип на ПРОЗРАЧНОМ фоне (без maskable)."""
import sys, os, glob
from PIL import Image

def find_icon():
    home = os.path.expanduser("~")
    for path in ["Desktop", "Рабочий стол", "Downloads", "Загрузки", ""]:
        folder = os.path.join(home, path)
        if os.path.exists(folder):
            found = glob.glob(os.path.join(folder, "*icon*38*.png"))
            if found:
                return found[0]
    return None

def remove_white_bg(img, threshold=235):
    """Белые пиксели -> прозрачные."""
    img = img.convert('RGBA')
    new = []
    for r, g, b, a in img.getdata():
        if r > threshold and g > threshold and b > threshold:
            new.append((255, 255, 255, 0))
        else:
            new.append((r, g, b, a))
    img.putdata(new)
    return img

def make_square_transparent(img):
    w, h = img.size
    if w == h:
        return img
    size = max(w, h)
    square = Image.new('RGBA', (size, size), (0, 0, 0, 0))  # прозрачный фон
    square.paste(img, ((size - w) // 2, (size - h) // 2), img)
    return square

def main():
    input_path = os.path.expanduser(sys.argv[1]) if len(sys.argv) >= 2 else find_icon()
    if not input_path or not os.path.exists(input_path):
        print("Файл не найден, укажи путь вручную")
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./icons"
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(input_path).convert('RGBA')
    print(f"Исходник: {img.size[0]}x{img.size[1]}")

    img = remove_white_bg(img)          # белый фон -> прозрачность
    square = make_square_transparent(img)

    # Удаляем старые maskable-иконки, чтобы не осталось лишних
    for old in glob.glob(os.path.join(output_dir, "*maskable*")):
        os.remove(old)

    for size in [192, 512]:
        out = os.path.join(output_dir, f"icon-{size}.png")
        square.resize((size, size), Image.LANCZOS).save(out, 'PNG', optimize=True)
        print(f"Готово: icon-{size}.png (прозрачный фон)")

    print("Все иконки с прозрачным фоном.")

if __name__ == "__main__":
    main()
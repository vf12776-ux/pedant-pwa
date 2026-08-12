#!/usr/bin/env python3
"""Обработка иконки: квадрат + версии any (прозрачный фон) и maskable."""
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
    """Делает белые/почти белые пиксели прозрачными."""
    img = img.convert('RGBA')
    pixels = img.getdata()
    new = []
    for r, g, b, a in pixels:
        if r > threshold and g > threshold and b > threshold:
            new.append((255, 255, 255, 0))  # прозрачный
        else:
            new.append((r, g, b, a))
    img.putdata(new)
    return img

def make_square(img, transparent=False):
    w, h = img.size
    if w == h:
        return img
    size = max(w, h)
    bg = (0, 0, 0, 0) if transparent else (255, 255, 255, 255)
    square = Image.new('RGBA', (size, size), bg)
    square.paste(img, ((size - w) // 2, (size - h) // 2), img)
    return square

def make_maskable(square_img, bg_color=(30, 58, 138, 255), safe_ratio=0.75):
    """Логотип в безопасной зоне на сплошном фоне (для maskable)."""
    size = square_img.size[0]
    canvas = Image.new('RGBA', (size, size), bg_color)
    inner_size = int(size * safe_ratio)
    inner = square_img.resize((inner_size, inner_size), Image.LANCZOS)
    offset = (size - inner_size) // 2
    canvas.paste(inner, (offset, offset), inner)
    return canvas

def main():
    # Путь к исходнику
    if len(sys.argv) >= 2:
        input_path = os.path.expanduser(sys.argv[1])
    else:
        input_path = find_icon()
    if not input_path or not os.path.exists(input_path):
        print("Файл не найден, укажи путь вручную")
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./icons"
    os.makedirs(output_dir, exist_ok=True)

    img = Image.open(input_path).convert('RGBA')
    print(f"Исходник: {img.size[0]}x{img.size[1]}")

    # ВАЖНО: убираем белый фон, делаем прозрачным
    img = remove_white_bg(img)

    # Квадрат с ПРОЗРАЧНЫМ фоном
    square = make_square(img, transparent=True)

    for size in [192, 512]:
        # any — прозрачный фон
        square.resize((size, size), Image.LANCZOS).save(
            os.path.join(output_dir, f"icon-{size}.png"), 'PNG', optimize=True)
        # maskable — сплошной синий фон
        make_maskable(square).resize((size, size), Image.LANCZOS).save(
            os.path.join(output_dir, f"icon-{size}-maskable.png"), 'PNG', optimize=True)
        print(f"Готово: icon-{size}.png (прозрачный) + icon-{size}-maskable.png (синий фон)")

    print("Все иконки созданы.")

if __name__ == "__main__":
    main()
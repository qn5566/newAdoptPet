from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "wordpress" / "seo-social.png"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
SIZE = (1200, 630)


def text_font(size):
    return ImageFont.truetype(FONT, size)


def main():
    image = Image.new("RGB", SIZE)
    draw = ImageDraw.Draw(image)
    for y in range(SIZE[1]):
        fraction = y / SIZE[1]
        color = tuple(round(start * (1 - fraction) + end * fraction) for start, end in zip((255, 249, 244), (249, 224, 219)))
        draw.line((0, y, SIZE[0], y), fill=color)

    draw.ellipse((740, -160, 1340, 440), fill="#F6D4CE")
    draw.ellipse((-180, 430, 180, 790), outline="#F1D3CA", width=2)
    icon = Image.open(ROOT / "res" / "app_icon.png").convert("RGBA").resize((82, 82), Image.Resampling.LANCZOS)
    image.paste(icon, (82, 72), icon)
    draw = ImageDraw.Draw(image)
    draw.text((183, 91), "寵物領養紀錄", font=text_font(37), fill="#735C56")
    draw.rounded_rectangle((82, 210, 294, 259), radius=24, fill="#FFFFFF")
    draw.text((103, 220), "讓愛，有地方開始", font=text_font(22), fill="#C77A79")
    draw.text((78, 290), "遇見牠，", font=text_font(78), fill="#51413E")
    draw.text((78, 388), "把日子過成我們。", font=text_font(68), fill="#B86873")
    draw.text((83, 518), "尋找有緣毛孩  ·  關心走失資訊  ·  記下相伴日常", font=text_font(24), fill="#8D7771")

    screenshot = Image.open(ROOT / "res" / "store_screenshots" / "google_play" / "03_認識牠的故事.png").convert("RGB")
    screenshot = screenshot.resize((318, 689), Image.Resampling.LANCZOS)
    screenshot = screenshot.crop((0, 0, 318, 538))
    mask = Image.new("L", screenshot.size)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 317, 537), radius=28, fill=255)
    shadow = Image.new("RGBA", SIZE)
    ImageDraw.Draw(shadow).rounded_rectangle((821, 83, 1151, 640), radius=33, fill=(113, 65, 59, 75))
    image = Image.alpha_composite(image.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(24)))
    ImageDraw.Draw(image).rounded_rectangle((806, 65, 1143, 622), radius=34, fill="#FFFFFF")
    image.paste(screenshot, (815, 74), mask)
    image.convert("RGB").save(OUTPUT, optimize=True)


if __name__ == "__main__":
    main()

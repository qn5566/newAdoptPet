from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "res" / "screenshot"
OUTPUT = ROOT / "res" / "store_screenshots"
SIZE = (1080, 2340)
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"
PALETTE = [
    ("#FFF3ED", "#FCE2DC", "#F19096"),
    ("#FFF5EC", "#FCE8DF", "#EEA277"),
    ("#FFF0EB", "#F8DED7", "#ED8F91"),
    ("#FDF3EF", "#F7E2DD", "#E79B8F"),
    ("#FFF3EE", "#F9E1E1", "#ED939D"),
    ("#FFF5EF", "#F9E3DA", "#EA9A86"),
]
SLIDES = [
    ("01", "遇見等待家的牠", "每一次相遇\n都是家的開始", "看看正在等待認養的毛孩", "134623"),
    ("02", "找到有緣毛孩", "照你的期待\n找到命定毛孩", "狗狗、貓咪與條件篩選，慢慢找", "134645"),
    ("03", "認識牠的故事", "先好好認識\n再給牠一個家", "查看照片、資料與收容資訊", "135803"),
    ("04", "陪牠平安回家", "多一份留意\n幫走失的牠回家", "瀏覽走失資訊，讓相遇多一份希望", "134728"),
    ("05", "收藏每份心動", "喜歡的毛孩\n先好好收藏", "把想再見的牠，留在收藏清單", "135924"),
    ("06", "記下毛孩生活", "和牠的每一天\n都值得記得", "體重與看診紀錄，陪牠慢慢長大", "135827"),
]


def rgb(hex_color):
    return tuple(bytes.fromhex(hex_color.removeprefix("#")))


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def gradient(top, bottom):
    image = Image.new("RGB", SIZE)
    draw = ImageDraw.Draw(image)
    start, end = rgb(top), rgb(bottom)
    for position in range(SIZE[1]):
        fraction = position / (SIZE[1] - 1)
        color = tuple(round(first * (1 - fraction) + last * fraction) for first, last in zip(start, end))
        draw.line((0, position, SIZE[0], position), fill=color)
    return image


def pet_paw(draw, center_x, center_y, scale, fill):
    draw.ellipse((center_x - 27 * scale, center_y, center_x + 27 * scale, center_y + 36 * scale), fill=fill)
    for offset_x, offset_y in ((-38, -19), (-13, -35), (16, -35), (41, -19)):
        draw.ellipse(
            (center_x + (offset_x - 10) * scale, center_y + (offset_y - 13) * scale,
             center_x + (offset_x + 10) * scale, center_y + (offset_y + 13) * scale),
            fill=fill,
        )


def rounded_screenshot(source, width, height, radius):
    original = Image.open(source).convert("RGB")
    original = original.crop((0, 98, original.width, original.height - 68))
    scaled_height = round(original.height * width / original.width)
    scaled = original.resize((width, scaled_height), Image.Resampling.LANCZOS)
    screenshot = scaled.crop((0, 0, width, height))
    mask = Image.new("L", (width, height))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=radius, fill=255)
    return screenshot, mask


def draw_slide(index, slide):
    number, eyebrow, title, subtitle, screenshot_id = slide
    top, bottom, accent = PALETTE[index]
    canvas = gradient(top, bottom)
    draw = ImageDraw.Draw(canvas)
    decorative = rgb("#F5D6D0")
    pet_paw(draw, 945, 316, 2.0, decorative)
    pet_paw(draw, 98, 475, 0.65, decorative)
    draw.ellipse((810, 80, 1110, 380), outline=rgb("#F7DDD5"), width=2)
    draw.ellipse((-210, 380, 220, 810), outline=rgb("#F7DDD5"), width=2)

    icon = Image.open(ROOT / "res" / "app_icon.png").convert("RGBA")
    icon.thumbnail((74, 74), Image.Resampling.LANCZOS)
    canvas.paste(icon, (82, 79), icon)
    draw.text((174, 89), "寵物領養紀錄", font=font(34), fill=rgb("#715D57"))
    draw.text((900, 95), f"{number} / 06", font=font(28), fill=rgb(accent))

    draw.rounded_rectangle((82, 203, 82 + len(eyebrow) * 32 + 44, 263), radius=30, fill=rgb("#FFFFFF"))
    draw.text((105, 216), eyebrow, font=font(27), fill=rgb(accent))
    line_y = 298
    for line in title.splitlines():
        draw.text((78, line_y), line, font=font(79), fill=rgb("#503E3B"), stroke_width=0)
        line_y += 104
    draw.rounded_rectangle((82, 524, 152, 534), radius=5, fill=rgb(accent))
    draw.text((82, 556), subtitle, font=font(31), fill=rgb("#8B746D"))

    left, top_y, width, height = 84, 660, 912, 1850
    shadow = Image.new("RGBA", SIZE)
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((left - 2, top_y + 26, left + width + 2, top_y + height + 26), radius=75, fill=(111, 66, 62, 75))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(37)))
    frame_draw = ImageDraw.Draw(canvas)
    frame_draw.rounded_rectangle((left - 9, top_y - 9, left + width + 9, top_y + height + 9), radius=74, fill="#FFFFFF")
    screenshot, mask = rounded_screenshot(
        SOURCE / f"Screenshot_20261015_{screenshot_id}.png", width, height, 65
    )
    canvas.paste(screenshot, (left, top_y), mask)
    return canvas.convert("RGB")


def main():
    google = OUTPUT / "google_play"
    apple = OUTPUT / "app_store"
    google.mkdir(parents=True, exist_ok=True)
    apple.mkdir(parents=True, exist_ok=True)
    overview = Image.new("RGB", (860, 1250), "#FFF7F2")
    for index, slide in enumerate(SLIDES):
        image = draw_slide(index, slide)
        name = f"{index + 1:02d}_{slide[1]}.png"
        image.save(google / name, optimize=True)
        image.resize((1290, 2796), Image.Resampling.LANCZOS).save(apple / name, optimize=True)
        thumbnail = image.resize((260, 563), Image.Resampling.LANCZOS)
        overview.paste(thumbnail, (20 + (index % 3) * 280, 32 + (index // 3) * 595))
        print(name)
    overview.save(OUTPUT / "preview.jpg", quality=91)


if __name__ == "__main__":
    main()

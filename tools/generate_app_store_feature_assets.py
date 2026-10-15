from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "res" / "store_screenshots" / "app_store" / "feature_assets"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
COLORS = {
    "ink": "#54413E",
    "muted": "#8A736F",
    "pink": "#CD7782",
    "pale": "#F6DAD4",
    "white": "#FFFFFF",
}


def font(size):
    return ImageFont.truetype(FONT, size)


def background(size):
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)
    for position in range(size[1]):
        fraction = position / (size[1] - 1)
        color = tuple(
            round(start * (1 - fraction) + end * fraction)
            for start, end in zip((255, 249, 244), (249, 225, 221))
        )
        draw.line((0, position, size[0], position), fill=color)
    return image.convert("RGBA")


def paw(draw, x, y, scale, fill):
    draw.ellipse((x - 26 * scale, y, x + 26 * scale, y + 34 * scale), fill=fill)
    for offset_x, offset_y in ((-37, -21), (-12, -35), (16, -35), (41, -19)):
        draw.ellipse(
            (x + (offset_x - 11) * scale, y + (offset_y - 13) * scale,
             x + (offset_x + 11) * scale, y + (offset_y + 13) * scale),
            fill=fill,
        )


def phone(source, width, angle):
    screenshot = Image.open(source).convert("RGB")
    screenshot = screenshot.crop((0, 100, screenshot.width, screenshot.height - 68))
    inset = round(width * 0.024)
    inner_width = width - inset * 2
    inner_height = round(screenshot.height * inner_width / screenshot.width)
    screenshot = screenshot.resize((inner_width, inner_height), Image.Resampling.LANCZOS)
    panel = Image.new("RGBA", (width, inner_height + inset * 2))
    panel_mask = Image.new("L", panel.size)
    ImageDraw.Draw(panel_mask).rounded_rectangle(
        (0, 0, panel.width - 1, panel.height - 1), radius=round(width * 0.075), fill=255
    )
    white = Image.new("RGBA", panel.size, COLORS["white"])
    panel.paste(white, (0, 0), panel_mask)
    screen_mask = Image.new("L", screenshot.size)
    ImageDraw.Draw(screen_mask).rounded_rectangle(
        (0, 0, screenshot.width - 1, screenshot.height - 1), radius=round(width * 0.055), fill=255
    )
    panel.paste(screenshot, (inset, inset), screen_mask)
    return panel.rotate(angle, Image.Resampling.BICUBIC, expand=True)


def paste_phone(canvas, source, width, angle, x, y, shadow_blur):
    device = phone(source, width, angle)
    alpha = device.getchannel("A")
    shadow = Image.new("RGBA", device.size, (105, 66, 60, 0))
    shadow.putalpha(alpha.point(lambda opacity: round(opacity * 0.27)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    canvas.alpha_composite(shadow, (x + round(shadow_blur * 0.65), y + round(shadow_blur * 0.8)))
    canvas.alpha_composite(device, (x, y))


def brand(canvas, x, y, icon_size, text_size):
    icon = Image.open(ROOT / "res" / "app_icon.png").convert("RGBA")
    icon = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (x, y))
    draw = ImageDraw.Draw(canvas)
    draw.text((x + icon_size + round(icon_size * 0.24), y + round(icon_size * 0.18)),
              "寵物領養紀錄", font=font(text_size), fill=COLORS["ink"])


def label(draw, x, y, text_value, text_size, padding_x, padding_y):
    text_box = draw.textbbox((0, 0), text_value, font=font(text_size))
    width = text_box[2] - text_box[0] + padding_x * 2
    height = text_box[3] - text_box[1] + padding_y * 2
    draw.rounded_rectangle((x, y, x + width, y + height), radius=height // 2, fill=COLORS["white"])
    draw.text((x + padding_x, y + padding_y - text_box[1]), text_value,
              font=font(text_size), fill=COLORS["pink"])


def feature_chip(draw, x, y, width, height, title):
    draw.rounded_rectangle((x, y, x + width, y + height), radius=height // 2, fill="#FFFFFF")
    draw.ellipse((x + 26, y + height / 2 - 12, x + 50, y + height / 2 + 12), fill="#E8979C")
    text_size = round(height * 0.37)
    draw.text((x + 70, y + round(height * 0.23)), title, font=font(text_size), fill=COLORS["ink"])


def title_asset():
    size = (5244, 2950)
    canvas = background(size)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((2630, -470, 5770, 2650), fill="#F7D9D2")
    draw.ellipse((-580, 2280, 610, 3470), outline="#F3D8D0", width=7)
    paw(draw, 2410, 595, 3.4, "#F2CFC9")
    brand(canvas, 300, 260, 174, 92)
    draw = ImageDraw.Draw(canvas)
    label(draw, 302, 710, "讓愛，有地方開始", 58, 50, 24)
    draw.text((278, 972), "遇見牠，", font=font(225), fill=COLORS["ink"])
    draw.text((278, 1240), "把日子過成我們。", font=font(198), fill=COLORS["pink"])
    draw.text((302, 1738), "尋找等待家的毛孩，", font=font(69), fill=COLORS["muted"])
    draw.text((302, 1840), "也記下和牠相伴的每一天。", font=font(69), fill=COLORS["muted"])
    feature_chip(draw, 302, 2400, 670, 138, "領養毛孩")
    feature_chip(draw, 1000, 2400, 670, 138, "走失資訊")
    feature_chip(draw, 1698, 2400, 670, 138, "生活紀錄")
    paste_phone(canvas, ROOT / "res/screenshot/Screenshot_20261015_134623.png", 1000, -9, 3900, 470, 72)
    paste_phone(canvas, ROOT / "res/screenshot/Screenshot_20261015_135827.png", 1160, 7, 2810, 252, 80)
    canvas.convert("RGB").save(OUTPUT / "title_5244x2950.png", optimize=True)


def wide_asset():
    size = (3840, 1646)
    canvas = background(size)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((1970, -670, 4190, 1540), fill="#F7D9D2")
    draw.ellipse((-380, 1280, 580, 2240), outline="#F3D8D0", width=5)
    paw(draw, 1860, 320, 2.2, "#F2CFC9")
    brand(canvas, 185, 140, 112, 61)
    draw = ImageDraw.Draw(canvas)
    label(draw, 188, 440, "讓愛，有地方開始", 38, 33, 17)
    draw.text((164, 620), "遇見牠，", font=font(150), fill=COLORS["ink"])
    draw.text((164, 814), "把日子過成我們。", font=font(130), fill=COLORS["pink"])
    draw.text((190, 1132), "從領養相遇，到珍藏毛孩日常。", font=font(49), fill=COLORS["muted"])
    feature_chip(draw, 188, 1345, 425, 87, "領養毛孩")
    feature_chip(draw, 637, 1345, 425, 87, "走失資訊")
    feature_chip(draw, 1086, 1345, 425, 87, "生活紀錄")
    paste_phone(canvas, ROOT / "res/screenshot/Screenshot_20261015_134623.png", 655, -9, 3030, 200, 48)
    paste_phone(canvas, ROOT / "res/screenshot/Screenshot_20261015_135827.png", 760, 7, 2280, 95, 54)
    canvas.convert("RGB").save(OUTPUT / "wide_3840x1646.png", optimize=True)


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    title_asset()
    wide_asset()
    print(OUTPUT / "title_5244x2950.png")
    print(OUTPUT / "wide_3840x1646.png")


if __name__ == "__main__":
    main()

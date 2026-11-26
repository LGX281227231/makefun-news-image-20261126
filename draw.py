"""Draw entry.png: a clean newspaper front page summing up
Thursday 26 November 2026 in five stories. Run locally with PIL;
the entry itself only ships the finished PNG (see main.py).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (255, 255, 255)
NAVY = (15, 42, 68)
RED = (178, 34, 34)
INK = (20, 20, 20)
GREY = (90, 90, 90)
RULE = (210, 210, 210)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    ("1", (178, 34, 34), "UNITED STATES  /  TRADE",
     "US proposes new tariffs; China hit hardest",
     "Washington moves against what it calls structural excess industrial capacity; "
     "India faces a 17% rate and Brazil 10% on aircraft."),
    ("2", (15, 42, 68), "UNITED STATES",
     "Macy\u2019s parade postponed for first time by storm",
     "The 100th parade moves to Saturday as a nor\u2019easter brings high winds "
     "and heavy rain to New York City."),
    ("3", (0, 110, 80), "NORTH KOREA",
     "Kim orders wider rollout of tactical nuclear weapons",
     "Kim Jong Un inspects warheads in a rare public display and dismisses "
     "Trump\u2019s offer to resume talks."),
    ("4", (150, 90, 0), "EGYPT",
     "Fuel tanker fire on Cairo ring road kills at least 30",
     "A tanker overturns and catches fire in Giza; at least 30 dead and 15 injured, "
     "the Health Ministry says."),
    ("5", (70, 70, 160), "SPACE  /  PAKISTAN",
     "Pakistan\u2019s first astronaut boards Tiangong",
     "The first Pakistani in orbit becomes the first foreign astronaut to visit "
     "the Tiangong space station."),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x0, x1 = 40, 984

    # Masthead
    d.rectangle([x0, 28, x1, 112], fill=NAVY)
    d.text((x0 + 20, 44), "WORLD NEWS", font=font(FONT_BOLD, 52), fill=(255, 255, 255))
    d.text((x1 - 20, 62), "26 NOV 2026", font=font(FONT_BOLD, 30), fill=(255, 210, 80), anchor="ra")
    # Date line
    d.text((x0, 128), "THURSDAY  26  NOVEMBER  2026", font=font(FONT_BOLD, 30), fill=NAVY)
    d.text((x0, 168), "The day in five stories \u2014 from Washington to Tiangong",
           font=font(FONT_REG, 22), fill=GREY)
    d.line([x0, 200, x1, 200], fill=RED, width=4)

    y = 222
    for num, color, tag, head, body in STORIES:
        # Number badge
        d.rounded_rectangle([x0, y, x0 + 54, y + 54], radius=10, fill=color)
        d.text((x0 + 27, y + 26), num, font=font(FONT_BOLD, 30), fill=(255, 255, 255), anchor="mm")
        tx = x0 + 74
        tw = x1 - tx
        d.text((tx, y + 2), tag, font=font(FONT_BOLD, 17), fill=color)
        hl = wrap(d, head, font(FONT_BOLD, 27), tw)
        hy = y + 24
        for line in hl:
            d.text((tx, hy), line, font=font(FONT_BOLD, 27), fill=INK)
            hy += 32
        bl = wrap(d, body, font(FONT_REG, 20), tw)
        by = hy + 4
        for line in bl:
            d.text((tx, by), line, font=font(FONT_REG, 20), fill=(60, 60, 60))
            by += 25
        y = by + 12
        if num != "5":
            d.line([x0, y - 8, x1, y - 8], fill=RULE, width=2)

    # Also today strip (fills the page, adds breadth)
    d.rounded_rectangle([x0, y + 2, x1, y + 104], radius=10, fill=(240, 244, 248))
    d.text((x0 + 16, y + 12), "ALSO TODAY", font=font(FONT_BOLD, 18), fill=NAVY)
    also = [
        "Australia and Solomon Islands sign a security pact; no foreign bases allowed.",
        "Duran Duran guitarist Andy Taylor dies at 65.",
        "Russia\u2019s Murmansk governor detained in a corruption probe; Putin fires him.",
    ]
    ay = y + 38
    for line in also:
        d.text((x0 + 16, ay), "\u2022  " + line, font=font(FONT_REG, 18), fill=(50, 50, 50))
        ay += 24

    # Footer
    d.line([x0, 968, x1, 968], fill=RULE, width=2)
    d.text((x0, 978), "Headlines as reported on 26 November 2026",
           font=font(FONT_REG, 18), fill=GREY)
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()

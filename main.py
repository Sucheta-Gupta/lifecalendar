from fastapi import FastAPI
from fastapi.responses import Response
from PIL import Image, ImageDraw
from datetime import date
import io

app = FastAPI()


@app.get("/calendar")
def life_calendar():
    # ===== Canvas (iPhone Pro wallpaper) =====
    WIDTH = 1179
    HEIGHT = 2556

    # ===== Colors =====
    BG_COLOR = "#0f0f10"
    DOT_GREY = "#3a3a3c"
    DOT_RED = "#ff3b30"

    # ===== Grid config (life calendar style) =====
    DAYS = 365
    COLS = 15
    DOT_SIZE = 8
    GAP = 14

    # ===== Create image =====
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    rows = (DAYS + COLS - 1) // COLS

    grid_width = COLS * DOT_SIZE + (COLS - 1) * GAP
    grid_height = rows * DOT_SIZE + (rows - 1) * GAP

    start_x = (WIDTH - grid_width) // 2
    start_y = 420  # top padding like original

    # ===== Today dot =====
    today = date.today()
    start_of_year = date(today.year, 1, 1)
    today_index = (today - start_of_year).days

    # ===== Draw dots =====
    for day in range(DAYS):
        row = day // COLS
        col = day % COLS

        x = start_x + col * (DOT_SIZE + GAP)
        y = start_y + row * (DOT_SIZE + GAP)

        color = DOT_RED if day == today_index else DOT_GREY

        draw.ellipse(
            (x, y, x + DOT_SIZE, y + DOT_SIZE),
            fill=color
        )

    # ===== Output =====
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return Response(buf.getvalue(), media_type="image/png")

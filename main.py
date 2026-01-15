from fastapi import FastAPI, Response
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import date

app = FastAPI()

# iPhone 17 Pro wallpaper size
WIDTH = 1290
HEIGHT = 2796
COLUMNS = 15
ROWS = 25
DOT_RADIUS = 15  # slightly bigger
GRID_WIDTH = 900
GRID_HEIGHT = 1500

# Move grid down by 1 row
GRID_X = (WIDTH - GRID_WIDTH) / 2
GRID_Y = (HEIGHT - GRID_HEIGHT) / 2 + GRID_HEIGHT / ROWS  # move down by 1 row height

# Font setup (Pillow default if no .ttf available)
try:
    FONT = ImageFont.truetype("Arial.ttf", 50)
except:
    FONT = ImageFont.load_default()


@app.get("/calendar")
def life_calendar():
    today = date.today()
    day_of_year = today.timetuple().tm_yday  # 1 to 365

    # dark neutral background
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    h_spacing = GRID_WIDTH / (COLUMNS - 1)
    v_spacing = GRID_HEIGHT / (ROWS - 1)

    for i in range(ROWS):
        for j in range(COLUMNS):
            dot_index = i * COLUMNS + j
            if dot_index >= 365:
                continue

            x = GRID_X + j * h_spacing
            y = GRID_Y + i * v_spacing

            color = (100, 100, 100)  # grey dot
            if dot_index + 1 == day_of_year:
                color = (255, 0, 0)  # red dot for today

            draw.ellipse(
                [x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS],
                fill=color
            )

    # Add bottom text: "Xd left • Y%"
    days_left = 365 - day_of_year
    percent_done = int(day_of_year / 365 * 100)
    text = f"{days_left}d left • {percent_done}%"

    # Measure text size for center alignment
    bbox = draw.textbbox((0, 0), text, font=FONT)  # returns (x0, y0, x1, y1)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (WIDTH - text_width) / 2
    text_y = HEIGHT - text_height - 50  # 50px from bottom

    draw.text((text_x, text_y), text, font=FONT, fill=(200, 200, 200))

    # Convert to PNG response
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")

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
DOT_RADIUS = 15  # dot size
GRID_WIDTH = 900
GRID_HEIGHT = 1500

# Grid starts 1 row down
GRID_X = (WIDTH - GRID_WIDTH) / 2
GRID_Y = (HEIGHT - GRID_HEIGHT) / 2 + (GRID_HEIGHT / ROWS)  # move grid 1 row down

# Font for bottom text same size as dots
try:
    TEXT_FONT = ImageFont.truetype("Arial.ttf", DOT_RADIUS * 4)  # font = dot size
except:
    TEXT_FONT = ImageFont.load_default()


@app.get("/calendar")
def life_calendar():
    today = date.today()
    day_of_year = today.timetuple().tm_yday  # 1 to 365

    # Dark background
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    h_spacing = GRID_WIDTH / (COLUMNS - 1)
    v_spacing = GRID_HEIGHT / (ROWS - 1)

    # Draw dots
    for i in range(ROWS):
        for j in range(COLUMNS):
            dot_index = i * COLUMNS + j
            if dot_index >= 365:
                continue

            x = GRID_X + j * h_spacing
            y = GRID_Y + i * v_spacing  # already shifted 1 row down

            # Color Logic
            if dot_index + 1 == day_of_year:
                color = (255, 0, 0)      # Today: Bright Red
            elif dot_index + 1 < day_of_year:
                color = (70, 70, 70)     # Past: Light/Dim Gray
            else:
                color = (130, 130, 130)  # Future: Medium Gray (Standard)

            draw.ellipse(
                [x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS],
                fill=color
            )

    # Bottom text: "Xd left • Y%"
    days_left = 365 - day_of_year
    percent_done = int(day_of_year / 365 * 100)
    text_left = f"{days_left}d left"
    text_percent = f" • {percent_done}%"

    # Measure text width for center alignment
    bbox_left = draw.textbbox((0, 0), text_left, font=TEXT_FONT)
    bbox_percent = draw.textbbox((0, 0), text_percent, font=TEXT_FONT)
    width_left = bbox_left[2] - bbox_left[0]
    width_percent = bbox_percent[2] - bbox_percent[0]
    total_width = width_left + width_percent

    text_x = (WIDTH - total_width) / 2

    # Text 2 rows above bottom
    row_height = GRID_HEIGHT / ROWS
    text_y = HEIGHT - (bbox_left[3] - bbox_left[1]) - 50 - 2 * row_height

    # Draw "Xd left" in red
    draw.text((text_x, text_y), text_left, font=TEXT_FONT, fill=(255, 0, 0))
    # Draw "• Y%" in grey
    draw.text((text_x + width_left, text_y), text_percent, font=TEXT_FONT, fill=(200, 200, 200))

    # Convert to PNG response
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")

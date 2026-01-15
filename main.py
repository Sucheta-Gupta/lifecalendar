from fastapi import FastAPI, Response
from PIL import Image, ImageDraw
from io import BytesIO
from datetime import date

app = FastAPI()

# iPhone 17 Pro wallpaper size
WIDTH = 1290
HEIGHT = 2796
COLUMNS = 15
ROWS = 25
DOT_RADIUS = 12  # small dot
GRID_WIDTH = 900  # total width of dot grid
GRID_HEIGHT = 1500  # total height of dot grid
GRID_X = (WIDTH - GRID_WIDTH) / 2  # center horizontally
GRID_Y = (HEIGHT - GRID_HEIGHT) / 2  # center vertically

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
                color = (255, 0, 0)  # today red dot

            draw.ellipse(
                [x - DOT_RADIUS, y - DOT_RADIUS, x + DOT_RADIUS, y + DOT_RADIUS],
                fill=color
            )

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")

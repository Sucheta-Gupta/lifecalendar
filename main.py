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
DOT_RADIUS = 18  # dot radius in pixels
MARGIN_X = 50    # horizontal margin
MARGIN_Y = 100   # vertical margin

@app.get("/calendar")
def life_calendar():
    today = date.today()
    day_of_year = today.timetuple().tm_yday  # 1 to 365

    # create white background
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    h_spacing = (WIDTH - 2*MARGIN_X) / (COLUMNS - 1)
    v_spacing = (HEIGHT - 2*MARGIN_Y) / (ROWS - 1)

    for i in range(ROWS):
        for j in range(COLUMNS):
            dot_index = i * COLUMNS + j
            if dot_index >= 365:
                continue

            x = MARGIN_X + j * h_spacing
            y = MARGIN_Y + i * v_spacing

            color = (200, 200, 200)  # grey dot
            if dot_index + 1 == day_of_year:
                color = (255, 0, 0)  # today red dot

            draw.ellipse(
                [x-DOT_RADIUS, y-DOT_RADIUS, x+DOT_RADIUS, y+DOT_RADIUS],
                fill=color
            )

    # save image to response
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="image/png")

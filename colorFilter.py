# Enrique Vega
# 4/27/2026
from PIL import Image, ImageOps
from flask import Flask, request, render_template
import random

app = Flask(__name__)

#Jigsaw function
def scramble_jigsaw(img, grid_size = 4):
   w, h = img.size

   tile_w = w // grid_size
   tile_h = h // grid_size

   tiles = []

   for row in range(grid_size):
      for col in range(grid_size):
         left = col * tile_w
         upper = row * tile_h

         # Last column/row must extend to the edge
         right = (col + 1) * tile_w if col < grid_size - 1 else w
         lower = (row + 1) * tile_h if row < grid_size - 1 else h

         # Safety check: ensure valid crop box
         if right > left and lower > upper:
             tiles.append(img.crop((left, upper, right, lower)))

    
   random.shuffle(tiles)
   scrambled = Image.new("RGB", (w, h))
   index = 0

   for row in range(grid_size):
      for col in range(grid_size):
         left = col * tile_w
         upper = row * tile_h

         scrambled.paste(tiles[index], (left, upper))
         index += 1

   return scrambled
# Sepia Color Filter

def sepia(p):
    # tint shadows
    if p[0] < 63:
        r,g,b = int(p[0] * 1.1), p[1], int(p[2] * 0.9)
    # tint midtones
    elif p[0] > 62 and p[0] < 192:
        r,g,b = int(p[0] * 1.15), p[1], int(p[2] * 0.85)
    # tint highlights
    else:
        r = int(p[0] * 1.08)
        g,b = p[1], int(p[2] * 0.5)
    return (r, g, b)


def apply_sepia(img): 
    width, height = img.size 
    new_img = Image.new("RGB", (width, height)) 

    for x in range(width): 
        for y in range(height): 
            pixel = img.getpixel((x, y)) 
            new_pixel = sepia(pixel) 
            new_img.putpixel((x, y), new_pixel) 
    return new_img

# Negative filter
def apply_negative(img):
    return ImageOps.invert(img)

@app.route("/", methods=["GET", "POST"])
def index():
    output = None

    if request.method == "POST":
        file = request.files["image"]
        filter_type = request.form["filter"]

        img = Image.open(file).convert("RGB")

        if filter_type == "sepia":
            img = apply_sepia(img)
        elif filter_type == "negative":
            img = apply_negative(img)
        if filter_type == "scramble":
            img = scramble_jigsaw(img)

    return render_template("buttons.html", output=output)

if __name__ == "__main__":
    app.run(debug=True)

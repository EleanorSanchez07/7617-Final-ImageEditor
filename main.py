# CST 205
# Project: 
# CSUMB Image Filter Editor
# Team: 
# Humberto Ramirez, Eleanor Sanchez, Abraham Sanchez, Jesus Ortiz, Enrique Vega
# GITBUH: https://github.com/EleanorSanchez07/7617-Final-ImageEditor

from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_bootstrap import Bootstrap5
from PIL import Image, ImageOps
from colormath.color_objects import sRGBColor, LabColor # In control of Chroma
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import numpy
import time
import os
import random
from multiprocessing import Pool
from typing import Any
# ABRAHAM SANCHEZ-PEREYRA - STARTING LAYOUT AND FOLDER INPUT/UPLOAD
app = Flask(__name__) # Initiates The Flask App
bootstrap = Bootstrap5(app)

# Variable saying where to save images (a constant)
UPLOAD_FOLDER = 'static/uploads' 
os.makedirs(UPLOAD_FOLDER, exist_ok=True) # Makes the folder through operating system

# Patching numpy so colormath doesn't break
def patch_asscalar(a):
    return a.item()

setattr(numpy, "asscalar", patch_asscalar)

# HUMBERTO RAMIREZ - MIRROR FUNCTION
def mirror_image(path):
    img = Image.open(path)
    img = img.transpose(Image.FLIP_LEFT_RIGHT) # Flips the image from left to right
    img.save(path)

# JESUS ORTIZ - SHRINK & GROW FUNCTIONS
def shrink_image(path):
    img = Image.open(path)
    width = img.width // 2   # Shrink the image by dividing w h
    height = img.height // 2
    img = img.resize((width, height))
    img.save(path)

def grow_image(path):
    img = Image.open(path)
    width = img.width * 2    # Multiplies the size to grow
    height = img.height * 2
    img = img.resize((width, height))
    img.save(path)

# ELEANOR SANCHEZ - CROP & CHROMA KEY FUNCTIONS
def crop(orig_image, top_left, bottom_right):
    orig_width = orig_image.width
    orig_height = orig_image.height
    new_width = bottom_right[0] - top_left[0]
    new_height = bottom_right[1] - top_left[1]

    try:
        assert (
            new_width > 0 and new_height > 0 and
            top_left[0] >= 0 and top_left[1] >= 0 and
            bottom_right[0] <= orig_width and
            bottom_right[1] <= orig_height
        )
    except AssertionError:
        print("Invalid Crop")
        return None

    cropped_image = Image.new("RGB", (new_width, new_height))
    for x in range(new_width):
        for y in range(new_height):
            _x = x + top_left[0]
            _y = y + top_left[1]
            pixel = orig_image.getpixel((_x, _y))
            cropped_image.putpixel((x, y), pixel)
    return cropped_image

def crop_image(path):
    img = Image.open(path).convert("RGB")
    width, height = img.size
    # Crop center of image
    top_left = (width // 4, height // 4)
    bottom_right = (3 * width // 4, 3 * height // 4)
    cropped = crop(img, top_left, bottom_right)
    if cropped:
        cropped.save(path)

def chromakey_pixel_replacement(original_pix, replacement_pix, target_lab):
    # Convert the current pixel to Lab for comparison
    original_rgb = sRGBColor(original_pix[0], original_pix[1], original_pix[2], is_upscaled=True)
    original_lab = convert_color(original_rgb, LabColor)
    
    # If the color is close enough to the chroma key, return replacement. Otherwise, original.
    # Color distance is the killer function regarding time complexity, and the reason for my use of multiprocessing.
    if delta_e_cie2000(original_lab, target_lab) < 77:
        return replacement_pix
    else:
        return original_pix

def chromakey(original: Image.Image, new_background: Image.Image, chroma_color: tuple[int, int, int], save_path: str | None = None):
    original = original.resize((256, 256))
    new_background = new_background.resize(original.size)
    
    target_rgb = sRGBColor(chroma_color[0], chroma_color[1], chroma_color[2], is_upscaled=True)
    target_lab = convert_color(target_rgb, LabColor)
    
    #List of all the pixels for the foreground image  (orig_pixels) and background pixels (new_pixels)
    orig_pixels = list(original.getdata())
    new_pixels = list(new_background.getdata())

     # t = time.time() # Start timer
    with Pool() as pool:
        # Take async results and use a list comprehension to put those results into the data of our return image. Using Pool().apply_async() 
        # runs this on multiple threads (in theory) for better performance, aproximately a 50% runtime decrease from my previous method.
        async_results = [
            pool.apply_async(chromakey_pixel_replacement, args=(orig_pixels[i], new_pixels[i], target_lab)) 
            for i in range(len(orig_pixels))
        ]
        result_pixels = [ar.get() for ar in async_results]
     # print(time.time() - t) # Print timer result.

     # Put the data into our image, save it, and return it.
    original.putdata(result_pixels) #pyright: ignore[reportArgumentType]
     # original.show()
    if save_path:
        original.save(save_path)
    return original

# HUMBERTO RAMIREZ - STACK FUNCTIONS
def stack_image(base_path, overlay_path):
    base = Image.open(base_path)
    overlay = Image.open(overlay_path)
    overlay = overlay.resize((base.width // 2, base.height // 2)) # Resize overlap
    x = (base.width - overlay.width) // 2 # Center
    y = (base.height - overlay.height) // 2
    base.paste(overlay, (x, y)) # Paste overlay
    base.save(base_path)

def random_stack_image(base_path, overlay_path):
    base = Image.open(base_path)
    overlay = Image.open(overlay_path)
    overlay = overlay.resize((base.width // 2, base.height // 2))
    max_x = base.width - overlay.width
    max_y = base.height - overlay.height
    x = random.randint(0, max_x) # Pick random position
    y = random.randint(0, max_y)
    base.paste(overlay, (x, y))
    base.save(base_path)

# ENRIQUE VEGA - JIGSAW, SEPIA, & NEGATIVE
def scramble_jigsaw_image(path, grid_size=4):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    tile_w, tile_h = w // grid_size, h // grid_size
    tiles = []
    # Cuts the image into sections
    for row in range(grid_size):
        for col in range(grid_size):
            left = col * tile_w
            upper = row * tile_h
            right = (col + 1) * tile_w if col < grid_size - 1 else w
            lower = (row + 1) * tile_h if row < grid_size - 1 else h
            tile = img.crop((left, upper, right, lower))
            tiles.append(tile)
    random.shuffle(tiles)
    scrambled = Image.new("RGB", (w, h))
    index = 0
    # Scrambles the tiles
    for row in range(grid_size):
        for col in range(grid_size):
            left = col * tile_w
            upper = row * tile_h
            scrambled.paste(tiles[index], (left, upper))
            index += 1
    scrambled.save(path)

def sepia_pixel(pixel):
    r, g, b = pixel
    # Tint shadows, midtones, and highlights differently
    if r < 63:
        r, b = int(r * 1.1), int(b * 0.9)
    elif r < 192:
        r, b = int(r * 1.15), int(b * 0.85)
    else:
        r, b = int(r * 1.08), int(b * 0.5)
    return (min(r, 255), min(g, 255), min(b, 255))

def apply_sepia_image(path):
    img = Image.open(path).convert("RGB")
    width, height = img.size
    new_img = Image.new("RGB", (width, height))
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            new_img.putpixel((x, y), sepia_pixel(pixel))
    new_img.save(path)

def apply_negative_image(path):
    img = Image.open(path).convert("RGB")
    img = ImageOps.invert(img)
    img.save(path)

# MAIN ROUTE
@app.route('/', methods=['GET', 'POST'])
def home():
    image_name = None
    if request.method == 'POST':
        # Upload image
        file = request.files.get('image_file')
        if file and file.filename != '':
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            image_name = file.filename
        # Apply filters by requesting to the html
        else:
            image_name = request.form.get('current_image')
            if image_name:
                filepath = os.path.join(UPLOAD_FOLDER, image_name)
                f_type = request.form.get('filter')
                
                if f_type == 'mirror': mirror_image(filepath)
                if f_type == 'shrink': shrink_image(filepath)
                if f_type == 'grow': grow_image(filepath)
                if f_type == 'crop': crop_image(filepath)
                if f_type == 'sepia': apply_sepia_image(filepath)
                if f_type == 'negative': apply_negative_image(filepath)
                if f_type == 'pixel_shuffle': scramble_jigsaw_image(filepath)
                
                if f_type == 'chroma':
                    bg_file = request.files.get('background_image')
                    if bg_file and bg_file.filename != '':
                        bg_path = os.path.join(UPLOAD_FOLDER, bg_file.filename)
                        bg_file.save(bg_path)
                        chromakey(Image.open(filepath).convert("RGB"), 
                                  Image.open(bg_path).convert("RGB"), 
                                  (0, 255, 0), save_path=filepath)
                
                if f_type == 'stack':
                    ov_file = request.files.get('overlay_image')
                    if ov_file and ov_file.filename != '':
                        ov_path = os.path.join(UPLOAD_FOLDER, ov_file.filename)
                        ov_file.save(ov_path)
                        stack_image(filepath, ov_path)

                if f_type == 'random_stack':
                    ov_file = request.files.get('overlay_image')
                    if ov_file and ov_file.filename != '':
                        ov_path = os.path.join(UPLOAD_FOLDER, ov_file.filename)
                        ov_file.save(ov_path)
                        random_stack_image(filepath, ov_path)

                # ABRAHAM SANCHEZ - SAVE & RESET LOGIC
                if f_type == 'save': # Checks for the save click button
                    return send_from_directory(UPLOAD_FOLDER, image_name, as_attachment=True)
                
                if f_type == 'reset': # Checks for the reset click button
                    return redirect(url_for('home')) # Refreshes to start from scratch

    return render_template('index.html', image_name=image_name)

if __name__ == '__main__':
    app.run(debug=True)

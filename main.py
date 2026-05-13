from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from PIL import Image, ImageOps
from colormath.color_objects import sRGBColor, LabColor #In control of Chroma
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from flask import Flask, render_template, request, send_from_directory, redirect, url_for #Needed for reset and save filters
import numpy
import time
import os
import random
from multiprocessing import Pool
from typing import Any




app = Flask(__name__)#Initiates The Flask App
bootstrap = Bootstrap5(app)


UPLOAD_FOLDER = 'static/uploads' #Variable saying where to save images (a constant)# makes the folder through operating system




os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Humberto Ramirez
# MIRROR FUNCTION
def mirror_image(path):
    img = Image.open(path)   #Flips the image from left to right
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    img.save(path)


# Jesus Ortiz
# SHRINK FUNCTION
def shrink_image(path):
    img = Image.open(path)


    width = img.width // 2   # Shrink the image by dividing w h
    height = img.height // 2


    img = img.resize((width, height))
    img.save(path)


#Jesus Ortiz
# GROW FUNCTION
def grow_image(path):
    img = Image.open(path)


    width = img.width * 2  # multiplies the size to grow
    height = img.height * 2


    img = img.resize((width, height))
    img.save(path)


# Eleanor Sanchez
# CROP
def crop(orig_image, top_left, bottom_right):
    orig_width = orig_image.width
    orig_height = orig_image.height


    new_width = bottom_right[0] - top_left[0]
    new_height = bottom_right[1] - top_left[1]


    try:
        assert (
            new_width > 0 and
            new_height > 0 and
            top_left[0] >= 0 and
            top_left[1] >= 0 and
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




# CROP
def crop_image(path):
    img = Image.open(path).convert("RGB")


    width, height = img.size


    # Crop center of image
    top_left = (width // 4, height // 4)
    bottom_right = (3 * width // 4, 3 * height // 4)


    cropped = crop(img, top_left, bottom_right)


    if cropped:
        cropped.save(path)
   
# Elanor Shanchez
# CHROMA KEY FUNCTION
def chroma_image(original_path, background_path):
    original = Image.open(original_path).convert("RGB")
    background = Image.open(background_path).convert("RGB")


    # Make background same size as original
    background = background.resize(original.size)


    width, height = original.size


    new_image = Image.new("RGB", (width, height))


    # Green screen color
    chroma_color = (0, 255, 0)


    for x in range(width):
        for y in range(height):
            original_pixel = original.getpixel((x, y))
            background_pixel = background.getpixel((x, y))


            r, g, b = original_pixel


            # If pixel is mostly green, replace it
            if g > 100 and g > r * 1.4 and g > b * 1.4:
                new_image.putpixel((x, y), background_pixel)
            else:
                new_image.putpixel((x, y), original_pixel)


    new_image.save(original_path)


# Humberto Ramirez
# STACK
def stack_image(base_path, overlay_path):
    base = Image.open(base_path)
    overlay = Image.open(overlay_path)


    # Resize overlap
    overlay = overlay.resize((base.width // 2, base.height // 2))


    # Center
    x = (base.width - overlay.width) // 2
    y = (base.height - overlay.height) // 2


    # Paste overlay
    base.paste(overlay, (x, y))


    base.save(base_path)


# Humberto Ramirez
# Random Stack
def random_stack_image(base_path, overlay_path):
    base = Image.open(base_path)
    overlay = Image.open(overlay_path)


    # Resize overlay
    overlay = overlay.resize((base.width // 2, base.height // 2))


    # Pick random position
    max_x = base.width - overlay.width
    max_y = base.height - overlay.height


    x = random.randint(0, max_x)
    y = random.randint(0, max_y)


    # Paste overlay
    base.paste(overlay, (x, y))


    base.save(base_path)


# Enrique Vega
# SCRAMBLE JIGSAW FUNCTION
def scramble_jigsaw_image(path, grid_size=4):
    img = Image.open(path).convert("RGB")


    w, h = img.size
    tile_w = w // grid_size
    tile_h = h // grid_size


    tiles = []
# Cuts the image into sections
    for row in range(grid_size):
        for col in range(grid_size):
            left = col * tile_w
            upper = row * tile_h


            tiles.append(tile)


    random.shuffle(tiles)


    scrambled = Image.new("RGB", (w, h))
    index = 0
	# scrambles the tiles
    for row in range(grid_size):
        for col in range(grid_size):
            left = col * tile_w
            upper = row * tile_h


            scrambled.paste(tiles[index], (left, upper))
            index += 1


    scrambled.save(path)


# Enrique Vega
# SEPIA FUNCTION
def sepia_pixel(pixel):
    r, g, b = pixel
	# tint shadows
    if r < 63:
        r = int(r * 1.1)
        b = int(b * 0.9)
	# tint midtones
    elif r < 192:
        r = int(r * 1.15)
        b = int(b * 0.85)
	# tint highlights
    else:
        r = int(r * 1.08)
        b = int(b * 0.5)


    r = min(r, 255)
    g = min(g, 255)
    b = min(b, 255)


    return (r, g, b)




def apply_sepia_image(path):
    img = Image.open(path).convert("RGB")
    width, height = img.size


    new_img = Image.new("RGB", (width, height))


    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            new_pixel = sepia_pixel(pixel)
            new_img.putpixel((x, y), new_pixel)


    new_img.save(path)


# Enrique Vega
# NEGATIVE FUNCTION
def apply_negative_image(path):
    img = Image.open(path).convert("RGB")
    img = ImageOps.invert(img)
    img.save(path)
 




# ROUTE
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


                if request.form.get('filter') == 'mirror':
                    mirror_image(filepath)


                if request.form.get('filter') == 'shrink':
                    shrink_image(filepath)


                if request.form.get('filter') == 'grow':
                    grow_image(filepath)
               
                if request.form.get('filter') == 'crop':
                    crop_image(filepath)
                if request.form.get('filter') == 'chroma':
                    background_file = request.files.get('background_image')
                   
                    if background_file and background_file.filename != '':
                        background_path = os.path.join(UPLOAD_FOLDER, background_file.filename)
                        background_file.save(background_path)
                       
                        chroma_image(filepath, background_path)


                if request.form.get('filter') == 'stack':
                    overlay_file = request.files.get('overlay_image')
                    if overlay_file and overlay_file.filename != '':
                        overlay_path = os.path.join(UPLOAD_FOLDER, overlay_file.filename)
                        overlay_file.save(overlay_path)
                       
                        stack_image(filepath, overlay_path)
   
                if request.form.get('filter') == 'sepia':
                    apply_sepia_image(filepath)


                if request.form.get('filter') == 'negative':
                    apply_negative_image(filepath)
                   
                if request.form.get('filter') == 'pixel_shuffle':
                    scramble_jigsaw_image(filepath)


                if request.form.get('filter') == 'random_stack':
                    overlay_file = request.files.get('overlay_image')
                    if overlay_file and overlay_file.filename != '':
                        overlay_path = os.path.join(UPLOAD_FOLDER, overlay_file.filename)
                        overlay_file.save(overlay_path)
                       
                        random_stack_image(filepath, overlay_path)
#Abraham Sanchez
                if request.form.get('filter') == 'save': #Checks for the save click button
                    return send_from_directory(UPLOAD_FOLDER, image_name, as_attachment=True)
                if request.form.get('filter') == 'reset': #Checks for the reset click button


                    return redirect(url_for('home'))#refreshes to start from scratch




    return render_template('index.html', image_name=image_name)




if __name__ == '__main__':
    app.run(debug=True)




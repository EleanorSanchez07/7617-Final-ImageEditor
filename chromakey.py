from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from PIL import Image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

import numpy

def patch_asscalar(a):
    return a.item()

setattr(numpy, "asscalar", patch_asscalar)

app = Flask(__name__)
bs = Bootstrap5(app)

def chromakey(original: Image.Image, new_background: Image.Image, chroma_color: tuple[int, int, int], save_path: str = None): # pyright: ignore[reportArgumentType]
    # Changes size of images we're working on. Reduce for performance, max should be 1440x1440. Bigger = waste.
    # The heat death of the universe will occur before my laptop finishes with anything above 256x256.
    # new_background = new_background.resize((256, 256))
    original = original.resize(new_background.size)
    
    orig_pixels = list(original.get_flattened_data())
    new_pixels = list(new_background.get_flattened_data())

    chroma_lab = convert_color(sRGBColor(chroma_color[0], chroma_color[1], chroma_color[2]), LabColor)

    for pix_index in range(len(orig_pixels)):
        cur_pixel = convert_color(sRGBColor(orig_pixels[pix_index][0], orig_pixels[pix_index][1], orig_pixels[pix_index][2]), LabColor) # pyright: ignore[reportIndexIssue]        
        
        if delta_e_cie2000(cur_pixel, chroma_lab) < 30:
            orig_pixels[pix_index] = new_pixels[pix_index]
            
    original.putdata(orig_pixels) #pyright: ignore[reportArgumentType]
    # original.show()
    
    if(save_path != None):
        original.save(save_path)
        
    return original

# chromakey(Image.open("Space Desert.jpg"), Image.open("Eleanor Colorful.png"), (29, 40, 58), "chromafied.png")
@app.route("/eleanor.html")
def eleanorPage():
    chromakey(Image.open("./static/images/Space Desert.jpg"), Image.open("./static/images/Eleanor Colorful.png"), (29, 40, 58), "./static/images/chromafied.png");
    return render_template("eleanor.html")
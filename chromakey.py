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

def chromakey(src: Image.Image, replace: Image.Image, chroma_color: tuple[int, int, int], save_path: str = None): # pyright: ignore[reportArgumentType]
    # Changes size of images we're working on. Reduce for performance, max should be 1440x1440. Bigger = waste.
    # The heat death of the universe will occur before my laptop finishes with anything above 256x256.
    replace = replace.resize((256, 256))
    src = src.resize(replace.size)
    
    for x in range(src.width):
        for y in range(src.height):
            cur_pixel = src.getpixel((x,y))
            
            # RGB to lab for the colormath stuff.
            cur_pixel = convert_color(sRGBColor(cur_pixel[0], cur_pixel[1], cur_pixel[2]), LabColor) # pyright: ignore[reportIndexIssue, reportOptionalSubscript]
            chroma_lab = convert_color(sRGBColor(chroma_color[0], chroma_color[1], chroma_color[2]), LabColor)
            
            if delta_e_cie2000(cur_pixel, chroma_lab) < 77:
                src.putpixel((x,y), replace.getpixel((x,y))) # pyright: ignore[reportArgumentType]
 
    src.show()
    if(save_path != None):
        src.save(save_path)
    
    return src

# chromakey(Image.open("Space Desert.jpg"), Image.open("Eleanor Colorful.png"), (29, 40, 58), "chromafied.png")
@app.route("/eleanor.html")
def eleanorPage():
    chromakey(Image.open("./static/images/Space Desert.jpg"), Image.open("./static/images/Eleanor Colorful.png"), (29, 40, 58), "chromafied.png");
    return render_template("eleanor.html")
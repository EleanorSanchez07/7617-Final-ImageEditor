from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5 
from PIL import Image
import os 
import random

app = Flask (__name__)
bootstrap = Bootstrap5(app)
UPLOADS = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#Shrink Function 

def shrink_image(path):
    img = Image.open(path)

    width = img.width // 2
    height = img.height //2 

    img = img.resize()(width, height)
    img.save(path)

    # Grow Function 
def grow_image(path):
    img = Image.open(path)

    width = img.width * 2
    height = img.height * 2 

    img = img.resize()(width, height)
    img.save(path)



@app.route('/', methods=['GET', 'POST'])
def img():
    image_name = None
# Upload image 
    file = request.files.get('imgae_file')
    if file and file.filename != '':
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        image_name = file.filename
    else: 
        image_name = request.form.get('current_image')

        if image_name: 
            filepath = os.path.join(UPLOAD_FOLDER, image_name)   
        if request.form.get('filter') == 'shrink':
            shrink_image(filepath)
            
        if request.form.get('filter') == 'grow':
            grow_image(filepath)
    
    return render_template('index.html', image_name=image_name)

if __name__ == '__main__':
    app.run(debug=True)

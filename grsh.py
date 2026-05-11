from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5 
from PIL import Image
import os 

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

    if request.method =='POST': 
        file = request.files.get('image_file')
        filter_name = request.forms.get('filter')
        current_image = request.form.get('current_image')

    if file and file.filename != '': 
        path = os.path.join(app.config['UPLOADS'], file.filename)
        file.save(path)
        image_name = file.filename 
    
    elif filter_name == 'shrink' and current_image: 
        path = os.path.join(app.config['UPLOADS'], current_image)
        if os.path.exits(path): 
            shrink_image(path)
            image_name = current_image
    
    if filter_name == 'grow' and current_image: 
        path = os.path.join(app.config['UPLOADS'], current_image)
        if os.path.exits(path): 
            grow_image(path)
            image_name = current_image
            
        elif current_image: 
            image_name = current_image 

        return render_template('index.html', image_name=image_name)

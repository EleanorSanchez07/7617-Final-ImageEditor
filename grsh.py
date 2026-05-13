# Jesus Ortiz-Ramos
#Date: 04-29-26
#Course: CST205-01_2262: Multimedia Design & Progmng
# Growing and Shrinking File
# This is a simple web-based image resizer. 
#It allows a user to upload a picture and then use buttons to either double its size ("grow") or cut its size in half ("shrink").

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from PIL import Image
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# Create a folder to store uploaded pictures if it doesn't exist
UPLOADS = 'static/uploads'
if not os.path.exists(UPLOADS):
    os.makedirs(UPLOADS)

app.config['UPLOADS'] = UPLOADS

# Function to cut image dimensions in half
def shrink_image(path):
    img = Image.open(path)
    width = img.width // 2
    height = img.height // 2
    img = img.resize((width, height))
    img.save(path)

# Function to double image dimensions
def grow_image(path):
    img = Image.open(path)
    width = img.width * 2
    height = img.height * 2
    img = img.resize((width, height))
    img.save(path)

# Main route for the website (handles both showing the page and submitting forms)
@app.route('/', methods=['GET', 'POST'])
def im():
    image_name = None

    if request.method == 'POST':
        # Get data from the form (file, clicked button, and current filename)
        file = request.files.get('image_file')
        filter_name = request.form.get('filter')
        current_image = request.form.get('current_image')

        # Scenario 1: User uploads a brand new image
        if file and file.filename != '':
            path = os.path.join(app.config['UPLOADS'], file.filename)
            file.save(path)
            image_name = file.filename

        # Scenario 2: User clicks 'shrink' on an existing image
        elif filter_name == 'shrink' and current_image:
            path = os.path.join(app.config['UPLOADS'], current_image)
            if os.path.exists(path):
                shrink_image(path)
                image_name = current_image

        # Scenario 3: User clicks 'grow' on an existing image
        if filter_name == 'grow' and current_image:
            path = os.path.join(app.config['UPLOADS'], current_image)
            if os.path.exists(path):
                grow_image(path)
                image_name = current_image
        
        # Keep the current image visible if no new action is taken
        elif current_image:
            image_name = current_image

    # Send the image name to the HTML template to display it
    return render_template('index.html', image_name=image_name)

# Start the local web server
if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from PIL import Image
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)

UPLOADS = 'static/uploads'
if not os.path.exists(UPLOADS):
    os.makedirs(UPLOADS)

app.config['UPLOADS'] = UPLOADS


def mirror_image(image_path):
    img = Image.open(image_path)
    mirrored = img.transpose(Image.FLIP_LEFT_RIGHT)
    mirrored.save(image_path)


@app.route('/', methods=['GET', 'POST'])
def im():
    image_name = None

    if request.method == 'POST':
        file = request.files.get('image_file')
        filter_name = request.form.get('filter')
        current_image = request.form.get('current_image')

        if file and file.filename != '':
            path = os.path.join(app.config['UPLOADS'], file.filename)
            file.save(path)
            image_name = file.filename

        elif filter_name == 'mirror' and current_image:
            path = os.path.join(app.config['UPLOADS'], current_image)
            if os.path.exists(path):
                mirror_image(path)
                image_name = current_image

        elif current_image:
            image_name = current_image

    return render_template('index.html', image_name=image_name)


if __name__ == '__main__':
    app.run(debug=True)
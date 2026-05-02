# Abraham Sanchez-Pereyra
# 4/28/26
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# You guys need an upload folder within your project in file explorer
UPLOADS = 'static/uploads'
if not os.path.exists(UPLOADS):
    os.makedirs(UPLOADS)

app.config['UPLOADS'] = UPLOADS

@app.route('/', methods=['GET', 'POST'])
def im():
    image_name = None 
    
    if request.method == 'POST':
        file = request.files.get('image_file')
        
        if file and file.filename != '':
            path = os.path.join(app.config['UPLOADS'], file.filename)
            file.save(path)
            image_name = file.filename
    
    return render_template('index.html', image_name=image_name)
if __name__ == "__main__":
    app.run(debug=True)

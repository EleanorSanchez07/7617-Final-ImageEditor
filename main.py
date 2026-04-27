# Abraham Sanchez-Pereyra
# 4/22/26
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)

# Ensure an upload folder exists
UPLOADS = 'static/uploads'
if not os.path.exists(UPLOADS):
    os.makedirs(UPLOADS)

app.config['UPLOADS'] = UPLOADS

@app.route('/', methods=['GET', 'POST'])
def im():
    # If the user uploads a file
    if request.method == 'POST':
        # Logic for saving file will go here later
        pass
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

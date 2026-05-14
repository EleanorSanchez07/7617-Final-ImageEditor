CSUMB Image Filter Editor
TEAM MEMBERS:
Humberto Ramirez, Eleanor Sanchez, 
Abraham Sanchez-Pereyra, Jesus Ortiz and Enrique Vega

CLASS: CST 205: Multimedia Design & Programming
DATE: May 13, 2026

PROJECT DESCRIPTION:
A web-based application built using Flask and the Pillow (PIL) library. 
It allows users to upload images and apply a variety of custom-coded filters and transformations.

A standout feature of this project is the Advanced Chroma Key filter, which utilizes the colormath library for 
CIEDE2000 Delta E color difference calculations and Python Multiprocessing to handle high-intensity mathematical 
operations efficiently.

RUN OPERATION:
1) Have Python installed and its libraries (flask, flask-bootstrap, Pillow, colormath, numpy)
2) Correct Structure:

project-folder/

│

├── static/

│   └── uploads/       # Processed images will be stored here (also monte logo)

├── templates/

│   └── index.html     # The html file

└── Image_editor.py  # The main Python file

3) In your terminal enter:
flask --app Image_editor.py --debug run 

Once the server starts, open your browser and navigate to (http://127.0.0.1:5000)

OPERATION WITHIN WEBSITE:
1) Click the Choose File bar to choose within your File Explorer
2) Click Upload to start editing
3) Click on each filter to apply
4) For Stack:
  Alike to the first step, click Choose File to pick among File Explorer.
  Once chosen click Stack
  DONE!
  (Same thing for Random Stack)

6) Once done, click Save to save it into the Upload folder in your File Explorer
7) Or click reset to start from scratch.

GITHUB REPOSITORY LINK
https://github.com/EleanorSanchez07/7617-Final-ImageEditor

FUTURE WORK
1) Add sliders to manage the amount of the filter user wants added.
2) Receive the Image information (width x height) added to a combo box to be managed by user as in grow or shrink.
3) Also receive location information (x,y) of stacked images to also be moved among the first image to inspire collages.
4) Use corner information for better user cropping.

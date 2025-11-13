from flask import Flask, render_template, request, flash, redirect
from PIL import Image, ImageDraw, ImageFont
import io
import os
import base64
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/") 
def index():
    return render_template("index.html")

@app.route("/certificate", methods=["POST"])
def certificate():

    # Gets the name that the user sent
    name = request.form.get("name")

    # Ensure that name is present
    if not name:
        flash("Please enter a name.")
        return redirect("/")
    
    # Ensure that name is not too long
    elif len(name) > 25:
        flash("Name is too long.")
        return redirect("/")

    # Opens certificate template using Pillow   
    img = Image.open('static/template/NNN 2025 Certificate.png')
    draw = ImageDraw.Draw(img)

    # Equation to convert point to pixels
    # pixel = point * 1.3333...
    point = 72
    pixel = round(point * 1.3333)

    # Assigns the font for the text
    font = ImageFont.truetype("static/font/Garamond Bold.ttf", pixel)

    # Gets the image dimensions
    W, H = img.size

    # Gets the text width and height dynamically
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]

    # Position of the text on the certificate
    y = 864
    x = (W - text_width) /2 

    # Creates the filled certificate
    draw.text((x, y), name, font=font, fill="black")

    # Creates a buffer in memory
    buffer = io.BytesIO()
    # Saves file in buffer
    img.save(buffer, format="PNG")
    # Moves the read/write cursor back to the beginning
    buffer.seek(0)
    # Turns the image into text to send to HTML
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return render_template("certificate.html", image=encoded_image)
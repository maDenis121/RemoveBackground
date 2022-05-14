from email import utils
import imp
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

#Importar parquetes necesarios

import cv2 
import numpy as np


#from matplotlib import pyplot as plt

from PIL import Image
#import mediapipe as mp
import shutil

#Parámetros globales
H = 512
w = 512


@app.route("/")


def quita_fondo():
    pass

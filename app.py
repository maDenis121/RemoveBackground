#Importar parquetes necesarios
from flask import Flask, render_template
app = Flask(__name__)

import cv2 
import numpy as np

@app.route("/")
def index():
    return render_template("main.html")





def quita_fondo():
    #leemos la imagen
    img = cv2.imread("prueba.png")
    
    #Mostramos la imagen
    cv2.imshow("imagen original", img)

    #Convertimos a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Mostramos la imagen gris
    cv2.imshow("imagen gris", gray)

    #Generamos la imagen binaria
    _,tresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    #Mostramos el resultado
    cv2.imshow("imagen binaria", tresh)

    #Detección de contornos
    img_contours = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2]
    img_contours = sorted(img_contours, key=cv2.contourArea)

    for i in img_contours:
            if cv2.contourArea(i) > 100:
                break

    #Generar máscara:
    mask = np.zeros(img.shape[:2], np.uint8)

    #Dibujar contornos
    cv2.drawContours(mask, [i], -1, 255, -1)

    #Substracción del fondo
    new_img = cv2.bitwise_and(img, img, mask=mask)


    #mostramos el resultado
    cv2.imshow("res", new_img)



import pixellib
from pixellib.tune_bg import alter_bg 


def eliminar_fondo():
    cambiar_fondo = alter_bg()
    cambiar_fondo.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
    cambiar_fondo.color_bg("imgs/01.jpg", colors = (0, 255, 0), output_image_name = "output/01_fondo_verde.jpg", detect = "person")


eliminar_fondo()

cv2.waitKey(0)
cv2.destroyAllWindows()
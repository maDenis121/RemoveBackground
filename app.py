#Importar parquetes necesarios
from flask import Flask, render_template, request
import cv2 
import numpy as np
import time
from matplotlib import pyplot as plt

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    imagenOriginal = request.files['imagenOriginal']
    imagenFondo = request.files['imagenFondo']
    chkUsarNuevoFondo = request.form['chkUsarNuevoFondo']
    selectTipoFondo = request.form['selectTipoFondo']
    # quitar fondo, meter nuevo fondo
    pass
    #return render_template("resultado.html", rutaImagen=rutaNuevaImagen)


#Constantes:
BLUR = 21 
CANNY_THRESH_1 = 10 
CANNY_THRESH_2 = 200 
MASK_DILATE_ITER = 10 
MASK_ERODE_ITER = 10 
MASK_COLOR = (1.0,1.0,1.0) # In BGR format 


def quita_fondo():
    #leemos la imagen
    img = cv2.imread("./imgs/01.jpg")
    
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



#import pixellib
#from pixellib.tune_bg import alter_bg 


#def eliminar_fondo():
    #cambiar_fondo = alter_bg()
    #cambiar_fondo.load_pascalvoc_model("deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")
    #cambiar_fondo.color_bg("imgs/01.jpg", colors = (0, 255, 0), output_image_name = "output/01_fondo_verde.jpg", detect = "person")


def prueba3():

    #Leemos la imagen y la pasamos a gris
    img = cv2.imread("persona.jpg")
    cv2.imshow("original", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Detección de bordes
    bordes = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    cv2.imshow("bordes1", bordes)

    bordes = cv2.dilate(bordes, None)
    cv2.imshow("bordes2", bordes)

    bordes = cv2.erode(bordes, None)
    cv2.imshow("bordes3", bordes)

    #Encontrar contornos en los bordes, ordenados por el área
    contour_info = [] 
    contours, _ = cv2.findContours(bordes, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) 

    for c in contours: 
            contour_info.append((
            c, 
            cv2.isContourConvex(c), 
            cv2.contourArea(c), 
            )) 
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True) 
    max_contour = contour_info[0]

    #Crea una máscara vacía, dibujando polígonos rellenos en el lugar correspondite al contrno más grnade.
    #Máscara negra, polígono blanco
    mask = np.zeros(bordes.shape) 
    cv2.fillConvexPoly(mask, max_contour[0], (255))
    cv2.imshow("mascara", mask)

    #Suavizado de la máscara, blur
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER) 
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER) 
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0) 
    mask_stack = np.dstack([mask]*3) # Crea un mapa de alfa de 3 canales
    

    #Hacemos un blend con la imagen para obtener una máscara de color del fondo
    mask_stack = mask_stack.astype('float32')/255.0   # matrices de float 
    img  = img.astype('float32')/255.0     # Más facil para hacer el blend 

    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR) # Blend 
    masked = (masked * 255).astype('uint8')      # Convert back to 8-bit
    cv2.imwrite("prueba.png",masked)

    fondo = cv2.imread("fondo.jpg")
    final = cv2.imread("prueba.png")
    wf, hf, channelsf = fondo.shape
    wi, hi, channelsi = final.shape
    #print(w,h,channels)
    aspRatf = wf/hf
    aspRati = wi/hi
    #print(aspRatf, aspRati)
    #res = cv2.add(masked, final)
    #res = cv2.addWeighted(final, 0.5, fondo, 0.5, 0.0)
    factor =0
    if aspRati > aspRatf:
        factor = wi/wf

    else:
        factor =hi/hf
    print(factor)
    imEsc = cv2.resize(fondo, None, factor, factor)
    cv2.imshow("final", res)

    
#quita_fondo()
#prueba3()

#cv2.waitKey(0)
#cv2.destroyAllWindows()

#Importar parquetes necesarios
from flask import Flask, render_template, request
import cv2 
import numpy as np






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
MASK_COLOR = (.0,.0,.0) # In BGR format 





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
    cv2.imwrite("mascara.png", mask)

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
    #fondo = Image.open("fondo.jpg")
    final = cv2.imread("prueba.png")


 
    wi, hi, channelsi = final.shape
    print(wi,hi)
    fondo_res = cv2.resize(fondo, dsize=(hi, wi), interpolation=cv2.INTER_CUBIC)

    #posible opción
    #fondo_res = cv2.subtract(fondo_res, final)
    #cv2.imshow("fondo",fondo_res) # Con la gilipollez queda guapo
    mascara = cv2.imread("mascara.png")
    fondo_res = cv2.subtract(fondo_res, mascara)
    cv2.imshow("fondo",fondo_res)

    res = cv2.addWeighted(final, 1, fondo_res, 1, 0.0)

    cv2.imshow("final final", res)

#
    
#quita_fondo()
prueba3()

cv2.waitKey(0)
cv2.destroyAllWindows()

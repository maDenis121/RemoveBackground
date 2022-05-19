#Importar parquetes necesarios
import cv2 
import numpy as np
from datetime import datetime
from upload import upload_file

#Constantes:
BLUR = 21 
CANNY_THRESH_1 = 10 
CANNY_THRESH_2 = 200 
MASK_DILATE_ITER = 10 
MASK_ERODE_ITER = 10 
MASK_COLOR = (.0,.0,.0) # In BGR format 

def quitar_fondo(imagenOriginal, imagenFondo):

    #Leemos la imagen y la pasamos a gris
    img = cv2.imread(imagenOriginal)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Detección de bordes
    bordes = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    
    bordes = cv2.dilate(bordes, None)

    bordes = cv2.erode(bordes, None)
    

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
    masked = (masked * 255).astype('uint8')      # Converitr el negro en colores de 8 bits
    cv2.imwrite(imagenOriginal,masked)

    #Leemos la imágen anterior y la imagen de fondo 
    fondo = cv2.imread(imagenFondo)
    final = cv2.imread(imagenOriginal)


    #Obtenemos las propiedades de la imagen final y reescalamos el fondo:
    wi, hi, channelsi = final.shape
    fondo_res = cv2.resize(fondo, dsize=(hi, wi), interpolation=cv2.INTER_CUBIC)

    #posible opción
    #fondo_res = cv2.subtract(fondo_res, final)
    #cv2.imshow("fondo",fondo_res) # Con la gilipollez queda guapo

    #Restamos al fondo la máscara 
    mascara = cv2.imread("mascara.png")
    fondo_res = cv2.subtract(fondo_res, mascara)

    #Combinamos la imagen tratada al principio con el fondo que acabamos de obtener 
    res = cv2.addWeighted(final, 1, fondo_res, 1, 0.0)

    #cv2.imshow("final final", res)

    fileName = datetime.now().strftime("%Y%m%d%m_%H%M%S") + ".png"
    fullPath = fileName
    cv2.imwrite(fullPath, res)
    #with open(fullPath, "rb") as data:
        #upload_file(fileName, data);

    return fileName;

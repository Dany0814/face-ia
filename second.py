import boto3
import cv2
import os
import numpy as np
import face_recognition
# from datetime import datetime
# from urllib import request
# from pathlib import Path
    
# Credenciales de Amazon
# Requisitos: Tener un bucket disponible, en este caso el bucket es "unida"    

def codefotos():
    ACCESS_KEY = "AKIA25L3WLNNENDOSZFM"
    SECRET_KEY = "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"
    # Cliente s3 y listado de objetos del bucket
    clientes3 = boto3.client(
        "s3",
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    response = clientes3.list_objects_v2(Bucket="unida")
    lista = response["Contents"]
    # Obtener solo el "key" de los objects del bucket seleccionado y descargarlo en una ruta local ./img
    for fichero in lista:
        classNames2 = fichero["Key"]
        clientes3.download_file('unida', f'{classNames2}', f'./img/{classNames2}') 
    # Listar los objetos descargados y obtener un array de cada objeto además de su nombre
    pathern = './img'
    images = []
    classNames = []
    myList = os.listdir(pathern)
    for cl in myList:
        curImg = cv2.imread(f'{pathern}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    print(images)
    return images

# Codificando imágenes
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        print(encodeList)
        print('Encoding Complete')
    return encodeList    
    
    print('Encoding Complete')

# Guardado de caras reconocidas por la cámara con hora
# def markAttendance(name):
#     with open('./Attendance.csv', 'r+') as f:
#         myDataList = f.readlines()
#         nameList = []
#         for line in myDataList:
#             entry = line.split(',')
#             nameList.append(entry[0])
#         if name not in nameList:
#             now = datetime.now()
#             dtString = now.strftime('%H:%M:%S')
#             f.writelines(f'\n{name}, {dtString}')
# encodeListKnown = findEncodings(images)


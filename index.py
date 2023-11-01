# save this as app.py
from flask import Flask
from flask import Flask, render_template, request, send_file
from FirmarArchivos import firmar
import io

app = Flask(__name__)

#  ESTO ES FLASK

@app.route('/FirmarDocumentos',  methods=['POST'])
def FirmarDocumentos():
    pdf = request.files.get("pdf")
    firma = request.files.get("firma")
    contra = request.form.get("palabra_secreta")  
    # CREO UNA VARIABLE Q ME PERMITE CONVERITIR LOS DATOS A PDF
    newPDF = io.BytesIO() 
    respStatus, respMsg = firmar(pdf,firma,contra,newPDF)    

    if(respStatus):
        return respMsg
    else:
        return respMsg
   
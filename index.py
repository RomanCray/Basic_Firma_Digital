# save this as app.py
from flask import Flask, request, jsonify
from FirmarArchivos import firmar
from BuscarFirma import ubiFirma
import io
import os
import json
import logging

app = Flask(__name__)

@app.route('/FirmarDocumentos',  methods=['POST'])
def FirmarDocumentos():
    # code_sigcenter = request.headers.get('code_sigcenter')
    # if code_sigcenter != 'tu_valor_esperado':
    #     return Response('Acceso no autorizado', status=401, content_type='text/plain')        
    try:
        pdf = request.files.get("pdf")
        datos = json.loads(request.form['datos'])      
        dni = request.form.get("dni")
        company = request.form.get("company_id") 

        # logging.info(dni)    
        if not company or company.strip() == "":
            return jsonify({"error": "El campo 'company_id' no puede estar en blanco"}), 400
        if not dni or dni.strip() == "":
            return jsonify({"error": "El campo 'dni' no puede estar en blanco"}), 400
        if not pdf:
            return jsonify({"error": "El campo 'pdf' es requerido"}), 400
        
        # CREO UNA VARIABLE Q ME PERMITE CONVERITIR LOS DATOS A PDF
        newPDF = io.BytesIO()         

        logging.warning ("--------------------- FUNCION FIRMA  --------------------- ")

        i = 0
        rutaPdfNew = None
        for dato in datos:
            firma = dato['firmaNom']
            contra = dato["password"]
            pagina = dato["paginas_a_firmar"]
            pre_x0 = dato["x0"]
            pre_y0 = dato["y0"]
            pre_x1 = dato["x1"]
            orientacion = dato["orientacion"]
            urlHook = dato["urlHook"]

            if i == 0:
                respStatus, respMsg = firmar('U',pdf, firma, contra, pagina, pre_x0, pre_y0, pre_x1, newPDF, company, dni, orientacion, urlHook)        

            else:                
                respStatus, respMsg = firmar('V',rutaPdfNew, firma, contra, pagina, pre_x0, pre_y0, pre_x1, newPDF, company, dni, orientacion, urlHook, i)

                os.remove('PDF_FIRMADOS/'+ rutaPdfNew)

            if(respStatus):
               rutaPdfNew = respMsg
            else:
                break

            i = i+1
            

        if(respStatus):
            # logging.info(respMsg)
            data = {'rutaPdf': respMsg}
            return jsonify(data), 200        
                
        data = {'rutaPdf': respMsg}    
        return jsonify(data), 500

    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500   
            

@app.route('/PdfVerificacion',  methods=['POST'])
def PdfVerificacion():
    newPDF = io.BytesIO() 
    pdf = request.files.get("pdf")
    dni = request.form.get("confirm")  

    if not pdf:
        return jsonify({"error": "El campo 'pdf' es requerido"}), 400
    if not dni or dni.strip() == "":
        return jsonify({"error": "El campo 'cedula' no puede estar en blanco"}), 400
    
    logging.warning ("--------------------- FUNCION VERIFICAR  --------------------- ")

    resp = ubiFirma(newPDF,pdf,dni)

    if(resp == False):
        data = {'rutaPdf': "ALGO SALIO MAL"}    
        return jsonify(data), 500
    
    # logging.info(resp)
    data = {'params': resp}
    return jsonify(data), 200            


@app.route('/')
def index():
    return ('<h3>Hola,Pagina erronea</h3>')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
   
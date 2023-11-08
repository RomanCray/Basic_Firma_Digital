# save this as app.py
from flask import Flask, render_template, request, jsonify
from FirmarArchivos import firmar
import io

app = Flask(__name__)

#  ESTO ES FLASK

@app.route('/FirmarDocumentos',  methods=['POST'])
def FirmarDocumentos():
    # code_sigcenter = request.headers.get('code_sigcenter')
    # if code_sigcenter != 'tu_valor_esperado':
    #     return Response('Acceso no autorizado', status=401, content_type='text/plain')

    pdf = request.files.get("pdf")
    firma = request.files.get("firma")
    contra = request.form.get("palabra_secreta")  
    dni = request.form.get("dni")  
    company = request.form.get("company_id") 
    paginas_a_firmar = request.form.get("paginas_a_firmar") 
    palabraClave = request.form.get("palabraClave")  

     # Validar que los archivos no estén en blanco
    if not pdf:
        return jsonify({"error": "El campo 'pdf' es requerido"}), 400
    if not firma:
        return jsonify({"error": "El campo 'firma' es requerido"}), 400
    if not contra or contra.strip() == "":
        return jsonify({"error": "El campo 'palabra_secreta' no puede estar en blanco"}), 400
    if not company or company.strip() == "":
        return jsonify({"error": "El campo 'company_id' no puede estar en blanco"}), 400
    if not dni or dni.strip() == "":
        return jsonify({"error": "El campo 'dni' no puede estar en blanco"}), 400
    
    # CREO UNA VARIABLE Q ME PERMITE CONVERITIR LOS DATOS A PDF
    newPDF = io.BytesIO() 
    respStatus, respMsg = firmar(pdf,firma,contra,newPDF,company,dni,paginas_a_firmar,palabraClave) 

    # respStatus = True
    # respMsg = "bien"

    if(respStatus):
        print(respMsg)
        data = {'rutaPdf': respMsg}
        return jsonify(data), 200        
        
    data = {'rutaPdf': respMsg}
    return jsonify(data), 500
   
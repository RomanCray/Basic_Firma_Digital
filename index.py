# save this as app.py
from flask import Flask, request, jsonify
from FirmarArchivos import firmar
from BuscarFirma import ubiFirma
import io

app = Flask(__name__)

#  ESTO ES FLASK

@app.route('/FirmarDocumentos',  methods=['POST'])
def FirmarDocumentos():
    # code_sigcenter = request.headers.get('code_sigcenter')
    # if code_sigcenter != 'tu_valor_esperado':
    #     return Response('Acceso no autorizado', status=401, content_type='text/plain')        
    try:
        pdf = request.files.get("pdf")
        datos = request.form.getlist("datos")        
        dni = request.form.get("dni")
        company = request.form.get("company_id") 

        print(dni)    
        if not company or company.strip() == "":
            return jsonify({"error": "El campo 'company_id' no puede estar en blanco"}), 400
        if not dni or dni.strip() == "":
            return jsonify({"error": "El campo 'dni' no puede estar en blanco"}), 400
        if not pdf:
            return jsonify({"error": "El campo 'pdf' es requerido"}), 400
        
        if datos:
            # Procesar los datos según sea necesario
            print("Datos del formulario:")
        else:
            return jsonify({"error": "El JSON no contiene 'datos' y 'pdf'"}), 400
        
        # CREO UNA VARIABLE Q ME PERMITE CONVERITIR LOS DATOS A PDF
        newPDF = io.BytesIO() 
        print("avanzar")      
        respStatus, respMsg = firmar(pdf,datos,newPDF,company,dni)

        if(respStatus):
            print(respMsg)
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
    
    resp = ubiFirma(newPDF,pdf,dni)

    if(resp == False):
        data = {'rutaPdf': "ALGO SALIO MAL"}    
        return jsonify(data), 500
    
    print(resp)
    data = {'params': resp}
    return jsonify(data), 200            


@app.route('/')
def index():
    return ('<h3>Hola,Pagina erronea</h3>')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
   
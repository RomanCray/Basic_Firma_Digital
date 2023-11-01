from endesive.pdf import cms
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12


def firmar(pdf,firma,contra,newPDF):    

    archivo_pdf_para_enviar_al_cliente = newPDF

    try:

        # Abre el archivo P12 como un objeto de archivo binario Y LEE LA INFORMACION Q HAY DENTRO   
        
        print("LEE EL p12")
        # with open(firma, 'rb') as p12_file:    
        p12 = pkcs12.load_key_and_certificates(
            firma.read(), contra.encode("ascii"), backends.default_backend()
        )        

        # Abre el archivo PDF como un objeto de archivo binario
        
        print("LEE EL PDF")
        # with open(pdf, 'rb') as pdf_file:
        datau = pdf.read()

        # ESTABLESO LOS PARAMETROS QUE VA TENER LA FIRMA
        date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
        date = date.strftime("D:%Y%m%d%H%M%S+00'00'")      

        dct = {
                    "aligned": 0,
                    "sigflags": 3,
                    "sigflagsft": 132,
                    "sigpage": 0,
                    "sigbutton": True,
                    "sigfield": "Signature1",
                    "auto_sigfield": True,
                    "sigandcertify": True,
                    "signaturebox": (470, 840, 570, 640),
                    "signature_img": "img/LogoIntelho.png",
                    # "signature": "Nombre Firmante",        
                    "contact": "hola@ejemplo.com",
                    "location": "QUITO",
                    "signingdate": date,
                    "reason": "PRUEBAS INTHELO",
                    "password": contra,
                }

        # CON ESTO USO EL ARCHIVO Q SE ESTA LEYENDO Y AGREGO LA FIRMA
        print("FIRMA EL PDF CON EL p12")
        datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")

        # BUELVO A UNIR TODAS LAR PARTES EL PDF Y LA FIRMA CON TODOS LOS CRETIFICADOS
        archivo_pdf_para_enviar_al_cliente.write(datau) 
        archivo_pdf_para_enviar_al_cliente.write(datas)
        archivo_pdf_para_enviar_al_cliente.seek(0)

        print("CREA EL NUEVO ARCHIVO")

        # MANDO A GUARDA EN ESA RUTA EL NUEVO ARCHIVO
        output_pdf_path = 'PDF_FIRMADOS/SOY_UN_PDF_firmado.pdf'

        with open(output_pdf_path, 'wb') as output_pdf_file:
            output_pdf_file.write(archivo_pdf_para_enviar_al_cliente.getvalue())   
        
        respMsg = "PDF Firmado"
        respStatus = True
        print(respMsg)
        return respStatus, respMsg
    
    except ValueError as e:
        print(f"Capturada excepción de tipo ")
        respMsg = f"{type(e)} | ERROR: " + str(e)
        respStatus = False
        print(respMsg)
        return respStatus, respMsg
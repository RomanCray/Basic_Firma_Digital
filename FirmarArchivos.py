import os
import datetime
from endesive.pdf import cms
from cryptography import x509
from BuscarFirma import ubiFirma
from CreateImage import generadorQR
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

def firmar(pdf,firma,contra,newPDF,company,dni,paginas_a_firmar,palabraClave):    

    archivo_pdf_para_enviar_al_cliente = newPDF
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")      

    try:
        # Abre el archivo P12 como un objeto de archivo binario Y LEE LA INFORMACION Q HAY DENTRO   
        print("LEE EL p12")
        # with open(firma, 'rb') as p12_file:    
        p12 = pkcs12.load_key_and_certificates(
            firma.read(), contra.encode("ascii"), backends.default_backend()
        )      

        # Obtener el campo CN (Nombre titular)
        cert = p12[1]
        P12_Nobre_remitente = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value

        # Abre el archivo PDF como un objeto de archivo binario
        print("LEE EL PDF")
        # with open(pdf, 'rb') as pdf_file:
        datau = pdf.read()              

        # ESTABLESO LOS PARAMETROS QUE VA TENER LA FIRMA

        paginas = paginas_a_firmar.split(',')
        for pagina in paginas:

            numero_pagina = int(pagina)

            date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
            date1 = date.strftime("D:%Y%m%d%H%M%S+00'00'")        
            nombreImgTemp = generadorQR(P12_Nobre_remitente,date1)        
            nombre_archivo = nombre_archivo = os.path.basename(pdf.filename)            

            positionx0,positiony0,positionx1,positiony1 = ubiFirma(newPDF,datau,date.strftime('%Y-%m-%d_%H-%M-%S_%f'),company,dni,nombre_archivo,palabraClave)
            print("POSICIONES")
            print(positionx0,positiony0,positionx1,positiony1)

            # dct = {
                #     "aligned": 0,
                #     "sigflags": 3,
                #     "sigflagsft": 132,
                #     "sigpage": numero_pagina,
                #     "sigbutton": True,
                #     "sigfield": "Signature1",
                #     "auto_sigfield": True,
                #     "sigandcertify": True,
                #     "signaturebox": ((float(positionx0)),10,(float(positionx1)),10),
                #     "signature_img": f"img/{nombreImgTemp}",
                #     # "signature": "Nombre Firmante",        
                #     "contact": "hola@ejemplo.com",
                #     "location": "QUITO",
                #     "signingdate": date1,
                #     "reason": "PRUEBAS INTHELO",
                #     "password": contra,
                # }

            dct = {
                    "aligned": 0,
                    "sigflags": 3,
                    "sigflagsft": 2,
                    "sigpage": numero_pagina,
                    "sigbutton": True,
                    "sigfield": "Signature1",
                    "auto_sigfield": True,
                    "sigandcertify": True,
                    "signaturebox": ((float(positionx0)),10,(float(positionx1)),10),
                    "signature_img": f"img/{nombreImgTemp}",
                    # "signature": "Nombre Firmante",        
                    "contact": "hola@ejemplo.com",
                    "location": "QUITO",
                    "signingdate": date1,
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

        date_str = date.strftime('%Y-%m-%d_%H-%M-%S_%f') 

        # MANDO A GUARDA EN ESA RUTA EL NUEVO ARCHIVO  
        if not os.path.exists(f'PDF_FIRMADOS/{company}'):
            os.makedirs(f'PDF_FIRMADOS/{company}')
        if not os.path.exists(f'PDF_FIRMADOS/{company}/{dni}'):
            os.makedirs(f'PDF_FIRMADOS/{company}/{dni}') 

        output_pdf_path = f'PDF_FIRMADOS/{company}/{dni}/FIRMADO_{date_str}_{nombre_archivo}'
        rutaRetorno = f'{company}/{dni}/FIRMADO_{date_str}_{nombre_archivo}'
        print(output_pdf_path)

        with open(output_pdf_path, 'wb') as output_pdf_file:
            output_pdf_file.write(archivo_pdf_para_enviar_al_cliente.getvalue())   
        
        respMsg = rutaRetorno
        respStatus = True        
        return respStatus, respMsg
    
    except ValueError as e:
        print(f"Capturada excepción de tipo ")
        respMsg = f"{type(e)} | ERROR: " + str(e)
        respStatus = False        
        return respStatus, respMsg
import os
import requests
import datetime
from endesive.pdf import cms
from cryptography import x509
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

import logging

def firmar(validador, pdf, firma, contra, pagina, pre_x0, pre_y0, pre_x1, newPDF, company, dni, orientacion, urlHook, i=0):

    logging.warning ("--------------------- FIRMA DIGITAL --------------------- ")
 
    archivo_pdf_para_enviar_al_cliente = newPDF
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)           

    try:

        if validador == 'U':
            datau = pdf.read()
            # nombre_archivo = os.path.basename(pdf.filename)
            nombreArchTemp = os.path.splitext(os.path.basename(pdf.filename))[0]

            logging.error(f"primer nombre: {nombreArchTemp}")
            partes = nombreArchTemp.split("@")
            nombreArchTemp = partes[-1]
            logging.error(f"FIST NOMBRE: {nombreArchTemp}")

        else:
            with open('PDF_FIRMADOS/'+ pdf, 'rb') as pdf_file:    
                datau = pdf_file.read()

            # nombre_archivo = os.path.basename(pdf_file.name)
            nombreArchTemp = os.path.splitext(os.path.basename(pdf_file.name))[0]
            partes = nombreArchTemp.split("@")
            nombreArchTemp = partes[-1]
            logging.error(f"OTRO NOMBRE: {nombreArchTemp}")


        logging.info("LEE EL PDF")
                         
        nombrePartes = firma.split()
        logging.info(nombrePartes[0])
        logging.info(nombrePartes[1])
        logging.info(nombrePartes[2])
        logging.info(nombrePartes[3])            

        url = 'http://localhost/SIGCENTER/restful/hook-firma-electronica/enviar-firma'
        dats = {
                'nom1': nombrePartes[0],
                'nom2': nombrePartes[1],
                'apell1':nombrePartes[2],
                'apell2':nombrePartes[3]
            }

         
        response = requests.post(url, data = dats)
            
        if response.status_code == 200:    

            date_str = date.strftime('%Y-%m-%d_%H-%M-%S_%f')                

            # MANDO A GUARDA EN ESA RUTA EL NUEVO ARCHIVO  
            if not os.path.exists(f'P12_TEMPORAL/{dni}'):
                os.makedirs(f'P12_TEMPORAL/{dni}')    

            print(nombreArchTemp)
            print(date_str)

            output_p12_path = f'P12_TEMPORAL/{dni}/TEMPORAL_{date_str}_{nombreArchTemp}.p12'
            logging.info(output_p12_path)                

            with open(output_p12_path, 'wb') as f:
                f.write(response.content)
                
            logging.info('Archivo descargado exitosamente.')

        else:
            logging.info(f'Error en la solicitud. Código de respuesta: {response.status_code}')
            respMsg = f"ERROR: En el hook "
            respStatus = False        
            return respStatus, respMsg

            
        # Abre el archivo P12 como un objeto de archivo binario Y LEE LA INFORMACION Q HAY DENTRO   
        logging.info("LEE EL p12")
        with open(output_p12_path, 'rb') as p12_file:
            p12 = pkcs12.load_key_and_certificates(
                p12_file.read(), contra.encode("ascii"), backends.default_backend()
            )      

        cert = p12[1]
        # Obtener el campo CN (Nombre titular)
        P12_Nobre_remitente = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
        logging.info(P12_Nobre_remitente)

        # ESTABLESO LOS PARAMETROS QUE VA TENER LA FIRMA
        date1 = date.strftime("D:%Y%m%d%H%M%S+00'00'")        
        # nombreImgTemp = generadorQR(P12_Nobre_remitente,date1)

        if not orientacion :
            x0 = pre_x0 - 40
            y0 = pre_y0 -400
            x1= pre_x1 + 40
            y1= y0 + 80   
        else:
            x0 = pre_x0 - 40
            y0 = pre_y0 -220
            x1= pre_x1 + 40
            y1= y0 + 80     
        
        x0 = x0 if x0 > 0 else 100
        y0 = y0 if y0 > 0 else 100
        x1 = x1 if x1 > 0 else 100
        y1 = y1 if y1 > 0 else 100
 

        #  794 x 1123 píxeles
        #  794 x 1123 píxeles
        dct ={
                "aligned": 0,
                "sigflags": 3,
                "sigflagsft": 132,
                "sigpage": int(pagina),
                "sigbutton": True,
                "sigfield": f"Signature{i}",
                "auto_sigfield": True,
                "sigandcertify": True,                    
                "signaturebox": (x0,y0,x1,y1),
                # "signature_img": f"img/{nombreImgTemp}",
                "signature": "",        
                "contact": "hola@ejemplo.com",
                "location": "QUITO",
                "signingdate": date1,
                "reason": "PRUEBAS INTHELO",
                "password": contra
            }            
        logging.info(dct)

        # CON ESTO USO EL ARCHIVO Q SE ESTA LEYENDO Y AGREGO LA FIRMA
        logging.info("FIRMA EL PDF CON EL p12")
        try:
            datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")                
        except Exception as e:
            print("Error al colocar la firma:", str(e))
                    

        # BUELVO A UNIR TODAS LAR PARTES EL PDF Y LA FIRMA CON TODOS LOS CRETIFICADOS
        archivo_pdf_para_enviar_al_cliente.write(datau) 
        archivo_pdf_para_enviar_al_cliente.write(datas)
        archivo_pdf_para_enviar_al_cliente.seek(0)
     
        os.remove(output_p12_path)            

        logging.info("CREA EL NUEVO ARCHIVO")

        date_str = date.strftime('%Y-%m-%d_%H-%M-%S_%f') 

        # MANDO A GUARDA EN ESA RUTA EL NUEVO ARCHIVO  
        if not os.path.exists(f'PDF_FIRMADOS/{company}'):
            os.makedirs(f'PDF_FIRMADOS/{company}')
        if not os.path.exists(f'PDF_FIRMADOS/{company}/{dni}'):
            os.makedirs(f'PDF_FIRMADOS/{company}/{dni}') 

        output_pdf_path = f'PDF_FIRMADOS/{company}/{dni}/FIRMADO({validador})_{date_str}@{nombreArchTemp}'
        rutaRetorno = f'{company}/{dni}/FIRMADO({validador})_{date_str}@{nombreArchTemp}'
        logging.info(output_pdf_path)

        with open(output_pdf_path, 'wb') as output_pdf_file:
            output_pdf_file.write(archivo_pdf_para_enviar_al_cliente.getvalue())   
            
        logging.warning ("--------------------- FIN FIRMA DIGITAL --------------------- ")
        respMsg = rutaRetorno
        respStatus = True        
        return respStatus, respMsg 
    

    except FileNotFoundError as fn:
        respMsg = f"El archivo {output_p12_path} no se encontró. {type(fn)} | ERROR: " + str(fn)
        logging.error(f"{respMsg}")
        respStatus = False        
        return respStatus, respMsg        

    except IOError as io :
        respMsg = f"Error de E/S al leer el archivo: {type(io)} | ERROR: " + str(io)
        logging.error(f"{respMsg}")
        respStatus = False        
        return respStatus, respMsg        

    except ValueError as ve:
        respMsg = f"La contraseña del archivo P12 no es correcta. {type(ve)} | ERROR: " + str(ve)
        logging.error(f"{respMsg}")
        respStatus = False        
        return respStatus, respMsg

    except Exception as e:
        respMsg = f"{type(e)} | ERROR: " + str(e)
        logging.error(f"{respMsg}")
        respStatus = False        
        return respStatus, respMsg
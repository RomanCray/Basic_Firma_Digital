import os
import math
import requests
import datetime
from endesive.pdf import cms
from cryptography import x509
from BuscarFirma import ubiFirma
from createImage import generadorQR
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

import json

def firmar(pdf,datos,newPDF,company,dni):    

    print("FUNCION (firmar)")
    datas=[]
    dct=[]
    archivo_pdf_para_enviar_al_cliente = newPDF
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)           

    try:
        print("LEE EL PDF")
        datau = pdf.read() 
 
        print(datos)
        i=0
        for dato in datos:
            firma = dato['firmaNom']
            contra = dato["password"]
            pagina = dato["paginas_a_firmar"]
            pre_x0 = dato["x0"]
            pre_y0 = dato["y0"]
            pre_x1 = dato["x1"]

            nombre_completo = firma
            nombrePartes = nombre_completo.split()
            print(nombrePartes[0])
            print(nombrePartes[1])
            print(nombrePartes[2])
            print(nombrePartes[3])            

            url = 'http://localhost/SIER/rel/ho/firma'
            dats = {
                    'nom1': nombrePartes[0],
                    'nom2': nombrePartes[1],
                    'apell1':nombrePartes[2],
                    'apell2':nombrePartes[3]
                }
            
            response = requests.post(url, data=dats)
            
            if response.status_code == 200:    

                date_str = date.strftime('%Y-%m-%d_%H-%M-%S_%f')
                nombreArchTemp = os.path.splitext(os.path.basename(pdf.filename))[0]

                # MANDO A GUARDA EN ESA RUTA EL NUEVO ARCHIVO  
                if not os.path.exists(f'P12_TEMPORAL/{dni}'):
                    os.makedirs(f'P12_TEMPORAL/{dni}')       

                output_p12_path = f'P12_TEMPORAL/{dni}/TEMPORAL_{date_str}_{nombreArchTemp}.p12'                
                print(output_p12_path)                

                with open(output_p12_path, 'wb') as f:
                    f.write(response.content)
                print('Archivo descargado exitosamente.')
            else:
                print(f'Error en la solicitud. Código de respuesta: {response.status_code}')

            # Abre el archivo P12 como un objeto de archivo binario Y LEE LA INFORMACION Q HAY DENTRO   
            print("LEE EL p12")
            with open(output_p12_path, 'rb') as p12_file:    
                p12 = pkcs12.load_key_and_certificates(
                        p12_file.read(), contra.encode("ascii"), backends.default_backend()
                    )      

            # Obtener el campo CN (Nombre titular)
            cert = p12[1]
            P12_Nobre_remitente = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
            print(P12_Nobre_remitente)   

            # ESTABLESO LOS PARAMETROS QUE VA TENER LA FIRMA
            date1 = date.strftime("D:%Y%m%d%H%M%S+00'00'")        
            # nombreImgTemp = generadorQR(P12_Nobre_remitente,date1)              

            nombre_archivo = os.path.basename(pdf.filename)

            print("POSICIONES")
            x0 = pre_x0 - 40
            y0 = pre_y0 -220
            x1= pre_x1 + 40
            y1= y0 +100
            print(i,x0,y0,x1,y1,pagina)


            #  794 x 1123 píxeles
            dct.append({
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
                })
            
            print(dct[-1])

            # CON ESTO USO EL ARCHIVO Q SE ESTA LEYENDO Y AGREGO LA FIRMA
            print("FIRMA EL PDF CON EL p12")
            datas1 = cms.sign(datau, dct[-1], p12[0], p12[1], p12[2], "sha256")
            datas.append(datas1)

            # BUELVO A UNIR TODAS LAR PARTES EL PDF Y LA FIRMA CON TODOS LOS CRETIFICADOS
            archivo_pdf_para_enviar_al_cliente.write(datau) 
            archivo_pdf_para_enviar_al_cliente.write(datas[-1])
            archivo_pdf_para_enviar_al_cliente.seek(0)

            i += 1
            os.remove(output_p12_path)            

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
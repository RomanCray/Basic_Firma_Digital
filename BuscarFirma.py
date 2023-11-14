from array import array
import fitz  # PyMuPDF
import datetime
import math
import os

def ubiFirma(newPDF,pdf,dni):
    arr=[]
    posicionesF = {
        'nom':"falso",
        'x0':20,
        'y0':80,
        'paginaN': 0
    }
    arr.append(posicionesF)

    # with open(pdf, 'rb') as pdf_file:
    datau = pdf.read()    

    nombre_archivo = nombre_archivo = os.path.basename(pdf.filename)

    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date_str = date.strftime('%Y-%m-%d_%H-%M-%S_%f')

    try:
        print("CREA EL NUEVO ARCHIVO TEMPORAL")

        newPDF.write(datau)         
        newPDF.seek(0)        

        # MANDO A GUARDA EN ESA RUTA EL NUEVO ARCHIVO  
        if not os.path.exists(f'PDF_TEMPORAL/{dni}'):
            os.makedirs(f'PDF_TEMPORAL/{dni}')       

        output_pdf_path = f'PDF_TEMPORAL/{dni}/TEMPORAL_{date_str}_{nombre_archivo}'
        rutaRetorno = f'/{dni}/TEMPORAL_{date_str}_{nombre_archivo}'
        print(output_pdf_path)

        with open(output_pdf_path, 'wb') as output_pdf_file:
            output_pdf_file.write(newPDF.getvalue())

        doc = fitz.open('PDF_TEMPORAL/'+ rutaRetorno)        

        for page in doc:
            # Hacer algo con la página, por ejemplo, extraer texto
            pagina = page.number

            texto = page.get_text()

            inicio_etiqueta = "[["
            fin_etiqueta = "]]"
            inicio_pos = texto.find(inicio_etiqueta)

            while inicio_pos != -1:
                fin_pos = texto.find(fin_etiqueta, inicio_pos + len(inicio_etiqueta))
                if fin_pos != -1:
                    
                    texto_etiqueta = texto[inicio_pos + len(inicio_etiqueta):fin_pos]

                    # Actualizar la posición de inicio de búsqueda
                    inicio_pos = texto.find(inicio_etiqueta, fin_pos + len(fin_etiqueta))

                    # Buscar la palabra "ejemplo" en la primera página            
                    rects = page.search_for(f'[[{texto_etiqueta}]]')

                    # Imprimir la posición de la palabra buscada            
                    for rect in rects:
                        positionx0 = f'{rect.x0:.1f}'
                        positiony0 = f'{rect.y0:.1f}'
                        positionx1 = f'{rect.x1:.1f}'

                        print(f"La palabra '{texto_etiqueta}' esta en la posición ({positionx0}, {positiony0})) de la pagina {pagina}")
                        posicionesF = {
                            'nom':texto_etiqueta,
                            'x0': math.floor(float(positionx0)),
                            'y0': math.floor(float(positiony0)),
                            'x1': math.floor(float(positionx1)),                            
                            'paginaN': pagina
                        }
                        arr.append(posicionesF)
        
        doc.close()
        os.remove(output_pdf_path)

        ultimos_valores = {}
        longitudArr = len(arr)        

        for i in range(longitudArr):
            if arr[i]['nom'] != 'falso':
                ultimos_valores[arr[i]['nom']] = arr[i]
            # print(arr[i]['x0'])
        resultado = list(ultimos_valores.values())
        
        return resultado
    except ValueError as e:
        print('*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-')
        print('ubifirma - fallo al crear el archivo')        
        return False
import fitz  # PyMuPDF
import os

def ubiFirma(newPDF,pdf,date_str,company,dni,nombre_archivo,palabraClave):
    positionx0  = 20
    positiony0 = 80
    positionx1 = 150
    positiony1 = 150
    try:
        print("CREA EL NUEVO ARCHIVO TEMPORAL")

        newPDF.write(pdf)         
        newPDF.seek(0)        

        # MANDO A GUARDA EN ESA RUTA EL NUEVO ARCHIVO  
        if not os.path.exists(f'PDF_TEMPORAL/{company}'):
            os.makedirs(f'PDF_TEMPORAL/{company}')
        if not os.path.exists(f'PDF_TEMPORAL/{company}/{dni}'):
            os.makedirs(f'PDF_TEMPORAL/{company}/{dni}') 

        output_pdf_path = f'PDF_TEMPORAL/{company}/{dni}/TEMPORAL_{date_str}_{nombre_archivo}'
        rutaRetorno = f'{company}/{dni}/TEMPORAL_{date_str}_{nombre_archivo}'
        print(output_pdf_path)

        with open(output_pdf_path, 'wb') as output_pdf_file:
            output_pdf_file.write(newPDF.getvalue())

        doc = fitz.open('PDF_TEMPORAL/'+ rutaRetorno)

        for page in doc:
            # Hacer algo con la página, por ejemplo, extraer texto
            pagina = page.number

            # Buscar la palabra "ejemplo" en la primera página            
            rects = page.search_for(palabraClave)

            # Imprimir la posición de la palabra buscada            
            for rect in rects:
                positionx0 = f'{rect.x0:.1f}'
                positiony0 = f'{rect.y0:.1f}'
                positionx1 = f'{rect.x1:.1f}'
                positiony1 = f'{rect.y1:.1f}'

                print(f"La palabra '{palabraClave}' esta en la posición ({positionx0}, {positiony0}) - ({positionx1}, {positiony1}) de la pagina {pagina}")
        
        doc.close()
        os.remove(output_pdf_path)
        return positionx0,positiony0,positionx1,positiony1
    except ValueError as e:
        print('*-*-*-*-*-*-*-*-*-*-*-*-*-*--*-*-')
        print('ubifirma - fallo al crear el archivo')        
        return positionx0,positiony0,positionx1,positiony1
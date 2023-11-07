from PyPDF2 import PdfFileReader
import fitz  # PyMuPDF

def ubiFirma(pdf):
    print('Abre el archivo PDF en modo de lectura binaria')
    with open(pdf, "rb") as pdf_file:
        print(' Crea un objeto PdfFileReader para trabajar con el PDF')
        pdf_reader = PdfFileReader(pdf_file)

        print(' Palabra que quieres buscar')
        palabra_buscar = "tu_palabra"

        print(' Recorre todas las páginas del PDF')
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            text = page.extractText()

            print(' Comprueba si la palabra está en el texto de la página actual')
            if palabra_buscar in text:
                pdf_document = fitz.open("tu_archivo.pdf")
                page = pdf_document[page_num]

                print(' Busca las coordenadas de la palabra en la página')
                palabra_coords = page.searchFor(palabra_buscar)

                if palabra_coords:
                    print(
                        f"La palabra '{palabra_buscar}' se encontró en la página {page_num + 1} en las siguientes coordenadas:"
                    )
                    for coords in palabra_coords:
                        print(f"Coordenadas: {coords}")
                else:
                    print(
                        f"No se pudieron encontrar las coordenadas de la palabra '{palabra_buscar}' en la página {page_num + 1}"
                    )

                pdf_document.close()

from PIL import Image
import imgkit

texto_html = ''' 
<div style="width: 400px;height: 150px;">
        <div style="position: absolute;">
            <img src="https://www.intelho.com/wp-content/uploads/2021/06/Logo_01.png" alt="intelho" style="opacity: 0.18;width: 600px;">
        </div>
        <div>
            <div style="width: 300px;display: inline-block;position: relative;right: -20px">
                <h1 style="position: relative;">nombre_de_la_persona</h1>
            </div>
            <<div style="width: 300px;display: inline-block;position: relative;right: -300px;top: -155px;">
                <p style="font-size: 25px;">
                    Digitallky signed by nombre_de_la_persona
                    <br>
                    DATE: 2023.20.31
                    16:15:00 +05´30´
                </p>
            </div>
        </div>
    </div>
'''

config = imgkit.config(wkhtmltoimage=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe')
imgkit.from_string(texto_html, "texto.png", config=config)

imagen_texto = Image.open("texto.png")

imagen_texto.save("texto.png", "PNG")
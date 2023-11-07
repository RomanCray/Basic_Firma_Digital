from PIL import Image, ImageDraw, ImageFont
import qrcode
import datetime

def generadorQR(nombre, fecha, razon='', localizacion=''):
    date = datetime.datetime.strptime(fecha, 'D:%Y%m%d%H%M%S+00\'00\'')
    formatted_date = date.strftime('%Y-%m-%dT%H:%M:%S.%f-05:00')

    # Datos que deseas codificar en el código QR
    data = f'''
    FIRMADO POR: {nombre}
    RAZON: {razon}
    LOCALIZACION: {localizacion}
    FECHA: {formatted_date}
    VALIDAR CON: www.firmadigital.gob.ec
    '''

    # Crea un objeto QRCode
    qr = qrcode.QRCode(
        version=1,  # Versión del código QR (puedes ajustarla según tus necesidades)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
        box_size=10,  # Tamaño de los bloques en el código QR
        border=4,  # Margen alrededor del código QR
    )

    # Agrega los datos al código QR
    qr.add_data(data)

    # Compila el código QR
    qr.make(fit=True)

    # Crea una imagen del código QR (requiere Pillow)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Redimensiona el código QR al tamaño deseado
    qr_img = qr_img.resize((110, 100))

    # Crea una imagen en blanco del tamaño total (300x300)
    img = Image.new('RGB', (250, 200), "white")

    # Pega el código QR en la parte superior izquierda
    img.paste(qr_img, (0, 0))

    # Añade texto en la parte derecha
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/static/Besley-Regular.ttf", 8) 
    font1 = ImageFont.truetype("fonts/static/Besley-Bold.ttf", 11) 
    text = "Firmado electronicamente por:"
    elementos = nombre.split(' ')
    text1 = f"{elementos[0]} {elementos[1]}"
    text2 = f"{elementos[2]} {elementos[3]}"
    draw.text((110, 32), text, fill="black", font=font)
    draw.text((110, 42), text1, fill="black", font=font1)
    draw.text((110, 57), text2, fill="black", font=font1)

    # Guarda la imagen en un archivo
    img.save(f"img/temp_codigo_qr_{nombre}.png")

    return f"temp_codigo_qr_{nombre}.png"

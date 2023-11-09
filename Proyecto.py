import tkinter as tk
from tkinter import messagebox
from pyzbar.pyzbar import decode
import mysql.connector, qrcode, requests, cv2

def agregar_registro():
    nombre = entry_nombre.get()
    cuenta = entry_cuenta.get()
    carrera = entry_carrera.get()
    telefono = entry_telefono.get()

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1.2.3.4.5',
            database='proyecto'
        )

        cursor = conn.cursor()

        sql = "INSERT INTO registro (nombre, cuenta, carrera, telefono) VALUES (%s, %s, %s, %s)"
        val = (nombre, cuenta, carrera, telefono)
        cursor.execute(sql, val)

        conn.commit()

        contenido_qr = f"Nombre: {nombre}\nCuenta: {cuenta}\nCarrera: {carrera}\nTelefono: {telefono}"
        img = qrcode.make(contenido_qr)
        nombre_archivoqr = f"qr{cuenta}.png"
        img.save(nombre_archivoqr)

        conn.close()

        message = f'Nuevo usuario registrado: {nombre}'
        send_telegram_message(message)

        messagebox.showinfo("Éxito", "Registro agregado correctamente")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el registro: {str(e)}")

def escanear_qr():
    cap = cv2.VideoCapture(0) 

    while True:
        ret, frame = cap.read()

        if not ret:
            continue

        decoded_objects = decode(frame)
        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            print('QR Data:', data)
            
            send_telegram_message(data)

        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()

def send_telegram_message(message):
    BOT_TOKEN = '6802789021:AAF2N1L_tffCLTD3IWYZy3UA7NVv1W-5Y68'
    CHAT_ID = '5526642255'
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Mensaje enviado a Telegram:", message)
    else:
        print("Error al enviar el mensaje a Telegram")

ventana = tk.Tk()
ventana.geometry("400x300")
ventana.title("Registro de Usuarios")

label_nombre = tk.Label(ventana, text="Nombre:")
label_nombre.pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

label_cuenta = tk.Label(ventana, text="Numero de cuenta:")
label_cuenta.pack()
entry_cuenta = tk.Entry(ventana)
entry_cuenta.pack()

label_carrera = tk.Label(ventana, text="Carrera:")
label_carrera.pack()
entry_carrera = tk.Entry(ventana)
entry_carrera.pack()

label_telefono = tk.Label(ventana, text="Telefono:")
label_telefono.pack()
entry_telefono = tk.Entry(ventana)
entry_telefono.pack()

boton_agregar = tk.Button(ventana, text="Agregar Registro", command=agregar_registro)
boton_agregar.pack()

boton_escanear_qr = tk.Button(ventana, text="Escanear QR", command=escanear_qr)
boton_escanear_qr.pack()

ventana.mainloop()
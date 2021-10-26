# Importamos las librerias necesarias para el proyecto
from code_list import lista_letras, lista_numeros, lista_simbolos
import random
import tkinter
from tkinter import messagebox


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def genera_pass():
    password = ""
    # Pasamos el campo password a "editable" para escribir en él
    texto_password.delete(0, tkinter.END)
    # Creamos la configuración de la clave que vamos a crear
    num_chars = random.randint(7, 12)
    num_numbers = random.randint(2, 6)
    num_simbols = random.randint(1, 3)
    # Hay que mezclarlos aleatoriamente. No vamos a poner los chars en fila, y luego los numbers y así.
    # Entramos aleatoriamente en las 3 listas y cogemos elementos al azar.
    total_num = num_chars + num_simbols + num_numbers
    while not total_num == 0:
        index = random.randint(0, 2)
        if index == 0 and num_chars > 0:
            # Aleatorizamos si el carácter irá en mayúsculas o en minúsculas generando un boleano al azar
            if random.getrandbits(1):
                password += random.choice(lista_letras).upper()
            else:
                password += random.choice(lista_letras)
            num_chars -= 1
            total_num -= 1
        elif index == 1 and num_numbers > 0:
            password += random.choice(lista_numeros)
            num_numbers -= 1
            total_num -= 1
        elif index == 2 and num_simbols > 0:
            password += random.choice(lista_simbolos)
            num_simbols -= 1
            total_num -= 1
    # Escribo el password en el campo de texto
    texto_password.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_pass():
    # Chequeamos que los campos no estén vacíos o contengan espacios
    if texto_user_mail.get() == "":
        messagebox.showinfo(title="Error", message="El campo Email/Username está vacío")
    elif not validar_cadena(texto_user_mail.get()):
        messagebox.showinfo(title="Error", message="El campo Email/Username tiene espacios en blanco.")
    elif texto_website.get() == "":
        messagebox.showinfo(title="Error", message="El campo Website está vacío")
    elif not validar_cadena(texto_website.get()):
        messagebox.showinfo(title="Error", message="El campo Website tiene espacios en blanco.")
    elif texto_password.get() == "":
        messagebox.showinfo(title="Error", message="El campo Password está vacío")
    elif not validar_cadena(texto_password.get()):
        messagebox.showinfo(title="Error", message="El campo Password tiene espacios en blanco.")
    else:
        # Si todos los campos están bien, accedo al archivo para salvar los datos.
        # Capturo la password
        pass_str = texto_password.get()
        # Pedimos confirmación
        mensaje_box = f"¿Desea guardar la siguiente información? \
                      \n\nEmailUser: {texto_user_mail.get()} \
                      Website: {texto_website.get()} \
                      Password: {pass_str}\n"
        bool_yes = messagebox.askyesno(title="Guardar Password", message=mensaje_box)
        if bool_yes:
            # Vemos si existe y si queremos sobreescribirlo
            user_mail = texto_user_mail.get()
            website = texto_website.get()
            # Declaro una variable bool para saber si lo he sobreescrito y para cancelar sobreescritura
            # Si cancelamos la sobreescritura, nos saltaremos a la opción que graba los datos como nuevos.
            bool_es_nueva = True
            # Buscamos en el archivo si existen estos datos.
            lista_lineas = []
            try:
                archivo = open("pass_generadas", mode="r")
            except FileNotFoundError:
                messagebox.showinfo(title="Advertencia", message="No existe ningún archivo de passwords. \
                                                                 Se va a crear uno nuevo.")
            else:
                # Leo
                lista_lineas = archivo.readlines()
                # No lo pongo en el Finally ya que si hay excepción, no se abre ni se crea archivo
                # Por lo que intentar cerrarlo en el Finally dará error
                archivo.close()
            # Itero la lista de lineas buscando la clave
            for linea in lista_lineas:
                # Saco los valores separados por comas
                lista_valores = linea.split(",")
                print(lista_valores)
                # comparo
                if user_mail == lista_valores[0] and website == lista_valores[1]:
                    # La marcamos como que no es nueva para no guardarla como nueva más abajo.
                    bool_es_nueva = False
                    sms = "Ya existe password para esos datos ¿desea sobreescribirlos?."
                    sobreescribir = messagebox.askyesno(title="Advertencia", message=sms)
                    if sobreescribir:
                        # Vamos a hacer la sustitución de la clave.
                        # La buscaremos en modo READ para hacer los cambios en texto
                        # y luego escribiremos los cambios en modo WRITE creando
                        # toda la infomación nueva.
                        try:
                            archivo = open("pass_generadas", mode="r")
                        except FileNotFoundError:
                            messagebox.showinfo(title="Error", message="No existe ningún archivo de passwords")
                        else:
                            datos_cambiados = ""
                            texto_original = f"{user_mail},{website},{lista_valores[2]},"
                            nuevo_texto = f"{user_mail},{website},{pass_str},"
                            for line in archivo:
                                line = line.strip()
                                cambios = line.replace(texto_original, nuevo_texto)
                                datos_cambiados = datos_cambiados + cambios + "\n"
                            # Cerramos el archivo, lo abrimos en modo WRITE y escribimos los cambios
                            archivo.close()
                            archivo = open("pass_generadas", "w")
                            archivo.write(datos_cambiados)
                            archivo.close()
                            # limpiamos para indicar que se ha salvado.
                            texto_user_mail.delete(0, tkinter.END)
                            texto_website.delete(0, tkinter.END)
                            texto_password.delete(0, tkinter.END)
                            # Indicamos que como hemos sobreescrito una clave
                            # no hay que guardarla como clave nueva
                            messagebox.showinfo(title="Guardar password",
                                                message="La clave se ha actualizado con éxito")
                    else:
                        break
            # Entramos aquí si la clave no esyá ya almacenada
            # Si queremos almacenar los datos, y no se ha sobreescrito ya... lo hacemos
            if bool_es_nueva:
                # Declaro la variable del archivo de salida para evitar errores en el "finally".
                archivo_salida = ""
                # Vamos a hacer un acceso a archivo, por lo que debemos controlar las excepciones
                try:
                    # abrimos en modo añadir-escritura
                    archivo_salida = open("pass_generadas", mode="a")
                except FileNotFoundError:
                    # Si el archivo no existe, lo creamos. Por si es la primera
                    # vez que se usa el software.
                    archivo_salida = open("pass_generadas", mode="w")
                else:
                    # Guardamos los datos
                    archivo_salida.write(f"{texto_user_mail.get()},{texto_website.get()},{pass_str},\n")
                    # Mostramos un mensaje de datos guardados
                    messagebox.showinfo(title="Guardar password", message="La password se ha guardado con éxito")
                finally:
                    archivo_salida.close()
                    # limpiamos para indicar que se ha salvado.
                    texto_user_mail.delete(0, tkinter.END)
                    texto_website.delete(0, tkinter.END)
                    texto_password.delete(0, tkinter.END)


# ---------------------------- LOAD PASSWORD ------------------------------- #
def load_pass():
    # Cogeremos los datos introducidos de user y website y buscaremos
    # en el archivo de pass si hay ya clave creada para ese sitio.
    # Si la hay, la mostramos.
    # primero borramos el campo pass por si ya hay una clave anterior que no se mezclen
    texto_password.delete(0, tkinter.END)
    # Ahora obtengo los datos para la búsqueda
    user_mail = texto_user_mail.get()
    website = texto_website.get()
    # Chequeamos que los campos no estén vacíos.
    if user_mail == "":
        messagebox.showinfo(title="Error", message="El campo Email/Username está vacío")
    elif website == "":
        messagebox.showinfo(title="Error", message="El campo Website está vacío")
    else:
        # Buscamos en el archivo si existen estos datos.
        lista_lineas = []
        try:
            archivo = open("pass_generadas", mode="r")
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No existe ningún archivo de passwords")
        else:
            # Leo
            lista_lineas = archivo.readlines()
            # No lo pongo en el Finally ya que si hay excepción, no se abre ni se crea archivo
            # Por lo que intentar cerrarlo en el Finally dará error
            archivo.close()
        # Itero la lista de lineas buscando la clave
        bool_finded = False
        for linea in lista_lineas:
            # Saco los valores separados por comas
            lista_valores = linea.split(",")
            # comparo
            if user_mail == lista_valores[0] and website == lista_valores[1]:
                messagebox.showinfo(title="Búsqueda", message="Password encontrada.")
                # Lo pintamos en su campo correspondiente
                texto_password.insert(0, lista_valores[2])
                bool_finded = True
                break
        if not bool_finded:
            messagebox.showinfo(title="Búsqueda", message="Password NO encontrada.")


# ------------------------ VALIDAR CADENA SIN ESPACIOS ------------------------ #
def validar_cadena(cadena):
    # Verificamos que no haya espacios en blanco en una cadena
    cadena_check = str(cadena)
    result = True
    for c in cadena_check:
        if c.isspace():
            result = False
            break
    return result


# ---------------------------- UI SETUP ------------------------------- #
ventana = tkinter.Tk()
ventana.title("Password Manager")
ventana.minsize(width=480, height=360)
# La configuramos para que no sea resizable
ventana.resizable(width=False, height=False)
ventana.config(padx=20, pady=20)
# Creo el canvas
canvas_ventana = tkinter.Canvas(width=200, heigh=200)
imagen_canvas = tkinter.PhotoImage(file="logo.png")
canvas_ventana.create_image(100, 100, image=imagen_canvas)
canvas_ventana.grid(row=0, column=1)
# Etiquetas
etiqueta_user_mail = tkinter.Label(text="Email/Username")
etiqueta_user_mail.grid(row=1, column=0)
etiqueta_website = tkinter.Label(text="Website")
etiqueta_website.grid(row=2, column=0)
etiqueta_password = tkinter.Label(text="Password")
etiqueta_password.grid(row=3, column=0)
# Entradas de texto
texto_user_mail = tkinter.Entry(width=39)
texto_user_mail.grid(row=1, column=1, columnspan=2)
texto_website = tkinter.Entry(width=39)
texto_website.grid(row=2, column=1, columnspan=2)
texto_password = tkinter.Entry(width=25)
texto_password.grid(row=3, column=1)
# Creo el botón generar clave
boton_generar = tkinter.Button(text="Generar Pass", command=genera_pass)
boton_generar.grid(row=3, column=2)
boton_add = tkinter.Button(text="Añadir password", width=36, command=add_pass)
boton_add.grid(row=4, column=1, columnspan=2)
boton_add = tkinter.Button(text="Cargar password", width=36, command=load_pass)
boton_add.grid(row=5, column=1, columnspan=2)
ventana.mainloop()

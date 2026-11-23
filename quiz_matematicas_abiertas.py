#quiz_matematicas
#Josué Damián Salido Ortíz

import tkinter as tk
from tkinter import messagebox
import random
import os
import unicodedata

puntos_por_dificultad = {1: 5, 2: 10, 3: 15}
fuente = ("Times New Roman", 16)
color = "#057496"
color_fondo = "#8A0808"
vidas_iniciales = 3

nombre = ""
preguntas_juego = []
numero = 0
puntaje = 0
correctas = 0
vidas = vidas_iniciales

ventana = tk.Tk()
ventana.title("Quiz de Matemáticas Aplicadas")
ventana.geometry("560x430")
ventana.columnconfigure(0, weight=1)

def leer_preguntas():
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(carpeta, "preguntas_matematicas.csv")
    try:
        archivo = open(ruta, encoding="utf-8-sig")
        lineas = archivo.readlines()
        archivo.close()
    except UnicodeDecodeError:
        archivo = open(ruta, encoding="cp1252")
        lineas = archivo.readlines()
        archivo.close()

    lista = []
    for linea in lineas:
        if ";" in linea:
            separador = ";"
        else:
            separador = ","
        partes = linea.strip().split(separador)
        if len(partes) < 3:
            continue
        try:
            dificultad = int(partes[-1])
        except ValueError:
            continue  
        if dificultad not in puntos_por_dificultad:
            continue
        respuesta = partes[-2].strip()
        pregunta = separador.join(partes[:-2]).strip()
        if pregunta == "" or respuesta == "":
            continue
        respuestas_validas = [r.strip() for r in respuesta.split("|") if r.strip() != ""]
        lista.append([pregunta, respuestas_validas, dificultad])
    return lista

def normalizar(texto):
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(texto.split())

def a_numero(texto):
    texto = texto.strip().replace(",", ".")
    try:
        if "/" in texto:
            arriba, abajo = texto.split("/")
            return float(arriba) / float(abajo)
        return float(texto)
    except (ValueError, ZeroDivisionError):
        return None

def es_correcta(respuesta_usuario, respuestas_validas):
    for valida in respuestas_validas:
        n1 = a_numero(respuesta_usuario)
        n2 = a_numero(valida)
        if n1 is not None and n2 is not None:
            if abs(n1 - n2) < 0.01:
                return True
        elif normalizar(respuesta_usuario) == normalizar(valida):
            return True
    return False

def aplicar_fondo():
    ventana.configure(bg=color_fondo)
    for widget in ventana.winfo_children():
        if widget.winfo_class() == "Label":
            widget.configure(bg=color_fondo)

def borrar_pantalla():
    for widget in ventana.winfo_children():
        widget.destroy()

def pantalla_inicio():
    global entry_nombre
    borrar_pantalla()
    tk.Label(ventana, text="Ingresa tu nombre:", font=fuente, fg=color).grid(row=0, column=0, pady=40)
    entry_nombre = tk.Entry(ventana, font=fuente)
    entry_nombre.grid(row=1, column=0)
    entry_nombre.focus()
    entry_nombre.bind("<Return>", lambda evento: comenzar())
    tk.Button(ventana, text="Comenzar", command=comenzar).grid(row=2, column=0, pady=20)
    aplicar_fondo()

def comenzar():
    global nombre, preguntas_juego, numero, puntaje, correctas, vidas
    nombre = entry_nombre.get().strip()
    if nombre == "":
        messagebox.showwarning("Nombre", "Escribe tu nombre.")
        return
    try:
        todas = leer_preguntas()
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró preguntas_matematicas.csv. Debe estar en la misma carpeta que este archivo.")
        return
    if len(todas) < 5:
        messagebox.showerror("Error", "Hay menos de 5 preguntas válidas en el archivo.")
        return
    preguntas_juego = random.sample(todas, 5)
    numero = 0
    puntaje = 0
    correctas = 0
    vidas = vidas_iniciales
    pantalla_juego()

def pantalla_juego():
    global entry_respuesta
    borrar_pantalla()
    pregunta = preguntas_juego[numero]
    dificultad = pregunta[2]

    info = "Puntaje: " + str(puntaje) + "   Vidas: " + str(vidas) + "   Dificultad: " + str(dificultad)
    tk.Label(ventana, text=info).grid(row=0, column=0, pady=10)
    tk.Label(ventana, text=pregunta[0], font=("Times New Roman", 20), fg=color, wraplength=500).grid(row=1, column=0, pady=25)
    tk.Label(ventana, text="Tu respuesta:", font=fuente, fg=color).grid(row=2, column=0)
    entry_respuesta = tk.Entry(ventana, font=fuente)
    entry_respuesta.grid(row=3, column=0, pady=10)
    entry_respuesta.focus()
    entry_respuesta.bind("<Return>", lambda evento: responder())
    tk.Button(ventana, text="Responder", command=responder).grid(row=4, column=0, pady=20)
    aplicar_fondo()

def responder():
    global numero, puntaje, correctas, vidas
    respuesta = entry_respuesta.get().strip()
    if respuesta == "":
        messagebox.showwarning("Respuesta", "Escribe una respuesta.")
        return
    pregunta = preguntas_juego[numero]
    if es_correcta(respuesta, pregunta[1]):
        ganados = puntos_por_dificultad[pregunta[2]]
        puntaje = puntaje + ganados
        correctas = correctas + 1
        messagebox.showinfo("Correcto", "¡Bien! Ganaste " + str(ganados) + " puntos.")
    else:
        vidas = vidas - 1
        messagebox.showerror("Incorrecto", "Respuesta incorrecta. La correcta era " + pregunta[1][0] + "\nTe quedan " + str(vidas) + " vidas.")

    numero = numero + 1
    if vidas == 0 or numero == 5:
        pantalla_resultados()
    else:
        pantalla_juego()

def pantalla_resultados():
    borrar_pantalla()
    if vidas == 0:
        motivo = "Te quedaste sin vidas"
    else:
        motivo = "Terminaste las preguntas"
    texto = (nombre + "\n" + motivo + "\nPuntaje total: " + str(puntaje) + "\nCorrectas: " + str(correctas)
             + "\nIncorrectas: " + str(numero - correctas) + "\nVidas restantes: " + str(vidas))
    tk.Label(ventana, text=texto, font=fuente, fg=color).grid(row=0, column=0, pady=40)
    tk.Button(ventana, text="Jugar de nuevo", command=pantalla_inicio).grid(row=1, column=0)
    aplicar_fondo()

pantalla_inicio()
ventana.mainloop()

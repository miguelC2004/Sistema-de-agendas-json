import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

def cargar_citas(archivo):
    with open(archivo) as f:
        return json.load(f)

def filtrar_citas_por_dia(citas, dia):
    return [cita for cita in citas if cita['Day'].lower() == dia.lower()]

def obtener_horas_disponibles(citas):
    horas_ocupadas = [datetime.strptime(cita['Hour'], '%H:%M') for cita in citas]
    hora_inicio = datetime.strptime('09:00', '%H:%M')
    hora_fin = datetime.strptime('17:00', '%H:%M')
    horas_disponibles = []

    while hora_inicio < hora_fin:
        if hora_inicio not in horas_ocupadas:
            horas_disponibles.append(hora_inicio.strftime('%H:%M'))
        hora_inicio += timedelta(minutes=30)

    return horas_disponibles

def actualizar_horas_disponibles(*args):
    dia_seleccionado = dia_var.get()
    citas = cargar_citas('data.json')
    citas_dia = filtrar_citas_por_dia(citas, dia_seleccionado)
    horas_disponibles = obtener_horas_disponibles(citas_dia)
    entrada_hora['values'] = horas_disponibles

def agendar_cita():
    dia = dia_var.get()
    hora = hora_var.get()
    duracion = duracion_var.get()
    citas = cargar_citas('data.json')
    cita = {
        "Day": dia,
        "Hour": hora,
        "Duration": str(duracion)
    }
    citas.append(cita)
    citas = sorted(citas, key=lambda x: (x['Day'], x['Hour']))
    with open('data.json', 'w') as f:
        json.dump(citas, f)
    resultado_var.set(f'Su cita ha sido agregada para el día {dia}, a la hora {hora}')

def calcular_cupos():
    dia = dia_var.get()
    citas = cargar_citas('data.json')
    citas = filtrar_citas_por_dia(citas, dia)
    citas = sorted(citas, key=lambda x: (x['Day'], x['Hour']))
    cupos = calcular_espacios_disponibles(citas)
    resultado_var.set(f'El número de cupos para agendar una cita hoy es: {cupos}')

def calcular_espacios_disponibles(citas):
    hora_inicio = datetime.strptime('09:00', '%H:%M')
    hora_fin = datetime.strptime('17:00', '%H:%M')

    espacios_disponibles = 0

    for i in range(len(citas) - 1):
        hora_cita_actual = datetime.strptime(citas[i]['Hour'], '%H:%M')
        duracion_cita_actual = timedelta(minutes=int(citas[i]['Duration']))
        hora_cita_siguiente = datetime.strptime(citas[i + 1]['Hour'], '%H:%M')

        # Calcular el espacio disponible entre citas
        espacio_entre_citas = hora_cita_siguiente - (hora_cita_actual + duracion_cita_actual)

        # Verificar si el espacio entre citas es mayor o igual a 30 minutos
        if espacio_entre_citas >= timedelta(minutes=30):
            espacios_disponibles += espacio_entre_citas.total_seconds() / 60 // 30

    # Verificar el espacio disponible antes de la primera cita
    espacio_inicio = citas[0]['Hour'] - hora_inicio
    if espacio_inicio >= timedelta(minutes=30):
        espacios_disponibles += espacio_inicio.total_seconds() / 60 // 30

    # Verificar el espacio disponible después de la última cita
    espacio_fin = hora_fin - (hora_cita_siguiente + timedelta(minutes=int(citas[-1]['Duration'])))
    if espacio_fin >= timedelta(minutes=30):
        espacios_disponibles += espacio_fin.total_seconds() / 60 // 30

    return int(espacios_disponibles)

root = tk.Tk()
root.title('Programador de Citas')

frame = ttk.Frame(root, padding='3 3 12 12')
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

ttk.Label(frame, text='Día:').grid(column=1, row=1, sticky=tk.W)
dia_var = tk.StringVar()
entrada_dia = ttk.Combobox(frame, textvariable=dia_var, values=('lunes', 'martes', 'miércoles', 'jueves', 'viernes'))
entrada_dia.grid(column=2, row=1, sticky=(tk.W, tk.E))
entrada_dia.bind("<<ComboboxSelected>>", actualizar_horas_disponibles)

ttk.Label(frame, text='Hora:').grid(column=1, row=2, sticky=tk.W)
hora_var = tk.StringVar()
entrada_hora = ttk.Combobox(frame, textvariable=hora_var)
entrada_hora.grid(column=2, row=2, sticky=(tk.W, tk.E))

ttk.Label(frame, text='Duración:').grid(column=1, row=3, sticky=tk.W)
duracion_var = tk.StringVar()
entrada_duracion = ttk.Entry(frame, textvariable=duracion_var)
entrada_duracion.grid(column=2, row=3, sticky=(tk.W, tk.E))

ttk.Button(frame, text='Agendar Cita', command=agendar_cita).grid(column=3, row=4, sticky=tk.W)
ttk.Button(frame, text='Calcular Cupos', command=calcular_cupos).grid(column=3, row=5, sticky=tk.W)

resultado_var = tk.StringVar()
ttk.Label(frame, textvariable=resultado_var).grid(column=2, row=6, sticky=(tk.W, tk.E))

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

entrada_dia.focus()
root.bind('<Return>', calcular_cupos)

root.mainloop()

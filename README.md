# Duración de las Citas

El script verifica que la duración de las citas esté entre 30 y 90 minutos. Utiliza la función `calcular_espacios_disponibles` para calcular los espacios disponibles entre citas respetando las restricciones de duración mínima.

# Horario de Atención

Establece el horario de atención del sistema de 9:00 a 17:00. Las citas programadas fuera de este horario no se cuentan como espacios disponibles.

# Archivo JSON como Entrada

Carga las citas desde un archivo JSON proporcionado como entrada.

# Método para Calcular Espacios Disponibles

La función `calcular_espacios_disponibles` toma como parámetro el día de la semana y devuelve el cálculo del total de espacios disponibles para ese día.

# Buena Práctica

El código utiliza funciones y módulos para mejorar la modularidad y legibilidad. Se manejan eventos y desplegables en la interfaz gráfica (GUI) para seleccionar el día y la hora de la cita, mostrando también el resultado de las operaciones.

# Ordenación de Citas

Después de agregar o cargar citas, se ordenan por día y hora para asegurar que estén organizadas correctamente.

# Consideración de Espacios entre Citas

La función `calcular_espacios_disponibles` tiene en cuenta los espacios entre citas al calcular el total de espacios disponibles.

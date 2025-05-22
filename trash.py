import pandas as pd
import random
import openpyxl

# Opciones para las columnas
#cliente 
entrada = [0, 5, 10, 15, 20, 25, 30]
# piso
zonas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
precio = [40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000, 150000, 160000, 170000, 180000, 190000, 200000, 210000, 220000, 230000, 240000, 250000, 260000, 270000, 280000, 290000, 300000, 310000, 320000, 330000, 340000, 350000, 360000, 370000, 380000, 390000, 400000]
estados = ['Obra Nueva', 'Buen Estado', 'A Reformar']
situacion = ['alquilado', 'nuda propiedad', 'ocupada ilegalmente', 'disponible']
ascensor = ['Si', 'No']
balcon = ['Si', 'No']
bajo = ['Si', 'No']
patio = ['Si', 'No']
terraza = ['Si', 'No']
garaje = ['Si', 'No']
trastero = ['Si', 'No']
calefaccion = ['Geotermia', 'Gas', 'Electrica', 'Bomba de calor', 'No disponible']
cocina = ['Gas', 'Electrica']
habitaciones = [1, 2, 3, 4, 5]
baños = [1, 2, 3, 4]
tipo_vivienda = ['Piso', 'Casa', 'Chalet', 'Adosado', 'Dúplex', 'Ático', 'Estudio']


# Número de filas a generar
num_filas = 1000

# Generar datos aleatorios
data = []
for _ in range(num_filas):
    fila = {
        # 'Entrada Cliente' : random.choice(entrada),
        'Entrada Cliente': random.choice(entrada),
        'Zona': random.choice(zonas),
        'Precio': random.choice(precio),
        'Tipo de Vivienda': random.choice(tipo_vivienda),
        'Situacion': random.choice(situacion),
        'Estado': random.choice(estados),
        'Ascensor': random.choice(ascensor),
        'Planta': random.randint(0, 9),
        'Metros Cuadrados': random.randint(30, 400),
        'Balcon': random.choice(balcon),
        'Bajo': random.choice(bajo),
        'Patio': random.choice(patio),
        'Terraza': random.choice(terraza),
        'Cocina': random.choice(cocina),
        'Garaje': random.choice(garaje),
        'Trastero': random.choice(trastero),
        'Calefaccion': random.choice(calefaccion),
        'Habitaciones': random.choice(habitaciones),
        'Baños': random.choice(baños)
    }
    data.append(fila)

# Crear DataFrame
df = pd.DataFrame(data)

# Guardar a Excel
output_path = 'clientes.xlsx'
df.to_excel(output_path, index=False)

print(f'Archivo Excel generado: {output_path}')
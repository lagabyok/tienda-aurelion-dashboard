import pandas as pd

# Cargar el dataset
df = pd.read_csv("data_final/productos_categorias_normalizadas.csv")

# Mostrar valores únicos de las columnas seleccionadas
columnas = ['medio_pago', 'categoria', 'ciudad']

for col in columnas:
    print(f"\n--- Valores únicos en '{col}' ---")
    print(df[col].unique())
    print(f"Total de valores únicos: {df[col].nunique()}")

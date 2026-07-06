import pandas as pd

from categorias import descobrir_categoria

# Lê o CSV tratando a coluna 'data' como data real
df = pd.read_csv("extrato_exemplo.csv", parse_dates=["data"])

df["categoria"] = df["descricao"].apply(descobrir_categoria)

print(df)

print()
print("--- TOTAL POR CATEGORIA ---")
total_por_categoria = df.groupby("categoria")["valor"].sum().round(2)
print(total_por_categoria)

print()
print("--- TOP 3 CATEGORIAS DE GASTO ---")
top3 = total_por_categoria[total_por_categoria < 0].sort_values().head(3)
print(top3)
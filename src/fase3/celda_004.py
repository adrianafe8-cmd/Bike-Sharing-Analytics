
# ==========================================================
# FASE 3 - CELDA 4
# División cronológica 70 % / 15 % / 15 %
# ==========================================================

n = len(df_modelo)

n_train = int(n * 0.70)
n_val = int(n * 0.15)

train_df = df_modelo.iloc[:n_train].copy()

val_df = df_modelo.iloc[
    n_train:n_train + n_val
].copy()

test_df = df_modelo.iloc[
    n_train + n_val:
].copy()

for nombre, datos in [
    ("Entrenamiento", train_df),
    ("Validación", val_df),
    ("Prueba", test_df)
]:
    print(
        f"{nombre}: {len(datos)} registros | "
        f"{datos['dteday'].min().date()} a "
        f"{datos['dteday'].max().date()}"
    )

# Verificar que no existan fechas compartidas
assert train_df["dteday"].max() < val_df["dteday"].min()
assert val_df["dteday"].max() < test_df["dteday"].min()

assert (
    len(train_df) + len(val_df) + len(test_df)
) == len(df_modelo)

print("División cronológica correcta.")

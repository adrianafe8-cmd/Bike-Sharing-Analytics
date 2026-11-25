requeridas = ['instant','dteday','season','yr','mnth','holiday','weekday','workingday','weathersit','temp','atemp','hum','windspeed','casual','registered','cnt']
assert set(requeridas).issubset(datos.columns), 'Faltan columnas del dataset original'
df = datos.copy()
df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')
df = df.sort_values('dteday').reset_index(drop=True)
nulos = df.isna().sum().to_frame('Valores faltantes')
nulos['Porcentaje (%)'] = (df.isna().mean()*100).round(2)
display(nulos)
print('Fechas duplicadas:', df.dteday.duplicated().sum())
print('Período:',df.dteday.min().date(),'a',df.dteday.max().date())
print('Alquileres promedio:',round(df.cnt.mean(),2))
assert df.isna().sum().sum() == 0, 'Hay nulos: analizar MCAR/MAR/MNAR antes de imputar'
assert not df.dteday.duplicated().any(), 'Hay fechas duplicadas'
assert (df.casual + df.registered == df.cnt).all(), 'Inconsistencia en cnt'
print('Sin imputación: no existen datos faltantes.')
df.to_csv(SALIDA/'datos_ordenados.csv',index=False)
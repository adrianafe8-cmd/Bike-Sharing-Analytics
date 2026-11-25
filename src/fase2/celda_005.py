url = 'https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip'
try:
    with urllib.request.urlopen(url, timeout=60) as respuesta:
        with zipfile.ZipFile(io.BytesIO(respuesta.read())) as archivo:
            datos = pd.read_csv(archivo.open('day.csv'))
    print('Dataset descargado desde UCI.')
except Exception as error:
    print('Descarga no disponible:', error)
    try:
        from google.colab import files
        subidos = files.upload()
        nombre = next((x for x in subidos if x.lower().endswith('day.csv')), None)
        if nombre is None:
            raise ValueError('Debes subir day.csv')
        datos = pd.read_csv(io.BytesIO(subidos[nombre]))
    except ImportError:
        datos = pd.read_csv('day.csv')
print('Dimensiones:', datos.shape)
display(datos.head())
print('Columnas:', datos.columns.tolist())
archivo_zip=shutil.make_archive('evidencias_proyecto_integrador_bicicletas','zip',root_dir=SALIDA)
print('Evidencias:',archivo_zip)
for archivo in sorted(SALIDA.iterdir()): print(' -',archivo.name)
try:
    from google.colab import files
    files.download(archivo_zip)
except ImportError:
    print('Descarga el ZIP manualmente desde la carpeta de trabajo.')
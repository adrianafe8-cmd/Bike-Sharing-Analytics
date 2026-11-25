import shutil
from pathlib import Path
from google.colab import files

origen = Path("/content/Bike_Sharing_Analytics.html")
destino = Path("/content/index.html")

shutil.copyfile(origen, destino)

assert origen.read_bytes() == destino.read_bytes()

print("Archivo:", destino.name)
print("Tamaño MB:", round(destino.stat().st_size / 1024**2, 2))

files.download(str(destino))
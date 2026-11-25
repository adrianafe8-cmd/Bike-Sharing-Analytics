if shutil.which('Rscript') is None:
    print('Rscript no está instalado. En Colab puede instalarse con:')
    print('!apt-get update -qq && apt-get install -y -qq r-base-core r-cran-ggplot2')
else:
    print('Rscript disponible:',shutil.which('Rscript'))
codigo_r = r'''args <- commandArgs(trailingOnly=TRUE)
ruta <- args[1]
train <- read.csv(file.path(ruta,'r_entrenamiento.csv'),check.names=FALSE)
test <- read.csv(file.path(ruta,'r_prueba.csv'),check.names=FALSE)
modelo_multiple_r <- lm(cnt ~ .,data=train)
cat('Resumen de regresión múltiple en R\n')
print(summary(modelo_multiple_r))
pred <- predict(modelo_multiple_r,newdata=test)
write.csv(data.frame(real=test$cnt,prediccion_R=pred),file.path(ruta,'predicciones_R.csv'),row.names=FALSE)
if (requireNamespace('ggplot2',quietly=TRUE)) {
  library(ggplot2)
  g <- ggplot(data.frame(real=test$cnt,predicho=pred),aes(x=real,y=predicho)) +
       geom_point(alpha=.5) + geom_abline(slope=1,intercept=0,linetype='dashed') +
       labs(title='Predicción múltiple en R (prueba)',x='Real',y='Predicho') + theme_minimal()
  ggsave(file.path(ruta,'07_regresion_R.png'),g,width=8,height=5,dpi=150)
}
'''
(SALIDA/'analisis_R.R').write_text(codigo_r,encoding='utf-8')
if shutil.which('Rscript'):
    proceso=subprocess.run(['Rscript',str(SALIDA/'analisis_R.R'),str(SALIDA.resolve())],capture_output=True,text=True)
    print(proceso.stdout[-3500:])
    if proceso.returncode: raise RuntimeError(proceso.stderr)
    pred_r=pd.read_csv(SALIDA/'predicciones_R.csv')
    # La equivalencia es con el modelo múltiple entrenado en Python, no con un baseline seleccionado.
    pred_python_multiple=modelo_multiple.predict(X_test_procesado)
    diferencia=np.max(np.abs(pred_r.prediccion_R.to_numpy()-pred_python_multiple))
    print('Diferencia máxima R vs Python:',diferencia)
    assert np.allclose(pred_r.prediccion_R,pred_python_multiple,atol=1e-4)
    print('Equivalencia entre lm() y LinearRegression: confirmada.')
else:
    print('Se generó analisis_R.R, pero no se ejecutó: falta Rscript.')
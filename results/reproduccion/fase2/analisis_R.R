args <- commandArgs(trailingOnly=TRUE)
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

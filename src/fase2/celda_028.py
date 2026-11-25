nombres=preprocesador.get_feature_names_out().tolist()
# Renombramos columnas para que los nombres sean seguros para fórmulas de R.
nombres_r=[f'x{i:02d}' for i in range(len(nombres))]
r_train=pd.DataFrame(X_train_procesado,columns=nombres_r)
r_train.insert(0,'cnt',y_train.to_numpy())
r_test=pd.DataFrame(X_test_procesado,columns=nombres_r)
r_test.insert(0,'cnt',y_test.to_numpy())
r_train.to_csv(SALIDA/'r_entrenamiento.csv',index=False)
r_test.to_csv(SALIDA/'r_prueba.csv',index=False)
print('Matrices equivalentes exportadas:',r_train.shape,r_test.shape)
print('Variables R:',nombres_r)
print('Para ejecutar R, debe estar instalado Rscript.')
modelo_multiple=LinearRegression().fit(X_train_procesado,y_train)
pred_multiple_val=modelo_multiple.predict(X_val_procesado)
met_multiple=metricas(y_val,pred_multiple_val)
mae_multiple=met_multiple['MAE'];rmse_multiple=met_multiple['RMSE'];r2_multiple=met_multiple['R2']
comparacion_modelos=pd.DataFrame([{'Modelo':'Regresión lineal simple',**met_baseline},{'Modelo':'Regresión lineal múltiple',**met_multiple}])
display(comparacion_modelos.round(4))
mejora_mae=100*(mae_baseline-mae_multiple)/mae_baseline
print(f'Mejora relativa de MAE: {mejora_mae:.2f}%')
modelo_elegido='multiple' if mae_multiple<mae_baseline else 'simple'
print('Modelo seleccionado según MAE de validación:',modelo_elegido)
assert np.isfinite(pred_multiple_val).all()
comparacion_modelos.to_csv(SALIDA/'metricas_validacion.csv',index=False)
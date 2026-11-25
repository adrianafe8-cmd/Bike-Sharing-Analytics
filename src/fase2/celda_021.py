if modelo_elegido=='multiple':
    pred_test=modelo_multiple.predict(X_test_procesado)
    met_val=met_multiple
else:
    pred_test=modelo_baseline.predict(test_df[['temp']])
    met_val=met_baseline
met_test=metricas(y_test,pred_test)
evaluacion_final=pd.DataFrame([{'Conjunto':'Validación',**met_val},{'Conjunto':'Prueba',**met_test}])
display(evaluacion_final.round(4))
resultados=test_df[['dteday','cnt','temp','hum','windspeed','workingday','weathersit']].copy()
resultados['prediccion']=pred_test
resultados['residuo']=resultados['cnt']-resultados['prediccion']
resultados.to_csv(SALIDA/'predicciones_prueba.csv',index=False)
evaluacion_final.to_csv(SALIDA/'metricas_finales.csv',index=False)
fig,ax=plt.subplots(figsize=(12,5))
ax.plot(resultados.dteday,resultados.cnt,label='Valores reales')
ax.plot(resultados.dteday,resultados.prediccion,label='Predicciones',linestyle='--')
ax.set(title='Demanda real vs. predicha (prueba)',xlabel='Fecha',ylabel='Alquileres diarios')
ax.legend();fig.autofmt_xdate();fig.tight_layout();fig.savefig(SALIDA/'02_real_vs_predicho.png',dpi=150);plt.show()
assert np.isfinite(pred_test).all() and len(pred_test)==len(test_df)
print('Evaluación final realizada una sola vez.')
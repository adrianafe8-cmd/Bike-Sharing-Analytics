modelo_baseline=LinearRegression().fit(train_df[['temp']],y_train)
pred_baseline_val=modelo_baseline.predict(val_df[['temp']])
def metricas(real,pred):
    return {'MAE':mean_absolute_error(real,pred),'RMSE':np.sqrt(mean_squared_error(real,pred)),'R2':r2_score(real,pred)}
met_baseline=metricas(y_val,pred_baseline_val)
mae_baseline=met_baseline['MAE'];rmse_baseline=met_baseline['RMSE'];r2_baseline=met_baseline['R2']
display(pd.DataFrame([{'Modelo':'Regresión lineal simple',**met_baseline}]).round(4))
print('Coeficiente:',modelo_baseline.coef_[0],'Intercepto:',modelo_baseline.intercept_)
assert np.isfinite(pred_baseline_val).all()
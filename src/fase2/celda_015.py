variables_numericas=['temp','hum','windspeed','temp_hum_interaccion']
variables_categoricas=['season','weathersit','workingday','yr','fin_de_semana']
variables_modelo=variables_numericas+variables_categoricas
X_train=train_df[variables_modelo].copy();y_train=train_df['cnt'].copy()
X_val=val_df[variables_modelo].copy();y_val=val_df['cnt'].copy()
X_test=test_df[variables_modelo].copy();y_test=test_df['cnt'].copy()
preprocesador=ColumnTransformer([
    ('numericas',Pipeline([('escalador',StandardScaler())]),variables_numericas),
    ('categoricas',Pipeline([('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),variables_categoricas)
])
X_train_procesado=preprocesador.fit_transform(X_train)
X_val_procesado=preprocesador.transform(X_val)
X_test_procesado=preprocesador.transform(X_test)
for nombre,x in [('Entrenamiento',X_train_procesado),('Validación',X_val_procesado),('Prueba',X_test_procesado)]: print(nombre,x.shape)
assert X_train_procesado.shape[1]==X_val_procesado.shape[1]==X_test_procesado.shape[1]
assert 'casual' not in variables_modelo and 'registered' not in variables_modelo
print('Codificación y escalamiento sin fuga de datos: verificados.')
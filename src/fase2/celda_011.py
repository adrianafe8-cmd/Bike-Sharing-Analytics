df_modelo=df.copy()
df_modelo['fin_de_semana']=(df_modelo.dteday.dt.weekday>=5).astype(int)
df_modelo['temp_hum_interaccion']=df_modelo['temp']*df_modelo['hum']
assert df_modelo.fin_de_semana.isin([0,1]).all()
assert df_modelo.temp_hum_interaccion.notna().all()
display(df_modelo[['dteday','temp','hum','fin_de_semana','temp_hum_interaccion','cnt']].head(10))
print('Dimensiones:',df_modelo.shape)
print(df_modelo.fin_de_semana.value_counts())
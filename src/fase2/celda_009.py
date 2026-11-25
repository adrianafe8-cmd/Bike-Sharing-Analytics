variables_outliers=['cnt','temp','hum','windspeed']
filas=[]
for variable in variables_outliers:
    q1,q3=df[variable].quantile([.25,.75]); iqr=q3-q1
    li,ls=q1-1.5*iqr,q3+1.5*iqr
    cantidad=int(((df[variable]<li)|(df[variable]>ls)).sum())
    filas.append({'Variable':variable,'Q1':q1,'Q3':q3,'IQR':iqr,'Límite inferior':li,'Límite superior':ls,'Outliers':cantidad,'Porcentaje':100*cantidad/len(df)})
tabla_outliers=pd.DataFrame(filas)
display(tabla_outliers.round(3))
fig,axs=plt.subplots(2,2,figsize=(12,8))
for ax,col in zip(axs.flat,variables_outliers):
    sns.boxplot(y=df[col],ax=ax); ax.set_title('Valores atípicos: '+col)
fig.suptitle('Diagnóstico IQR (sin eliminación ni winsorización)')
fig.tight_layout();fig.savefig(SALIDA/'01_outliers.png',dpi=150);plt.show()
print('Decisión: conservar observaciones; no aplicar imputación ni recorte.')
from plotly.subplots import make_subplots
panel=make_subplots(rows=2,cols=2,specs=[[{'colspan':2},None],[{},{}]],subplot_titles=('Demanda diaria','Distribución de alquileres','Temperatura y demanda'),vertical_spacing=.15)
anos=sorted(df['dteday'].dt.year.unique())
for i,ano in enumerate(anos):
    sub=df[df['dteday'].dt.year==ano]
    visible=(i==0)
    panel.add_trace(go.Scatter(x=sub.dteday,y=sub.cnt,mode='lines',name=f'Demanda {ano}',visible=visible),row=1,col=1)
    panel.add_trace(go.Histogram(x=sub.cnt,nbinsx=25,name=f'Distribución {ano}',visible=visible),row=2,col=1)
    panel.add_trace(go.Scatter(x=sub.temp,y=sub.cnt,mode='markers',marker={'opacity':.4,'size':5},name=f'Temperatura {ano}',visible=visible),row=2,col=2)
botones=[]
for i,ano in enumerate(anos):
    vis=[j//3==i for j in range(3*len(anos))]
    botones.append(dict(label=str(ano),method='update',args=[{'visible':vis},{'title':f'Dashboard de alquileres de bicicletas — {ano}'}]))
panel.update_layout(height=800,title=f'Dashboard de alquileres de bicicletas — {anos[0]}',template='plotly_white',updatemenus=[dict(buttons=botones,direction='down',x=1,y=1.14,xanchor='right',yanchor='top')],showlegend=False)
panel.update_xaxes(title_text='Fecha',row=1,col=1);panel.update_yaxes(title_text='Alquileres',row=1,col=1)
panel.update_xaxes(title_text='Alquileres diarios',row=2,col=1);panel.update_yaxes(title_text='Frecuencia',row=2,col=1)
panel.update_xaxes(title_text='Temperatura normalizada',row=2,col=2);panel.update_yaxes(title_text='Alquileres',row=2,col=2)
panel.write_html(str(SALIDA/'07_dashboard_interactivo.html'),include_plotlyjs=True)
panel.show()
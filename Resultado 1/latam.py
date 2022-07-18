import pandas as pd

df = pd.read_excel('STOCK ALMACEN AL 02-05-22.xlsx', sheet_name='contour-export')
df.fillna('')

nuevo=pd.DataFrame()
nuevo['CODIGO BARRA']=df['BARCODE_SDESC']
nuevo['NUMERO DE SERIE']=df['PART_NO_OEM']
nuevo['CLASE']=df['INV_CLASS_CD']
nuevo['ZONA']=df['Zona']
nuevo['ROTACION']=df['RC_ROTACION']
nuevo['CLASE'] = nuevo['CLASE'].map({'SER':'TRK',
                             'TRK':'TRK',
                             'BATCH':'BATCH',
                             'KIT':'KIT'},
                             )

PRIORIDAD = [0 for i in range(len(nuevo))]
nuevo['PRIORIDAD'] = pd.Series(PRIORIDAD)

#Definicion de prioridades
mask1 = ((nuevo['CLASE'] == 'BATCH')|(nuevo['CLASE'] == 'KIT'))&(nuevo['ROTACION'] == 'FM')
mask2 = (nuevo['CLASE'] == 'TRK')&(nuevo['ROTACION'] == 'FM')
mask3 = ((nuevo['CLASE'] == 'BATCH')|(nuevo['CLASE'] == 'KIT'))&(nuevo['ROTACION'] == 'MM')
mask4 = (nuevo['CLASE'] == 'TRK')&(nuevo['ROTACION'] == 'MM')
mask5 = ((nuevo['CLASE'] == 'BATCH')|(nuevo['CLASE'] == 'KIT'))&(nuevo['ROTACION'] == 'SM')
mask6 = (nuevo['CLASE'] == 'TRK')&(nuevo['ROTACION'] == 'SM')
mask7 = ((nuevo['CLASE'] == 'BATCH')|(nuevo['CLASE'] == 'KIT'))&(nuevo['ROTACION'] == 'NM')
mask8 = (nuevo['CLASE'] == 'TRK')&(nuevo['ROTACION'] == 'NM')
Prior = [mask1,mask2,mask3,mask4,mask5,mask6,mask7,mask8]

c = 1
for i in Prior:
  nuevo.loc[i,'PRIORIDAD'] = nuevo.loc[i,'PRIORIDAD'].replace(0,c,regex=True)
  c += 1

NZONA = [0 for i in range(len(nuevo))]
nuevo['NZONA'] = pd.Series(NZONA)

zonas_prior = ['ALMACEN PRINCIPAL','72 ALMACEN','RETRO ALMACEN','WINGLET','COPA AGUA','ZONA ESCALERAS','CARPA','SUSPEL ALMACEN']

#Numero de Prioridad por zona
c = 1
for i in zonas_prior:
  nuevo.loc[(nuevo['ZONA'] == i),'NZONA'] = nuevo.loc[(nuevo['ZONA'] == i),'NZONA'].replace(0,c,regex=True)
  c += 1
#Se dio un numero alto a 'TRANSITO' para connsiderarlo de ultima prioridad
nuevo.loc[(nuevo['ZONA'] == 'TRANSITO'),'NZONA'] = nuevo.loc[(nuevo['ZONA'] == 'TRANSITO'),'NZONA'].replace(0,1000,regex=True)

final = nuevo.loc[mask1].sort_values(by = 'NZONA').copy()
Prior.pop(0)
for i in Prior:
  final = pd.concat([final,nuevo.loc[i].sort_values(by = 'NZONA').copy()],axis = 0)

final.reset_index(drop=True).to_excel('AVANCE1.xlsx')

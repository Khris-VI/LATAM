from scipy.optimize import linprog
import numpy as np
import PySimpleGUI as sg

def personas(T,N,P,dias,datos):
    turnos = len(T)
    productos_dias = datos/dias
    c = [1 for i in range(turnos)]
    primera = [-(P[i]*60/T[i]) for i in range(turnos)]
    A = [primera] + np.identity(turnos).tolist()
    b = [-productos_dias]+[N[i] for i in range(turnos)]
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(0,None) for i in range(turnos)])
    return res

def showWindow(T,pagina,Hora_I=0,Hora_F=0,Turnos=0,persona=0):
    sg.theme('DarkBlue 15')
    if pagina==0:
        Turnos=[
        [sg.T('Cantidad de turnos',
              key='Titulo_0',
              font='consalo 24')],
        [sg.T('Turnos',
              key='T',font='consalo 14'),
         sg.I(0, key='Edit_T', size=(10,1),pad=(10,10))],
        [sg.B('Siguiente',
              key='turnosCheck',
              border_width=5,
              pad=(10,10))],
        ]
        layout = [Turnos]
    elif pagina==1:
        Tiempos=[[sg.T('Tiempo de conteo por línea [min]',
                       key='Titulo_1',
                       font='consalo 24')]]
        Trabajadores=[[sg.T('Cantidad maxima de trabajadores por turno',
                            key='Titulo_3',
                            font='consalo 24')]]
        Horas=[[sg.T('Productividad por turno [horas]',
                     key='Titulo_2',
                     font='consalo 24')],]
        OtrasCantidades=[
        [sg.T('Otras Cantidades', key='Titulo_4',font='consalo 24')],
        [sg.T('Dias deseados: ', key='dias', font='consalo 14'), sg.I(1, key='Edit_dias', size=(7,1),pad=(10,10))],
        [sg.T('Datos a contar: ', key='datos', font='consalo 14'), sg.I(0, key='Edit_datos', size=(15,1),pad=(10,10))]
        ]
        calcular=[[sg.B('Calcular',
                        key='calcular',
                        border_width=5,
                        pad=(10,10))],]
        auxTRABAJADORES=[]
        auxHorainit = []
        auxHorafin = []
        auxTIEMPO=[]
        auxPROD=[]
        for i in range(T):
            number=str(i+1)
            auxTIEMPO.append(sg.T('Turno '+number+' ', key='Turno_'+number, font='consalo 14'))
            auxTIEMPO.append(sg.I(1, key='Edit_Turno_'+number, size=(7,1),pad=(10,10)))
            auxHorainit.append(sg.T('H. Inicio', key='Inicio_'+number, font='consalo 14'))
            auxHorainit.append(sg.I(0, key='Edit_Inicio_'+number, size=(7,1),pad=(10,10)))
            auxHorafin.append(sg.T('H. Final ', key='Final_'+number, font='consalo 14'))
            auxHorafin.append(sg.I(0, key='Edit_Final_'+number, size=(7,1),pad=(10,10)))
            auxTRABAJADORES.append(sg.T('Turno '+number, key='Trabajadores_'+number, font='consalo 14'))
            auxTRABAJADORES.append(sg.I(0, key='Edit_Trabajadores_'+number, size=(7,1),pad=(10,10)))
            auxPROD.append(sg.T('Horas T_'+number, key='p_'+number, font='consalo 14'))
            auxPROD.append(sg.I(0, key='Edit_p_'+number,size=(7,1), pad=(10,10)))

            if (i+1)%7==0:
                Tiempos.append(auxTIEMPO)
                Tiempos.append(auxHorainit)
                Tiempos.append(auxHorafin)
                Trabajadores.append(auxTRABAJADORES)
                Horas.append(auxPROD)
                auxTRABAJADORES=[]
                auxTIEMPO=[]
                auxHorainit = []
                auxHorafin = []
                auxPROD = []
        if len(auxTIEMPO)>0:
            Tiempos.append(auxTIEMPO)
            Tiempos.append(auxHorainit)
            Tiempos.append(auxHorafin)
            Trabajadores.append(auxTRABAJADORES)
            Horas.append(auxPROD)
            auxTRABAJADORES=[]
            auxHorainit = []
            auxHorafin = []
            auxTIEMPO=[]
            auxPROD =[]

        layout = [
        Tiempos,
        Trabajadores,
        Horas,
        OtrasCantidades,
        calcular]
    elif pagina==2:
        s = 0
        for i in range(len(Turnos)):
            s += round(persona.x[i])
            if(persona.success):
                textoAux=("Se necesitan exactamente: "+str(round(persona.fun,4))+
                          " pero en la realidad: "+str(s)+" personas \nDistribuidas de la siguiente forma:")
                layout = [[sg.T('El óptimo existe',
                                key='Titulo_0',
                                font='consalo 24')],
                          [sg.T(textoAux, key='Titulo_0',font='consalo 24')]
                         ]
                for i in range(len(Turnos)):
                    textoAux=("Turno "+str(i+1)+' ('+str(Hora_I[i])+' - '+ str(Hora_F[i])+') : '+str(round(persona.x[i],4))+
                              " Redondeado: "+str(round(persona.x[i])))
                    layout.append([sg.T(textoAux, key='Titulo_0',font='consalo 24')])
            else:
                textoAux=("El óptimo no existe, no se puede contar en "+str(dias)+
                          " dias con las restricciones específicadas")
                layout = [[sg.T(textoAux,
                                key='Titulo_0',
                                font='consalo 24')]
                         ]
            layout.append([sg.B('Reiniciar', key='Reiniciar', border_width=5, pad=(10,10))])
    if pagina!=0:
        layout.append([sg.B('Volver', key='Volver', border_width=5, pad=(10,10))])
    window = sg.Window('Óptimo Personas', layout, size=(1200,600),resizable=True)
    return window

TurnosIngresados=-1
pagina=0
window=showWindow(TurnosIngresados,pagina)

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event =='turnosCheck':
        window.close()
        TurnosIngresados=int(values['Edit_T'])
        pagina=1
        window=showWindow(TurnosIngresados,pagina)
    elif event =="Volver":
        window.close()
        pagina-=1
        window=showWindow(TurnosIngresados,pagina)
    elif event == 'Reiniciar':
        window.close()
        pagina=0
        TurnosIngresados=-1
        window=showWindow(TurnosIngresados,pagina)
    elif event == 'calcular':
        Turnos=[]
        N_max=[]
        P = []
        Hora_I = []
        Hora_F = [] 
        dias =int(values['Edit_dias'])
        datos = int(values['Edit_datos'])

        for i in range(TurnosIngresados):
            number=str(i+1)
            Turnos.append(int(values['Edit_Turno_'+number]))
            Hora_I.append(values['Edit_Inicio_'+number])
            Hora_F.append(values['Edit_Final_'+number])
            N_max.append(int(values['Edit_Trabajadores_'+number]))
            P.append(int(values['Edit_p_'+number]))
        persona = personas(Turnos,N_max,P,dias,datos)
        window.close()
        pagina=2
        window=showWindow(TurnosIngresados,pagina,Hora_I,Hora_F,Turnos,persona)
window.close()


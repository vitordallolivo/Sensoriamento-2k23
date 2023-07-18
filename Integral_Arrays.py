import scipy.integrate
from KalmanFilter import filtered_data

Funcao=filtered_data

Integral_F=[]
Integral_F=scipy.integrate.cumtrapz(Funcao)

Integral_Filtrada=[]
for i in range(len(Integral_F)):
    if (i !=0 and (((Integral_F[i]-Integral_F[i-1])>0.5) or (Integral_F[i]-Integral_F[i-1])<0.5) ):
        Integral_Filtrada.append(Integral_F[i]-Integral_F[i-1])
    else:
        Integral_Filtrada.append(Integral_F[i])

print('Integral:')
print(Integral_Filtrada)
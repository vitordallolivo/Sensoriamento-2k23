import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from voo5_accel_gyro import dt,accel_data,gyro_data
from Kalman_get_Integral_Valor import output
from Dados import a

input=output[0]

#data = np.array(input)
data= np.array(integrate.cumulative_trapezoid(input))

# Ajusta uma curva polinomial de grau 3 aos dados integrados
time = np.arange(0, len(data) * dt, dt)
poly_coeffs = np.polyfit(time, data, 7)
drift_curve = np.polyval(poly_coeffs, time)

# Subtrai a curva polinomial dos dados integrados para remover o drift
drift_removed_data = data - drift_curve


plt.figure(1)
plt.subplot(3, 1, 1)
# Plot dos dados originais, dados integrados e dados sem drift
plt.plot(time, drift_curve, label='Polyval dos dados')
plt.plot(time, data, label='Dados Integrados')
plt.plot(time, drift_removed_data, label='Dados Sem Drift (Polinomial)')
plt.xlabel('Tempo (s)')
plt.ylabel('Valores')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time, drift_removed_data, label='Dados Sem Drift (Polinomial)')
plt.xlabel('Tempo (s)')
plt.ylabel('Valores')

plt.subplot(3, 1, 3)
plt.plot(input)
plt.xlabel('Nº de amostras')
plt.show()

output_polyfit = drift_removed_data.tolist()
print(f'Polyfit:{output_polyfit}')

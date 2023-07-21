import numpy as np
import matplotlib.pyplot as plt
from voo5_accel_gyro import accel_data,dt

a= accel_data[1]

# Realiza a integração dos dados usando a regra dos trapézios
integrated_data = np.cumsum(a) * dt
#integrated_data= np.array(a)

# Ajusta uma curva polinomial de grau 3 aos dados integrados
time = np.arange(0, len(a)*dt, dt)
poly_coeffs = np.polyfit(time, integrated_data,6)
drift_curve = np.polyval(poly_coeffs, time)

# Subtrai a curva polinomial dos dados integrados para remover o drift
drift_removed_data = integrated_data - drift_curve

# Plot dos dados originais, dados integrados e dados sem drift
plt.plot(time, a, label='Dados Originais')
plt.plot(time,drift_curve,label='Polyval dos dados')
plt.plot(time, integrated_data, label='Dados Integrados')
plt.plot(time, drift_removed_data, label='Dados Sem Drift (Polinomial)')
plt.xlabel('Tempo (s)')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.show()

print(drift_removed_data.tolist())

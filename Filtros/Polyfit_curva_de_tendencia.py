import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
from voo5_accel_gyro import dt
# from Filtro_Complementar import angle_estimate_degrees
from Dados import a

data = np.array(a)
# data= np.array(integrate.cumulative_trapezoid(a))

# Ajusta uma curva polinomial de grau 3 aos dados integrados
time = np.arange(0, len(data) * dt, dt)
poly_coeffs = np.polyfit(time, data, 3)
drift_curve = np.polyval(poly_coeffs, time)

# Subtrai a curva polinomial dos dados integrados para remover o drift
drift_removed_data = data - drift_curve

# Plot dos dados originais, dados integrados e dados sem drift
plt.plot(time, drift_curve, label='Polyval dos dados')
plt.plot(time, data, label='Dados Integrados')
plt.plot(time, drift_removed_data, label='Dados Sem Drift (Polinomial)')
plt.xlabel('Tempo (s)')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.show()

output_polyfit = drift_removed_data.tolist()
print(f'Polyfit:{output_polyfit}')

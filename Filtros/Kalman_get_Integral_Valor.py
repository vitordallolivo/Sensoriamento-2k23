from voo5_accel_gyro import gyro_data,dt,accel_data
from scipy import integrate
import matplotlib.pyplot as plt
import math
from Dados import a,dt

data= accel_data# Uma lista que é de [[X],[Y],[Z]]
class KalmanFilter:
    def __init__(self, process_noise, measurement_noise):
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise
        self.angle = 0.0
        self.uncertainty = 0.0

    def update(self, measurement, dt):
        # Predição do estado
        self.angle += dt * (measurement - self.angle)

        # Atualização do erro de estimativa
        self.uncertainty += dt * self.process_noise

        # Ganho de Kalman
        kalman_gain = self.uncertainty / (self.uncertainty + self.measurement_noise)

        # Atualização do estado estimado
        self.angle += kalman_gain * (measurement - self.angle)

        # Atualização do erro de estimativa
        self.uncertainty = (1 - kalman_gain) * self.uncertainty

        return self.angle

# Exemplo de uso:
# Supondo que você tenha a leitura do giroscópio (em rad/s) armazenada na variável 'gyro_rate'
# e o intervalo de amostragem dt em segundos (por exemplo, dt = 0.01 para uma amostragem de 100Hz)
process_noise =.1 # Valor a ser ajustado conforme necessário

# Famoso Q

measurement_noise =0.01  # Valor a ser ajustado conforme necessário

# Famoso R

kalman_filter = KalmanFilter(process_noise, measurement_noise)

output=[[],[],[]]
# Aplicar o filtro de Kalman para estimar o ângulo

for i in range(len(data)):
    # Verifica se o elemento data[0] é do tipo float
    if isinstance(data[0], float):
        # Caso seja float, itera apenas uma vez
        for j in range(1):
            output[i].append(kalman_filter.update(data[i], dt))
    else:
        # Caso contrário, itera sobre todos os elementos da sequência data[0]
        for j in range(len(data[0])):
            output[i].append(kalman_filter.update(data[i][j], dt))

plt.figure(1)
plt.subplot(3, 1, 1)
for i in  range(len(output)):
    print(f'Vetor_Output_{i}={output[i]}')
    plt.plot((output[i]),label=f'Output{i}')


plt.title('Integral com filtro de Kalman')
plt.grid()
plt.legend(loc='lower left')

data=accel_data
Integral=[[],[],[]]

plt.subplot(3, 1, 2)
plt.title("Integral sem Filtro")
for i in range(len(data)):
    Integral[i] = integrate.cumulative_trapezoid(data[i],dx=dt)
    plt.plot(Integral[i],label=f'Int{i}')

plt.grid()
plt.legend(loc='lower left')


plt.subplot(3, 1, 3)
plt.title('Dados originais')
for i in range(len(data)):
    plt.plot(data[i],label=f'{i}')
plt.grid()
plt.legend(loc='lower left')

# Adicionar texto abaixo dos subplots
plt.figtext(0.5, 0.01, f'Q={process_noise} e R={measurement_noise}', ha='center', fontsize=12)
# Ajustar o espaçamento entre os subplots
plt.subplots_adjust(hspace=0.4)  # Espaçamento vertical entre os subplots
plt.show()
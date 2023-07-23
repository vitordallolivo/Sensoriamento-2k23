from voo5_accel_gyro import gyro_data,dt,accel_data
import matplotlib.pyplot as plt
import math

data= accel_data # Uma lista que é de [[X],[Y],[Z]]
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
process_noise =.01 # Valor a ser ajustado conforme necessário

# Famoso Q

measurement_noise =0.01  # Valor a ser ajustado conforme necessário

# Famoso R

kalman_filter = KalmanFilter(process_noise, measurement_noise)

angle=[[],[],[]]
# Aplicar o filtro de Kalman para estimar o ângulo
for j in range(len(data)):
    for i in range(len(data[0])):
        angle[j].append(math.degrees(kalman_filter.update(data[j][i], dt)))

    print(f'Ângulo{j}', angle[j])
plt.plot(angle[0],label='X')
plt.plot(angle[1],label='Y')
plt.plot(angle[2],label='Z')
plt.legend()
plt.show()
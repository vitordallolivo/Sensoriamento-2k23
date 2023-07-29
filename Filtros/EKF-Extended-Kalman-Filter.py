import numpy as np
from voo5_accel_gyro import accel_data,gyro_data,dt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from Dados import a,dt
import math
# Função de transição do estado (dinâmica do sistema)

def state_transition_function(state, dt):
    # Considerando o modelo de velocidade como a integral da aceleração
    velocity, acceleration = state
    velocity_next = velocity + acceleration * dt
    return np.array([velocity_next, acceleration])

# Função de observação (medição da aceleração)
def observation_function(state):
    return state[1]  # A aceleração é diretamente observada

# Matrizes de covariância do processo e medição
Q = np.diag([0.1, .01])  # Covariância do processo (erro do modelo)
R = 1 # Covariância da medição (ruído do acelerômetro)

# Inicialização do estado estimado e covariância do erro de estimativa para cada eixo
state_estimate_x = np.array([0.0, 0.0])  # [velocidade inicial, aceleração inicial]
state_estimate_y = np.array([0.0, 0.0])
state_estimate_z = np.array([0.0, 0.0])
covariance_estimate_x = np.eye(2)
covariance_estimate_y = np.eye(2)
covariance_estimate_z = np.eye(2)

# Dados de aceleração nos eixos x, y e z
accel_data_x, accel_data_y, accel_data_z = a

# Loop principal do EKF para cada eixo
estimated_velocities_x = []
estimated_velocities_y = []
estimated_velocities_z = []

for i in range(len(accel_data_x)):
    # Leituras de aceleração no instante i
    measurement_x = accel_data_x[i]
    measurement_y = accel_data_y[i]
    measurement_z = accel_data_z[i]

    # Predição do próximo estado estimado e matriz de covariância para cada eixo
    state_prediction_x = state_transition_function(state_estimate_x, dt)
    state_prediction_y = state_transition_function(state_estimate_y, dt)
    state_prediction_z = state_transition_function(state_estimate_z, dt)

    # Predição da matriz de covariância do erro de estimativa para cada eixo
    A = np.array([[1.0, dt], [0.0, 1.0]])  # Matriz jacobiana da função de transição
    covariance_prediction_x = A @ covariance_estimate_x @ A.T + Q
    covariance_prediction_y = A @ covariance_estimate_y @ A.T + Q
    covariance_prediction_z = A @ covariance_estimate_z @ A.T + Q

    # Atualização com as medições de aceleração reais para cada eixo
    innovation_x = measurement_x - observation_function(state_prediction_x)
    innovation_y = measurement_y - observation_function(state_prediction_y)
    innovation_z = measurement_z - observation_function(state_prediction_z)

    H = np.array([0.0, 1.0])  # Matriz jacobiana da função de observação
    innovation_covariance = H @ covariance_prediction_x @ H.T + R

    kalman_gain_x = covariance_prediction_x @ H.T / innovation_covariance
    kalman_gain_y = covariance_prediction_y @ H.T / innovation_covariance
    kalman_gain_z = covariance_prediction_z @ H.T / innovation_covariance

    state_estimate_x = state_prediction_x + kalman_gain_x * innovation_x
    state_estimate_y = state_prediction_y + kalman_gain_y * innovation_y
    state_estimate_z = state_prediction_z + kalman_gain_z * innovation_z

    # Atualização das matrizes de covariância do erro de estimativa para cada eixo
    covariance_estimate_x = (np.eye(2) - kalman_gain_x @ H) @ covariance_prediction_x
    covariance_estimate_y = (np.eye(2) - kalman_gain_y @ H) @ covariance_prediction_y
    covariance_estimate_z = (np.eye(2) - kalman_gain_z @ H) @ covariance_prediction_z

    # Salvando as velocidades estimadas em cada eixo
    estimated_velocities_x.append(state_estimate_x[0])
    estimated_velocities_y.append(state_estimate_y[0])
    estimated_velocities_z.append(state_estimate_z[0])

# As velocidades estimadas em cada eixo estarão disponíveis nas listas estimated_velocities_x, estimated_velocities_y e estimated_velocities_z
print("x=", estimated_velocities_x)
print("y=", estimated_velocities_y)
print("z=", estimated_velocities_z)

print(f'X_max={max(estimated_velocities_x)}',f'\tX_min={min(estimated_velocities_x)}')
print(f'Y_max={max(estimated_velocities_y)}',f'\tY_min={min(estimated_velocities_y)}')
print(f'Z_max={max(estimated_velocities_z)}',f'\tZ_min={min(estimated_velocities_z)}')

plt.plot(estimated_velocities_x,label='x')
plt.plot(estimated_velocities_y,label='y')
plt.plot(estimated_velocities_z,label='z')
plt.legend()
plt.show()


x=np.array(estimated_velocities_x)
y=np.array(estimated_velocities_y)
z=np.array(estimated_velocities_z)

# Criar uma figura e um subplot 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plotar os pontos em 3D
ax.scatter(x, y, z)

# Definir rótulos dos eixos
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.set_zlabel('Eixo Z')

# Mostrar o gráfico
plt.show()

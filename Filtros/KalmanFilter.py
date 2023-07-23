import numpy as np
import matplotlib.pyplot as plt
#from quartenions import yaw_lista
#from voo5_accel_gyro import Roll_List,Pitch_List,Yaw_List
from Dados import a,Polyfit

data = Polyfit # tem que ser uma lista

# VALORES DE Q e R devem ser mudados de acordo com seu set de dados


# Função para aplicar o filtro de Kalman na lista de valores
def kalman_filter(data, Q, R):
    # Inicialização das variáveis do filtro
    n = len(data)
    filtered_data = [data[0]]  # Valor inicial do filtro
    x_hat = data[0]
    P = 1.0

    # Loop para aplicar o filtro de Kalman nos valores da lista
    for i in range(1, n):
        # Predição do próximo estado usando o modelo de transição (no caso, assumimos um modelo simples x_k = x_{k-1})
        x_hat_minus = x_hat
        P_minus = P + Q

        # Atualização do estado baseado na nova medição
        K = P_minus / (P_minus + R)
        x_hat = x_hat_minus + K * (data[i] - x_hat_minus)
        P = (1 - K) * P_minus

        # Adiciona o valor filtrado na lista de saída
        filtered_data.append(x_hat)

    return filtered_data

# Dados de exemplo
np.random.seed(0)
n_samples = 100


# Parâmetros do filtro de Kalman
Q = 1e-2# Process noise (covariance da estimativa do ruído do processo)
R =  0.6121# Measurement noise (covariance da medição)

# Aplica o filtro de Kalman nos dados
filtered_data = kalman_filter(data, Q, R)

# Plot dos resultados
plt.figure(figsize=(10, 6))
plt.plot(data, label='Dados originais')
plt.plot(filtered_data, label='Dados filtrados', color='red', linewidth=2)
plt.legend()
plt.xlabel('Amostras')
plt.ylabel('Valor')
plt.title('Filtro de Kalman')
plt.grid(True)
plt.show()

print(f'Funcao={filtered_data}')
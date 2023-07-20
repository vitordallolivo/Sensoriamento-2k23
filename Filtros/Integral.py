import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz
from Dados import a, dt

# Função para integrar os dados usando a regra dos trapézios
def integration_trapezoidal(data, dt):
    integrated_data = cumtrapz(data)
    return integrated_data

# Função para remover o drift da integral usando regressão linear
def remove_drift_from_integral(integral_data):
    # Criar um array de tempo (assumindo que os valores são amostrados em intervalos iguais)
    time = np.arange(len(integral_data))*0.5

    # Ajustar uma reta (linha) aos dados usando a regressão linear
    coeffs = np.polyfit(time, integral_data, 1)
    drift_estimate = np.polyval(coeffs, time)

    # Subtrair a tendência linear dos dados originais
    integral_without_drift = integral_data - drift_estimate

    return integral_without_drift

# Função para aplicar o filtro de média móvel a uma lista de dados
def apply_moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Converter a lista 'a' para um array numpy para facilitar os cálculos
data_array = np.array(a)

# Realiza a integração dos dados usando a regra dos trapézios
integrated_data = integration_trapezoidal(data_array, dt)

# Remove a linha de tendência das integrais
detrended_data = remove_drift_from_integral(integrated_data)

# Aplica o filtro de média móvel para suavizar os valores de velocidade
window_size = 3  # Tamanho da janela do filtro de média móvel
detrended_data = apply_moving_average(detrended_data, window_size)

detrended_data=detrended_data*3.6

# Output das mudanças angulares integradas para cada eixo como lista no mesmo formato de entrada
output_list = detrended_data.tolist()

print("Integral de a:")
print(integrated_data)
print("Integral sem linha de tendencia")
print(output_list)

plt.plot(output_list, label='Sem Tendencia', color='red')
#plt.plot(integrated_data, label='Com Tendencia', color='green')
plt.plot(a, label='Original', color='blue')
plt.legend()
plt.show()

import matplotlib.pyplot as plt
from voo5_accel_gyro import accel_data,dt,gyro_data
from statistics import median
from Dados import a

def median_filter(data, window_size):
    filtered_data = []
    half_window = window_size // 2

    for i in range(len(data)):
        start_idx = max(0, i - half_window)
        end_idx = min(len(data), i + half_window + 1)
        window = data[start_idx:end_idx]
        filtered_data.append(median(window))

    return filtered_data
''
# Lista de entrada obtida do arquivo Dados.py
input_data = accel_data[0]

# Tamanho da janela do filtro de mediana (deve ser ímpar)
window_size = 27

# Aplicar o filtro de mediana na lista de entrada
filtered_data = median_filter(input_data, window_size)

# Plot dos dados originais e dos dados filtrados
plt.figure(figsize=(10, 6))
plt.plot(input_data, label='Dados Originais', color ='red')
plt.plot(filtered_data, label='Dados Filtrados', color ='blue')
plt.xlabel('Amostras')
plt.ylabel('Valores')
plt.title('Filtro de Mediana')
plt.legend()
plt.grid(True)
plt.show()

print(filtered_data)
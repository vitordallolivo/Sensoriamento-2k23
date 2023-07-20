import math
from Dados import gyro,accel
def complementary_filter(alpha, gyro_data, accel_data):
    # Variáveis para armazenar a estimativa do ângulo e a estimativa do bias
    angle_estimate = [[0.0], [0.0], [0.0]]  # Iniciamos com ângulos 0 para x, y, z
    gyro_bias = [0.0, 0.0, 0.0]  # Iniciamos com bias 0 para x, y, z

    dt = 0.01  # Intervalo de tempo entre as amostras (exemplo: 0.01 segundos)

    # Loop para iterar sobre os dados
    for i in range(1, len(gyro_data[0])):
        # Atualizar o bias do giroscópio usando as medidas do acelerômetro
        angle_acc = [math.atan2(accel_data[1][i], accel_data[2][i]),  # ângulo estimado para x
                     math.atan2(accel_data[0][i], accel_data[2][i]),  # ângulo estimado para y
                     math.atan2(accel_data[0][i], accel_data[1][i])]  # ângulo estimado para z
        gyro_bias = [alpha * (gyro_bias[j] + math.radians(gyro_data[j][i]) * dt) + (1 - alpha) * angle_acc[j]
                     for j in range(3)]

        # Atualizar a estimativa do ângulo usando os dados do giroscópio
        for j in range(3):
            angle_estimate[j].append(math.degrees(math.radians(gyro_data[j][i]) - gyro_bias[j]))

    return angle_estimate

alpha_value = 0.9
angle_estimate_degrees = complementary_filter(alpha_value, gyro, accel)

# Imprime os ângulos estimados para x, y, z
print("Ângulos estimados (graus):")
print(f"x: {angle_estimate_degrees[0]}")
print(f"y: {angle_estimate_degrees[1]}")
print(f"z: {angle_estimate_degrees[2]}")

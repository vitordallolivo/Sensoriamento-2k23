import numpy as np
from voo5_accel_gyro import gyro_data,accel_data
from Dados import dt

def madgwick_filter(accel_data, gyro_data, dt, beta=0.1):
    # Parâmetros iniciais
    pitch, yaw, roll = 0.0, 0.0, 0.0
    gyro_bias = np.zeros(3)

    # Listas para armazenar os ângulos
    pitch_list, yaw_list, roll_list = [], [], []

    # Loop para iterar sobre os dados
    for i in range(1, len(gyro_data[0])):
        # Obter as leituras do giroscópio em graus/s
        gx, gy, gz = gyro_data[0][i], gyro_data[1][i], gyro_data[2][i]

        # Obter as leituras do acelerômetro em m/s² e normalizá-las
        ax, ay, az = accel_data[0][i], accel_data[1][i], accel_data[2][i]
        accel_magnitude = np.sqrt(ax**2 + ay**2 + az**2)
        ax, ay, az = ax / accel_magnitude, ay / accel_magnitude, az / accel_magnitude

        # Cálculo das derivadas dos ângulos de Euler
        pitch += dt * (gy - gyro_bias[0])
        yaw += dt * (gz - gyro_bias[1])
        roll += dt * (gx - gyro_bias[2])

        # Cálculo das estimativas dos ângulos de Euler usando o filtro de Madgwick
        pitch += dt * (gyro_data[1][i] - gyro_bias[0])
        yaw += dt * (gyro_data[2][i] - gyro_bias[1])
        roll += dt * (gyro_data[0][i] - gyro_bias[2])

        # Atualização do bias do giroscópio
        gyro_bias[0] += beta * (gy - gyro_bias[0])
        gyro_bias[1] += beta * (gz - gyro_bias[1])
        gyro_bias[2] += beta * (gx - gyro_bias[2])

        # Adicionar os ângulos calculados nas listas
        pitch_list.append(np.degrees(pitch))
        yaw_list.append(np.degrees(yaw))
        roll_list.append(np.degrees(roll))

    return pitch_list, yaw_list, roll_list


pitch_list, yaw_list, roll_list = madgwick_filter(accel_data, gyro_data, dt)
print("Pitch List:", pitch_list)
print("Yaw List:", yaw_list)
print("Roll List:", roll_list)

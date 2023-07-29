import math
from Dados import a,dt
from scipy import integrate
import matplotlib.pyplot as plt
from voo5_accel_gyro import accel_data,gyro_data,dt
from Kalman_get_Integral_Valor import output

alpha=0.5


def calculate_angles(accel_data,gyro_data):
    # Extrair as acelerações nas direções x, y e z
    ax, ay, az = accel_data[0][0], accel_data[1][0], accel_data[2][0]
    constante=0

    pitch,roll,yaw=[],[],[]

    for i in range(len(accel_data[1])):
        ax, ay, az = accel_data[0][i], accel_data[1][i], accel_data[2][i]
        gx, gy, gz = gyro_data[0][i],gyro_data[1][i],gyro_data[2][i]
        # Calcular o ângulo de pitch usando o acelerômetro
        pitch.append(alpha*(math.atan2(ay, math.sqrt(ax**2 + az**2)) * 180.0 / math.pi)+(1-alpha)*output[1][i])

        # Calcular o ângulo de roll usando o acelerômetro
        roll.append(alpha*(math.atan2(-ax, math.sqrt(ay**2 + az**2)) * 180.0 / math.pi)+(1-alpha)*output[0][i])

        constante= output[2][i]
        yaw.append(constante)

    return pitch, roll, yaw

# Exemplo de uso:
pitch, roll, yaw = calculate_angles(accel_data,gyro_data)

print(f'\nRoll={roll}\nPitch={pitch}\nYaw={yaw}')
plt.plot(roll,label='Roll')
plt.plot(pitch,label='Pitch')
plt.plot(yaw,label='Yaw')
plt.legend()
plt.grid()
plt.show()
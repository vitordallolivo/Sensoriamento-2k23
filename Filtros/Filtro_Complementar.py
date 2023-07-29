import math
from Dados import a,dt
from scipy import integrate
import matplotlib.pyplot as plt
from voo5_accel_gyro import accel_data,gyro_data,dt
from Kalman_get_Integral_Valor import output

alpha=0.4


def calculate_angles(accel_data,gyro_data):
    # Extrair as acelerações nas direções x, y e z
    ax, ay, az = accel_data[0][0], accel_data[1][0], accel_data[2][0]
    constante=0
    gyro_rate_y=0
    gyro_rate_x=0

    pitch,roll,yaw=[],[],[]

    for i in range(len(accel_data[1])):
        ax, ay, az = accel_data[0][i], accel_data[1][i], accel_data[2][i]
        gx, gy, gz = gyro_data[0][i],gyro_data[1][i],gyro_data[2][i]
        # Calcular o ângulo de pitch usando o acelerômetro
        gyro_rate_y +=output[1][i]*dt
        gyro_rate_x += output[0][i] * dt
        pitch.append(alpha*(math.atan2(ay, math.sqrt(ax**2 + az**2)) * 180.0 / math.pi)+(1-alpha)*gyro_rate_y)

        # Calcular o ângulo de roll usando o acelerômetro
        roll.append(alpha*(math.atan2(-ax, math.sqrt(ay**2 + az**2)) * 180.0 / math.pi)+(1-alpha)*gyro_rate_x)

        constante+= output[2][i]*dt
        yaw.append(constante)

    return pitch, roll, yaw

# Exemplo de uso:
pitch, roll, yaw = calculate_angles(accel_data,gyro_data)

print(f'\nRoll={roll}\nPitch={pitch}\nYaw={yaw}')

plt.figure(1)

plt.subplot(3, 1, 1)
plt.title('Roll')
plt.grid()
plt.plot(roll,label='Roll',color='blue')

plt.subplot(3, 1, 2)
plt.title('Pitch')
plt.grid()
plt.plot(pitch,label='Pitch',color='green')

plt.subplot(3, 1, 3)
plt.title('Yaw')
plt.plot(yaw,label='Yaw',color='orange')
plt.grid()
plt.subplots_adjust(hspace=0.4)
plt.figtext(0.5, 0.01, f'Alpha={alpha*100}%', ha='center', fontsize=12)
plt.show()

import numpy as np
import math
from voo5_accel_gyro import gyro_data, accel_data,dt

def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

def madgwick_filter(gyro_data, accel_data, sample_rate, beta=0.1):

    quaternions = [[1.0, 0.0, 0.0, 0.0]] * len(gyro_data[0])  # Inicializa os quaterniões com [w, x, y, z] = [1, 0, 0, 0]

    for i in range(1, len(gyro_data[0])):
        gx, gy, gz = np.radians(gyro_data[0][i]), np.radians(gyro_data[1][i]), np.radians(gyro_data[2][i])
        ax, ay, az = accel_data[0][i], accel_data[1][i], accel_data[2][i]

        qw, qx, qy, qz = quaternions[i-1]

        # Cálculo das taxas de mudança do quaternião
        q_dot = 0.5 * np.array([
            -qx * gx - qy * gy - qz * gz,
            qw * gx + qy * gz - qz * gy,
            qw * gy - qx * gz + qz * gx,
            qw * gz + qx * gy - qy * gx
        ])

        # Integração numérica usando o método de trapézio
        qw_next = qw + q_dot[0] * dt
        qx_next = qx + q_dot[1] * dt
        qy_next = qy + q_dot[2] * dt
        qz_next = qz + q_dot[3] * dt

        # Correção do quaternião baseada na leitura do acelerômetro
        acc_magnitude = np.sqrt(ax * ax + ay * ay + az * az)
        if acc_magnitude > 0.0:
            # Cálculo do erro entre a leitura do acelerômetro e a direção estimada da gravidade
            acc_direction = np.array([ax, ay, az]) / acc_magnitude
            est_gravity_direction = quaternion_multiply(quaternion_multiply([qw, qx, qy, qz], [0, ax, ay, az]), [qw, -qx, -qy, -qz])
            acc_correction = beta * np.cross(est_gravity_direction[1:], acc_direction)
            qx_next += acc_correction[0] * dt
            qy_next += acc_correction[1] * dt
            qz_next += acc_correction[2] * dt

        # Normalização do quaternião
        norm = np.sqrt(qw_next**2 + qx_next**2 + qy_next**2 + qz_next**2)
        qw_next /= norm
        qx_next /= norm
        qy_next /= norm
        qz_next /= norm

        # Armazena os quaterniões estimados nas listas
        quaternions[i] = [qw_next, qx_next, qy_next, qz_next]

    return quaternions

def euler_angles_from_quaternion(q):
    qw, qx, qy, qz = q
    roll = math.atan2(2 * (qw*qx + qy*qz), 1 - 2 * (qx*qx + qy*qy))
    pitch = math.asin(2 * (qw*qy - qz*qx))
    yaw = math.atan2(2 * (qw*qz + qx*qy), 1 - 2 * (qy*qy + qz*qz))
    return math.degrees(roll), math.degrees(pitch), math.degrees(yaw)


# Calcular os quaterniões usando o filtro de Madgwick
quaternions = madgwick_filter(gyro_data, accel_data, 0)

# Imprimir os ângulos de Euler estimados
print("Ângulos de Euler estimados:")

roll_lista,pitch_lista,yaw_lista=[],[],[]

for i in range(len(quaternions)):
    roll, pitch, yaw = euler_angles_from_quaternion(quaternions[i])
    roll_lista.append(roll)
    pitch_lista.append(pitch)
    yaw_lista.append(yaw)

print('roll',roll_lista)
print('pitch',pitch_lista)
print('yaw',yaw_lista)

from Dados import a

def wrap_angle(angle):
    while angle > 90:
        angle -= 90
    while angle < 0:
        angle += 90
    return angle

def reduce_angles_to_first_quadrant(angle_list):
    reduced_angles = [wrap_angle(angle) for angle in angle_list]
    return reduced_angles

# Exemplo de uso:
angles = a
reduced_angles = reduce_angles_to_first_quadrant(angles)
print(reduced_angles)  # Output: [10, 70, 10, 60, 45]

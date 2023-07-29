import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyproj

# Exemplo de coordenadas ECEF (x, y, z)
ecef_coords = np.array([
    [5000000, 10000000, 2000000],
    [6000000, 11000000, 2500000],
    [7000000, 12000000, 3000000]
])

# Criação do objeto Geod para converter ECEF para latitude, longitude e altitude
geod = pyproj.Geod(ellps='WGS84')

# Converte as coordenadas ECEF para latitude, longitude e altitude
lon, lat, alt = geod.ecef2geodetic(ecef_coords[:, 0], ecef_coords[:, 1], ecef_coords[:, 2])

# Configuração do gráfico 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plota as coordenadas ECEF em 3D
ax.scatter(ecef_coords[:, 0], ecef_coords[:, 1], ecef_coords[:, 2], c='red', marker='o')

# Rótulos dos eixos
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')

# Título do gráfico
ax.set_title('Gráfico 3D usando coordenadas ECEF')

# Mostra o gráfico
plt.show()

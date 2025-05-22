import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from PIL import Image

# Загрузка фона
background_path = "input\Screenshot_1731407782.png"  # Замените обратный слеш на прямой для совместимости
background_img = Image.open(background_path)
background_img = background_img.resize((1920, 1080))  # Изменение размера до 1920x1080 для соответствия

# Координаты точек
coordinates = [
    (150, 840),
    (160, 700),
    (143, 699),
    (142, 600),
    (145, 850),
    (143, 861),
    (150, 743),
    (150, 645),
    (150, 765)
]

# Создание 2D-гистограммы для плотности тепловой карты
x_coords, y_coords = zip(*coordinates)
x_coords = np.array(x_coords)
y_coords = np.array(y_coords)

# Определение разрешения и размера сетки
x_bins = np.linspace(0, 1920, 192)  # 192 корзины по ширине
y_bins = np.linspace(0, 1080, 108)  # 108 корзин по высоте

# Построение 2D-гистограммы
heatmap, xedges, yedges = np.histogram2d(x_coords, y_coords, bins=[x_bins, y_bins])

# Применение фильтра Гаусса для создания эффекта размытия
heatmap = gaussian_filter(heatmap, sigma=10)

# Построение изображения
plt.figure(figsize=(19.2, 10.8))

# Отображение фона
plt.imshow(background_img, extent=[0, 1920, 0, 1080], alpha=1.0, aspect='auto')

# Отображение тепловой карты поверх фона
plt.imshow(heatmap.T, cmap='hot', origin='lower', extent=[0, 1920, 0, 1080], alpha=0.6)

# Настройки осей
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Heatmap Screenshot_1741334213')
plt.colorbar(label='Intensity')

# Сохранение графика в файл
output_path = "output/heatmap_output1o.png"  # Укажите путь для сохранения файла
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Heatmap saved at: {output_path}")

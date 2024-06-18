"""
Общий конфиг для скриптов
"""
MATRIX_IP = '192.168.50.88'  # IP адрес контроллера матрицы
STREAM_CONNECTION_MODE = 'websocket'  # Тип подключения для трансляций. Может быть websocket или post
WIDTH = 16  # Ширина матрицы(по X)
HEIGHT = 16  # Высота матрицы(по Y)
PHOTO_PATH = 'photos/photo.png'  # Путь до картинки для отправки на матрицу
IMAGE_PATH = 'photos/photo.bin'  # Путь до подготовленной картинки для отправки на матрицу
EFFECTS_IDS = ('rainbow', 'ball', 'perlin', 'lava', 'sinusoid', 'snowing', 'confetti')  # Названия(effect_id) всех эффектов
ASPECT = (1, 2)  # Отношения сторон (ширина, высота) при выводе матрицы в терминал

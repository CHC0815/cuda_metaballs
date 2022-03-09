from unittest import runner
import numpy as np
from numba import cuda, jit
import pygame
import math
import time

# PARAMS
size = 1024
level = 1.0
dt = 0
speed = 200

# KERNEL
@cuda.jit
def kernel(io_array, circles):
    row, col = cuda.grid(2)
    if row < io_array.shape[0] and col < io_array.shape[1]:
        sum = 0
        for circle in circles:
            sum += (math.pow(circle[2], 2) / (math.pow(row - circle[0], 2) + math.pow(col - circle[1], 2)))
        io_array[row, col] = sum

# GLOBALS
pygame.init()
screen = pygame.display.set_mode((size, size))
running = True
data = np.zeros((size, size))
threadsperblock = (16, 16)
blockspergrid_x = math.ceil(data.shape[0] / threadsperblock[0])
blockspergrid_y = math.ceil(data.shape[1] / threadsperblock[1])
circles = []
circles_global_mem = None
data_global_mem = None

# INIT FUNCTION
def init():
    global circles
    circles = []
    for i in range(5):
        circles.append(np.array([np.random.randint(0, data.shape[0]),
            np.random.randint(0, data.shape[1]),
            np.random.randint(100, 150), 
            np.random.randint(-speed, speed), np.random.randint(-speed, speed)], dtype=np.float32))

# RENDER FUNCTION
def render():
    global data, level, screen
    surf = pygame.surfarray.make_surface(data)

    screen.blit(surf, (0, 0))

# UPDATE FUNCTION
def update():
    global circles_global_mem, data_global_mem, circles, data, dt
    for circle in circles:
        if circle[0] >= data.shape[0]:
            circle[3] = -circle[3]
        elif circle[0] <= 0:
            circle[3] = -circle[3]
        if circle[1] >= data.shape[1]:
            circle[4] = -circle[4]
        elif circle[1] <= 0:
            circle[4] = -circle[4]
        circle[0] += circle[3] * dt
        circle[1] += circle[4] * dt

    circles_global_mem = cuda.to_device(circles)
    data_global_mem = cuda.device_array(data.shape)
    kernel[(blockspergrid_x, blockspergrid_y), threadsperblock](data_global_mem, circles_global_mem)
    data = data_global_mem.copy_to_host()

# MAIN LOOP
init()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    update_start = time.time()
    update()
    update_end = time.time()
    render()
    render_end = time.time()
    print("Update: %f, Render: %f, FPS: %f" % (update_end - update_start, render_end - update_end, 1 / (render_end - update_start)))
    dt = (update_end - update_start)
    pygame.display.flip()
pygame.quit()

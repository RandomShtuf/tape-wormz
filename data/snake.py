import pygame


class snake:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface

    def move(self, length, x, y, add_x, add_y, snake_pos, rotation):
        for i in range(length-1, 0, -1):
            x[i] = x[i - 1]
            y[i] = y[i - 1]
            snake_pos[i] = (x[i], y[i])
            rotation[i] = rotation[i - 1]

        x[0] += add_x
        y[0] += add_y

        if x[0] < 0:
            x[0] = 39*8
        if x[0] >= 40*8:
            x[0] = 0
        if y[0] < 0:
            y[0] = 24*8
        if y[0] >= 25*8:
            y[0] = 0

        snake_pos[0] = (x[0], y[0])

        return snake_pos, rotation

    def update_body_rects(self, body_rects, snake_pos):
        for i in range(len(body_rects)):
            body_rects[i].x = snake_pos[i + 2][0]
            body_rects[i].y = snake_pos[i + 2][1]
        return body_rects

    def draw(self, pos, rotation, img):
        rotate = 270
        if rotation == 'right':
            rotate = 270
        elif rotation == 'left':
            rotate = 90
        elif rotation == 'up':
            rotate = 0
        else:
            rotate = 180
        snake = pygame.transform.rotate(img, rotate)
        self.parent_surface.blit(snake, pos)
        pygame.display.update()

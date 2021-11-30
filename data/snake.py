import pygame


class snake:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface

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

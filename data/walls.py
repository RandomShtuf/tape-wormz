#!/usr/bin/python3
import pygame


class wall:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface

    def draw(self, pos_x, pos_y, flip, img):
        draw_pos = (pos_x, pos_y)
        if flip is True:
            draw_img = pygame.transform.flip(
                img,
                True,
                True
            )
        else:
            draw_img = img
        self.parent_surface.blit(draw_img, draw_pos)

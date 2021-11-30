#!/usr/bin/python3
import pygame


class food:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface

    def draw(self, food_pos, food_id):
        def set_img(food_id):
            if food_id == 1:
                food = pygame.image.load(
                    'data/sprites/orange.png'
                ).convert()
            elif food_id == 2:
                food = pygame.image.load(
                    'data/sprites/meat.png'
                ).convert()
            elif food_id == 3:
                food = pygame.image.load(
                    'data/sprites/sugar.png'
                ).convert()
            else:
                food = pygame.image.load(
                    'data/sprites/bogir.png'
                ).convert()

            return food

        food = set_img(food_id)
        food.set_colorkey((255, 255, 255))
        self.parent_surface.blit(food, food_pos)
        pygame.display.update()

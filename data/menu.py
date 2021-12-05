#!/usr/bin/python3
import pygame


class menu:
    def __init__(self, parent_surface):
        self.parent_surface = parent_surface

    def draw(self, img):
        self.parent_surface.blit(img, (0, 0))

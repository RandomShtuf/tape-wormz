#!/usr/bin/python3
import pygame


class animation:
    def __init__(self):
        self.animation_frames = {}

    def load_animation(self, path, frame_durations):
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 1
        for frame in frame_durations:
            animation_frame_id = animation_name + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            # player_animations/idle/idle_0.png
            animation_image = pygame.image.load(img_loc).convert()
            animation_image.set_colorkey((255, 255, 255))
            self.animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

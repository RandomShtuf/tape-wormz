#!/usr/bin/python3
import pygame
import sys
import random
import data.snake as S
import data.food as F
import data.animation as A
import data.walls as W
# import math

from pygame.locals import *


class game:
    def __init__(self, WINDOW_SIZE, high_score):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.WINDOW_SIZE = WINDOW_SIZE
        self.window = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
        pygame.display.set_caption('This is a window')
        self.SCREEN_SIZE = (320, 200)
        self.screen = pygame.Surface(self.SCREEN_SIZE)
        self.s = S.snake(self.screen)
        self.f = F.food(self.screen)
        self.w = W.wall(self.screen)
        self.a = A.animation()
        self.high_score = high_score

    def update_score(self):
        return self.high_score

    def dead(self):
        # time.sleep(1.00)
        SCREEN_WIDTH = 320
        SCREEN_HEIGHT = 200
        font = pygame.font.SysFont('dejavusans', 100, True)
        score_font = pygame.font.SysFont('dejavusans', 8, True)
        again_font = pygame.font.SysFont('dejavusans', 16, True)

        death_text = font.render("O O F", True, (255, 255, 255))

        again_text = again_font.render(
            "Play Again? y/n",
            True,
            (255, 255, 255)
        )

        score = score_font.render(
            'HIGH SCORE : %s' % (self.high_score),
            False,
            (255, 255, 255)
        )

        death_text_rect = death_text.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        )

        again_text_rect = again_text.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        )

        again_text_rect.top = death_text_rect.bottom
        again_text_rect.y -= 8

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        self.update_score()
                        self.run()
                    if event.key == K_n:
                        self.update_score()
                        pygame.quit()
                        sys.exit()

            self.screen.blit(death_text, death_text_rect)
            self.screen.blit(again_text, again_text_rect)
            self.screen.blit(score, (234, 9))

            scale = pygame.transform.scale(self.screen, self.WINDOW_SIZE)
            self.window.blit(scale, (0, 0))
            pygame.display.update()
            self.clock.tick(60)

    def run(self):
        # things for dawing the worm
        SNAKE_SIZE = 8
        length = 3
        snake_x = [0]*length
        snake_y = [0]*length
        snake_pos = [0]*length
        snake_x[0] = 160
        snake_y[0] = 104
        snake_x[1] = -16
        snake_y[1] = -16
        rotation = [0]*length
        rotation[0] = 'right'
        rotation[1] = 'right'

        # things for moving the worm
        add_x = 8
        add_y = 0
        move_time = 5
        max_move_time = 5

        # things for drawing the food
        food_x = random.randint(2, 38)*8
        food_y = random.randint(2, 23)*8
        food_category = random.randint(1, 100)
        if food_category <= 75:
            food_id = random.randint(1, 3)
        else:
            food_id = 4

        # R E C T S
        segment_rect = [0]*length
        body_rects = []
        wall_rects = []
        for i in range(length-1, 1, -1):
            segment_rect[i] = pygame.Rect(
                snake_x[1],
                snake_y[1],
                SNAKE_SIZE,
                SNAKE_SIZE,
            )
            body_rects.append(segment_rect[i])
        segment_rect[0] = pygame.Rect(
            snake_x[0],
            snake_y[0],
            SNAKE_SIZE,
            SNAKE_SIZE
        )
        player_rect = segment_rect[0]
        food_rect = pygame.Rect(
            -16,
            -16,
            SNAKE_SIZE,
            SNAKE_SIZE
        )
        bogir_rect = pygame.Rect(
            -16,
            -16,
            SNAKE_SIZE,
            SNAKE_SIZE
        )
        if food_id == 4:
            bogir_rect.x = food_x
            bogir_rect.y = food_y
        else:
            food_rect.x = food_x
            food_rect.y = food_y

        # sprites
        floor = pygame.image.load(
            'data/sprites/floor.png'
        ).convert()

        # animations
        animation_database = {}
        snake_frame_durations = [5]*48  # [60fps/12fps]*frame count
        wall_frame_durations = [5]*24  # [60fps/12fps]*frame count

        animation_database['snake_head'] = self.a.load_animation(
            'data/sprites/worm-head',
            snake_frame_durations
        )

        animation_database['snake_body'] = self.a.load_animation(
            'data/sprites/worm-body',
            snake_frame_durations
        )

        animation_database['wall_corner'] = self.a.load_animation(
            'data/sprites/wall',
            wall_frame_durations
        )
        animation_database['wall_edge1'] = self.a.load_animation(
            'data/sprites/wall-top',
            wall_frame_durations
        )
        animation_database['wall_edge2'] = self.a.load_animation(
            'data/sprites/wall-left',
            wall_frame_durations
        )

        snake_frame = 0
        wall_frame = 0

        # things for recording score
        font = pygame.font.SysFont('dejavusans', 8, True)
        score = font.render(
            'YOUR SCORE : %s' % (length),
            False,
            (255, 255, 255)
        )
        # game over?
        oof = False

        # F U N C T I O N S
        def load_map(path):
            f = open(path, 'r')
            data = f.read()
            f.close()
            data = data.split('\n')
            game_map = []
            for row in data:
                game_map.append(list(row))

            return game_map

        game_map = load_map('data/map.txt')
        # print(str(game_map))

        def collision_test(rect, other_rects):
            collision_list = []

            for rects in other_rects:
                if rect.colliderect(rects):
                    collision_list.append(rects)

            return collision_list

        def update_snake_data():
            # max_move_time -= 0.5
            snake_x.append(-16)
            snake_y.append(-16)
            snake_pos.append((-16, -16))
            rotation.append(rotation[1])
            body_rects.append(
                pygame.Rect(
                    -16,
                    -16,
                    SNAKE_SIZE,
                    SNAKE_SIZE
                )
            )

        while True:
            self.screen.fill((0, 15, 20))

            snake_frame += 1
            if snake_frame >= len(animation_database['snake_head']):
                snake_frame = 0

            head_img_id = animation_database[
                'snake_head'
            ][
                snake_frame
            ]
            head_img = self.a.animation_frames[head_img_id]

            snake_img_id = animation_database[
                'snake_body'
            ][
                snake_frame
            ]
            snake_img = self.a.animation_frames[snake_img_id]

            wall_frame += 1
            # used wall_corner because all walls have same frame count
            if wall_frame >= len(animation_database['wall_corner']):
                wall_frame = 0

            wall_corner_img_id = animation_database[
                'wall_corner'
            ][
                wall_frame
            ]
            wall_corner_img = self.a.animation_frames[wall_corner_img_id]

            wall_edge1_img_id = animation_database[
                'wall_edge1'
            ][
                wall_frame
            ]
            wall_edge1_img = self.a.animation_frames[wall_edge1_img_id]

            wall_edge2_img_id = animation_database[
                'wall_edge2'
            ][
                wall_frame
            ]
            wall_edge2_img = self.a.animation_frames[wall_edge2_img_id]

            y = 0
            for row in game_map:
                x = 0
                for tile in row:
                    if tile == '1':
                        self.w.draw(
                            x*SNAKE_SIZE,
                            y*SNAKE_SIZE,
                            False,
                            wall_corner_img
                        )
                    if tile == '2':
                        self.w.draw(
                            x*SNAKE_SIZE,
                            y*SNAKE_SIZE,
                            False,
                            wall_edge1_img
                        )
                    if tile == '3':
                        self.w.draw(
                            x*SNAKE_SIZE,
                            y*SNAKE_SIZE,
                            False,
                            wall_edge2_img
                        )
                    if tile == '4':
                        self.w.draw(
                            x*SNAKE_SIZE,
                            y*SNAKE_SIZE,
                            True,
                            wall_edge2_img
                        )
                    if tile == '5':
                        self.w.draw(
                            x*SNAKE_SIZE,
                            y*SNAKE_SIZE,
                            True,
                            wall_edge1_img
                        )
                    if tile == '0':
                        self.w.draw(
                            x*SNAKE_SIZE,
                            y*SNAKE_SIZE,
                            False,
                            floor
                        )
                    if tile != '0':
                        wall_rects.append(
                            pygame.Rect(
                                x*SNAKE_SIZE,
                                y*SNAKE_SIZE,
                                SNAKE_SIZE,
                                SNAKE_SIZE
                            )
                        )

                    x += 1
                y += 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        oof = True
                    if add_x == 0:
                        if event.key == K_d or event.key == K_RIGHT:
                            add_x = SNAKE_SIZE
                            add_y = 0
                            rotation[0] = 'right'
                            move_time = max_move_time
                        if event.key == K_a or event.key == K_LEFT:
                            add_x = -SNAKE_SIZE
                            add_y = 0
                            rotation[0] = 'left'
                            move_time = max_move_time
                    if add_y == 0:
                        if event.key == K_w or event.key == K_UP:
                            add_x = 0
                            add_y = -SNAKE_SIZE
                            rotation[0] = 'up'
                            move_time = max_move_time
                        if event.key == K_s or event.key == K_DOWN:
                            add_x = 0
                            add_y = SNAKE_SIZE
                            rotation[0] = 'down'
                            move_time = max_move_time

            if player_rect.colliderect(food_rect):
                bogir_rect.x = -16
                bogir_rect.y = -16
                food_rect.x = -16
                food_rect.y = -16
                food_x = random.randint(2, 38)*8
                food_y = random.randint(2, 23)*8
                food_category = random.randint(1, 100)
                if food_category <= 75:
                    food_id = random.randint(1, 3)
                else:
                    food_id = 4
                if food_id == 4:
                    bogir_rect.x = food_x
                    bogir_rect.y = food_y
                else:
                    food_rect.x = food_x
                    food_rect.y = food_y
                update_snake_data()
                length = len(snake_pos)
                score = font.render(
                    'YOUR SCORE : %s' % (length),
                    False,
                    (255, 255, 255)
                )

            if player_rect.colliderect(bogir_rect):
                bogir_rect.x = -16
                bogir_rect.y = -16
                food_rect.x = -16
                food_rect.y = -16
                food_x = random.randint(2, 38)*8
                food_y = random.randint(2, 23)*8
                food_category = random.randint(1, 100)
                if food_category <= 75:
                    food_id = random.randint(1, 3)
                else:
                    food_id = 4
                if food_id == 4:
                    bogir_rect.x = food_x
                    bogir_rect.y = food_y
                else:
                    food_rect.x = food_x
                    food_rect.y = food_y
                update_snake_data()
                update_snake_data()
                update_snake_data()
                length = len(snake_pos)
                score = font.render(
                    'YOUR SCORE : %s' % (length),
                    False,
                    (255, 255, 255)
                )

            if length == 15:
                max_move_time = 2.5
            if length == 35:
                max_move_time = 0

            move_time += 1
            if move_time >= max_move_time:
                move_time = 0

                for i in range(length-1, 0, -1):
                    snake_x[i] = snake_x[i - 1]
                    snake_y[i] = snake_y[i - 1]
                    snake_pos[i] = (snake_x[i], snake_y[i])
                    rotation[i] = rotation[i - 1]

                snake_x[0] += add_x
                snake_y[0] += add_y
                snake_pos[0] = (snake_x[0], snake_y[0])

                for i in range(len(body_rects)):
                    body_rects[i].x = snake_pos[i + 2][0]
                    body_rects[i].y = snake_pos[i + 2][1]

            collision_list = []
            collision_list = collision_test(player_rect, body_rects)
            wall_collisions = []
            wall_collisions = collision_test(player_rect, wall_rects)
            if collision_list != [] or wall_collisions != []:
                snake_pos[0] = snake_pos[1]
                oof = True
                # print(str(collision_list))
                # print(str(wall_collisions))

            if snake_x[0] < 0:
                snake_x[0] = 39*8
            if snake_x[0] >= 40*8:
                snake_x[0] = 0
            if snake_y[0] < 0:
                snake_y[0] = 24*8
            if snake_y[0] >= 25*8:
                snake_y[0] = 0

            food_pos = (food_x, food_y)
            self.f.draw(food_pos, food_id)

            for i in range(length):
                if i != 0:
                    self.s.draw(snake_pos[i], rotation[i], snake_img)
                else:
                    self.s.draw(snake_pos[i], rotation[i], head_img)

            # for i in range(len(body_rects)):
                # pygame.draw.rect(self.screen, (255, 0, 0), body_rects[i])

            player_rect.x = snake_x[0]
            player_rect.y = snake_y[0]
            # pygame.draw.rect(self.screen, (0, 255, 0), player_rect)

            # pygame.draw.rect(self.screen, (0, 20, 5), food_rect)
            # pygame.draw.rect(self.screen, (20, 0, 5), bogir_rect)

            self.screen.blit(score, (232, 0))

            if oof:
                if length > self.high_score:
                    self.high_score = length
                self.dead()

            scale = pygame.transform.scale(self.screen, self.WINDOW_SIZE)
            self.window.blit(scale, (0, 0))
            self.clock.tick(60)
            fps = font.render(str(self.clock.get_fps()), True, (255, 255, 255))
            self.window.blit(fps, (1034, 692))
            pygame.display.update()

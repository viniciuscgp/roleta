import pygame
import math
import random
from enum import Enum

class RouletteState(Enum):
    ROTATING = 1
    ADJUSTING = 2
    STOPPED = 3

class Roulette(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, initial_power, handle_image_path=None, background_image_path=None):
        super().__init__()
        self.center = (x, y)
        self.radius = radius
        self.num_segments = 10
        self.angle_step = 360 / self.num_segments
        self.current_power = initial_power
        self.current_angle = 0
        self.state = RouletteState.ROTATING

        # Random target angle (multiple of 36 degrees)
        self.target_angle = random.randint(0, 9) * self.angle_step

        # Random number of complete circles
        self.complete_circles = random.randint(1, 3)

        # Total angle to cover
        total_angle = 360 * self.complete_circles + self.target_angle

        # Calculate deceleration to stop exactly at the target angle
        self.deceleration = initial_power**2 / (2 * total_angle)

        # Load images
        if handle_image_path:
            self.handle_image = pygame.image.load(handle_image_path).convert_alpha()
        else:
            self.handle_image = None
        
        if background_image_path:
            self.background_image = pygame.image.load(background_image_path).convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (2 * radius, 2 * radius))
        else:
            self.background_image = None

    def update(self):
        if self.state == RouletteState.ROTATING:
            self.current_angle += self.current_power
            if self.current_angle >= 360:
                self.current_angle -= 360

            # Decrease power to simulate slowing down
            self.current_power -= self.deceleration

            # Check if power has reduced to zero and adjust
            if self.current_power <= 0:
                self.current_power = 0
                self.state = RouletteState.STOPPED
                print("Stopped at angle:", self.current_angle)
                print("Stopped at number:", self.get_roulette_number(self.current_angle))

    def draw(self, surface):
        if self.background_image:
            rotated_background = pygame.transform.rotate(self.background_image, -self.current_angle)
            background_rect = rotated_background.get_rect(center=self.center)
            surface.blit(rotated_background, background_rect.topleft)

        if self.handle_image:
            handle_rect = self.handle_image.get_rect(center=self.center)
            handle_rect.x += handle_rect.w / 2.4
            surface.blit(self.handle_image, handle_rect)

    def get_final_angle(self):
        if self.state == RouletteState.STOPPED:
            return self.current_angle % 360
        return None

    def reset(self, new_power=None):
        self.current_angle = random.uniform(0, 360)
        self.state = RouletteState.ROTATING
        if new_power is not None:
            self.current_power = new_power

    def get_roulette_number(self, current_angle):
        normalized_angle = current_angle % 360
        slice_size = 360 / 10
        slice_index = math.floor(normalized_angle / slice_size)
        number = (slice_index + 1) % 10
        return number

    def adjust_to_nearest_slice(self, angle):
        normalized_angle = angle % 360
        slice_size = 360 / 10
        slice_index = round(normalized_angle / slice_size)
        adjusted_angle = slice_index * slice_size
        return adjusted_angle

import os
import sys
import math
import datetime
import pygame


class MickeyClock:
    def __init__(self):
        pygame.init()

        self.width = 600
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mickey's Clock")
        self.clock = pygame.time.Clock()

        self.center = (self.width // 2, self.height // 2)
        self.bg_color = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (220, 20, 60)
        self.skin = (245, 215, 180)

        self.hand_image = self.load_hand_image()

    def load_hand_image(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "images", "mikey_hand.png")

        if os.path.exists(image_path):
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (140, 50))
            return image

        return None

    def draw_clock_face(self):
        pygame.draw.circle(self.screen, self.black, self.center, 220, 4)

        for i in range(60):
            angle = math.radians(i * 6 - 90)

            outer_x = self.center[0] + 210 * math.cos(angle)
            outer_y = self.center[1] + 210 * math.sin(angle)

            if i % 5 == 0:
                inner_radius = 180
                line_width = 4
            else:
                inner_radius = 195
                line_width = 2

            inner_x = self.center[0] + inner_radius * math.cos(angle)
            inner_y = self.center[1] + inner_radius * math.sin(angle)

            pygame.draw.line(
                self.screen,
                self.black,
                (inner_x, inner_y),
                (outer_x, outer_y),
                line_width
            )

        pygame.draw.circle(self.screen, self.black, self.center, 8)

    def rotate_hand_image(self, image, angle, scale=1.0):
        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)
        scaled = pygame.transform.scale(image, (width, height))
        rotated = pygame.transform.rotate(scaled, -angle)
        rect = rotated.get_rect(center=self.center)
        return rotated, rect

    def draw_simple_hand(self, angle, length, width):
        rad = math.radians(angle - 90)
        end_x = self.center[0] + length * math.cos(rad)
        end_y = self.center[1] + length * math.sin(rad)

        pygame.draw.line(self.screen, self.black, self.center, (end_x, end_y), width)
        pygame.draw.circle(self.screen, self.skin, self.center, 12)
        pygame.draw.circle(self.screen, self.skin, (int(end_x), int(end_y)), 10)

    def draw_hands(self):
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        minute_angle = minutes * 6
        second_angle = seconds * 6

        if self.hand_image:
            minute_img, minute_rect = self.rotate_hand_image(self.hand_image, minute_angle, 1.0)
            second_img, second_rect = self.rotate_hand_image(self.hand_image, second_angle, 0.8)

            self.screen.blit(minute_img, minute_rect)
            self.screen.blit(second_img, second_rect)
        else:
            self.draw_simple_hand(minute_angle, 90, 7)
            self.draw_simple_hand(second_angle, 120, 5)

        font = pygame.font.SysFont("Arial", 30)
        time_text = font.render(f"{minutes:02d}:{seconds:02d}", True, self.red)
        text_rect = time_text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(time_text, text_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(self.bg_color)
            self.draw_clock_face()
            self.draw_hands()

            pygame.display.flip()
            self.clock.tick(1)
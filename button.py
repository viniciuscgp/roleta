import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, bg_color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action  # This will be the lambda or any callable

    def draw(self, surface):
        # Draw the button rectangle
        pygame.draw.rect(surface, self.bg_color, self.rect)

        # Render the text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

import pygame

FONT_PATH = 'src/pygrain/Vogue.ttf'


def show_text(screen, text, centre_x, centre_y, font_colour=(0, 0, 0),
              font_bg=(255, 255, 255), font_size=10):
    # initialises font for displaying text
    try:
        for line in text.split('\n'):
            basic_font = pygame.font.Font(FONT_PATH, font_size)
            text = basic_font.render(text, True, font_colour, font_bg)
            text_rect = text.get_rect()
            text_rect.center = (centre_x, centre_y)  #
            screen.blit(text, text_rect)  # Shows text on self.screen
    finally:
        pass


def show_image(screen, path, x, y):
    image = pygame.image.load(path).convert()
    screen.blit(image, (x, y))

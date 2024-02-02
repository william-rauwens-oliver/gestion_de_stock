# Stock_management_app.py
import pygame
from pygame.locals import *
from pygame.transform import scale
import mysql.connector
from tkinter import simpledialog, messagebox
from Product import ProductManagement
from Category import CategoryManagement

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class StockManagementApp:
    def __init__(self):
        # Connexion à la base de données
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="willy",
            database="store",
        )
        self.cursor = self.connection.cursor()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gestion de Stock")
        self.clock = pygame.time.Clock()

        # Charge l'image du fond d'écran et redimensionne-la
        self.background_img = scale(pygame.image.load('photos/fond.webp'), (WINDOW_WIDTH, WINDOW_HEIGHT))

        self.product_management = ProductManagement(self)
        self.category_management = CategoryManagement(self)
        self.create_widgets()

    def create_widgets(self):
        button_x, button_y = 650, 50
        running = True
        while running:
            self.screen.fill(WHITE)

            # Blitte l'image du fond d'écran
            self.screen.blit(self.background_img, (0, 0))

            self.product_management.show_products()
            self.category_management.show_categories()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_x < mouse_x < button_x + 100:
                        if button_y < mouse_y < button_y + 40:
                            self.product_management.add_product()
                        elif button_y + 100 < mouse_y < button_y + 140:
                            self.product_management.delete_product()
                        elif button_y + 200 < mouse_y < button_y + 240:
                            self.product_management.update_product()
                    else:
                        self.product_management.handle_product_click(mouse_y)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
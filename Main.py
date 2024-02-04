import pygame
from pygame.locals import *
from pygame.transform import scale
import csv
import mysql.connector
from tkinter import simpledialog, messagebox
from Category import Category
from Product import Product

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
WHITE = (255, 255, 255)

class StockManagementApp:
    def __init__(self):
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

        self.background_img = scale(pygame.image.load('photos/fond.webp'), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.category_instance = Category(self.connection, self.cursor)
        self.product_instance = Product(self.connection, self.cursor, self.screen, self.clock)

        self.create_widgets()

    def create_widgets(self):
        button_x, button_y = 650, 50
        running = True
        while running:
            self.screen.fill(WHITE)
            self.screen.blit(self.background_img, (0, 0))

            self.product_instance.show_products()
            self.screen.blit(self.product_instance.add_button_img, (button_x, button_y))
            self.screen.blit(self.product_instance.delete_button_img, (button_x, button_y + 100))
            self.screen.blit(self.product_instance.update_button_img, (button_x, button_y + 200))
            self.screen.blit(self.product_instance.export_button_img, (button_x, button_y + 300))

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_x < mouse_x < button_x + 100:
                        if button_y < mouse_y < button_y + 40:
                            self.product_instance.add_product()
                        elif button_y + 100 < mouse_y < button_y + 140:
                            self.product_instance.delete_product()
                        elif button_y + 200 < mouse_y < button_y + 240:
                            self.product_instance.update_product()
                        elif button_y + 300 < mouse_y < button_y + 340:
                            self.product_instance.export_to_csv()
                    else:
                        self.product_instance.handle_product_click(mouse_y)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
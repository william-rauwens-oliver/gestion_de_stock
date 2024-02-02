import pygame
import mysql.connector
from pygame.locals import *

pygame.init()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="willy",
    database="store",
)

cursor = db.cursor()

# Vérifier si la catégorie existe, sinon l'insérer
cursor.execute("INSERT INTO category (name) VALUES ('Électronique') ON DUPLICATE KEY UPDATE id=id")
cursor.execute("INSERT INTO category (name) VALUES ('Vêtements') ON DUPLICATE KEY UPDATE id=id")
cursor.execute("INSERT INTO category (name) VALUES ('Alimentation') ON DUPLICATE KEY UPDATE id=id")
db.commit()

# Vérifier si les produits existent, sinon les insérer
product_data = [
    ("Chaussure", "Air Jordan 1 Mid", 1200, 10, 1),
    ("Jogging", "Nike Sportswear Club", 20, 50, 2),
    ("Veste Nike", "Nike Sportswear Tech Fleece Windrunner", 2, 100, 3)
]

for data in product_data:
    product_name = data[0]
    cursor.execute("SELECT id FROM product WHERE name = %s", (product_name,))
    existing_product = cursor.fetchone()

    if not existing_product:
        # Si le produit n'existe pas, alors l'insérer
        cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)", data)
        db.commit()

def get_products():
    cursor.execute("SELECT * FROM product")
    return cursor.fetchall()

def add_product(name, description, price, quantity, category_id):
    cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)",
                   (name, description, price, quantity, category_id))
    db.commit()

def delete_products(product_ids):
    for product_id in product_ids:
        cursor.execute("DELETE FROM product WHERE id=%s", (product_id,))
    db.commit()

def update_product(product_id, quantity, price):
    cursor.execute("UPDATE product SET quantity=%s, price=%s WHERE id=%s", (quantity, price, product_id))
    db.commit()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gestion de Stock")

font = pygame.font.Font(None, 36)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_button(x, y, width, height, color, text, action=None):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 24)
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + width // 2 - button_text.get_width() // 2, y + height // 2 - button_text.get_height() // 2))

def draw_quantity_buttons(x, y, product_id):
    draw_button(x, y, 30, 30, (0, 255, 0), "+", action=lambda: update_quantity(product_id, 1))
    draw_button(x + 40, y, 30, 30, (255, 0, 0), "-", action=lambda: update_quantity(product_id, -1))

def update_quantity(product_id, delta):
    cursor.execute("SELECT quantity FROM product WHERE id=%s", (product_id,))
    current_quantity = cursor.fetchone()[0]
    new_quantity = max(0, current_quantity + delta)
    cursor.execute("UPDATE product SET quantity=%s WHERE id=%s", (new_quantity, product_id))
    db.commit()

# Fonction pour afficher un message
def show_message(message):
    text = font.render(message, True, BLACK)
    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Affiche le message pendant 2 secondes

# Fonction pour obtenir une entrée utilisateur
def get_user_input(screen, font, x, y, prompt):
    input_text = ""
    input_box = pygame.Rect(x, y, 200, 30)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = font.render(prompt, True, color)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            elif event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        return input_text
                    elif event.key == K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                if event.key == K_TAB:
                    active = not active
                    color = color_active if active else color_inactive

        screen.fill(WHITE)
        pygame.draw.rect(screen, color, input_box, 2)
        width = max(200, text.get_width() + 10)
        input_box.w = width
        screen.blit(text, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            # Ajouter une fenêtre pour l'ajout de produit
            if 600 < x < 750 and 50 < y < 80:
                add_product_screen()

    screen.fill(WHITE)

    products = get_products()
    y_offset = 50
    for product in products:
        text = font.render(f"ID: {product[0]} - {product[1]} - Prix: {product[3]} - Quantité: {product[4]}", True, BLACK)
        screen.blit(text, (50, y_offset))

        # Dessiner les boutons "+" et "-"
        draw_quantity_buttons(700, y_offset, product[0])

        y_offset += 40

    pygame.display.flip()

cursor.close()
db.close()

pygame.quit()

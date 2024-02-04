import pygame
from pygame.locals import *
from pygame.transform import scale
import csv
import mysql.connector
from tkinter import simpledialog, messagebox

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

        # Ajout des images des boutons
        self.add_button_img = scale(pygame.image.load('photos/add.png'), (50, 50))
        self.delete_button_img = scale(pygame.image.load('photos/delete.webp'), (50, 50))
        self.update_button_img = scale(pygame.image.load('photos/update_button.png'), (50, 50))
        self.export_button_img = scale(pygame.image.load('photos/csv.png'), (50, 50))

        self.create_widgets()

    def create_widgets(self):
        button_x, button_y = 650, 50
        running = True
        while running:
            self.screen.fill(WHITE)
            
            # Blitte l'image du fond d'écran
            self.screen.blit(self.background_img, (0, 0))

            self.show_products()
            self.screen.blit(self.add_button_img, (button_x, button_y))
            self.screen.blit(self.delete_button_img, (button_x, button_y + 100))
            self.screen.blit(self.update_button_img, (button_x, button_y + 200))
            self.screen.blit(self.export_button_img, (button_x, button_y + 300))

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if button_x < mouse_x < button_x + 100:
                        if button_y < mouse_y < button_y + 40:
                            self.add_product()
                        elif button_y + 100 < mouse_y < button_y + 140:
                            self.delete_product()
                        elif button_y + 200 < mouse_y < button_y + 240:
                            self.update_product()
                        elif button_y + 300 < mouse_y < button_y + 340:
                            self.export_to_csv()
                    else:
                        self.handle_product_click(mouse_y)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def show_products(self, products=None):
        products = products or self.get_products()
        for i, product in enumerate(products):
            product_text = f"{product[1]} - {product[2]} - {product[3]}$ - {product[4]} unités"
            font = pygame.font.Font(None, 36)

            # Texte principal (sans ombre)
            text = font.render(product_text, True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (50, 50 + i * 40)
            self.screen.blit(text, text_rect)

            # Ombre du texte (décalé de 2 pixels vers le bas et la droite, couleur noire)
            shadow_text = font.render(product_text, True, BLACK)
            shadow_rect = shadow_text.get_rect()
            shadow_rect.topleft = (51, 51 + i * 40)
            self.screen.blit(shadow_text, shadow_rect)

    def handle_product_click(self, mouse_y):
        product_index = (mouse_y - 50) // 40
        if 0 <= product_index < len(self.get_products()):
            product_id = self.get_products()[product_index][0]
            choice = simpledialog.askstring("Gérer Produit", "Choisissez l'action:\n- Supprimer\n- Mettre à jour")
            if choice:
                choice = choice.lower()
                if choice == "supprimer":
                    self.delete_product_by_id(product_id)
                elif choice == "mettre à jour":
                    self.update_product_by_id(product_id)
                else:
                    messagebox.showwarning("Avertissement", "Choix invalide. Veuillez choisir 'Supprimer' ou 'Mettre à jour'.")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne d'article valide.")

    def add_product(self):
        name = simpledialog.askstring("Ajouter Produit", "Nom du Produit:")
        description = simpledialog.askstring("Ajouter Produit", "Description:")
        price = simpledialog.askfloat("Ajouter Produit", "Prix:")
        quantity = simpledialog.askinteger("Ajouter Produit", "Quantité:")
        category = simpledialog.askstring("Ajouter Produit", "Catégorie:")

        if name and price and quantity and category:
            try:
                self.cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) "
                                    "VALUES (%s, %s, %s, %s, (SELECT id FROM category WHERE name = %s))",
                                    (name, description, price, quantity, category))
                self.connection.commit()
                messagebox.showinfo("Succès", "Produit ajouté avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du produit : {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs.")

    def delete_product(self):
        selected_product = pygame.mouse.get_pos()
        product_index = (selected_product[1] - 50) // 40
        if 0 <= product_index < len(self.get_products()):
            product_id = self.get_products()[product_index][0]
            self.delete_product_by_id(product_id)
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne d'article valide.")

    def update_product(self):
        selected_product = pygame.mouse.get_pos()
        product_index = (selected_product[1] - 50) // 40
        if 0 <= product_index < len(self.get_products()):
            product_id = self.get_products()[product_index][0]
            self.update_product_by_id(product_id)
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne d'article valide.")

    def delete_product_by_id(self, product_id):
        try:
            self.cursor.execute("DELETE FROM product WHERE id=%s", (product_id,))
            self.connection.commit()
            messagebox.showinfo("Succès", "Produit supprimé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit : {str(e)}")

    def update_product_by_id(self, product_id):
        new_quantity = simpledialog.askinteger("Modifier Produit", "Nouvelle quantité:")
        if new_quantity is not None:
            try:
                self.cursor.execute("UPDATE product SET quantity=%s WHERE id=%s", (new_quantity, product_id))
                self.connection.commit()
                messagebox.showinfo("Succès", "Produit mis à jour avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du produit : {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer une nouvelle quantité valide.")

    def export_to_csv(self):
        products = self.get_products()
        file_path = "stock.csv"

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Nom", "Description", "Prix", "Quantité", "Catégorie"])

            for product in products:
                writer.writerow(product)

        messagebox.showinfo("Export CSV", f"Les produits ont été exportés avec succès sous {file_path}")

    def get_products(self):
        self.cursor.execute("SELECT * FROM product")
        return self.cursor.fetchall()

    def get_categories(self):
        self.cursor.execute("SELECT name FROM category")
        return [category[0] for category in self.cursor.fetchall()]

if __name__ == "__main__":
    app = StockManagementApp()

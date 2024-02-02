import pygame
from pygame.locals import *
from pygame.transform import scale 
import mysql.connector
from tkinter import simpledialog, messagebox

# Initialiser Pygame
pygame.init()

# Taille de la fenêtre
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

# Couleurs
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

        # Initialiser Pygame
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Gestion de Stock")

        # Interface graphique
        self.clock = pygame.time.Clock()
        self.create_widgets()

    def create_widgets(self):
        # Chargement des images pour les boutons, redimensionnées à 50x50 pixels
        self.add_button_img = scale(pygame.image.load('photos/add.png'), (50, 50))
        self.delete_button_img = scale(pygame.image.load('photos/delete.webp'), (50, 50))
        self.update_button_img = scale(pygame.image.load('photos/update_button.png'), (50, 50))

        # Position des boutons
        button_x, button_y = 650, 50

        # Boucle principale
        running = True
        while running:
            self.screen.fill(WHITE)

            # Afficher les produits
            self.show_products()

            # Afficher les boutons
            self.screen.blit(self.add_button_img, (button_x, button_y))
            self.screen.blit(self.delete_button_img, (button_x, button_y + 100))
            self.screen.blit(self.update_button_img, (button_x, button_y + 200))

            # Gérer les événements
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

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def show_products(self):
        # Afficher la liste des produits
        products_text = []
        self.cursor.execute("SELECT * FROM product")
        products = self.cursor.fetchall()
        for i, product in enumerate(products):
            product_text = f"{product[1]} - {product[2]} - {product[3]}$ - {product[4]} unités"
            products_text.append(product_text)
            font = pygame.font.Font(None, 36)
            text = font.render(product_text, True, BLACK)
            self.screen.blit(text, (50, 50 + i * 40))

    def add_product(self):
        # Ajouter un produit
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
        # Supprimer un produit
        selected_product = pygame.mouse.get_pos()
        product_index = (selected_product[1] - 50) // 40
        if 0 <= product_index < len(self.get_products()):
            product_id = self.get_products()[product_index][0]
            try:
                self.cursor.execute("DELETE FROM product WHERE id=%s", (product_id,))
                self.connection.commit()
                messagebox.showinfo("Succès", "Produit supprimé avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit : {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à supprimer.")

    def update_product(self):
        # Mettre à jour la quantité d'un produit
        selected_product = pygame.mouse.get_pos()
        product_index = (selected_product[1] - 50) // 40
        if 0 <= product_index < len(self.get_products()):
            product_id = self.get_products()[product_index][0]
            new_quantity = simpledialog.askinteger("Modifier Produit", "Nouvelle quantité:")
            if new_quantity is not None:
                try:
                    self.cursor.execute("UPDATE product SET quantity=%s WHERE id=%s", (new_quantity, product_id))
                    self.connection.commit()
                    messagebox.showinfo("Succès", "Produit mis à jour avec succès.")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du produit : {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un produit à mettre à jour.")

    def get_products(self):
        # Récupérer la liste des produits
        self.cursor.execute("SELECT * FROM product")
        return self.cursor.fetchall()


if __name__ == "__main__":
    app = StockManagementApp()

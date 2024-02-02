# product.py
import pygame
from pygame.locals import *
from pygame.transform import scale
from tkinter import simpledialog, messagebox

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class ProductManagement:
    def __init__(self, app_instance):
        self.app = app_instance

    def show_products(self):
        products_text = []
        self.app.cursor.execute("SELECT * FROM product")
        products = self.app.cursor.fetchall()
        for i, product in enumerate(products):
            product_text = f"{product[1]} - {product[2]} - {product[3]}$ - {product[4]} unités"
            products_text.append(product_text)
            font = pygame.font.Font(None, 36)

            # Crée une surface de texte
            text = font.render(product_text, True, WHITE)
            text_rect = text.get_rect()
            text_rect.topleft = (50, 50 + i * 40)

            # Crée une copie du texte avec l'effet d'ombre
            shadow_text = font.render(product_text, True, BLACK)
            shadow_rect = shadow_text.get_rect()
            shadow_rect.topleft = (52, 52 + i * 40)

            # Blitte le texte avec l'effet d'ombre
            self.app.screen.blit(shadow_text, shadow_rect)

            # Blitte le texte principal
            self.app.screen.blit(text, text_rect)

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
                self.app.cursor.execute("INSERT INTO product (name, description, price, quantity, id_category) "
                                        "VALUES (%s, %s, %s, %s, (SELECT id FROM category WHERE name = %s))",
                                        (name, description, price, quantity, category))
                self.app.connection.commit()
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
            self.app.cursor.execute("DELETE FROM product WHERE id=%s", (product_id,))
            self.app.connection.commit()
            messagebox.showinfo("Succès", "Produit supprimé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression du produit : {str(e)}")

    def update_product_by_id(self, product_id):
        new_quantity = simpledialog.askinteger("Modifier Produit", "Nouvelle quantité:")
        if new_quantity is not None:
            try:
                self.app.cursor.execute("UPDATE product SET quantity=%s WHERE id=%s", (new_quantity, product_id))
                self.app.connection.commit()
                messagebox.showinfo("Succès", "Produit mis à jour avec succès.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du produit : {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer une nouvelle quantité valide.")

    def get_products(self):
        self.app.cursor.execute("SELECT * FROM product")
        return self.app.cursor.fetchall()

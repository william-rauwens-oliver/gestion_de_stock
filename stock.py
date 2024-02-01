import mysql.connector
import pygame

mydb = mysql.connector.connect(
host = "localhost",
user = "root",
password = "willy",
database = "LaPlateforme",
)

pygame.init()

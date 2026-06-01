import pygame
import sys
import math
pygame.init()
pygame.font.init()
import Constantes

ANCHO = 1100
ALTO = 800

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Over Cook Tec")
fondo1 = pygame.image.load("fondo1.png")
fondo1 = pygame.transform.scale(fondo1, (ANCHO, ALTO))

def pantalla_nivel_1():
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(Constantes.BLANCO)
    while True:
        ventana.blit(fondo, (0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return  # volver a pantalla de niveles

        pygame.display.update()


def pantalla_nivel_2():
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(Constantes.BLANCO)
    while True:
        ventana.blit(fondo, (0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return  # volver a pantalla de niveles

        pygame.display.update()

def pantalla_nivel_3():
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(Constantes.BLANCO)
    while True:
        ventana.blit(fondo, (0, 0))
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return  # volver a pantalla de niveles

        pygame.display.update()


def pantalla_niveles():
    titulo=Constantes.fuente_bonita_grande.render("Selecciona un nivel", True, Constantes.NEGRO)
    dificil_txt=Constantes.fuente_bonita_pequeña.render("Difícil",True,Constantes.NEGRO)
    medio_txt=Constantes.fuente_bonita_pequeña.render("Medio",True,Constantes.NEGRO)
    facil_txt=Constantes.fuente_bonita_pequeña.render("Fácil",True,Constantes.NEGRO)
    botones = [
        {"rect": pygame.Rect(ANCHO//2 - 500, ALTO//2 + 30, 200, 80), "texto": "Nivel 1", "icono": "icono_nivel1.png"},
        {"rect": pygame.Rect(ANCHO//2 -100, ALTO//2 + 30, 200, 80), "texto": "Nivel 2", "icono": "icono_nivel2.png"},
        {"rect": pygame.Rect(ANCHO//2 + 300, ALTO//2 + 30, 200, 80), "texto": "Nivel 3", "icono": "icono_nivel3.png"},
    ]

    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(Constantes.BLANCO)

    while True:
        ventana.blit(fondo, (0, 0))
        ventana.blit(titulo, (ANCHO//2-250, 50))
        ventana.blit(dificil_txt,(ANCHO//2 + 340, ALTO//2 - 210))
        ventana.blit(medio_txt,(ANCHO//2 -50, ALTO//2 - 210))
        ventana.blit(facil_txt,(ANCHO//2 - 450, ALTO//2 - 210))
        mouse_pos = pygame.mouse.get_pos()


        #Crear los botones
        for boton in botones:
            color = Constantes.NARANJA if boton["rect"].collidepoint(mouse_pos) else Constantes.AMARILLO
            pygame.draw.rect(ventana, color, boton["rect"])
            texto = Constantes.fuente_bonita.render(boton["texto"], True, Constantes.BLANCO)
            ventana.blit(texto, (boton["rect"].x + 20, boton["rect"].y + 20))

            # Mostrar icono encima del botón
            icono_img = pygame.image.load(boton["icono"])
            icono_img = pygame.transform.scale(icono_img, (170, 170))
            ventana.blit(icono_img, (boton["rect"].x + 20, boton["rect"].y -200))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for boton in botones:
                    if boton["rect"].collidepoint(evento.pos):
                        if boton["texto"] == "Nivel 1":
                            pantalla_nivel_1()
                        elif boton["texto"] == "Nivel 2":
                            pantalla_nivel_2()
                        elif boton["texto"] == "Nivel 3":
                            pantalla_nivel_3()

        pygame.display.update()
# Función pantalla inicial
def pantalla_inicial():
    # Crear botón
    boton_rect = pygame.Rect(ANCHO//2 - 110, ALTO//2 +100, 230, 80)  # centrado
    texto_boton = Constantes.fuente_bonita.render("Comenzar", True, Constantes.BLANCO)

    while True:
        ventana.blit(fondo1, (0, 0))  # dibujar fondo

        # Dibujar botón
        mouse_pos = pygame.mouse.get_pos()
        if boton_rect.collidepoint(mouse_pos):
            color_boton = Constantes.AZUL_CLARO  # hover
        else:
            color_boton = Constantes.AZUL

        pygame.draw.rect(ventana, color_boton, boton_rect)
        ventana.blit(texto_boton, (boton_rect.x + 20, boton_rect.y + 20))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    pantalla_niveles()

        pygame.display.update()

pantalla_inicial()
pygame.quit()




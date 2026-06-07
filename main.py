import pygame
import sys
from Clases import (
    Chef, Cocina,
    EstacionDespensa, EstacionEntrega, Estacion,
    Proteina, VegetalesYFrutas, PanesYBases
)
from mundo import Mundo

pygame.init()
pygame.font.init()
import Constantes
ANCHO = 1100
ALTO  = 800

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Over Cook Tec")

fondo1 = pygame.image.load("fondo1.png")
fondo1 = pygame.transform.scale(fondo1, (ANCHO, ALTO))

clock = pygame.time.Clock()

"""
Video de 6 horas
"""
tile_list = []
for x in range(125):
    tile_image = pygame.image.load(f"/tileset/tile{x+1}.png")
    tile_image = pygame.transform.scale(tile_image, 60)
    tile_list.append(tile_image)

world_data = [
    [1,1,1,1,1,1,1]

]
world = Mundo()
world.process_data(world_data, )

def dibujar_grid():
    for x in range (30):
        pygame.draw.line(ventana, Constantes.BLANCO, start_pos=(x*60, 0), end_pos=(x*60, ALTO))
        pygame.draw.line(ventana, Constantes.BLANCO, start_pos=(0, x*60), end_pos=(ANCHO, x*60))

# ─────────────────────────────────────────────
#  NIVEL 1  –  usa las clases Chef y Cocina
# ─────────────────────────────────────────────
def pantalla_nivel_1():

    # ── Crear cocina ──────────────────────────
    cocina = Cocina(tiempo_total=120, nivel="nivel1")

    # ── Crear chefs: ambos se mueven simultáneamente ──
    # teclas = (arriba, abajo, izquierda, derecha)
    chef1 = Chef(
        nombre="Chef 1",
        imagen_path="gato.png",
        x=200, y=300,
        teclas=(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
        velocidad=3
    )

    chef2 = Chef(
        nombre="Chef 2",
        imagen_path="gato2.png",
        x=400, y=300,
        teclas=(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT),
        velocidad=3
    )

    cocina.agregar_chef(chef1)
    cocina.agregar_chef(chef2)




    # ── Fuente HUD ────────────────────────────
    fuente = pygame.font.SysFont("Arial", 22)

    run = True
    while run:
        delta = clock.tick(60) / 1000.0     # segundos desde el último frame

        # ── Eventos ───────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # ── Movimiento: ambos chefs se mueven a la vez ──
        keys = pygame.key.get_pressed()
        for chef in cocina.chefs:
            chef.mover(keys, ANCHO, ALTO)

        # ── Actualizar lógica ─────────────────
        cocina.actualizar(delta)

        # ── Fin de tiempo ─────────────────────
        if cocina.tiempo <= 0:
            run = False

        # ── Dibujar ───────────────────────────
        ventana.fill((30, 30, 30))
        cocina.dibujar(ventana)
        world.draw(ventana)
        dibujar_grid()

        # HUD: tiempo y puntos
        tiempo_txt = fuente.render(f"Tiempo: {max(0, int(cocina.tiempo))}s", True, (255, 255, 255))
        pts1_txt   = fuente.render(f"Chef 1 : {chef1.puntos} pts", True, (200, 230, 255))
        pts2_txt   = fuente.render(f"Chef 2 : {chef2.puntos} pts", True, (255, 230, 180))

        ventana.blit(tiempo_txt, (20, 20))
        ventana.blit(pts1_txt,   (20, 50))
        ventana.blit(pts2_txt,   (20, 75))

        # HUD: órdenes activas
        y_orden = 105
        ventana.blit(fuente.render("Recetas", True, (255, 255, 100)), (20, y_orden))
        for orden in cocina.ordenes:
            y_orden += 22
            txt = fuente.render(
                f"  {orden.nombre}  {orden.puntos_receta}pts  {int(orden.max_time_receta - orden.tiempo_transcurrido)}s",
                True, (255, 200, 100)
            )
            ventana.blit(txt, (20, y_orden))

        pygame.display.update()


# ─────────────────────────────────────────────
#  NIVELES 2 Y 3  (sin cambios)
# ─────────────────────────────────────────────
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
                return
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
                return
        pygame.display.update()


# ─────────────────────────────────────────────
#  MENÚ DE NIVELES
# ─────────────────────────────────────────────
def pantalla_niveles():
    titulo     = Constantes.fuente_bonita_grande.render("Selecciona un nivel", True, Constantes.NEGRO)
    dificil_txt= Constantes.fuente_bonita_pequeña.render("Difícil", True, Constantes.NEGRO)
    medio_txt  = Constantes.fuente_bonita_pequeña.render("Medio",   True, Constantes.NEGRO)
    facil_txt  = Constantes.fuente_bonita_pequeña.render("Fácil",   True, Constantes.NEGRO)

    botones = [
        {"rect": pygame.Rect(ANCHO//2 - 500, ALTO//2 + 30, 200, 80), "texto": "Nivel 1", "icono": "icono_nivel1.png"},
        {"rect": pygame.Rect(ANCHO//2 - 100, ALTO//2 + 30, 200, 80), "texto": "Nivel 2", "icono": "icono_nivel2.png"},
        {"rect": pygame.Rect(ANCHO//2 + 300, ALTO//2 + 30, 200, 80), "texto": "Nivel 3", "icono": "icono_nivel3.png"},
    ]

    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(Constantes.BLANCO)

    while True:
        ventana.blit(fondo, (0, 0))
        ventana.blit(titulo,      (ANCHO//2 - 250, 50))
        ventana.blit(dificil_txt, (ANCHO//2 + 340, ALTO//2 - 210))
        ventana.blit(medio_txt,   (ANCHO//2 -  50, ALTO//2 - 210))
        ventana.blit(facil_txt,   (ANCHO//2 - 450, ALTO//2 - 210))

        mouse_pos = pygame.mouse.get_pos()
        for boton in botones:
            color = Constantes.NARANJA if boton["rect"].collidepoint(mouse_pos) else Constantes.AMARILLO
            pygame.draw.rect(ventana, color, boton["rect"])
            texto = Constantes.fuente_bonita.render(boton["texto"], True, Constantes.BLANCO)
            ventana.blit(texto, (boton["rect"].x + 20, boton["rect"].y + 20))
            icono_img = pygame.image.load(boton["icono"])
            icono_img = pygame.transform.scale(icono_img, (170, 170))
            ventana.blit(icono_img, (boton["rect"].x + 20, boton["rect"].y - 200))

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



# ─────────────────────────────────────────────
#  PANTALLA INICIAL
# ─────────────────────────────────────────────
def pantalla_inicial():
    boton_rect  = pygame.Rect(ANCHO//2 - 110, ALTO//2 + 100, 230, 80)
    texto_boton = Constantes.fuente_bonita.render("Comenzar", True, Constantes.BLANCO)

    while True:
        ventana.blit(fondo1, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        color_boton = Constantes.AZUL_CLARO if boton_rect.collidepoint(mouse_pos) else Constantes.AZUL
        pygame.draw.rect(ventana, color_boton, boton_rect)
        ventana.blit(texto_boton, (boton_rect.x + 20, boton_rect.y + 20))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    pantalla_niveles()

        pygame.display.update()



pantalla_inicial()
pygame.quit()

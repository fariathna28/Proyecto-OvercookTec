import pygame
import sys





pygame.init()
pygame.font.init()
import Constantes

from mundo import Mundo
from Clases import (
    Chef, Cocina,
    EstacionDespensa, EstacionEntrega, Estacion,
    Proteina, VegetalesYFrutas, PanesYBases, Plato
)


ANCHO = 1200
ALTO  = 750
Constantes.fuente_basica = pygame.font.SysFont("impact", 20)
Constantes.fuente_bonita = pygame.font.SysFont("Mocha Choco", 36, bold=True)
Constantes.fuente_bonita_grande = pygame.font.SysFont("Mocha Choco", 50)
Constantes.fuente_bonita_pequeña = pygame.font.SysFont("Mocha Choco", 28)

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Over Cook Tec")

fondo1 = pygame.image.load("Imagenes/fondo1.png")
fondo1 = pygame.transform.scale(fondo1, (ANCHO, ALTO))

clock = pygame.time.Clock()

"""
Video de 6 horas
"""
tile_list = []
for x in range(63):
    tile_image = pygame.image.load(f"tileset/tile{x+1}.png")
    tile_image = pygame.transform.scale(tile_image, size=(Constantes.TILE_SIZE, Constantes.TILE_SIZE))
    tile_list.append(tile_image)

world_data = [
    [0,0,9,0,0,5,0,0],
    [45,1,2,0,2,1,2,6],
    [0,2,1,36,1,2,1,0],
    [3,1,2,1,2,0,2,0],
    [0,0,4,0,18,0,27,0],

]

world = Mundo()
world.process_data(world_data, tile_list, "nivel2")
for tile in world.map_tiles:
    print(tile[1].x, tile[1].y) 


def dibujar_grid():
    for x in range (30):
        pygame.draw.line(ventana, Constantes.BLANCO, start_pos=(x*Constantes.TILE_SIZE, 0), end_pos=(x*Constantes.TILE_SIZE, ALTO))
        pygame.draw.line(ventana, Constantes.BLANCO, start_pos=(0, x*Constantes.TILE_SIZE), end_pos=(ANCHO, x*Constantes.TILE_SIZE))

# ─────────────────────────────────────────────
#  NIVEL 1  –  usa las clases Chef y Cocina
# ─────────────────────────────────────────────
def pantalla_nivel_2():
    mesa_tiles1 = {
        "Carne": 16,
        "Carne_cocinada": 15,
        "Tomate": 25,
        "Tomate_cut": 26,
        "Pan" : 24,
        "Papa": 22,
        "Papa_cocinada": 23,
        "Plato": 36,
        "plato_pan": 34,
        "plato_papa": 35,
        "plato_pan_carne": 41,
        "plato_pan_carne2": 40,
        "plato_pan_carne_tomate": 39,
        "plato_pan_carne_tomate_papa": 38
    }
    mesa_ingredientes = {
    "mesa_Carne_cruda": lambda: Proteina("Carne"),
    "mesa_Tomate_cruda": lambda: VegetalesYFrutas("Tomate"),
    "mesa_Pan_cruda": lambda: PanesYBases("Pan"),
    "mesa_Papa_cruda": lambda: VegetalesYFrutas("Papa"),
    # los platos y cocinados los agregas después según tu lógica
    }

    # ── Crear cocina ──────────────────────────
    cocina = Cocina(tiempo_total=120, nivel="nivel2")

    # ── Crear chefs: ambos se mueven simultáneamente ──
    # teclas = (arriba, abajo, izquierda, derecha)
    chef1 = Chef(
        nombre="Chef 1",
        imagen_path="Imagenes/gato.png",
        x=200, y=300,
        teclas=(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_e),
        velocidad=3
    )

    chef2 = Chef(
        nombre="Chef 2",
        imagen_path="Imagenes/gato2.png",
        x=400, y=300,
        teclas=(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP0),
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
                
                for chef in cocina.chefs:
                    if event.key == chef.teclas[4]:
                        tipo = chef.agarrar(world.estaciones_tiles)

                        if chef.ingrediente_mano is None:
                            if tipo == "estacion_carne":
                                chef.ingrediente_mano = Proteina("Carne")
                            elif tipo == "estacion_pan":    
                                chef.ingrediente_mano = PanesYBases("Pan")
                            elif tipo == "estacion_tomates":    
                                chef.ingrediente_mano = VegetalesYFrutas("Tomate")
                            elif tipo == "estacion_papas":      
                                chef.ingrediente_mano = VegetalesYFrutas("Papa")
                            elif tipo == "estacion_platos":      
                                chef.ingrediente_mano = Plato()
                            elif tipo in mesa_ingredientes:
                                for tile_data in world.map_tiles:
                                    if tile_data[1].colliderect(chef.rect) and tile_data[4] != 0 and tile_data[4] != 1 and tile_data[4] != 2:
                                        tile_data[0] = tile_list[0]
                                        tile_data[4] = 0
                                        break
                                world.actualizar_estaciones("nivel2")
                                chef.ingrediente_mano = mesa_ingredientes[tipo]()


                        elif chef.ingrediente_mano is not None:
                            if tipo == "cocina":
                                if isinstance(chef.ingrediente_mano, Proteina):
                                    chef.esta_procesando = True
                            elif tipo == "freidor":
                                if isinstance(chef.ingrediente_mano, (Proteina, VegetalesYFrutas)):
                                    chef.esta_procesando = True
                            elif tipo == "tabla_picar":
                                if isinstance(chef.ingrediente_mano, VegetalesYFrutas):
                                    chef.esta_procesando = True
                            elif tipo == "entrega":
                                chef.ingrediente_mano = None

                            
                            elif tipo == "mesa":
                                if chef.ingrediente_mano and chef.ingrediente_mano.nombre in mesa_tiles1:
                                    for tile_data in world.map_tiles:
                                        if tile_data[1].colliderect(chef.rect) and tile_data[4] == 0:
                                            indice = mesa_tiles1[chef.ingrediente_mano.nombre]
                                            tile_data[0] = tile_list[indice]
                                            tile_data[4] = indice
                                            break
                                    world.actualizar_estaciones("nivel2")
                                chef.ingrediente_mano = None


        # ── Movimiento: ambos chefs se mueven a la vez ──
        keys = pygame.key.get_pressed()
        for chef in cocina.chefs:
            chef.mover(keys, ANCHO, ALTO, world.obstaculos_tiles)

        # ── Actualizar lógica ─────────────────
        cocina.actualizar(delta)

        # ── Fin de tiempo ─────────────────────
        if cocina.tiempo <= 0:
            run = False

        # ── Dibujar ───────────────────────────
        ventana.fill((30, 30, 30))
        dibujar_grid()
        world.draw(ventana)
        cocina.dibujar(ventana)
        
        

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
        {"rect": pygame.Rect(ANCHO//2 - 500, ALTO//2 + 30, 200, 80), "texto": "Nivel 1", "icono": "Imagenes/icono_nivel1.png"},
        {"rect": pygame.Rect(ANCHO//2 - 100, ALTO//2 + 30, 200, 80), "texto": "Nivel 2", "icono": "Imagenes/icono_nivel2.png"},
        {"rect": pygame.Rect(ANCHO//2 + 300, ALTO//2 + 30, 200, 80), "texto": "Nivel 3", "icono": "Imagenes/icono_nivel3.png"},
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

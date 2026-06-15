import pygame
import sys
 
pygame.init()
pygame.font.init()
import Constantes
 
from mundo import Mundo
from Clases import (
    Chef, Cocina, Ingrediente,
    EstacionDespensa, EstacionEntrega, Estacion,
    Proteina, VegetalesYFrutas, PanesYBases, Plato
)
 
ANCHO = 1200
ALTO  = 750
Constantes.fuente_basica         = pygame.font.SysFont("impact", 20)
Constantes.fuente_bonita         = pygame.font.SysFont("Mocha Choco", 36, bold=True)
Constantes.fuente_bonita_grande  = pygame.font.SysFont("Mocha Choco", 50)
Constantes.fuente_bonita_pequeña = pygame.font.SysFont("Mocha Choco", 28)
 
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Over Cook Tec")
 
fondo1 = pygame.image.load("Imagenes/fondo1.png")
fondo1 = pygame.transform.scale(fondo1, (ANCHO, ALTO))
 
clock = pygame.time.Clock()
 
tile_list = []
for x in range(63):
    tile_image = pygame.image.load(f"tileset/tile{x+1}.png")
    tile_image = pygame.transform.scale(tile_image, size=(Constantes.TILE_SIZE, Constantes.TILE_SIZE))
    tile_list.append(tile_image)
 

 
 
def dibujar_grid():
    for x in range(30):
        pygame.draw.line(ventana, Constantes.BLANCO,
                         start_pos=(x * Constantes.TILE_SIZE, 0),
                         end_pos=(x * Constantes.TILE_SIZE, ALTO))
        pygame.draw.line(ventana, Constantes.BLANCO,
                         start_pos=(0, x * Constantes.TILE_SIZE),
                         end_pos=(ANCHO, x * Constantes.TILE_SIZE))
 
 
def pantalla_nivel_1():
 
    # ── Cargar tileset de sushi ──────────────
    tile_list_sushi = []
    for x in range(62):
        tile_image = pygame.image.load(f"sushi_tiles/tile{x+1}.png")
        tile_image = pygame.transform.scale(tile_image, size=(Constantes.TILE_SIZE, Constantes.TILE_SIZE))
        tile_list_sushi.append(tile_image)
 
    # ── World propio del nivel 1 ─────────────
    world = Mundo()
    world_data_nivel1 = [
        [33, 1, 33, 33, 33, 33,  2, 33],
        [23,  0,  0,  0,  0,  0,  0, 33],
        [33,  0,  0, 22, 14,  0,  0, 15],
        [ 4,  0,  0,  0,  0,  0,  0, 33],
        [33,  5, 33, 33, 33, 33,  8, 33],
    ]
    world.process_data(world_data_nivel1, tile_list_sushi, "nivel1")
    print(f"Estaciones registradas: {[(e['tipo'], e['rect']) for e in world.estaciones_tiles]}")
    print(f"Obstáculos: {world.obstaculos_tiles}")
 
    # ── Tiles de ingredientes en mesa ────────
    mesa_tiles1 = {
        "Pescado_entero":                          19,
        "Pescado_cortado":                         21,
        "Pescado_cocinado":                        20,
        "Pepino":                                  26,
        "Pepino_cortado":                          28,
        "Arroz":                                   27,
        "Plato":                                   23,
        "Plato_alga":                              24,
        "Plato_alga_arroz":                        30,
        "Plato_alga_arroz_pepino":                 29,
        "Plato_alga_arroz_pepino_pescado":         32,
        "Plato_alga_arroz_pepino_pescado_cocinado":31,
    }
 
    # ── Cocina ───────────────────────────────
    cocina = Cocina(tiempo_total=120, nivel="nivel1")
 
    # ── Chefs ────────────────────────────────
    chef1 = Chef(
        nombre="Chef 1",
        imagen_path="Imagenes/gato.png",
        x=200, y=300,
        teclas=(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_e),
        velocidad=3,
    )
    chef2 = Chef(
        nombre="Chef 2",
        imagen_path="Imagenes/gato2.png",
        x=400, y=300,
        teclas=(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP0),
        velocidad=3,
    )
    cocina.agregar_chef(chef1)
    cocina.agregar_chef(chef2)
 
    # ── Estado de procesamiento ──────────────
    procesando_estaciones = {}
 
    TIEMPOS_PROCESO = {
        "tabla_picar": 3.0,
        "cocina":      5.0,
        "freidor":     4.0,
    }
 
    # tile a mostrar MIENTRAS procesa (índice base 1, restamos 1 al acceder)
    TILE_OVERLAY_CRUDO = {
        "tabla_picar": 19,  # pescado entero o pepino crudo
        "cocina":      21,  # pescado cortado crudo
        "freidor":     32,  # sushi sobre freidor
    }
 
    # tile a mostrar cuando YA está listo
    TILE_OVERLAY_LISTO = {
        "tabla_picar_Pepino":         28,  # pepino cortado
        "tabla_picar_Pescado_entero": 21,  # pescado cortado crudo
        "cocina":                     20,  # pescado cocinado
        "freidor":                    31,  # sushi tempura
    }
 
    # ── Helpers ──────────────────────────────
    def encontrar_estacion_cercana(chef):
        centro_chef = pygame.Vector2(chef.rect.centerx, chef.rect.centery)
        mejor_tipo  = None
        menor_dist  = float("inf")
        for estacion in world.estaciones_tiles:
            if chef.rect.colliderect(estacion["rect"]):
                centro_est = pygame.Vector2(estacion["rect"].centerx, estacion["rect"].centery)
                dist = centro_chef.distance_to(centro_est)
                if dist < menor_dist:
                    menor_dist = dist
                    mejor_tipo = estacion["tipo"]
        return mejor_tipo
 
    def pos_estacion(tipo_estacion):
        for estacion in world.estaciones_tiles:
            if estacion["tipo"] == tipo_estacion:
                return (estacion["rect"].x, estacion["rect"].y)
        return None
 
    def nombre_tile_para_ingrediente(ing):
        if isinstance(ing, Proteina):
            return ing.nombre  # "Pescado_entero", "Pescado_cortado", "Pescado_cocinado"
        elif isinstance(ing, VegetalesYFrutas) and ing.nombre == "Pepino":
            return "Pepino_cortado" if ing.estado == "preparado" else "Pepino"
        elif isinstance(ing, PanesYBases) and ing.nombre == "Arroz":
            return "Arroz"
        return None
 
    fuente_hud = pygame.font.SysFont("Arial", 22)
 
    run = True
    while run:
        delta = clock.tick(60) / 1000.0
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
 
                for chef in cocina.chefs:
                    if event.key != chef.teclas[4]:
                        if event.type == pygame.KEYDOWN:
                            print(f"Tecla presionada: {event.key}")
                            print(f"Teclas chefs: {[chef.teclas[4] for chef in cocina.chefs]}")
                            if event.key == pygame.K_ESCAPE:
                                return
                        continue
 
                    tipo = encontrar_estacion_cercana(chef)
 
                    # ══════════════════════════════════════
                    #  MANOS VACÍAS
                    # ══════════════════════════════════════
                    if chef.ingrediente_mano is None:
 
                        if tipo == "estacion_pepino":
                            chef.ingrediente_mano = VegetalesYFrutas("Pepino")
                        elif tipo == "estacion_pescaso":   # nombre tal como está en mundo.py
                            chef.ingrediente_mano = Proteina("Pescado_entero")
                        elif tipo == "estacion_arroz":
                            chef.ingrediente_mano = PanesYBases("Arroz")
                        elif tipo == "estacion_platos":
                            chef.ingrediente_mano = Plato()
 
                        # Recoger de tabla de picar
                        elif tipo == "tabla_picar":
                            if "tabla_picar" in procesando_estaciones:
                                datos = procesando_estaciones["tabla_picar"]
                                if datos["listo"]:
                                    nombre_ing = datos["ingrediente"]
                                    if nombre_ing == "Pepino":
                                        ing = VegetalesYFrutas("Pepino")
                                        ing.estado = "preparado"
                                    else:  # Pescado_entero
                                        ing = Proteina("Pescado_cortado")
                                    ing.tiempo_preparacion = ing.tiempo_minimo
                                    chef.ingrediente_mano = ing
                                    world.quitar_overlay(datos["pos"])
                                    del procesando_estaciones["tabla_picar"]
 
                        # Recoger pescado cocinado de cocina
                        elif tipo == "cocina":
                            if "cocina" in procesando_estaciones:
                                datos = procesando_estaciones["cocina"]
                                if datos["listo"]:
                                    ing = Proteina("Pescado_cocinado")
                                    ing.estado = "preparado"
                                    ing.tiempo_preparacion = ing.tiempo_minimo
                                    chef.ingrediente_mano = ing
                                    world.quitar_overlay(datos["pos"])
                                    del procesando_estaciones["cocina"]
 
                        # Recoger sushi tempura del freidor
                        elif tipo == "freidor":
                            if "freidor" in procesando_estaciones:
                                datos = procesando_estaciones["freidor"]
                                if datos["listo"]:
                                    plato_temp = datos["plato"]
                                    plato_temp.es_tempura = True
                                    chef.ingrediente_mano = plato_temp
                                    world.quitar_overlay(datos["pos"])
                                    del procesando_estaciones["freidor"]
 
                        # Recoger de mesa
                        elif tipo == "mesa":
                            for tile_data in world.map_tiles:
                                if tile_data[1].colliderect(chef.rect) and tile_data[5] is not None:
                                    chef.ingrediente_mano = tile_data[5]
                                    tile_data[5] = None
                                    tile_data[0] = tile_list_sushi[0]
                                    tile_data[4] = 0
                                    world.actualizar_estaciones("nivel1")
                                    break
 
                    # ══════════════════════════════════════
                    #  CON INGREDIENTE EN MANO (no plato)
                    # ══════════════════════════════════════
                    elif isinstance(chef.ingrediente_mano, Ingrediente) \
                            and not isinstance(chef.ingrediente_mano, Plato):
                        ing = chef.ingrediente_mano
 
                        # Pepino crudo o Pescado entero → tabla de picar
                        if tipo == "tabla_picar" \
                                and ing.nombre in ("Pepino", "Pescado_entero") \
                                and ing.estado != "preparado":
                            if "tabla_picar" not in procesando_estaciones:
                                pos = pos_estacion("tabla_picar")
                                if pos:
                                    world.poner_overlay(pos, tile_list_sushi[TILE_OVERLAY_CRUDO["tabla_picar"] - 1])
                                    procesando_estaciones["tabla_picar"] = {
                                        "pos": pos,
                                        "timer": 0.0,
                                        "listo": False,
                                        "ingrediente": ing.nombre,
                                    }
                                    chef.ingrediente_mano = None
 
                        # Pescado cortado → cocina
                        elif tipo == "cocina" \
                                and isinstance(ing, Proteina) \
                                and ing.nombre == "Pescado_cortado":
                            if "cocina" not in procesando_estaciones:
                                pos = pos_estacion("cocina")
                                if pos:
                                    world.poner_overlay(pos, tile_list_sushi[TILE_OVERLAY_CRUDO["cocina"] - 1])
                                    procesando_estaciones["cocina"] = {
                                        "pos": pos, "timer": 0.0, "listo": False,
                                        "ingrediente": "Pescado_cortado",
                                    }
                                    chef.ingrediente_mano = None
 
                        # Dejar en mesa vacía
                        elif tipo == "mesa":
                            nombre_tile = nombre_tile_para_ingrediente(ing)
                            if nombre_tile and nombre_tile in mesa_tiles1:
                                for tile_data in world.map_tiles:
                                    if tile_data[1].colliderect(chef.rect) and tile_data[4] == 0:
                                        indice = mesa_tiles1[nombre_tile]
                                        tile_data[0] = tile_list_sushi[indice - 1]
                                        tile_data[4] = indice
                                        tile_data[5] = ing
                                        break
                                world.actualizar_estaciones("nivel1")
                            chef.ingrediente_mano = None
 
                        elif tipo == "entrega":
                            chef.ingrediente_mano = None
 
                    # ══════════════════════════════════════
                    #  CON PLATO EN MANO
                    # ══════════════════════════════════════
                    elif isinstance(chef.ingrediente_mano, Plato):
                        plato = chef.ingrediente_mano
 
                        # Alga directo desde estación
                        if tipo == "estacion_algas":
                            ing_alga = PanesYBases("Alga")
                            if plato.puede_agregar(ing_alga):
                                plato.agregar(ing_alga)
 
                        # Arroz directo desde estación
                        elif tipo == "estacion_arroz":
                            ing_arroz = PanesYBases("Arroz")
                            if plato.puede_agregar(ing_arroz):
                                plato.agregar(ing_arroz)
 
                        # Agregar ingrediente desde mesa
                        elif tipo == "mesa":
                            for tile_data in world.map_tiles:
                                if tile_data[1].colliderect(chef.rect) and tile_data[5] is not None:
                                    if plato.puede_agregar(tile_data[5]):
                                        plato.agregar(tile_data[5])
                                        tile_data[5] = None
                                        tile_data[0] = tile_list_sushi[0]
                                        tile_data[4] = 0
                                        world.actualizar_estaciones("nivel1")
                                    break
 
                        # Plato completo → freidor → sushi tempura
                        elif tipo == "freidor":
                            nombres = [i.nombre for i in plato.ingredientes]
                            if sorted(nombres) == sorted(["Alga", "Arroz", "Pepino", "Pescado_cocinado"]):
                                if "freidor" not in procesando_estaciones:
                                    pos = pos_estacion("freidor")
                                    if pos:
                                        world.poner_overlay(pos, tile_list_sushi[TILE_OVERLAY_CRUDO["freidor"] - 1])
                                        procesando_estaciones["freidor"] = {
                                            "pos": pos, "timer": 0.0, "listo": False,
                                            "plato": plato,
                                        }
                                        chef.ingrediente_mano = None
 
                        # Entregar plato
                        elif tipo == "entrega":
                            puntos = 0
                            for orden in cocina.ordenes:
                                if orden.activa and orden.comparar_receta(plato):
                                    puntos = orden.puntos_receta
                                    orden.activa = False
                                    break
                            if puntos > 0:
                                chef.puntos += puntos
                            chef.ingrediente_mano = None
 
        # ── Movimiento ───────────────────────
        keys = pygame.key.get_pressed()
        for chef in cocina.chefs:
            chef.mover(keys, ANCHO, ALTO, world.obstaculos_tiles)
 
        # ── Lógica ───────────────────────────
        cocina.actualizar(delta)
 
        # Avanzar timers
        for tipo_est, datos in list(procesando_estaciones.items()):
            if not datos["listo"]:
                datos["timer"] += delta
                if datos["timer"] >= TIEMPOS_PROCESO[tipo_est]:
                    datos["listo"] = True
                    if tipo_est == "tabla_picar":
                        clave = f"tabla_picar_{datos['ingrediente']}"
                        idx = TILE_OVERLAY_LISTO.get(clave, 28)
                    else:
                        idx = TILE_OVERLAY_LISTO[tipo_est]
                    world.poner_overlay(datos["pos"], tile_list_sushi[idx - 1])
 
        if cocina.tiempo <= 0:
            run = False
 
        # ── Dibujo ───────────────────────────
        ventana.fill((30, 30, 30))
        dibujar_grid()
        world.draw(ventana)
        cocina.dibujar(ventana)
 
        tiempo_txt = fuente_hud.render(f"Tiempo: {max(0, int(cocina.tiempo))}s", True, (255, 255, 255))
        pts1_txt   = fuente_hud.render(f"Chef 1: {chef1.puntos} pts", True, (200, 230, 255))
        pts2_txt   = fuente_hud.render(f"Chef 2: {chef2.puntos} pts", True, (255, 230, 180))
        ventana.blit(tiempo_txt, (20, 20))
        ventana.blit(pts1_txt,   (20, 50))
        ventana.blit(pts2_txt,   (20, 75))
 
        y_orden = 105
        ventana.blit(fuente_hud.render("Recetas", True, (255, 255, 100)), (20, y_orden))
        for orden in cocina.ordenes:
            y_orden += 22
            txt = fuente_hud.render(
                f"  {orden.nombre}  {orden.puntos_receta}pts"
                f"  {int(orden.max_time_receta - orden.tiempo_transcurrido)}s",
                True, (255, 200, 100),
            )
            ventana.blit(txt, (20, y_orden))
 
        pygame.display.update()
 
 
# ─────────────────────────────────────────────
#  NIVEL 2 — HAMBURGUESAS
# ─────────────────────────────────────────────
def pantalla_nivel_2():
 
    # ── World propio del nivel 2 ─────────────
    world = Mundo()
    world_data_nivel2 = [
        [0,0,9,0,0,5,0,0],
        [45,1,2,0,2,1,2,6],
        [0,2,1,36,1,2,1,0],
        [3,1,2,1,2,0,2,0],
        [0,0,4,0,18,0,27,0],
    ]
    world.process_data(world_data_nivel2, tile_list, "nivel2")
 
    mesa_tiles1 = {
        "Carne":                       16,
        "Carne_cocinada":              15,
        "Tomate":                      25,
        "Tomate_cut":                  26,
        "Pan":                         24,
        "Papa":                        22,
        "Papa_cocinada":               23,
        "Plato":                       10,
        "plato_pan":                   34,
        "plato_papa":                  35,
        "plato_pan_carne":             41,
        "plato_pan_carne2":            40,
        "plato_pan_carne_tomate":      39,
        "plato_pan_carne_tomate_papa": 38,
    }
 
    cocina = Cocina(tiempo_total=120, nivel="nivel2")
 
    chef1 = Chef(
        nombre="Chef 1",
        imagen_path="Imagenes/gato.png",
        x=200, y=300,
        teclas=(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_e),
        velocidad=3,
    )
    chef2 = Chef(
        nombre="Chef 2",
        imagen_path="Imagenes/gato2.png",
        x=400, y=300,
        teclas=(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_KP0),
        velocidad=3,
    )
    cocina.agregar_chef(chef1)
    cocina.agregar_chef(chef2)
 
    procesando_estaciones = {}
 
    TIEMPOS_PROCESO = {
        "cocina":      5.0,
        "tabla_picar": 3.0,
        "freidor":     4.0,
    }
    TILE_OVERLAY_CRUDO = {
        "cocina":      16,
        "tabla_picar": 25,
        "freidor":     22,
    }
    TILE_OVERLAY_LISTO = {
        "cocina":      15,
        "tabla_picar": 26,
        "freidor":     23,
    }
    INGREDIENTE_RESULTADO = {
        "cocina":      lambda: Proteina("Carne"),
        "tabla_picar": lambda: VegetalesYFrutas("Tomate"),
        "freidor":     lambda: VegetalesYFrutas("Papa"),
    }
 
    def encontrar_estacion_cercana(chef):
        centro_chef = pygame.Vector2(chef.rect.centerx, chef.rect.centery)
        mejor_tipo  = None
        menor_dist  = float("inf")
        for estacion in world.estaciones_tiles:
            if chef.rect.colliderect(estacion["rect"]):
                centro_est = pygame.Vector2(estacion["rect"].centerx, estacion["rect"].centery)
                dist = centro_chef.distance_to(centro_est)
                if dist < menor_dist:
                    menor_dist = dist
                    mejor_tipo = estacion["tipo"]
        return mejor_tipo
 
    def pos_estacion(tipo_estacion):
        for estacion in world.estaciones_tiles:
            if estacion["tipo"] == tipo_estacion:
                return (estacion["rect"].x, estacion["rect"].y)
        return None
 
    def nombre_tile_para_ingrediente(ing):
        if isinstance(ing, Proteina):
            return "Carne_cocinada" if ing.estado == "preparado" else "Carne"
        elif isinstance(ing, VegetalesYFrutas):
            if ing.nombre == "Tomate":
                return "Tomate_cut" if ing.estado == "preparado" else "Tomate"
            elif ing.nombre == "Papa":
                return "Papa_cocinada" if ing.estado == "preparado" else "Papa"
        elif isinstance(ing, PanesYBases):
            return "Pan"
        return None
 
    fuente_hud = pygame.font.SysFont("Arial", 22)
 
    run = True
    while run:
        delta = clock.tick(60) / 1000.0
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
 
                for chef in cocina.chefs:
                    if event.key != chef.teclas[4]:
                        continue
 
                    tipo = encontrar_estacion_cercana(chef)
                    print(f"Tipo detectado: {tipo}")
                    print(f"Estaciones disponibles: {[e['tipo'] for e in world.estaciones_tiles]}")
                    print(f"Chef rect: {chef.rect}")
                    
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
 
                        elif tipo in ("cocina", "tabla_picar", "freidor"):
                            if tipo in procesando_estaciones:
                                datos = procesando_estaciones[tipo]
                                if datos["listo"]:
                                    ing = INGREDIENTE_RESULTADO[tipo]()
                                    ing.estado = "preparado"
                                    ing.tiempo_preparacion = ing.tiempo_minimo
                                    if hasattr(ing, "cocinada"):
                                        ing.cocinada = True
                                    chef.ingrediente_mano = ing
                                    world.quitar_overlay(datos["pos"])
                                    del procesando_estaciones[tipo]
 
                        elif tipo == "mesa":
                            for tile_data in world.map_tiles:
                                if tile_data[1].colliderect(chef.rect) and tile_data[5] is not None:
                                    chef.ingrediente_mano = tile_data[5]
                                    tile_data[5] = None
                                    tile_data[0] = tile_list[0]
                                    tile_data[4] = 0
                                    world.actualizar_estaciones("nivel2")
                                    break
 
                        elif tipo in ("mesa_Carne_cruda", "mesa_Carne_cocinada_cruda",
                                      "mesa_Tomate_cruda", "mesa_Tomate_cut_cruda",
                                      "mesa_Pan_cruda", "mesa_Papa_cruda",
                                      "mesa_Papa_cocinada_cruda"):
                            for tile_data in world.map_tiles:
                                if tile_data[1].colliderect(chef.rect) and tile_data[5] is not None:
                                    chef.ingrediente_mano = tile_data[5]
                                    tile_data[5] = None
                                    tile_data[0] = tile_list[0]
                                    tile_data[4] = 0
                                    world.actualizar_estaciones("nivel2")
                                    break
 
                    elif isinstance(chef.ingrediente_mano, Ingrediente) \
                            and not isinstance(chef.ingrediente_mano, Plato):
                        ing = chef.ingrediente_mano
 
                        if tipo == "cocina" and isinstance(ing, Proteina):
                            if "cocina" not in procesando_estaciones:
                                pos = pos_estacion("cocina")
                                if pos:
                                    world.poner_overlay(pos, tile_list[TILE_OVERLAY_CRUDO["cocina"]])
                                    procesando_estaciones["cocina"] = {
                                        "pos": pos, "timer": 0.0, "listo": False}
                                    chef.ingrediente_mano = None
 
                        elif tipo == "tabla_picar" \
                                and isinstance(ing, VegetalesYFrutas) \
                                and ing.nombre == "Tomate":
                            if "tabla_picar" not in procesando_estaciones:
                                pos = pos_estacion("tabla_picar")
                                if pos:
                                    world.poner_overlay(pos, tile_list[TILE_OVERLAY_CRUDO["tabla_picar"]])
                                    procesando_estaciones["tabla_picar"] = {
                                        "pos": pos, "timer": 0.0, "listo": False}
                                    chef.ingrediente_mano = None
 
                        elif tipo == "freidor" \
                                and isinstance(ing, VegetalesYFrutas) \
                                and ing.nombre == "Papa":
                            if "freidor" not in procesando_estaciones:
                                pos = pos_estacion("freidor")
                                if pos:
                                    world.poner_overlay(pos, tile_list[TILE_OVERLAY_CRUDO["freidor"]])
                                    procesando_estaciones["freidor"] = {
                                        "pos": pos, "timer": 0.0, "listo": False}
                                    chef.ingrediente_mano = None
 
                        elif tipo == "mesa":
                            nombre_tile = nombre_tile_para_ingrediente(ing)
                            if nombre_tile and nombre_tile in mesa_tiles1:
                                for tile_data in world.map_tiles:
                                    if tile_data[1].colliderect(chef.rect) and tile_data[4] == 0:
                                        indice = mesa_tiles1[nombre_tile]
                                        tile_data[0] = tile_list[indice]
                                        tile_data[4] = indice
                                        tile_data[5] = ing
                                        break
                                world.actualizar_estaciones("nivel2")
                            chef.ingrediente_mano = None
 
                        elif tipo == "entrega":
                            chef.ingrediente_mano = None
 
                    elif isinstance(chef.ingrediente_mano, Plato):
                        plato = chef.ingrediente_mano
 
                        if tipo == "estacion_pan":
                            ing_pan = PanesYBases("Pan")
                            if plato.puede_agregar(ing_pan):
                                plato.agregar(ing_pan)
 
                        elif tipo in ("mesa_Carne_cruda", "mesa_Carne_cocinada_cruda",
                                      "mesa_Tomate_cruda", "mesa_Tomate_cut_cruda",
                                      "mesa_Pan_cruda", "mesa_Papa_cruda",
                                      "mesa_Papa_cocinada_cruda"):
                            for tile_data in world.map_tiles:
                                if tile_data[1].colliderect(chef.rect) and tile_data[5] is not None:
                                    if plato.puede_agregar(tile_data[5]):
                                        plato.agregar(tile_data[5])
                                        tile_data[5] = None
                                        tile_data[0] = tile_list[0]
                                        tile_data[4] = 0
                                        world.actualizar_estaciones("nivel2")
                                    break
 
                        elif tipo == "mesa":
                            for tile_data in world.map_tiles:
                                if tile_data[1].colliderect(chef.rect) and tile_data[5] is not None:
                                    if plato.puede_agregar(tile_data[5]):
                                        plato.agregar(tile_data[5])
                                        tile_data[5] = None
                                        tile_data[0] = tile_list[0]
                                        tile_data[4] = 0
                                        world.actualizar_estaciones("nivel2")
                                    break
 
                        elif tipo == "entrega":
                            puntos = 0
                            for orden in cocina.ordenes:
                                if orden.activa and orden.comparar_receta(plato):
                                    puntos = orden.puntos_receta
                                    orden.activa = False
                                    break
                            if puntos > 0:
                                chef.puntos += puntos
                            chef.ingrediente_mano = None
 
        keys = pygame.key.get_pressed()
        for chef in cocina.chefs:
            chef.mover(keys, ANCHO, ALTO, world.obstaculos_tiles)
 
        cocina.actualizar(delta)
 
        for tipo_est, datos in list(procesando_estaciones.items()):
            if not datos["listo"]:
                datos["timer"] += delta
                if datos["timer"] >= TIEMPOS_PROCESO[tipo_est]:
                    datos["listo"] = True
                    world.poner_overlay(datos["pos"], tile_list[TILE_OVERLAY_LISTO[tipo_est]])
 
        if cocina.tiempo <= 0:
            run = False
 
        ventana.fill((30, 30, 30))
        dibujar_grid()
        world.draw(ventana)
        cocina.dibujar(ventana)
 
        tiempo_txt = fuente_hud.render(f"Tiempo: {max(0, int(cocina.tiempo))}s", True, (255, 255, 255))
        pts1_txt   = fuente_hud.render(f"Chef 1: {chef1.puntos} pts", True, (200, 230, 255))
        pts2_txt   = fuente_hud.render(f"Chef 2: {chef2.puntos} pts", True, (255, 230, 180))
        ventana.blit(tiempo_txt, (20, 20))
        ventana.blit(pts1_txt,   (20, 50))
        ventana.blit(pts2_txt,   (20, 75))
 
        y_orden = 105
        ventana.blit(fuente_hud.render("Recetas", True, (255, 255, 100)), (20, y_orden))
        for orden in cocina.ordenes:
            y_orden += 22
            txt = fuente_hud.render(
                f"  {orden.nombre}  {orden.puntos_receta}pts"
                f"  {int(orden.max_time_receta - orden.tiempo_transcurrido)}s",
                True, (255, 200, 100),
            )
            ventana.blit(txt, (20, y_orden))
 
        pygame.display.update()
 
 
# ─────────────────────────────────────────────
#  NIVEL 3 (pendiente)
# ─────────────────────────────────────────────
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
    titulo      = Constantes.fuente_bonita_grande.render("Selecciona un nivel", True, Constantes.NEGRO)
    dificil_txt = Constantes.fuente_bonita_pequeña.render("Difícil", True, Constantes.NEGRO)
    medio_txt   = Constantes.fuente_bonita_pequeña.render("Medio",   True, Constantes.NEGRO)
    facil_txt   = Constantes.fuente_bonita_pequeña.render("Fácil",   True, Constantes.NEGRO)
 
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
        mouse_pos   = pygame.mouse.get_pos()
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
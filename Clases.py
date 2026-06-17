import pygame
import random

# ─────────────────────────────────────────────
#  INGREDIENTE (clase base)
# ─────────────────────────────────────────────
class Ingrediente:
    tiempo_minimo = 5

    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = "crudo"
        self.tiempo_preparacion = 0


# ─────────────────────────────────────────────
#  SUBCLASES DE INGREDIENTE
# ─────────────────────────────────────────────
class VegetalesYFrutas(Ingrediente):
    tiempo_minimo = 3


class PanesYBases(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.estado = "preparado"  


class Proteina(Ingrediente):
    tiempo_minimo = 5
    tiempo_maximo = 15   

    def actualizar_estado(self, delta):
        if self.estado in ("crudo", "preparado"):
            self.tiempo_preparacion += delta
            if self.tiempo_preparacion >= self.tiempo_maximo:
                self.estado = "quemado"
                self.cocinada = False
            elif self.tiempo_preparacion >= self.tiempo_minimo: 
                self.estado = "preparado"
                self.cocinada = True

class Plato:
    # Orden fijo de ensamblado
    ORDEN_POR_NIVEL = {
    "nivel1": ["Alga", "Arroz", "Pepino", "Pescado_cocinado"],
    "nivel2": ["Pan", "Carne", "Tomate", "Papa"],
    "nivel3": ["Arroz", "Frijoles", "Huevo", "Salchichon", "Platano"]}
    
    
    # Qué tile mostrar según contenido
    TILE_POR_CONTENIDO = {
        (): 10,
        ("Pan",): 34,
        ("Pan", "Carne"): 41,
        ("Pan", "Carne", "Tomate"): 39,
        ("Pan", "Carne", "Tomate", "Papa"): 38,

        ("Alga",): 24,
        ("Alga", "Arroz"): 30,
        ("Alga", "Arroz", "Pepino"): 29,
        ("Alga", "Arroz", "Pepino", "Pescado_cocinado"): 32,
        ("Alga", "Arroz", "Pepino", "Pescado_cocinado", "tempura"): 31,

        ("Arroz",):43 ,           # ← pon el número de tile correcto
        ("Arroz", "Frijoles"): 36,
        ("Arroz", "Frijoles", "Huevo"): 37,
        ("Arroz", "Frijoles", "Huevo", "Salchichon"): 38,
        ("Arroz", "Frijoles", "Huevo", "Salchichon", "Platano"): 41,
    }


    def __init__(self, nivel="nivel2"):
        self.nombre = "Plato"
        self.ingredientes = []
        self.orden = self.ORDEN_POR_NIVEL[nivel]

    def puede_agregar(self, ingrediente):
        if ingrediente.estado != "preparado":
            return False
        # Verifica que sea el siguiente en el orden
        siguiente_idx = len(self.ingredientes)
        if siguiente_idx >= len(self.orden):
            return False
        return ingrediente.nombre == self.orden[siguiente_idx]

    def agregar(self, ingrediente):
        if self.puede_agregar(ingrediente):
            self.ingredientes.append(ingrediente)
            print(f"Plato tiene: {[i.nombre for i in self.ingredientes]}")
            return True
        else:
            print(f"No se puede agregar {ingrediente.nombre} - estado: {ingrediente.estado}")
        return False

    def tile_actual(self):
        clave = tuple(i.nombre for i in self.ingredientes)
        return self.TILE_POR_CONTENIDO.get(clave, 10)
    


# ─────────────────────────────────────────────
#  RECETA
# ─────────────────────────────────────────────
class Receta:
    def __init__(self, nombre, lista_ingredientes):
        self.nombre = nombre
        self.lista_ingredientes = lista_ingredientes
        self.puntos_receta = len(lista_ingredientes) * 10
        self.max_time_receta = len(lista_ingredientes) * 30
        self.tiempo_transcurrido = 0
        self.activa = True

    def actualizar(self, delta):
        if not self.activa:
            return
        self.tiempo_transcurrido += delta
        if self.tiempo_transcurrido >= self.max_time_receta:
            self.tiempo_transcurrido = 0
            self.puntos_receta //= 2
            if self.puntos_receta <= 0:
                self.activa = False
            return True  
        return False

    def comparar_receta(self, plato):
        # plato es un objeto Plato con lista de ingredientes ensamblados
        nombres_receta = [i.nombre for i in self.lista_ingredientes]
        nombres_plato  = [i.nombre for i in plato.ingredientes]
        return nombres_receta == nombres_plato

    def __str__(self):
        ingredientes = ", ".join(str(i) for i in self.lista_ingredientes)
        return f"Receta: {self.nombre} | Pts: {self.puntos_receta} | Tiempo: {self.max_time_receta}s | Ingredientes: [{ingredientes}]"


# ─────────────────────────────────────────────
#  ESTACION
# ─────────────────────────────────────────────
class Estacion:
    TIEMPO_PROCESO = 0.0
    TIEMPO_QUEMADO = 0.0 

    def __init__(self, nombre, ingredientes_aceptados=None):
        self.nombre = nombre
        self.ingredientes_aceptados = ingredientes_aceptados or []
        self.timer = 0.0
        self.timer_quemado = 0.0
        self.listo = False
        self.procesando = False
        self.quemado = False
        self.pos = None
        self.ingrediente = None

    def iniciar(self, pos, ingrediente=None):
        self.timer = 0.0
        self.timer_quemado = 0.0
        self.listo = False
        self.quemado = False
        self.procesando = True
        self.pos = pos
        self.ingrediente = ingrediente

    def actualizar(self, delta):
        if self.procesando and not self.listo:
            self.timer += delta
            if self.timer >= self.TIEMPO_PROCESO:
                self.listo = True
                self.procesando = False
        elif self.listo and self.TIEMPO_QUEMADO > 0:
            self.timer_quemado += delta
            if self.timer_quemado >= self.TIEMPO_QUEMADO:
                self.quemado = True

    def reiniciar(self):
        self.timer = 0.0
        self.timer_quemado = 0.0
        self.listo = False
        self.quemado = False
        self.procesando = False
        self.pos = None
        self.ingrediente = None

    def __str__(self):
        return f"Estación: {self.nombre}"


class TablaPicar(Estacion):
    TIEMPO_PROCESO = 3.0
    TIEMPO_QUEMADO = 0.0 


class EstacionCocina(Estacion):
    TIEMPO_PROCESO = 5.0
    TIEMPO_QUEMADO = 8.0 


class Freidor(Estacion):
    TIEMPO_PROCESO = 4.0
    TIEMPO_QUEMADO = 8.0



class EstacionEntrega(Estacion):
    def __init__(self):
        super().__init__("Entrega")

    def entregar_receta(self, receta_jugador, ordenes_activas):
        for orden in ordenes_activas:
            if orden.activa and orden.comparar_receta(receta_jugador):
                puntos = orden.puntos_receta
                orden.activa = False
                return puntos
        return 0


# ─────────────────────────────────────────────
#  CHEF
#  Cada chef tiene sus propias teclas y se
#  mueve de forma independiente y simultánea.
#  Chef 1: W / A / S / D
#  Chef 2: flechas ↑ ↓ ← →
# ─────────────────────────────────────────────
class Chef:

    def __init__(self, nombre, imagen_path, x, y, teclas, velocidad=3):
        self.nombre = nombre
        self.puntos = 0
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.rect = pygame.Rect(self.x , self.y , 80, 80)

        # teclas es una tupla: (arriba, abajo, izquierda, derecha)
        self.teclas = teclas
        self.ingrediente_mano = None

        self.imagen = pygame.image.load(imagen_path)
        self.imagen = pygame.transform.scale(self.imagen, (80, 80))

        #Tiles de ingredientes
        self.ingredientes_tiles = {
            "Pescado_entero": pygame.transform.scale(pygame.image.load("sushi_tiles/tile14.png"), (40, 40)),
            "Pescado_cortado": pygame.transform.scale(pygame.image.load("sushi_tiles/tile5.png"), (40, 40)),
            "Pescado_cocinado": pygame.transform.scale(pygame.image.load("sushi_tiles/tile35.png"), (40, 40)),
            "Pepino": pygame.transform.scale(pygame.image.load("sushi_tiles/tile20.png"), (40, 40)),
            "pepino_cortado": pygame.transform.scale(pygame.image.load("sushi_tiles/tile8.png"), (40, 40)),
            "Arroz": pygame.transform.scale(pygame.image.load("sushi_tiles/tile37.png"), (40, 40)),
            "Alga": pygame.transform.scale(pygame.image.load("sushi_tiles/tile39.png"), (40, 40)),
            "plato": pygame.transform.scale(pygame.image.load("sushi_tiles/tile38.png"), (40, 40)),
            "plato_alga": pygame.transform.scale(pygame.image.load("sushi_tiles/tile15.png"), (40, 40)),
            "plato_alga_arroz": pygame.transform.scale(pygame.image.load("sushi_tiles/tile13.png"), (40, 40)),
            "plato_alga,arroz,pepino": pygame.transform.scale(pygame.image.load("sushi_tiles/tile12.png"), (40, 40)),
            "plato_alga,arroz,pepino,pescado": pygame.transform.scale(pygame.image.load("sushi_tiles/tile11.png"), (40, 40)),
            "plato_alga,arroz,pepino,pescado,tempura": pygame.transform.scale(pygame.image.load("sushi_tiles/tile19.png"), (40, 40)),
            #Nivel 2
            "Carne":  pygame.transform.scale(pygame.image.load("tileset/tile13.png"), (40, 40)),
            "Papa":   pygame.transform.scale(pygame.image.load("tileset/tile15.png"),  (40, 40)),
            "Tomate": pygame.transform.scale(pygame.image.load("tileset/tile21.png"),  (40, 40)),
            "Pan":    pygame.transform.scale(pygame.image.load("tileset/tile20.png"), (40, 40)),
            "Plato":  pygame.transform.scale(pygame.image.load("tileset/tile11.png"), (40, 40)),
            "plato_vacio": pygame.transform.scale(pygame.image.load("tileset/tile11.png"), (40, 40)),
            "plato_pan": pygame.transform.scale(pygame.image.load("tileset/tile29.png"), (40, 40)),
            "plato_pan_carne": pygame.transform.scale(pygame.image.load("tileset/tile30.png"), (40, 40)),
            "plato_pan_carne_tomate": pygame.transform.scale(pygame.image.load("tileset/tile32.png"), (40, 40)),
            "plato_pan_carne_tomate_papa": pygame.transform.scale(pygame.image.load("tileset/tile33.png"), (40, 40)),
            #Nivel3
            "Huevo": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile22.png"), (40, 40)),
            "Huevo_cocinado": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile21.png"), (40, 40)),
            "Salchichon_entero": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile25.png"), (40, 40)),
            "Salchichon_crudo": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile17.png"), (40, 40)),
            "Salchichon_cocinado": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile16.png"), (40, 40)),
            "Platano_entero": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile26.png"), (40, 40)),
            "Platano_crudo": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile19.png"), (40, 40)),
            "Platano_cocinado": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile20.png"), (40, 40)),
            "Arroz": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile23.png"), (40, 40)),
            "Frijoles": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile24.png"), (40, 40)),
            # Platos nivel 3
            "plato_vacio_cr": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile47.png"), (40, 40)),
            "plato_arroz": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile46.png"), (40, 40)),
            "plato_arroz_frijoles": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile13.png"), (40, 40)),
            "plato_arroz_frijoles_huevo": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile14.png"), (40, 40)),
            "plato_arroz_frijoles_huevo_salchichon": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile15.png"), (40, 40)),
            "plato_completo_cr": pygame.transform.scale(pygame.image.load("cr_food_tiles/tile10.png"), (40, 40)),

        }   

    def mover(self, keys, ancho_ventana, alto_ventana, obstaculos_tiles):
        arriba, abajo, izquierda, derecha, accion = self.teclas

        chef_rect = pygame.Rect(self.x, self.y, 80, 80)

        #Movimiento horizontal
        dx = 0
        if keys[izquierda]:
            dx -= self.velocidad
        if keys[derecha]:
            dx += self.velocidad
        chef_rect.x += dx
        for obstaculo in obstaculos_tiles:
            if chef_rect.colliderect(obstaculo):
                if dx > 0:  # moviéndose a la derecha
                    chef_rect.right = obstaculo.left
                elif dx < 0:  # moviéndose a la izquierda
                    chef_rect.left = obstaculo.right

        dy = 0
        if keys[arriba]:
            dy -= self.velocidad
        if keys[abajo]:
            dy += self.velocidad
        chef_rect.y += dy

        for obstaculo in obstaculos_tiles:
            if chef_rect.colliderect(obstaculo):
                if dy > 0:  # moviéndose hacia abajo
                    chef_rect.bottom = obstaculo.top
                elif dy < 0:  # moviéndose hacia arriba
                    chef_rect.top = obstaculo.bottom
        

        self.x = chef_rect.x
        self.y = chef_rect.y
        self.rect = pygame.Rect(self.x - 10, self.y - 10, 100, 100)

    def agarrar(self, estaciones_tiles):
        arriba, abajo, izquierda, derecha, accion = self.teclas
        chef_rect = pygame.Rect(self.x -10, self.y -10, 100, 100)

        for estacion in estaciones_tiles:
            if chef_rect.colliderect(estacion["rect"]):
                return estacion["tipo"]  # devuelve qué estación tocó
        return None

    def dibujar(self, ventana):
        ventana.blit(self.imagen, (self.x, self.y))
        
        if self.ingrediente_mano is None:
            return
        
        if isinstance(self.ingrediente_mano, Plato):
            clave = tuple(i.nombre for i in self.ingrediente_mano.ingredientes)
            nombres_clave = {
                (): "plato_vacio",
                ("Pan",): "plato_pan",
                ("Pan", "Carne"): "plato_pan_carne",
                ("Pan", "Carne", "Tomate"): "plato_pan_carne_tomate",
                ("Pan", "Carne", "Tomate", "Papa"): "plato_pan_carne_tomate_papa",

                ("Alga",): "plato_alga",
                ("Alga", "Arroz"): "plato_alga_arroz",
                ("Alga", "Arroz", "Pepino"): "plato_alga,arroz,pepino",
                ("Alga", "Arroz", "Pepino", "Pescado_cocinado"): "plato_alga,arroz,pepino,pescado",
            
                ("Arroz",): "plato_arroz",
                ("Arroz", "Frijoles"): "plato_arroz_frijoles",
                ("Arroz", "Frijoles", "Huevo"): "plato_arroz_frijoles_huevo",
                ("Arroz", "Frijoles", "Huevo", "Salchichon"): "plato_arroz_frijoles_huevo_salchichon",
                ("Arroz", "Frijoles", "Huevo", "Salchichon", "Platano"): "plato_completo_cr",
            }
            nombre_img = nombres_clave.get(clave, "plato_vacio")
            img = self.ingredientes_tiles.get(nombre_img)
            if img:
                ventana.blit(img, (self.x + 40, self.y - 10))
        else:
            nombre = self.ingrediente_mano.nombre
            if nombre == "Salchichon":
                nombre = "Salchichon_entero" 
            elif nombre == "Salchichon_cortado":
                nombre = "Salchichon_crudo" 
            elif nombre == "Platano":
                nombre = "Platano_entero"
            elif nombre == "Platano_cortado":
                nombre = "Platano_crudo"
            if nombre in self.ingredientes_tiles:
                img = self.ingredientes_tiles[nombre]
                ventana.blit(img, (self.x + 40, self.y - 10))

    def __str__(self):
        return f"Chef: {self.nombre} | Pts: {self.puntos}"


# ─────────────────────────────────────────────
#  COCINA
# ─────────────────────────────────────────────
class Cocina:
    RECETAS_DISPONIBLES = RECETAS_DISPONIBLES = {
    "nivel1": [
        ("Sushi Pepino",  [("PanesYBases","Alga"), ("PanesYBases","Arroz"), ("VegetalesYFrutas","Pepino")]),
        ("Sushi Pescado", [("PanesYBases","Alga"), ("PanesYBases","Arroz"), ("VegetalesYFrutas","Pepino"), ("Proteina","Pescado_cocinado")]),
        ("Sushi Tempura", [("PanesYBases","Alga"), ("PanesYBases","Arroz"), ("VegetalesYFrutas","Pepino"), ("Proteina","Pescado_cocinado")]),
    ],

    "nivel2": [
        ("Hamburguesa Simple",     [("PanesYBases", "Pan"), ("Proteina", "Carne")]),
        ("Hamburguesa con Tomate", [("PanesYBases", "Pan"), ("Proteina", "Carne"), ("VegetalesYFrutas", "Tomate")]),
        ("Hamburguesa Completa",   [("PanesYBases", "Pan"), ("Proteina", "Carne"), ("VegetalesYFrutas", "Tomate"), ("VegetalesYFrutas", "Papa")]),
    ],
    "nivel3": [
        ("Arroz Blanco",    [("PanesYBases", "Arroz")]),
        ("Gallo Pinto Simple",    [("PanesYBases", "Arroz"), ("PanesYBases", "Frijoles")]),
        ("Gallo Pinto con Huevo", [("PanesYBases", "Arroz"), ("PanesYBases", "Frijoles"), ("Proteina", "Huevo")]),
        ("Gallo Pinto con Huevo y Salchichón",  [("PanesYBases", "Arroz"), ("PanesYBases", "Frijoles"), ("Proteina", "Huevo"), ("Proteina", "Salchichon")]),
        ("Gallo Pinto Completo",  [("PanesYBases", "Arroz"), ("PanesYBases", "Frijoles"), ("Proteina", "Huevo"), ("Proteina", "Salchichon"), ("VegetalesYFrutas", "Platano")])
    ]
    }
    TIPOS = {
        "Proteina": Proteina,
        "VegetalesYFrutas": VegetalesYFrutas,
        "PanesYBases": PanesYBases,
    }

    def __init__(self, tiempo_total, nivel="nivel1"):
        self.tiempo = tiempo_total
        self.chefs = []
        self.ordenes = []
        self.nivel = nivel
        self.intervalo_receta = 30
        self.tiempo_ultima_receta = 0

        for _ in range(1):
            nueva = self.generar_receta()
            if nueva:
                self.ordenes.append(nueva)

    def agregar_chef(self, chef):
        self.chefs.append(chef)

    def generar_receta(self):
        opciones = self.RECETAS_DISPONIBLES.get(self.nivel, [])
        if not opciones:
            return None
        nombre, ingredientes_raw = random.choice(opciones)
        ingredientes = [self.TIPOS[tipo](nombre_ing) for tipo, nombre_ing in ingredientes_raw]
        return Receta(nombre, ingredientes)

    def actualizar(self, delta):
        self.tiempo -= delta

        self.tiempo_ultima_receta += delta
        if self.tiempo_ultima_receta >= self.intervalo_receta and self.tiempo > 0:
            nueva = self.generar_receta()
            if nueva:
                self.ordenes.append(nueva)
            self.tiempo_ultima_receta = 0

        for orden in self.ordenes:
            if not orden.activa:
                continue
            venció = orden.actualizar(delta)   # ahora actualizar() devuelve True si expiró este frame
            if venció:
                penalizacion = 10  # o el valor fijo que quieras, ya que orden.puntos_receta puede ya estar reducido
                for chef in self.chefs:
                    chef.puntos = max(0, chef.puntos - penalizacion)
                print(f"¡Receta expirada! Penalización de -{penalizacion} pts a los chefs.")

        self.ordenes = [o for o in self.ordenes if o.activa]

    def dibujar(self, ventana):
        for chef in self.chefs:
            chef.dibujar(ventana)


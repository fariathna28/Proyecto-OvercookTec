import pygame


# ─────────────────────────────────────────────
#  INGREDIENTE (clase base)
# ─────────────────────────────────────────────
class Ingrediente:
    tiempo_minimo = 5

    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = "crudo"
        self.tiempo_preparacion = 0

    def actualizar_estado(self, delta):
        if self.estado == "crudo":
            self.tiempo_preparacion += delta
            if self.tiempo_preparacion >= self.tiempo_minimo:
                self.estado = "preparado"

    def mostrar(self):
        print(f"{self.nombre} [{self.estado}]")


# ─────────────────────────────────────────────
#  SUBCLASES DE INGREDIENTE
# ─────────────────────────────────────────────
class VegetalesYFrutas(Ingrediente):
    tiempo_minimo = 3

    def actualizar_estado(self, delta):
        super().actualizar_estado(delta)


class PanesYBases(Ingrediente):

    def __init__(self, nombre):
        super().__init__(nombre)
        self.estado = "preparado"   # listos desde la despensa, no necesitan preparación


class Proteina(Ingrediente):
    tiempo_minimo = 5
    tiempo_maximo = 10              # si se supera → quemado

    def __init__(self, nombre):
        super().__init__(nombre)
        self.cocinada = False

    def actualizar_estado(self, delta):
        if self.estado in ("crudo", "preparado"):
            self.tiempo_preparacion += delta
            if self.tiempo_preparacion >= self.tiempo_maximo:   # corregido: era MAX_TIEMPO
                self.estado = "quemado"
                self.cocinada = False
            elif self.tiempo_preparacion >= self.tiempo_minimo: # corregido: era MIN_TIEMPO
                self.estado = "preparado"
                self.cocinada = True


# ─────────────────────────────────────────────
#  RECETA
# ─────────────────────────────────────────────
class Receta:
    def __init__(self, nombre, lista_ingredientes):
        self.nombre = nombre
        self.lista_ingredientes = lista_ingredientes
        self.puntos_receta = len(lista_ingredientes) * 10
        self.max_time_receta = len(lista_ingredientes) * 15
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

    def comparar_receta(self, otra_receta):
        nombres_self = sorted([i.nombre for i in self.lista_ingredientes])
        nombres_otra = sorted([i.nombre for i in otra_receta.lista_ingredientes])
        return nombres_self == nombres_otra

    def __str__(self):
        ingredientes = ", ".join(str(i) for i in self.lista_ingredientes)
        return f"Receta: {self.nombre} | Pts: {self.puntos_receta} | Tiempo: {self.max_time_receta}s | Ingredientes: [{ingredientes}]"


# ─────────────────────────────────────────────
#  ESTACION
# ─────────────────────────────────────────────
class Estacion:
    def __init__(self, nombre, ingredientes_aceptados=None):
        self.nombre = nombre
        self.ingredientes_aceptados = ingredientes_aceptados or []
        self.ingrediente_actual = None
        self.procesando = False

    def aceptar_ingrediente(self, ingrediente):
        tipo = type(ingrediente).__name__
        if tipo in self.ingredientes_aceptados and self.ingrediente_actual is None:
            self.ingrediente_actual = ingrediente
            self.procesando = True
            return True
        return False

    def actualizar(self, delta):
        if self.procesando and self.ingrediente_actual:
            self.ingrediente_actual.actualizar_estado(delta)
            if self.ingrediente_actual.estado in ("preparado", "quemado"):
                self.procesando = False

    def retirar_ingrediente(self):
        ing = self.ingrediente_actual
        self.ingrediente_actual = None
        self.procesando = False
        return ing

    def generar_receta(self):
        return None

    def __str__(self):
        return f"Estación: {self.nombre}"


class EstacionDespensa(Estacion):
    def __init__(self, nombre, ingrediente_clase, nombre_ingrediente):
        super().__init__(nombre)
        self.ingrediente_clase = ingrediente_clase
        self.nombre_ingrediente = nombre_ingrediente

    def entregar_ingrediente(self):
        return self.ingrediente_clase(self.nombre_ingrediente)


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

        # teclas es una tupla: (arriba, abajo, izquierda, derecha)
        self.teclas = teclas
        self.ingrediente_mano = None

        self.imagen = pygame.image.load(imagen_path)
        self.imagen = pygame.transform.scale(self.imagen, (80, 80))

        #Tiles de ingredientes
        self.ingredientes_tiles = {
            "Carne":  pygame.transform.scale(pygame.image.load("tileset/tile13.png"), (40, 40)),
            "Papa":   pygame.transform.scale(pygame.image.load("tileset/tile15.png"),  (40, 40)),
            "Tomate": pygame.transform.scale(pygame.image.load("tileset/tile21.png"),  (40, 40)),
            "Pan":    pygame.transform.scale(pygame.image.load("tileset/tile20.png"), (40, 40)),
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
                if dx < 0:  # moviéndose a la izquierda
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
                if dy < 0:  # moviéndose hacia arriba
                    chef_rect.top = obstaculo.bottom
        

        self.x = chef_rect.x
        self.y = chef_rect.y

    def agarrar(self, estaciones_tiles):
        arriba, abajo, izquierda, derecha, accion = self.teclas
        chef_rect = pygame.Rect(self.x -10, self.y -10, 100, 100)

        for estacion in estaciones_tiles:
            if chef_rect.colliderect(estacion["rect"]):
                return estacion["tipo"]  # devuelve qué estación tocó
        return None

    def dibujar(self, ventana):
        ventana.blit(self.imagen, (self.x, self.y))

        if self.ingrediente_mano:
            nombre = self.ingrediente_mano.nombre
            print(f"Dibujando ingrediente: '{nombre}', en tiles: {list(self.ingredientes_tiles.keys())}")
            if nombre in self.ingredientes_tiles:
                img = self.ingredientes_tiles[nombre]
                ventana.blit(img, (self.x + 40, self.y - 10))

    def __str__(self):
        return f"Chef: {self.nombre} | Pts: {self.puntos}"


# ─────────────────────────────────────────────
#  COCINA
# ─────────────────────────────────────────────
class Cocina:
    RECETAS_DISPONIBLES = {
        "nivel1": [
            ("Hamburguesa", [("Proteina", "Carne"), ("PanesYBases", "Pan"), ("VegetalesYFrutas", "Lechuga")]),
            ("Hot Dog",     [("Proteina", "Salchicha"), ("PanesYBases", "Pan Largo")]),
            ("Ensalada",    [("VegetalesYFrutas", "Tomate"), ("VegetalesYFrutas", "Lechuga")]),
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
        self.estaciones = []
        self.ordenes = []
        self.nivel = nivel
        self.intervalo_receta = 15
        self.tiempo_ultima_receta = 0

    def agregar_chef(self, chef):
        self.chefs.append(chef)

    def agregar_estacion(self, estacion):
        self.estaciones.append(estacion)

    def generar_receta(self):
        import random
        opciones = self.RECETAS_DISPONIBLES.get(self.nivel, [])
        if not opciones:
            return None
        nombre, ingredientes_raw = random.choice(opciones)
        ingredientes = [self.TIPOS[tipo](nombre_ing) for tipo, nombre_ing in ingredientes_raw]
        return Receta(nombre, ingredientes)

    def actualizar(self, delta):
        self.tiempo -= delta

        # Generar receta nueva a intervalos
        self.tiempo_ultima_receta += delta
        if self.tiempo_ultima_receta >= self.intervalo_receta and self.tiempo > 0:
            nueva = self.generar_receta()
            if nueva:
                self.ordenes.append(nueva)
            self.tiempo_ultima_receta = 0

        # Actualizar recetas y descontar puntos si expiran
        for orden in self.ordenes:
            orden.actualizar(delta)

        # Limpiar recetas vencidas
        self.ordenes = [o for o in self.ordenes if o.activa]

        # Actualizar estaciones
        for estacion in self.estaciones:
            estacion.actualizar(delta)

    def dibujar(self, ventana):
        for chef in self.chefs:
            chef.dibujar(ventana)

    def __str__(self):
        return (f"Cocina | Tiempo: {self.tiempo:.1f}s | "
                f"Órdenes activas: {len(self.ordenes)} | "
                f"Chefs: {[c.nombre for c in self.chefs]}")

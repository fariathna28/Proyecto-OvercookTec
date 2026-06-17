import Constantes
import pygame
 
estaciones_tiles = {
    "nivel1": {
        2:  "tabla_picar",
        3:  "estacion_pescado",
        5:  "estacion_arroz",
        6:  "estacion_pepino",
        9:  "estacion_algas",
        15: "freidor",
        16: "entrega",
        23: "cocina",
        24: "estacion_platos",
        0: "mesa",
        39:"mesa_alga",
        20:"mesa_pescado_entero",
        22:"mesa_pescado_cortado",
        21:"mesa_pescado_cocinado",
        25:"mesa_plato_alga",
        27:"mesa_pepino_entero",
        28:"mesa_arroz",
        29:"mesa_pepino_cortado",
        30:"mesa_sushi_pepino"
        

},
    
    "nivel2": {
        3:  "estacion_papas",
        4:  "tabla_picar",
        5:  "estacion_tomates",
        6:  "entrega",
        9:  "freidor",
        18: "estacion_carne",
        27: "estacion_pan",
        36: "estacion_platos",
        45: "cocina",
        0:  "mesa",
        16: "mesa_Carne_cruda",
        15: "mesa_Carne_cocinada_cruda",
        25: "mesa_Tomate_cruda",
        26: "mesa_Tomate_cut_cruda",
        24: "mesa_Pan_cruda",
        22: "mesa_Papa_cruda",
        23: "mesa_Papa_cocinada_cruda",
        34: "mesa_plato_pan_cruda",
        35: "mesa_plato_papa_cruda",
        41: "mesa_plato_pan_carne_cruda",
        40: "mesa_plato_pan_carne2_cruda",
        39: "mesa_plato_pan_carne_tomate_cruda",
        38: "mesa_plato_pan_carne_tomate_papa_cruda",
    },

    "nivel3": {
        2: "tabla_picar",
        3: "estacion_huevos",
        4: "estacion_arroz",
        5: "estacion_frijoles",
        6: "estacion_salchichon",
        7: "estacion_platano",
        47: "estacion_platos",
        10: "freidor",
        11: "entrega",
        42: "cocina",
        0:  "mesa",
        27: "mesa_Platano_crudo",
        29: "mesa_Platano_cocinado",
        30: "mesa_Huevo",
        29: "mesa_Huevo_cocinado",
        31: "mesa_Arroz",
        32: "mesa_Frijoles",
        33: "mesa_Salchichon",
        34: "mesa_Platano",
        39: "mesa_Salchichon_cocinado",
        40: "mesa_Salchichon_crudo",

    }
}
 
obstaculos_tiles = {
    "nivel1": {0, 2, 3, 5, 6, 9, 15, 16, 23, 24},
    "nivel2": {0, 3, 4, 5, 6, 9, 18, 27, 36, 45},
    "nivel3": {0, 2, 3, 4, 5, 6, 7, 9, 10, 42, 38}
}
 
 
class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.obstaculos_tiles = []
        self.estaciones_tiles = []
        # clave: (x, y) topleft en píxeles → imagen a dibujar encima del tile
        self.overlay_tiles = {}
 
    def process_data(self, data, tile_list, nivel):
        estaciones = estaciones_tiles.get(nivel, {})
        obstaculos = obstaculos_tiles.get(nivel, set())
        self.level_length = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * Constantes.TILE_SIZE
                image_y = y * Constantes.TILE_SIZE
                image_rect.topleft = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y, tile, None]
 
                if tile in obstaculos:
                    self.obstaculos_tiles.append(
                        pygame.Rect(image_x, image_y, Constantes.TILE_SIZE, Constantes.TILE_SIZE))
 
                if tile in estaciones:
                    self.estaciones_tiles.append({
                        "tipo": estaciones[tile],
                        "rect": pygame.Rect(image_x, image_y, Constantes.TILE_SIZE, Constantes.TILE_SIZE)
                    })
 
                self.map_tiles.append(tile_data)
 
    def draw(self, surface):
        # 1. Dibujar tiles base
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
        # 2. Dibujar overlays encima (ingredientes sobre estaciones)
        for (ox, oy), imagen in self.overlay_tiles.items():
            surface.blit(imagen, (ox, oy))
 
    def poner_overlay(self, pos_topleft, imagen):
        """Muestra una imagen encima del tile sin modificar el tile base."""
        self.overlay_tiles[pos_topleft] = imagen
 
    def quitar_overlay(self, pos_topleft):
        """Quita el overlay de esa posición."""
        self.overlay_tiles.pop(pos_topleft, None)
 
    def actualizar_estaciones(self, nivel):
        estaciones = estaciones_tiles.get(nivel)
        self.estaciones_tiles = []
        for tile_data in self.map_tiles:
            num_tile = tile_data[4]
            if num_tile in estaciones:
                self.estaciones_tiles.append({
                    "tipo": estaciones[num_tile],
                    "rect": tile_data[1]
                })
 
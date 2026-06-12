import Constantes
import pygame

estaciones_tiles = {
    "nivel1":
    {3: "estacion_papas",
    4: "tabla_picar",
    5: "estacion_tomates",
    6: "entrega",
    9: "freidor",
    18: "estacion_carne",
    27: "estacion_pan",
    36: "estacion_platos",
    45: "cocina"
    }

}
obstaculos_tiles = {
    "nivel1": {0, 3, 4, 5, 6, 9, 18, 27, 36, 45}
}
class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.obstaculos_tiles = []
        self.estaciones_tiles = []


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
                tile_data = [image, image_rect, image_x, image_y]
                
                if tile in obstaculos:
                    self.obstaculos_tiles.append(pygame.Rect(image_x, image_y, Constantes.TILE_SIZE, Constantes.TILE_SIZE))
                
                if tile in estaciones:
                    self.estaciones_tiles.append({
                        "tipo": estaciones[tile],
                        "rect": pygame.Rect(image_x, image_y, Constantes.TILE_SIZE, Constantes.TILE_SIZE)})

                self.map_tiles.append(tile_data)

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
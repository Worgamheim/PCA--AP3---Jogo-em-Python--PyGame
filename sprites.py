import pygame
import json

class Sprite:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.sprites = pygame.image.load(arquivo).convert()
        self.meta_data = self.arquivo.replace("png","json")
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()


    def getSprite(self,x,y,largura,altura):
        sprite = pygame.Surface((largura, altura))
        sprite.set_colorkey((255,0,255))
        sprite.blit(self.sprites, (0,0), (x, y, largura, altura))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, largura, altura = sprite["x"], sprite["y"], sprite["largura"], sprite["altura"]
        image = self.getSprite(x, y, largura, altura)
        return image
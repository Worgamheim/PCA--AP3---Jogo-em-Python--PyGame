import pygame
import constantes
from sprites import Sprite
import os
import random

class Game:
    def __init__(self):
        #criando a tela do jogo
        pygame.init()
        pygame.mixer.init()
        self.canvas = pygame.Surface((constantes.LARGURA, constantes.ALTURA))
        self.tela = pygame.display.set_mode((constantes.LARGURA, constantes.ALTURA))
        pygame.display.set_caption(constantes.TITULO_JOGO)
        self.relogio = pygame.time.Clock()
        self.esta_rodando = True
        self.fonte = pygame.font.match_font(constantes.FONTE)
        self.carregar_arquivos()
        self.telaInicialAnim = 0
        #personagem
        self.index = 0
        self.x = 0
        self.y = 0
        self.velocidade = 4
        self.sentido = 0 #0 baixo, 4 esquerda, 8 direita, 12 cima
        #pontuacao
        self.pontuacao = 0
        self.reciclados = {
            "vidro": {
                "quantidade" : 0,
                "Kg" : 0
            },
            "papel": {
                "quantidade" : 0,
                "Kg" : 0
            },            
            "plastico": {
                "quantidade" : 0,
                "Kg" : 0
            },
            "metal": {
                "quantidade" : 0,
                "Kg" : 0
            }
        
        }
        

    def novo_jogo(self):
        #instancia as classes das sprites do jogo
        self.todas_as_sprites = pygame.sprite.Group()
        pygame.mixer.music.load(os.path.join(self.diretorio_audios, constantes.MUSICA_JOGO))
        pygame.mixer.music.play(-1)
        self.rodar()
    
    def rodar(self):
        #loop do jogo
        self.jogando = True
        while self.jogando:
            self.relogio.tick(constantes.FPS)
            self.eventos()
            self.atualizar_sprites()
            self.desenhar_sprites()

    def eventos(self):
        #define os eventos do jogo
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.esta_rodando = False

        self.relogio.tick(constantes.FPS)
        keys=pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.y += self.velocidade
            self.sentido = 0
            self.index = (self.index + 0.3) % 4 + self.sentido
        elif keys[pygame.K_LEFT]:
            self.x -= self.velocidade
            self.sentido = 4
            self.index = (self.index + 0.3) % 4 + self.sentido
        elif keys[pygame.K_RIGHT]:
            self.x += self.velocidade
            self.sentido = 8
            self.index = (self.index + 0.3) % 4 + self.sentido
        elif keys[pygame.K_UP]:
            self.y -= self.velocidade
            self.sentido = 12
            self.index = (self.index + 0.3) % 4 + self.sentido
        if keys[pygame.K_SPACE]:
            if self.lixosAtual < 0:
                if self.lixoXY[0] <= 194 or self.lixoXY[0] > 264:
                    colisaoY = self.lixoXY[1] - self.y
                    if colisaoY >= -32 and colisaoY <= 32:
                        if self.lixoXY[0] >= (self.x - 32) and self.lixoXY[0] <= (self.x + 32):
                            #pegou
                            self.lixosAtual = random.randint(0, len(self.lixos)-1)
                            self.lixoXY[0] = -128.0
                            self.lixoXY[1] = 300.0
            else:
                #verde      0   - 32    vidro       index 0
                #azul       33  - 84    papel       index 1
                #vermelha   85  - 136   plastico    index 2
                #amarelo    137 - 188   metal       index 3
                if self.y > 320:
                    if self.x >= 0 and self.x <= 32: #verde
                        if self.lixosAtual == 0:      #vidro
                            self.lixosAtual = -1
                            self.pontuacao += 1
                            self.reciclados['vidro']['quantidade'] += 1
                        else:
                            self.lixosAtual = -1
                            self.pontuacao -= 1

                    if self.x >= 33 and self.x <= 84: #azul
                        if self.lixosAtual == 1:       #papel
                            self.lixosAtual = -1
                            self.pontuacao += 1
                            self.reciclados['papel']['quantidade'] += 1
                        else:
                            self.lixosAtual = -1
                            self.pontuacao -= 1

                    if self.x >= 85 and self.x <= 136: #vermelho
                        if self.lixosAtual == 2:        #plastico
                            self.lixosAtual = -1
                            self.pontuacao += 1
                            self.reciclados['plastico']['quantidade'] += 1
                        else:
                            self.lixosAtual = -1
                            self.pontuacao -= 1

                    if self.x >= 137 and self.x <= 188: #amarelo
                        if self.lixosAtual == 3:         #metal
                            self.lixosAtual = -1
                            self.pontuacao += 1
                            self.reciclados['metal']['quantidade'] += 1
                        else:
                            self.lixosAtual = -1
                            self.pontuacao -= 1

    def atualizar_sprites(self):
        #atualizar sprites
        self.todas_as_sprites.update()

    def desenhar_sprites(self):
        #desenhar sprites
        self.tela.fill(constantes.PRETO) #limpando a tela
        self.todas_as_sprites.draw(self.tela) #desenhando as sprites
        self.tela.blit(self.cenario, (0,0))
        self.tela.blit(self.lixo[int(self.lixoAtual)], (int(self.lixoXY[0]), int(self.lixoXY[1])))
        self.lixoXY[0] += 2
        self.lixoXY[1] = self.lixoXY[1] + random.uniform(-1.1, 1.0)
        if self.lixoXY[0] > constantes.LARGURA - 128:
           self.lixoXY[1] = self.lixoXY[1] + random.uniform(1.0, 2.0) 
        if self.lixoXY[0] > constantes.LARGURA:
            self.lixoXY[0] = -128.0
            self.lixoXY[1] = 300.0
        self.lixoAtual += 0.1
        if self.lixoAtual > len(self.lixo):
            self.lixoAtual = 0

        self.tela.blit(self.ponte, (212, 44))

        for x in range(0,4): 
            self.tela.blit(self.lixeiras[x], ((x*64)+5, constantes.ALTURA - 110))
        
        self.tela.blit(self.personagem[int(self.index)], (self.x, self.y))

        if self.lixosAtual >= 0:
            self.tela.blit(self.lixos[self.lixosAtual], (4, 4))

        pygame.draw.rect( self.tela, constantes.PRETO, pygame.Rect(constantes.LARGURA -120, 20, 100, 40)) 
        self.mostrar_texto('$ '+str(self.pontuacao), 32, constantes.BRANCO, constantes.LARGURA -100, 20)

        #debug
        #self.mostrar_texto('boneco y:'+str(self.y)+'  lixo y:'+str(int(self.lixoXY[1])), 24, constantes.PRETO, constantes.LARGURA / 2, 20)
        pygame.display.flip()
    
    def carregar_arquivos(self):
        #Carregar os arquivos de audio e imagens
        diretorioImagens = os.path.join(os.getcwd(), 'imagens')
        self.diretorio_audios = os.path.join(os.getcwd(), 'audios')
        #self.spritesheet = os.path.join(diretorioImagens, constantes.SPRITESHEET)
        self.telaInicial = []
        for x in range(1,9,1):
            tempImagem = os.path.join(diretorioImagens, "telaInicial\{}.png".format(x))
            tempImagem = pygame.image.load(tempImagem).convert()
            tempImagem = pygame.transform.scale(tempImagem,(constantes.LARGURA, constantes.ALTURA))
            self.telaInicial.append(tempImagem)
        self.cenario = os.path.join(diretorioImagens, constantes.CENARIO)
        self.cenario = pygame.image.load(self.cenario).convert()
        self.ponte = os.path.join(diretorioImagens, constantes.PONTE)
        self.ponte = pygame.image.load(self.ponte).convert()
        self.spritePersonagem = os.path.join(diretorioImagens, constantes.SPRITEPERSONAGEM)
        minhaSprite = Sprite(self.spritePersonagem)
        self.personagem = [
                            minhaSprite.parse_sprite("pBaixo1.png"),
                            minhaSprite.parse_sprite("pBaixo2.png"),
                            minhaSprite.parse_sprite("pBaixo3.png"),
                            minhaSprite.parse_sprite("pBaixo4.png"),
                            minhaSprite.parse_sprite("pEsquerda1.png"),
                            minhaSprite.parse_sprite("pEsquerda2.png"),
                            minhaSprite.parse_sprite("pEsquerda3.png"),
                            minhaSprite.parse_sprite("pEsquerda4.png"),
                            minhaSprite.parse_sprite("pDireita1.png"),
                            minhaSprite.parse_sprite("pDireita2.png"),
                            minhaSprite.parse_sprite("pDireita3.png"),
                            minhaSprite.parse_sprite("pDireita4.png"),
                            minhaSprite.parse_sprite("pCima1.png"),
                            minhaSprite.parse_sprite("pCima2.png"),
                            minhaSprite.parse_sprite("pCima3.png"),
                            minhaSprite.parse_sprite("pCima4.png")                                                                                    
                          ]
        self.spriteLixo = os.path.join(diretorioImagens, constantes.SPRITELIXO)
        minhaSprite = Sprite(self.spriteLixo)
        self.lixo = [
                            minhaSprite.parse_sprite("lixo1.png"),
                            minhaSprite.parse_sprite("lixo2.png"),
                            minhaSprite.parse_sprite("lixo3.png"),
                            minhaSprite.parse_sprite("lixo4.png")
                    ]                    
        self.lixoAtual = 0
        self.lixoXY = [-128.0, 300.0]

        self.lixos = []

        self.spriteVidro = os.path.join(diretorioImagens, constantes.SPRITEVIDRO)
        minhaSprite = Sprite(self.spriteVidro)
        self.lixos.append(minhaSprite.parse_sprite("vidro.png"))

        self.spritePapel = os.path.join(diretorioImagens, constantes.SPRITEPAPEL)
        minhaSprite = Sprite(self.spritePapel)
        self.lixos.append(minhaSprite.parse_sprite("papel.png"))

        self.spritePlastico = os.path.join(diretorioImagens, constantes.SPRITEPLASTICO)
        minhaSprite = Sprite(self.spritePlastico)
        self.lixos.append(minhaSprite.parse_sprite("plastico.png"))

        self.spriteMetal = os.path.join(diretorioImagens, constantes.SPRITEMETAL)
        minhaSprite = Sprite(self.spriteMetal)
        self.lixos.append(minhaSprite.parse_sprite("metal.png"))

        #self.spriteOrganico = os.path.join(diretorioImagens, constantes.SPRITEORGANICO)
        #minhaSprite = Sprite(self.spriteOrganico)
        #self.lixos.append(minhaSprite.parse_sprite("organico.png"))


        self.lixosAtual = -1

        self.spriteLixeiras = os.path.join(diretorioImagens, constantes.SPRITELIXEIRAS)
        minhaSprite = Sprite(self.spriteLixeiras)
        self.lixeiras = [
                            minhaSprite.parse_sprite("lixeira1.png"),
                            minhaSprite.parse_sprite("lixeira2.png"),
                            minhaSprite.parse_sprite("lixeira3.png"),
                            minhaSprite.parse_sprite("lixeira4.png")
                    ]
        #self.todas_as_sprites.add(personagem)
        

    def mostrar_texto(self, texto, tamanho, cor, x, y):
        #Exibe um texto na tela do jogo
        fonte = pygame.font.Font(self.fonte, tamanho)
        texto = fonte.render(texto, True, cor)
        texto_rect = texto.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto, texto_rect)

    def mostrar_start_logo(self):
        self.telaInicialAnim = self.telaInicialAnim + 0.15
        if self.telaInicialAnim >= len(self.telaInicial):
            self.telaInicialAnim = 0
        self.tela.blit(self.telaInicial[int(self.telaInicialAnim)], (0,0))
        self.mostrar_texto( 
            '-Pressione [ENTER] para jogar',
            32,
            constantes.BRANCO,
            constantes.LARGURA / 2,
            320
        )   
        self.mostrar_texto( 
            'PCA - Sustentabilidade',
            19,
            constantes.BRANCO,
            constantes.LARGURA / 2,
            570
        )   
        pygame.display.flip()

    def mostrar_tela_start(self):
        pygame.mixer.music.load(os.path.join(self.diretorio_audios, constantes.MUSICA_START))
        pygame.mixer.music.play(-1)

        self.mostrar_start_logo()

        self.esperar_por_jogador()
    
    def esperar_por_jogador(self):
        esperando = True
        while esperando:
            self.relogio.tick(constantes.FPS)
            self.mostrar_start_logo()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                    self.esta_rodando = False
                if evento.type == pygame.KEYUP:
                    if evento.key == pygame.K_RETURN:
                        esperando = False
                        pygame.mixer.music.stop()         
                        pygame.mixer.Sound(os.path.join(self.diretorio_audios, constantes.TECLA_START)).play() 

    def mostrar_tela_game_over(self):
        pass

jogo = Game()
jogo.mostrar_tela_start()

while jogo.esta_rodando:
    jogo.novo_jogo()
    jogo.mostrar_tela_game_over()
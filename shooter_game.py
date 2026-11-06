# ¡Crea tu propio juego de disparos!
from random import randint
from pygame import *

init()

#Constantes
ANCHO = 800
ALTO = 500
FPS = 30

# Crear pantalla
pantalla = display.set_mode((ANCHO, ALTO))
# Titulo
display.set_caption('El Disparador')

clock = time.Clock()
FPS = 60

# Fondo
background = transform.scale(image.load('galaxy.jpg'), (ANCHO, ALTO))

# MUSICA DE FONDO


# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self):
        pantalla.blit(self.image, (self.rect.x, self.rect.y))

    def isCollision(self, object):
        return self.rect.colliderect(object.rect)
            
# Listas
Isloser = False
enemigos = []
bullets = []
contador = 0

class Bullet(GameSprite):
    def moveUp(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            if self in bullets:
                bullets.remove(self)
            

class Player(GameSprite):

    def moves(self):
        Keys = key.get_pressed()

        if (Keys[K_a] or Keys[K_LEFT]) and self.rect.x > 0:
            self.rect.x -= self.speed
        elif (Keys[K_d] or Keys[K_RIGHT]) and self.rect.x < ANCHO - self.rect.width:
            self.rect.x += self.speed

    def shoot(self):
            bullet = Bullet('bullet.png', self.rect.x + 10, self.rect.y - 20, 30, 20, 5)
            bullets.append(bullet)
            mixer.music.load('fire.ogg')
            mixer.music.play() #sonido de disparo

class Enemy(GameSprite):
    def moveDown(self):
        self.rect.y += self.speed
        if self.rect.y > ALTO + 20:
            self.rect.y = 0

# FUNCIONES
def setTextos(text, size, fuente = 'Arial', coors = (0, 0), color = (255, 255, 255)):
    sysfont = font.SysFont(fuente, size)
    render = sysfont.render(text, '', color)
    pantalla.blit(render, coors)



#OBJEtos
player = Player('rocket.png', 370, 420, 50, 50, 5)


# Creacion de enemigos
def generarEnemigos():
    for i in range(randint(4, 10)):
        tmpSpeed = randint(1, 5)
        tmpX = randint(0, ANCHO)
        enemigo = Enemy('ufo.png', tmpX, 0, 50, 50, tmpSpeed)
        enemigos.append(enemigo)

#FONDOS
background = transform.scale(image.load('galaxy.jpg'), (ANCHO, ALTO))

game_over = False
isLoser = False
starButton = False

while not game_over:

    for evento in event.get():
        if evento.type == QUIT:
            game_over = True
        if evento.type == KEYDOWN:
            if evento.key == K_SPACE and not isLoser:
                player.shoot()
            if evento.key == K_t:
                starButton = True
                generarEnemigos()
    
    pantalla.blit(background,(0, 0))

    if starButton:
        #mostrar jugador
            if not isLoser:
                player.reset()
                player.moves()
            else:
                setTextos('Perdiste', 50, coors= (ANCHO / 3, ALTO / 2), color = (217,45, 11))
        
            # mostrar enemigos
            for enemy in enemigos:
                enemy.reset()
                enemy.moveDown()
        
                ## mostrar balas
                for bullet in bullets:
                    bullet.reset()
                    bullet.moveUp()
        
                    #Colision de balas enemigos
                    if bullet.isCollision(enemy):
                        if enemy in enemigos:
                            enemigos.remove(enemy)
                        if bullet in bullets:
                            bullets.remove(bullet)
                        contador += 1
        
                if enemy.isCollision(player):
                    isLoser = True

            if contador > 8:
                setTextos('Ganaste', 50, coors= (ANCHO / 3, ALTO / 2), color = (0 , 255, 0))
                # pantalla.blit(textvictory, (ANCHO/ 2, ALTO / 2))

    else:
        setTextos('Presione T para Iniciar', 50, coors= (ANCHO / 5, ALTO / 2))

    #actualizar juego
    display.update()
    clock.tick(FPS)


import pygame, math
import pygame
from pygame.locals import *
import os
import sys
import random

size = width, height = 1300, 600 
GANE = "!!! HAS PERDIDOO !!!"
PROTECCION = "NO PROTEGIDO"
estadoanimo = "normal"
IMG_DIR = "imagenes"
SONIDO_DIR = "sonidos"
maxintento = 3
intentos = maxintento
MUERTEALPANDA = 0
mostrar = 1

def printos(surface, text, x, y, color, font):
    text_in_lines = text.split('\n')
    for line in text_in_lines:
        new = font.render(line, 1, color)
        surface.blit(new, (x, y))
        y += new.get_height()
 
def arrow(screen, color, x, y, ang):
    pygame.draw.line(screen, color, (x, y), (x + 20*math.cos(math.radians(ang + 150.0)), y - 20*math.sin(math.radians(ang + 150.0))),5)
    pygame.draw.line(screen, color, (x, y), (x + 20*math.cos(math.radians(ang + 210.0)), y - 20*math.sin(math.radians(ang + 210.0))),5)
 
def vector(screen, color, x, y, ang):
    w, z = x + v0*10*math.cos(math.radians(ang)), y - v0*10*math.sin(math.radians(ang))
    x, y, w, z = int(x), int(y), int(w), int(z)
    arrow(screen, color, w, z, ang)
    pygame.draw.line(screen, blue, (x, y), (w, z),5)

def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print ("Error, no se puede cargar la imagen: ", ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image
 
 
def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
        sonido = pygame.mixer.Sound(ruta)
    except pygame.error:
        print ("No se pudo cargar el sonido:", ruta)
        sonido = None
    return sonido
 
class Pelota(pygame.sprite.Sprite):
  #  "La bola y su comportamiento en la pantalla"
 
    def __init__(self,sonido_chidori,sonido_gane, sonido_pola):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bola.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = 10
        self.rect.centery = 600 - 10
        self.sonido_gane = sonido_gane
        self.sonido_chidori = sonido_chidori
        self.sonido_pola = sonido_pola
        
 
    def update(self, posx, posy):
       
        self.rect.centerx = posx
        self.rect.centery = posy
 
    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            
            self.sonido_gane.play()  # Reproducir sonido de rebote
            self.sonido_pola.stop()
            return "!!! HAS GANADO !!!"
        return "!!! HAS PERDIDOO !!!"
    
    def colisionescudo(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            
            self.sonido_chidori.play()  # Reproducir sonido de rebote
            return "PROTEGIDO"
        return "NO PROTEGIDO"

class Paleta(pygame.sprite.Sprite):
   # "Define el comportamiento de las paletas de ambos jugadores"
 
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("Pangoro.png", IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = 1250
        self.rect.centery = height / 2
        self.speed = [0, 5]
 
    def cpu(self):
       
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1]))
    def feliz(self):
        self.image = load_image("Panda.png", IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = 1250
        self.rect.centery = height / 2
        self.speed = [0, 10]
    def normal(self):
        self.image = load_image("Pangoro.png", IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = 1250
        self.rect.centery = height / 2
        self.speed = [0, 5]
    

class Pola(pygame.sprite.Sprite):
   # "Define el comportamiento de las paletas de ambos jugadores"
 
    def __init__(self,sonido_pola,daza,escudo,rayos, sonido_polaabrir):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("pola.png", IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = 650
        self.rect.centery = height / 2
        self.sonido_pola = sonido_pola
        self.daza = daza
        self.escudo = escudo
        self.rayos = rayos
        self.sonido_polaabrir = sonido_polaabrir
        
 
    def cambio(self):
       
        self.rect.centerx = random.randint(0, 900)
        self.rect.centery = random.randint(0, (height-radio-100))

    def colision(self, objetivo):
        if self.rect.colliderect(objetivo.rect):
            #self.sonido_polaabrir.play()
            self.sonido_pola.play()  # Reproducir sonido de rebote
            self.escudo.feliz()
            self.daza.feliz()
            self.rayos.feliz()
            return "feliz"
        return "normal"
        


class Escudo(pygame.sprite.Sprite):
 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("escudo.png", IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = 1050
        self.rect.centery = height / 2
        self.speed = [0, 5]

    def feliz(self):
        self.rect.centerx = 1050
        self.rect.centery = height + 600
        
        
    def normal(self):
        self.rect.centerx = 1050
        self.rect.centery = height / 2
        self.speed = [0, 5]
        
    def cpu(self):
       
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1]))
class Rayos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("rayos.png", IMG_DIR, alpha=True)
        self.image = pygame.transform.scale(self.image, (250, 250))
        self.rect = self.image.get_rect()
        self.rect.centerx = 1050
        self.rect.centery = height / 2
        self.speed = [0, 5]

    def feliz(self):
        self.rect.centerx = 1050
        self.rect.centery = height + 600
        
        
    def normal(self):
        self.rect.centerx = 1050
        self.rect.centery = height / 2
        self.speed = [0, 5]
        
    def cpu(self):
       
        if self.rect.top < (-50) or self.rect.bottom > (height+50):
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1]))
        
class Matastealpanda(pygame.sprite.Sprite):
 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("gane.png", IMG_DIR, alpha=True)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = height
        self.rect.centery = height / 2
class Pandagana(pygame.sprite.Sprite):
 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("pierde.png", IMG_DIR, alpha=True)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = height
        self.rect.centery = height / 2
  
 
pygame.init() 
 

 
black = (0, 0, 0)
blue = (0, 0, 0)
green = (0, 255, 0)
background = (255, 255, 255)
 
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Tiro_al_Panda") 
 
 
radio = 10
x = 10
y = height - radio
 
pygame.font.init() 
font = pygame.font.Font(None, 30) 
 
clock = pygame.time.Clock()
 
t = 0.0
dt = 0.3
 
v0 = 25.0
a = 1.0
ang = 45.0
 
vx = 0
vy = 0
 
lock = True
lock1 = False
second = False


sonido_chidori = load_sound("chidori.ogg", SONIDO_DIR)
sonido_pola = load_sound("one_piece.ogg", SONIDO_DIR)
sonido_gane = load_sound("gane.ogg", SONIDO_DIR)
sonido_polaabrir = load_sound("pola.ogg", SONIDO_DIR)
fondo = load_image("bambu.png", IMG_DIR, alpha=True)
fondo = pygame.transform.scale(fondo, (1300, 700))

bola = Pelota(sonido_chidori, sonido_gane,sonido_pola)
daza = Paleta(300)
escudo = Escudo()
rayos = Rayos()
pola = Pola(sonido_pola,daza,escudo,rayos,sonido_polaabrir)
ganador = Matastealpanda()
perdedor = Pandagana()



#daza.resize(200,200)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
cambiopola=0
superestado=0
posenx = 0
activaproteccion = 0
tiemporayos = 0
duracionrayos = 0
while 1:

    cambiopola =cambiopola+1;
    if cambiopola == 100 :
        cambiopola=0
        pola.cambio()
    
    clock.tick(60)
    pos_mouse = pygame.mouse.get_pos()
    mov_mouse = pygame.mouse.get_rel()
    daza.cpu()
    escudo.cpu()
    rayos.cpu()
    bola.update(int(x),int(y))
    if GANE == "!!! HAS PERDIDOO !!!" :
        GANE = bola.colision(daza)
        PROTECCION = bola.colisionescudo(escudo)
    else :
        MUERTEALPANDA = 1
        
    if estadoanimo == "normal" :
        if activaproteccion ==0 :
            estadoanimo = pola.colision(bola)
    if estadoanimo == "feliz" :
        
        superestado =superestado+1;
        if superestado == 570 :
            superestado=0
            estadoanimo = "normal"
            daza.normal()
            escudo.normal()
            rayos.normal()
            
            
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        if mov_mouse[1] != 0:
            if lock :
                posxs = pos_mouse[0]

                posys = pos_mouse[1]
                if posxs > (width -500):
                    posxs = (width -500)
                if estadoanimo == "feliz" :
                    if posxs > ((width -500) /2):
                        posxs = ((width -500) /2)
                
                if posxs > 0:
                    ang=math.degrees(math.atan(((height-posys)/ posxs)))
                    v0 =math.sqrt((math.pow((height-posys - radio),2)+math.pow((posxs),2)))/10
               # ddddd=math.atan((pos_mouse[1]/ pos_mouse[0]))
    teclado = pygame.key.get_pressed()


    
    if(tuple(set(teclado)) == (0,1) and lock):
        if (teclado[pygame.K_SPACE]):
            print ("Disparo...")
            lock = False
            lock1 = True
            vy0 = v0*math.sin(math.radians(ang))
    if (teclado[pygame.K_ESCAPE]):
        print ()
        break
    vx0 = v0*math.cos(math.radians(ang))
    vy = a*t - v0*math.sin(math.radians(ang))

    if(lock1):
        y = (height - radio) - vy0*t + .5*a*(t**2)
        if PROTECCION == "NO PROTEGIDO" :
            if activaproteccion ==0 :
                x = radio + vx0*t
                posenx = x
            else :
                x = posenx +(posenx - radio - vx0*t)
        else :
            activaproteccion=1
            x = posenx +(posenx - radio - vx0*t)
            
           
        t += dt
        if(y > (height - radio) or x > (width - radio) or x < 0 ):
            y = height - radio
            x=radio
            t = 0
            lock1 = False
            second = True
    if(second):
        if GANE == "!!! HAS PERDIDOO !!!":
            
            if intentos == 0 :
                printos(screen, GANE , 0, 40, green, font)
                mensage = "Ha eso se le llama se malo"
            else :
                mensage = 'Continuar Y/N Intentos restante '+str(intentos)
            printos(screen, mensage, 0, 60, green, font)
        if(True):
            if MUERTEALPANDA == 0 and intentos > -1  :
                lock = True
                second = False
                x = radio
                GANE = "!!! HAS PERDIDOO !!!"
                intentos=intentos-1
                posenx = 0
                activaproteccion =0
                duracionrayos = 0
                ROTECCION = "NO PROTEGIDO"
                #estadoanimo = "normal"
            elif(teclado[pygame.K_y]):
                GANE = "!!! HAS PERDIDOO !!!"
                intentos = (maxintento + 1)
                sonido_pola.stop
                superestado=0
                estadoanimo = "normal"
                daza.normal()
                escudo.normal()
                rayos.normal()
                MUERTEALPANDA = 0
                sonido_gane.stop()
            
        
        elif(teclado[pygame.K_n]):
            break
 
   # printos(screen, "x = %d y = %d ang = %d v0 = %d vx = %d vy = %d"%(x - radio, height - radio - y, ang, v0, vx0, vy), 0, 0, green, font)
    
    #pygame.draw.circle(screen, blue, (int(x), int(y)), radio)
    screen.blit(fondo, (0, 0))
    if intentos > -1  :
        if MUERTEALPANDA == 0 :
            if estadoanimo == "normal" :
                if lock :
                    vector(screen, blue, x, y, ang)
                if duracionrayos < 8 :
                    if activaproteccion == 1 :
                        
                        if tiemporayos < 4:
                            todos = pygame.sprite.RenderPlain(bola,daza,pola,escudo,rayos)
                        else :
                            todos = pygame.sprite.RenderPlain(bola,daza,pola,escudo)
                        if tiemporayos == 8:
                            tiemporayos = 0
                            duracionrayos =  duracionrayos +1
                        tiemporayos = tiemporayos + 1
                    else :
                       todos = pygame.sprite.RenderPlain(bola,daza,pola,escudo)
            elif estadoanimo == "feliz" :
            
                todos = pygame.sprite.RenderPlain(bola,daza)
                if lock :
                    vector(screen, blue, x, y, ang)
        else :
            sonido_pola.stop()
            todos = pygame.sprite.RenderPlain(ganador)
            
    else :
        todos = pygame.sprite.RenderPlain(perdedor)
        sonido_pola.stop()
        if(teclado[pygame.K_y]):
            sonido_pola.stop()
            GANE = "!!! HAS PERDIDOO !!!"
            intentos = maxintento
            superestado=0
            estadoanimo = "normal"
            daza.normal()
            escudo.normal()
            rayos.normal()
            MUERTEALPANDA = 0
            
    if intentos == 0 :
        mensage = '!!!!ULTIMO INTENTO ANIMO!!!! '
    else :
        mensage = 'INTENTOS RESTANTES '+str(intentos)
    printos(screen, mensage, 40, 60, blue, font)
    todos.draw(screen)
    if mostrar == 3 :
        
        if lock :
            print("PosX = %d PosY = %d Angulo = %d V0 = %d Vx = %d Vy = %d"%(x - radio, height - radio - y, ang, v0, vx0, vy*-1))
        else :
            print("PosX = %d PosY = %d t = %d Angulo = %d V0 = %d Vx = %d Vy = %d"%(x - radio, height - radio - y, t, ang, v0, vx0, vy*-1))
        mostrar=0
    mostrar=mostrar+1
    pygame.display.flip()
    clock.tick(30)

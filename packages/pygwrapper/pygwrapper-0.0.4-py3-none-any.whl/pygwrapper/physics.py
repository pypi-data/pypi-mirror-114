import pygame,pymunk,os
class DummyFrame:
    def __init__(self,x,y,img,screen):
        self.image = pygame.image.load(img)
        self.screen = screen


class BoxBasedSprite(DummyFrame):
    def __init__(self,x,y,img,screen,space,body_type):
        super().__init__(x,y,img,screen)
        self.body = pymunk.Body(1,100,body_type=body_type)
        self.body.position = (x,y)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.body.shape = pymunk.Poly.create_box(self.body, (self.rect.width, self.rect.height))
        self.img_frames = []
        self.current_frame = 0
        self.is_animate = False
        space.add(self.body, self.body.shape)
    def show(self):
        self.screen.blit(self.image,(int(self.body.position.x),int(self.body.position.y)))
        self.rect.x,self.rect.y = int(self.body.position.x),int(self.body.position.y)
        pygame.draw.rect(self.screen,(0,0,0),self.rect,1)
    def animation_setup(self,path):
        for  fl in os.listdir(path):
            self.img_frames.append(fl)
    def animate(self,framerate):
        self.rect.x,self.rect.y = int(self.body.position.x),int(self.body.position.y)
        if self.is_animate:
            if self.current_frame < len(self.img_frames):
                self.current_frame += framerate/1000
                self.screen.blit(self.img_frames[int(self.current_frame)],(int(self.body.position.x),int(self.body.position.y)))
            else:
                self.current_frame = 0

class RectBasedSprite(DummyFrame):
    def __init__(self,x,y,img,screen,space,body_type):
        super().__init__(x,y,img,screen)
        self.body = pymunk.Body(1,100,body_type=body_type)
        self.body.position = (x,y)
        self.rect = self.image.get_rect(topleft=(x,y))
        self.vertices = ((self.x,self.y),(self.x+self.width,self.y),(self.x,self.y+self.height),(self.x+self.width,self.y+self.height))
        self.shape = pymunk.Poly(self.body,self.vertices)
        self.img_frames = []
        self.current_frame = 0
        self.is_animate = False
        space.add(self.body, self.body.shape)
    def show(self):
        self.screen.blit(self.image,(int(self.body.position.x),int(self.body.position.y)))
        self.rect.x,self.rect.y = int(self.body.position.x),int(self.body.position.y)
        pygame.draw.rect(self.screen,(0,0,0),self.rect,1)
    def animation_setup(self,path):
        for  fl in os.listdir(path):
            self.img_frames.append(fl)
    def animate(self,framerate):
        self.rect.x,self.rect.y = int(self.body.position.x),int(self.body.position.y)
        if self.is_animate:
            if self.current_frame < len(self.img_frames):
                self.current_frame += framerate/1000
                self.screen.blit(self.img_frames[int(self.current_frame)],(int(self.body.position.x),int(self.body.position.y)))
            else:
                self.current_frame = 0

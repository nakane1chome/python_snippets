import numpy
import pygame 
from pygame import surfarray

# Capture image data as array
DATA = numpy.array((
    (3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3),
    (3,3,3,3,3,3,0,0,0,0,3,3,3,3,3,3),
    (3,3,3,3,0,0,1,1,1,1,0,0,3,3,3,3),
    (3,3,3,0,1,1,1,1,1,1,1,1,0,3,3,3),
    (3,3,0,1,2,2,1,1,1,1,2,2,1,0,3,3),
    (3,3,0,1,2,2,1,1,1,1,2,2,1,0,3,3),
    (3,0,1,1,1,1,1,1,1,1,1,1,1,1,0,3),
    (3,0,1,1,1,1,1,1,1,1,1,1,1,1,0,3),
    (3,0,1,1,2,1,1,1,1,1,1,2,1,1,0,3),
    (3,0,1,1,2,2,2,2,2,2,2,2,1,1,0,3),
    (3,3,0,1,1,2,2,2,2,2,2,1,1,0,3,3),
    (3,3,0,1,1,1,2,2,2,2,1,1,1,0,3,3),
    (3,3,3,0,1,1,1,1,1,1,1,1,0,3,3,3),
    (3,3,3,3,0,0,1,1,1,1,0,0,3,3,3,3),
    (3,3,3,3,3,3,0,0,0,0,3,3,3,3,3,3),
    (3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3),
), dtype=numpy.ubyte)

# Palette for above image
WHITE=(255,255,255)
BLACK=(0,0,0)
YELLOW=(255,255,0)
BLUE=(0, 0, 255)
PALETTE=(
    BLACK,
    YELLOW,
    BLUE,
    WHITE
)

# Placeholder
VBL=pygame.event.Event(0)

def get_icon(screen, data, palette, scale=None):
    """ Convert byte array to pygame surface
    """
    array_img = numpy.rot90(data, k=1)
    surf0 = pygame.Surface(array_img.shape[:2], flags=0, depth=8)
    surf0.set_palette(palette)
    pygame.pixelcopy.array_to_surface(surf0, array_img)
    surf1= surf0.convert(screen)
    if scale is None:
        return surf1
    return pygame.transform.scale(surf1, [x * scale for x in array_img.shape])

class Object:
    """ Simple model for object motion
    """
    def __init__(self, size, bounds):
        self._pos = [0.0, 0.0]
        self._speed = [0.0, 0.0]
        self._bounds = (bounds[0] - size[0], bounds[1] - size[1])

    def incr_x_speed(self, v):
        self._speed[0] += v

    def incr_y_speed(self, v):
        self._speed[1] += v
    
    def update(self):
        for xy in (0,1):
            self._pos[xy] += self._speed[xy]
            if self._pos[xy] < 0:
                self._pos[xy] = 0
                self._speed[xy] *= -1
            elif self._pos[xy] > self._bounds[xy]:
                self._pos[xy] = self._bounds[xy]
                self._speed[xy] *= -1
        return (int(self._pos[0]), int(self._pos[1]))

def main():
    # Event loop update rate
    hz = 50
    # Display size
    dim = (512, 512)
    # Setup screen
    screen = pygame.display.set_mode(dim, flags=0, depth=32)
    # Object to display
    icon = get_icon(screen, DATA, PALETTE, 2)
    obj = Object(icon.get_size(), dim)
    # Window title
    pygame.display.set_caption("Pygame Core Loop Test")
    # Event loop frame timer
    pygame.time.set_timer(VBL, int(1000.0/hz)) 

    while True:
        e = pygame.event.wait()

        # Input handlers
        if e.type == pygame.MOUSEBUTTONDOWN: 
            break
        elif e.type == pygame.KEYDOWN :
            if e.key == pygame.K_q:
                break
            elif e.key == pygame.K_LEFT:
                obj.incr_x_speed(-1)
            elif e.key == pygame.K_RIGHT:
                obj.incr_x_speed(1)
            elif e.key == pygame.K_UP:
                obj.incr_y_speed(-1)
            elif e.key == pygame.K_DOWN:
                obj.incr_y_speed(1)
            elif e.key == pygame.K_s:
                pygame.image.save(screen, name+'.png')
        elif e.type == pygame.QUIT:
            break

        # Update display on timer
        if e == VBL:
            pos = obj.update()
            screen.fill((WHITE))        
            screen.blit(icon, pos)
            pygame.display.flip()

if __name__ == '__main__':
    main()

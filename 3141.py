import pygame, sys, pymunk

# Constants
GRAVITY = (0, 10000)
SIZE = (100, 100)
ELASTICITY = 1
FRICTION = 0
POLY_RADIUS = 0.1
ITERATIONS = 100
RIGHT_BLOCK_MASS = 1000000
RIGHT_BLOCK_VELOCITY = (-75, 0)
STEP_SIZE = 1/500

def createBlock(space, position, mass, velocity=(0, 0), size=(100, 100), elasticity=1, friction=0, id=None):
    body = pymunk.Body(mass, pymunk.moment_for_box(mass, size), body_type = pymunk.Body.DYNAMIC)
    body.position = position
    body.velocity = velocity
    shape = pymunk.Poly.create_box(body, size, .1)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.collision_type = id
    space.add(body, shape)
    return shape

def drawBlocks(blocks):
    for block in blocks:
        vertices = [block.body.local_to_world(v) for v in block.get_vertices()]
        color = (200, 200, 200)
        pygame.draw.polygon(screen, color , vertices)

def createStatic(space, position, size, elasticity=1, friction=0, id=None):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = position
    shape = pymunk.Poly.create_box(body, size, .1)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.collision_type = id
    space.add(body, shape)
    return shape
    
pygame.init()
screen = pygame.display.set_mode((2000, 464))
clock = pygame.time.Clock()
space = pymunk.Space()
space.iterations = 100

collision_counter = 0

def collision_handler(arbiter, space, data):
    global collision_counter
    collision_counter += 1
    print(f"Collision detected! Total count: {collision_counter}")

    return True

font = pygame.font.Font(None, 36)

wall = createStatic(space, (-450, 250), (1100, 350), id = 3)
floor = createStatic(space, (550, 415), (2000, 20), id = 4)
left_block = createBlock(space, (700, 380), 1, id = 1)
right_block = createBlock(space, (1100, 380), 1000000, (-50, 0), id = 2)
objects = [left_block, right_block, wall, floor]

handler = space.add_collision_handler(1, 2)
handler.begin = collision_handler
handler = space.add_collision_handler(1, 3)
handler.begin = collision_handler

space.gravity = (0, 10000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0, 0, 0))
    drawBlocks(objects)
    space.step(1/500)

    collision_text = font.render(f"Collisions: {collision_counter}", True, (255, 255, 255))
    screen.blit(collision_text, (10, 10))  # Position the text on screen

    pygame.display.update()
    clock.tick(60)

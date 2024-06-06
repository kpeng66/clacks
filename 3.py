import pygame, sys, pymunk

# Constants
GRAVITY = (0, 10000)
SIZE = (100, 100)
ELASTICITY = 1
FRICTION = 0
POLY_RADIUS = 0.1
ITERATIONS = 10
RIGHT_BLOCK_MASS = 1
RIGHT_BLOCK_VELOCITY = (-50, 0)
STEP_SIZE = 1/10

def createBlock(space, position, mass, color, velocity=(0, 0), size=SIZE, elasticity=ELASTICITY, friction=FRICTION, id=None):
    body = pymunk.Body(mass, pymunk.moment_for_box(mass, size), body_type = pymunk.Body.DYNAMIC)
    body.position = position
    body.velocity = velocity

    shape = pymunk.Poly.create_box(body, size, POLY_RADIUS)
    shape.mass = mass
    shape.color = color
    shape.elasticity = elasticity
    shape.friction = friction
    shape.collision_type = id

    space.add(body, shape)

    return shape

def drawBlocks(blocks):
    for block in blocks:
        vertices = [block.body.local_to_world(v) for v in block.get_vertices()]
        pygame.draw.polygon(screen, block.color, vertices)

        center_x = sum([v.x for v in vertices]) / 4
        center_y = sum([v.y for v in vertices]) / 4

        mass_text = font.render(f"{str(block.mass)} kg" , True, (0, 0, 0))
        text_rect = mass_text.get_rect(center=(center_x, center_y))
        screen.blit(mass_text, text_rect)

def drawWallAndFloor(objects):
    for object in objects:
        vertices = [object.body.local_to_world(v) for v in object.get_vertices()]
        color = (200, 200, 200)
        pygame.draw.polygon(screen, color , vertices)

def createStatic(space, position, size, elasticity=ELASTICITY, friction=FRICTION, id=None):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = position
    shape = pymunk.Poly.create_box(body, size, POLY_RADIUS)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.collision_type = id
    space.add(body, shape)

    return shape
    
pygame.init()
screen = pygame.display.set_mode((2000, 464))
clock = pygame.time.Clock()
space = pymunk.Space()
space.iterations = ITERATIONS

collision_counter = 0

def collision_handler(arbiter, space, data):
    global collision_counter
    collision_counter += 1

    return True

font = pygame.font.Font(None, 36)

wall = createStatic(space, (-450, 250), (1100, 350), id = 3)
floor = createStatic(space, (550, 415), (2000, 20), id = 4)
left_block = createBlock(space, (700, 380), 1, (67.8, 84.7, 90.2), id = 1)
right_block = createBlock(space, (1100, 380), RIGHT_BLOCK_MASS, (0, 0, 200), RIGHT_BLOCK_VELOCITY, id = 2)
blocks = [left_block, right_block]
objects = [wall, floor]

handler = space.add_collision_handler(1, 2)
handler.begin = collision_handler
handler = space.add_collision_handler(1, 3)
handler.begin = collision_handler

space.gravity = GRAVITY

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0, 0, 0))
    drawBlocks(blocks)
    drawWallAndFloor(objects)
    space.step(STEP_SIZE)

    collision_text = font.render(f"Collisions: {collision_counter}", True, (255, 255, 255))
    screen.blit(collision_text, (10, 10))  # Position the text on screen

    pygame.display.update()
    clock.tick(60)

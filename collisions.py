import pygame, sys, pymunk


def calculateSize(mass):
    base_size = (50, 50)
    scale_factor = (mass ** (1/3))
    return (base_size[0] * scale_factor, base_size[1] * scale_factor)

def createBlock(space, position, mass, velocity=(0, 0), size=(50, 50), elasticity=1.0, friction=0, id=None):
    # size = calculateSize(mass)
    body = pymunk.Body(mass, pymunk.moment_for_box(mass, size), body_type = pymunk.Body.DYNAMIC)
    body.position = position
    body.velocity = velocity
    shape = pymunk.Poly.create_box(body, size)
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

def createStatic(space, position, size, elasticity=1.0, friction=0, id=None):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = position
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = elasticity
    shape.friction = friction
    shape.collision_type = id
    space.add(body, shape)
    return shape
    
pygame.init()
screen = pygame.display.set_mode((1038, 464))
clock = pygame.time.Clock()
space = pymunk.Space()
space.iterations = 10000

collision_counter = 0

def collision_handler(arbiter, space, data):
    global collision_counter
    collision_counter += 1
    print(f"Collision detected! Total count: {collision_counter}")

    for shape in arbiter.shapes:
        body = shape.body
        vel = body.velocity
        # Reset y-velocity to 0 or any other desired constant value
        body.velocity = pymunk.Vec2d(vel.x, 0)  # Keeps the body moving only horizontally

    return True

wall = createStatic(space, (-450, 250), (1100, 350), id = 3)
floor = createStatic(space, (550, 415), (1100, 20), id = 4)
left_block = createBlock(space, (700, 380), 1, id = 1)
right_block = createBlock(space, (850, 380), 1000000, (-200, 0), id = 2)
objects = [left_block, right_block, wall, floor]

handler = space.add_collision_handler(1, 2)
handler.begin = collision_handler
handler = space.add_collision_handler(1, 3)
handler.begin = collision_handler

def gravity(body, gravity, damping, dt):
    pymunk.Body.update_velocity(body, (0, 1000), damping, dt)

left_block.velocity_func = gravity
right_block.velocity_func = gravity

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((0, 0, 0))
    drawBlocks(objects)
    space.step(1/5000)
    pygame.display.update()
    clock.tick(60)

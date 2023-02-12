# Mini-Project 8: RiceRocks
# On less performant computers the game may perform slower

import simplequi as simplegui
import math
import random

# Globals		 
DIMENSIONS = 2
CANVAS_RES = (800, 600)
score = INIT_SCORE = 0
lives = INIT_LIVES = 3
time = 0.5
started = False
# constants for varying different quantities
const_friction = .01
const_thrust = .1
const_rotation = .1
const_missile = 5
const_rock_vicinity = 3  # the rocks won't spawn at a distance closer than 3 radii to the center of the ship
const_rock_speed = INIT_ROCK_SPEED = 1  # the rocks will move/spin faster the greater the constant is


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# Art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# Debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris_blend.png")

# Nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

# Splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# Ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# Missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# Asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")

# Animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")

# Sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# Setting volume
soundtrack.set_volume(.7)
missile_sound.set_volume(.2)
ship_thrust_sound.set_volume(.5)
explosion_sound.set_volume(.5)


# Helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


def process_sprite_group(sprite_group, canvas):
    """Function to draw sprites on canvas, update them and delete those who became old"""
    remove_sprites = set([])

    for sprite in sprite_group:
        sprite.draw(canvas)

        if sprite.update():  # update returns True if the sprite became old, else False
            remove_sprites.add(sprite)

    if len(remove_sprites):  # if something needs to be deleted
        sprite_group.difference_update(remove_sprites)


def group_collide(sprite_group, other_object):
    """
    Function takes a group of sprites and another object (e.g. the ship, a sprite) 
    and if these two collided makes an explosion, returning True; else False
    """
    remove_sprites = set([])

    for sprite in sprite_group:
        if sprite.collide(other_object):
            remove_sprites.add(sprite)

    if len(remove_sprites):  # if something collided..
        sprite_group.difference_update(remove_sprites)
        an_explosion = Sprite(other_object.get_pos(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
        explosion_group.add(an_explosion)
        return True

    else:  # if not..
        return False


def group_group_collide(rock_group, missile_group):
    """
    Function takes two groups of sprites (i.e. the rock group, the missile group) 
    and returns the number of rocks destroyed
    """
    rocks_destroyed = 0

    for missile in list(missile_group):  # iterating over a copy of the missile group
        if group_collide(rock_group, missile):
            rocks_destroyed += 1
            # safely mutating the missile group because we iterate on a copy
            missile_group.discard(missile)

    return rocks_destroyed


class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(ship_image, [3 * self.image_center[0], self.image_center[1]],
                              self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(ship_image, self.image_center,
                              self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # determining where is "forward"
        forward_vector = angle_to_vector(self.angle)

        for i in range(DIMENSIONS):
            # suggested in "Programming Tips 7", avoiding code repetition
            # "wrapping" the canvas, updating position, velocity, adding friction, thrusting
            self.pos[i] %= CANVAS_RES[i]
            self.pos[i] += self.vel[i]
            self.vel[i] *= (1 - const_friction)

            if self.thrust:
                self.vel[i] += forward_vector[i] * const_thrust

        # updating angle
        self.angle += self.angle_vel

    # methods called by key pressing: turn, accelerate, fire
    def turn(self, turn):
        self.angle_vel = const_rotation * turn

    def accelerate(self, thrust_on):
        if thrust_on > 0:
            self.thrust = True
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            self.thrust = False
            ship_thrust_sound.pause()

    def fire(self, shoot):
        if shoot > 0:
            forward_vector = angle_to_vector(self.angle)
            newpos = [0, 0]
            newvel = [0, 0]

            for i in range(DIMENSIONS):  # determining position and velocity of the missile
                newpos[i] = self.pos[i] + forward_vector[i] * self.image_size[i] / 2
                newvel[i] = self.vel[i] + forward_vector[i] * const_missile

            a_missile = Sprite(newpos, newvel, 0, 0, missile_image, missile_info, missile_sound)
            missile_group.add(a_missile)


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_pos(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def draw(self, canvas):
        if self.animated:
            new_image_center = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, new_image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        for i in range(DIMENSIONS):
            self.pos[i] %= CANVAS_RES[i]
            self.pos[i] += self.vel[i]

        self.angle += self.angle_vel
        self.age += 1

        # return True if the sprite is old and needs to be destroyed
        if self.age < self.lifespan:
            return False
        else:
            return True

    def collide(self, other_object):
        """
        Method that takes as input a sprite and another object (e.g. the ship, a sprite)
        and returns True if they collide, else False
        """
        distance = dist(self.pos, other_object.get_pos())
        sum_radii = self.radius + other_object.get_radius()

        if distance < sum_radii:
            return True
        else:
            return False


# Event handlers
def click(pos):
    """
    Mouseclick handler that resets UI and conditions whether splash image is drawn.
    Additionally, resets the number of lives and the score, the background soundtrack
    """
    global lives, score, started, const_rock_speed

    center = [CANVAS_RES[0] / 2, CANVAS_RES[1] / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)

    if (not started) and inwidth and inheight:
        started = True
        timer.start()
        soundtrack.rewind()
        soundtrack.play()
        lives = INIT_LIVES
        score = INIT_SCORE
        const_rock_speed = INIT_ROCK_SPEED


def draw(canvas):
    global time, lives, score, started

    # animate background
    time += 1
    wtime = (time / 4) % CANVAS_RES[0]
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(),
                      [CANVAS_RES[0] / 2, CANVAS_RES[1] / 2], [CANVAS_RES[0], CANVAS_RES[1]])
    canvas.draw_image(debris_image, center, size, (wtime - CANVAS_RES[0] / 2, CANVAS_RES[1] / 2),
                      (CANVAS_RES[0], CANVAS_RES[1]))
    canvas.draw_image(debris_image, center, size, (wtime + CANVAS_RES[0] / 2, CANVAS_RES[1] / 2),
                      (CANVAS_RES[0], CANVAS_RES[1]))

    # draw/update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    if group_collide(rock_group, my_ship):  # ship collides with a rock
        lives -= 1

    # score updated by the number of rocks destroyed (by zero if none)
    score += 10 * group_group_collide(rock_group, missile_group)

    if lives == 0:  # game over
        started = False
        timer.stop()
        soundtrack.pause()
        rock_group.difference_update(rock_group)

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [CANVAS_RES[0] / 2, CANVAS_RES[1] / 2],
                          splash_info.get_size())

    # draw text
    canvas.draw_text("Lives", [30, 40], 36, "Orange", "monospace")
    canvas.draw_text(str(lives), [30, 76], 36, "Orange", "monospace")
    canvas.draw_text("Score", [670, 40], 36, "Orange", "monospace")
    canvas.draw_text(str(score), [670, 76], 36, "Orange", "monospace")


def keydown(key):
    for i in inputs:  # suggested in "Programming Tips 7", avoiding long if/elif constructions
        if key == simplegui.KEY_MAP[i]:
            inputs[i][0](inputs[i][1])


def keyup(key):
    for i in inputs:  # suggested in "Programming Tips 7", avoiding long if/elif constructions
        if key == simplegui.KEY_MAP[i]:
            inputs[i][0](0)


def rock_spawner():
    """Timer handler that spawns a rock"""
    global const_rock_speed
    const_rock_speed += 1 / 300.0  # in 5 minutes the speed of the rocks will be 2 times bigger

    if len(rock_group) < 12:
        # global rock_group
        newpos = [0, 0]
        newvel = [0, 0]

        # generating random values for he rock movement
        for i in range(DIMENSIONS):
            newpos[i] = random.randrange(0, CANVAS_RES[i])
            newvel[i] = const_rock_speed * (random.random() * 2 - 1)

        # prevents the spawn of a rock in the near vicinity of the ship
        if dist(newpos, my_ship.get_pos()) < const_rock_vicinity * my_ship.get_radius():
            rock_spawner()  # call to generate another rock
            return  # to stop further executing of the function

        newang = random.random() * 2 * math.pi
        newangvel = const_rock_speed * (random.random() * .2 - .1)

        a_rock = Sprite(newpos, newvel, newang, newangvel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)


# Frame initialized
frame = simplegui.create_frame("Asteroids", CANVAS_RES[0], CANVAS_RES[1])

# Ship and three groups of sprites initialized
my_ship = Ship([CANVAS_RES[0] / 2, CANVAS_RES[1] / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# suggested in "Programming Tips 7", avoiding long if/elif constructions
# tuple - function_name and command(e.g. turn left or right...)
inputs = {"left": (my_ship.turn, -1),
          "right": (my_ship.turn, 1),
          "up": (my_ship.accelerate, 1),
          "space": (my_ship.fire, 1)}

# Handlers registered
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000, rock_spawner)

# Lastly and most importantly
frame.start()

import Box2D
import random
from math import cos, sin, pi
from Box2D.b2 import (world, circleShape, staticBody, dynamicBody, polygonShape)

MAX_TORQUE = 1e4
WHEEL_FRICTION = 5.0
#CHANGED SPEED TO NEGATIVE TO MOVE FORWARD
SPEED = -5

class Bipedal:

    def __init__(self, name, gene):
        self.genome = {'width': gene[0],'height': gene[1],'right_leg': gene[2],'left_leg': gene[2]}
        self.name = name

    def build(self, world, x0, y0):
        width = self.genome['width']
        height = self.genome['height']
        length1 = self.genome['right_leg']
        length2 = self.genome['left_leg']

        body = world.CreateDynamicBody(position=(x0, y0))
        body.fixedRotation = True
        body.CreatePolygonFixture(box=(width, height), density=1, friction=0.3)

        head = world.CreateDynamicBody(position=(x0, y0+4))
        head.fixedRotation = True
        head.CreateCircleFixture(radius = 1.8, density=1, friction=0.3)

        neck = world.CreateDynamicBody(position=(x0, y0+2.5))
        neck.fixedRotation = True
        neck.CreatePolygonFixture(box = (0.5, 1), density=1, friction=WHEEL_FRICTION)

        #world.CreateDistanceJoint(bodyA = head, bodyB = body, anchorA = head.worldCenter, anchorB= body.worldCenter,
        #collideConnected = True)
        world.CreateRevoluteJoint(bodyA=head, bodyB=neck, anchor = head.worldCenter, enableMotor = False)
        world.CreateRevoluteJoint(bodyA=neck, bodyB=body, anchor = body.worldCenter, enableMotor = False)

        right_leg = world.CreateDynamicBody(position=(x0+1, y0-2))
        right_leg.CreatePolygonFixture(box = (0.5,3), density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=body, bodyB=right_leg,
                anchor = body.worldCenter + (1,-2),
                lowerAngle = -0.3 * pi, upperAngle = 0.3 * pi,
                enableLimit = True,
                maxMotorTorque = MAX_TORQUE, motorSpeed = cos(SPEED),
                enableMotor = True)

        left_leg = world.CreateDynamicBody(position=(x0-1, y0-2))
        left_leg.CreatePolygonFixture(box = (0.5,3), density=1, friction=WHEEL_FRICTION)
        world.CreateRevoluteJoint(bodyA=body, bodyB=left_leg,
                anchor = body.worldCenter + (-1, -2),
                lowerAngle = -0.3 * pi, upperAngle = 0.3 * pi,
                enableLimit = True,
                maxMotorTorque = MAX_TORQUE, motorSpeed = sin(SPEED),
                enableMotor = True)


        self.bodies = [body, head, neck, right_leg, left_leg]
        self.tracker = body.worldCenter
        # return the body object for tracking position
        return body

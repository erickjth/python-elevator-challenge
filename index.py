from elevator import ElevatorLogic

UP = 1
DOWN = 2
FLOOR_COUNT = 6

class Elevator(object):
     def call(self, floor, direction):
         self._logic_delegate.on_called(floor, direction)

     def select_floor(self, floor):
         self._logic_delegate.on_floor_selected(floor)

class Elevator(Elevator):
     def __init__(self, logic_delegate, starting_floor=1):
         self._current_floor = starting_floor
         print "%s..." % starting_floor,
         self._motor_direction = None
         self._logic_delegate = logic_delegate
         self._logic_delegate.callbacks = self.Callbacks(self)

     class Callbacks(object):
         def __init__(self, outer):
             self._outer = outer

         @property
         def current_floor(self):
             return self._outer._current_floor

         @property
         def motor_direction(self):
             return self._outer._motor_direction

         @motor_direction.setter
         def motor_direction(self, direction):
             self._outer._motor_direction = direction

class Elevator(Elevator):
     def step(self):
        delta = 0
        if self._motor_direction == UP: delta = 1
        elif self._motor_direction == DOWN: delta = -1

        if delta:
            self._current_floor = self._current_floor + delta
            print "%s..." % self._current_floor,
            self._logic_delegate.on_floor_changed()
        else:
            self._logic_delegate.on_ready()

        assert self._current_floor >= 1
        assert self._current_floor <= FLOOR_COUNT

     def run_until_stopped(self):
         print ''
         self.step()
         while self._motor_direction is not None: self.step()

     def run_until_floor(self, floor):
         for i in range(100):
             self.step()
             if self._current_floor == floor: break
         else: assert False

# Basic test
print 'Basic tests'
e = Elevator(ElevatorLogic())
#    1...
e.call(5, DOWN)
e.run_until_stopped()
#    2... 3... 4... 5...
e.select_floor(1)
e.call(3, DOWN)
e.run_until_stopped()
#    4... 3...
e.run_until_stopped()
#    2... 1...

print ''
print 'Directionality'
e = Elevator(ElevatorLogic())
#    1...
e.call(2, DOWN)
e.select_floor(5)
e.run_until_stopped()
#    2... 3... 4... 5...
e.run_until_stopped()
#    4... 3... 2...

print ''
print 'Directionality 2'
e = Elevator(ElevatorLogic())
#    1...
e.select_floor(3)
e.select_floor(5)
e.run_until_stopped()
#    2... 3...
e.select_floor(2)
e.run_until_stopped()
#    4... 5...
e.run_until_stopped()  # nothing happens, because e.select_floor(2) was ignored
e.select_floor(2)
e.run_until_stopped()
#    4... 3... 2...


print ''
print 'Changing direction'
e = Elevator(ElevatorLogic())
#1...
e.call(2, DOWN)
e.call(4, UP)
e.run_until_stopped()
#2... 3... 4...
e.select_floor(5)
e.run_until_stopped()
#5...
e.run_until_stopped()
#4... 3... 2...
# #

print ''
print 'Changing direction 2'
e = Elevator(ElevatorLogic())
#1...
e.call(2, DOWN)
e.call(4, UP)
e.run_until_stopped()
#2... 3... 4...
e.run_until_stopped()
#3... 2...
# #
print ''
print 'Changing direction 3'
e = Elevator(ElevatorLogic())
#1...
e.select_floor(5)
e.call(5, UP)
e.call(5, DOWN)
e.run_until_stopped()
#2... 3... 4... 5...
e.select_floor(4)  # ignored
e.run_until_stopped()
e.select_floor(6)  # ignored
e.run_until_stopped()
e.select_floor(6)
e.run_until_stopped()
#6...

print ''
print 'En passant'
e = Elevator(ElevatorLogic())
#    1...
e.select_floor(6)
e.run_until_floor(2)  # elevator is not stopped
#    2...
e.select_floor(3)
e.run_until_stopped()  # stops for above
#    3...
e.run_until_floor(4)
#    4...
e.call(5, UP)
e.run_until_stopped()  # stops for above
#    5...

print ''
print 'En passant 2'
e = Elevator(ElevatorLogic())
# 1...
e.select_floor(5)
e.run_until_floor(2)
# 2...
e.call(2, UP)  # missed the boat, come back later
e.step()  # doesn't stop
# 3...
e.select_floor(3)  # missed the boat, ignored
e.step()  # doesn't stop
# 4...
e.run_until_stopped()  # service e.select_floor(5)
# 5...
e.run_until_stopped()  # service e.call(2, UP)
# 4... 3... 2...

print ''
print 'Fuzz testing'
import random
e = Elevator(ElevatorLogic())
#    1...
try: print '-',  # doctest:+ELLIPSIS
finally:
    for i in range(100000):
        r = random.randrange(6)
        if r == 0: e.call(
            random.randrange(FLOOR_COUNT) + 1,
            random.choice((UP, DOWN)))
        elif r == 1: e.select_floor(random.randrange(FLOOR_COUNT) + 1)
        else: e.step()

print ''
print 'More examples'
e = Elevator(ElevatorLogic())
#    1...
e.call(5, UP)
e.run_until_stopped()
#    2... 3... 4... 5...
e.run_until_stopped()
e.run_until_stopped()

print ''
print 'More examples 2'
e = Elevator(ElevatorLogic())
# 1...
e.call(3, UP)
e.call(5, UP)
e.run_until_stopped()
# 2... 3...
e.run_until_stopped()
# 4... 5...

print ''
print 'More examples 3'
e = Elevator(ElevatorLogic())
# 1...
e.call(5, UP)
e.call(3, UP)
e.run_until_stopped()
# 2... 3...
e.run_until_stopped()
# 4... 5...


print ''
print 'More examples 4'
e = Elevator(ElevatorLogic())
# 1...
e.call(3, DOWN)
e.call(5, DOWN)
e.run_until_stopped()
# 2... 3... 4... 5...
e.run_until_stopped()
# 4... 3...

print ''
print 'More examples 5'
e = Elevator(ElevatorLogic())
#1...
e.call(3, UP)
e.call(5, DOWN)
e.run_until_stopped()
#2... 3...
e.run_until_stopped()
#4... 5...

print ''
print 'More examples 6'
e = Elevator(ElevatorLogic())
#1...
e.call(3, DOWN)
e.call(5, UP)
e.run_until_stopped()
#2... 3... 4... 5...
e.run_until_stopped()
#4... 3...


print ''
print 'More examples 7'
e = Elevator(ElevatorLogic(), 3)
#3...
e.call(2, UP)
e.call(4, UP)
e.run_until_stopped()
#2...
e.run_until_stopped()
#3... 4...


print ''
print 'More examples 8'
e = Elevator(ElevatorLogic(), 3)
#3...
e.call(4, UP)
e.call(2, UP)
e.run_until_stopped()
#4...
e.run_until_stopped()
#3... 2...

print ''
print 'More examples 9'
e = Elevator(ElevatorLogic())
#1...
e.call(5, UP)
e.run_until_floor(2)
#2...
e.call(3, UP)
e.run_until_stopped()
#3...
e.run_until_stopped()
#4... 5...

print ''
print 'More examples 10'
e = Elevator(ElevatorLogic())
#1...
e.call(5, UP)
e.run_until_floor(3)
#2... 3...
e.call(3, UP)
e.run_until_stopped()
#4... 5...
e.run_until_stopped()
#4... 3...


print ''
print 'More examples 11'
e = Elevator(ElevatorLogic())
#1...
e.select_floor(3)
e.select_floor(5)
e.run_until_stopped()
#2... 3...
e.run_until_stopped()
#4... 5...

print ''
print 'More examples 12'
e = Elevator(ElevatorLogic())
#1...
e.select_floor(5)
e.select_floor(3)
e.run_until_stopped()
#2... 3...
e.run_until_stopped()
#4... 5...

print ''
print 'More examples 13'
e = Elevator(ElevatorLogic(), 3)
#3...
e.select_floor(2)
e.select_floor(4)
e.run_until_stopped()
#2...
e.run_until_stopped()

print ''
print 'More examples 14'
e = Elevator(ElevatorLogic(), 3)
#3...
e.select_floor(4)
e.select_floor(2)
e.run_until_stopped()
#4...
e.run_until_stopped()

# # If the elevator is called to a floor going up, it should ignore a request to go down.
print ''
print 'More examples 15'
e = Elevator(ElevatorLogic())
#1...
e.call(5, UP)
e.run_until_stopped()
#2... 3... 4... 5...
e.select_floor(6)
e.select_floor(4)
e.run_until_stopped()
#6...
e.run_until_stopped()

# Like above, but going in other direction.
print ''
print 'More examples 16'
e = Elevator(ElevatorLogic())
#1...
e.call(5, DOWN)
e.run_until_stopped()
#2... 3... 4... 5...
e.select_floor(6)
e.select_floor(4)
e.run_until_stopped()
#4...
e.run_until_stopped()


print ''
print 'More examples 17'
e = Elevator(ElevatorLogic())
#1...
e.call(5, DOWN)
e.select_floor(5)
e.run_until_stopped()
#2... 3... 4... 5...
e.select_floor(4)
e.run_until_stopped()
#4...
e.run_until_stopped()

# Similarly, if the elevator is called at a floor where it is stopped, it should not go back later.
print ''
print 'More examples 18'
e = Elevator(ElevatorLogic())
#1...
e.call(3, UP)
e.run_until_stopped()
#2... 3...
e.call(3, UP)
e.call(5, DOWN)
e.run_until_stopped()
#4... 5...
e.run_until_stopped()


print ''
print 'More examples 19'
e = Elevator(ElevatorLogic())
#1...
e.call(2, DOWN)
e.call(4, UP)
e.run_until_stopped()
#2... 3... 4...
e.call(5, DOWN)  # It's not too late.
e.run_until_stopped()
#5...
e.run_until_stopped()
#4... 3... 2...

# When changing directions, wait one step to clear current direction.
print ''
print 'More examples 20'
e = Elevator(ElevatorLogic())
#1...
e.select_floor(5)
e.call(5, UP)
e.call(5, DOWN)
e.run_until_stopped()
#2... 3... 4... 5...
e.select_floor(4)  # ignored
e.run_until_stopped()
e.select_floor(6)  # ignored
e.select_floor(4)
e.run_until_stopped()
#4...
e.run_until_stopped()


print ''
print 'More examples 21'
e = Elevator(ElevatorLogic(), 6)
#6...
e.select_floor(2)
e.call(2, UP)
e.call(2, DOWN)
e.run_until_stopped()
#5... 4... 3... 2...
e.select_floor(3)  # ignored
e.run_until_stopped()
e.select_floor(1)  # ignored
e.select_floor(3)
e.run_until_stopped()
#3...
e.run_until_stopped()


print ''
print 'More examples 22'
e = Elevator(ElevatorLogic())
#1...
e.select_floor(5)
e.call(5, UP)
e.call(5, DOWN)
e.run_until_stopped()
#2... 3... 4... 5...
e.select_floor(6)
e.run_until_stopped()
#6...
e.run_until_stopped()
#5...
e.select_floor(6)  # ignored
e.select_floor(4)
e.run_until_stopped()
#4...
e.run_until_stopped()

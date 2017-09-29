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
#
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
#
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

# print ''
# print 'En passant 2'
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

# import random
# e = Elevator(ElevatorLogic())
# #    1...
# try: print '-',  # doctest:+ELLIPSIS
# finally:
#     for i in range(100000):
#         r = random.randrange(6)
#         if r == 0: e.call(
#             random.randrange(FLOOR_COUNT) + 1,
#             random.choice((UP, DOWN)))
#         elif r == 1: e.select_floor(random.randrange(FLOOR_COUNT) + 1)
#         else: e.step()
# #    - ...

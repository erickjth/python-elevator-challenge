UP = 1
DOWN = 2
FLOOR_COUNT = 6

CALL = 2
SELECT = 1

class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this is done.
    """

    def __init__(self):
        # Feel free to add any instance variables you want.
        self.callbacks = None
        self.requests = []
        self.breadcrumbs = []

    def clean_requests(self, result, request):
        result_check_equals = filter(lambda x: x["floor"] == request["floor"], result)

        if len(result_check_equals) == 0:
            result.append(request)

        return result

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        #direction = self.callbacks.motor_direction
        sort = -1 if direction == DOWN else 1
        self.requests.append({ "floor" : floor, "type" : CALL, "sort": sort })
        self.requests.sort(key=lambda x: (x['type'], x['floor'], x['sort']), reverse=direction == DOWN)
        # print 'on Called'
        # print self.requests

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        direction = self.callbacks.motor_direction
        ignored = False

        if self.callbacks.motor_direction == None and floor < self.callbacks.current_floor:
            direction = DOWN
        elif self.callbacks.motor_direction == None and floor > self.callbacks.current_floor:
            direction = UP

        if len(self.requests) > 0:
            last_destination = self.requests[-1]
            #print "Floor %s %s" % (floor, direction)

            if direction == DOWN and floor < last_destination['floor']:
                ignored = True
                #print "ignore %s" % floor

        sort = -1 if direction == DOWN else 1

        if ignored == False:
            self.requests.append({ "floor" : floor, "type" : SELECT, "sort": sort })

        self.requests.sort(key=lambda x: (x['type'], x['floor'], x['sort']), reverse=direction == DOWN)

        # print "Floor %s" % floor
        # print 'on Selected'
        # print self.requests

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        #print "Floor %s" % self.callbacks.current_floor
        if len(self.requests) > 0:
            # self.breadcrumbs.append((self.callbacks.current_floor, self.callbacks.motor_direction))

            #print "%s == %s" % (self.requests[0]["floor"], self.callbacks.current_floor)
            if self.requests[0]["floor"] == self.callbacks.current_floor:
                removed = self.requests.pop(0)
                self.callbacks.motor_direction = None

            # if self.callbacks.current_floor >= FLOOR_COUNT:
            #     self.callbacks.motor_direction = None

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        #print 'ready... %s %s' % (self.callbacks.current_floor, self.callbacks.motor_direction)

        if len(self.requests) > 0:
            destination_floor = self.requests[0]["floor"]
            #print "%s == %s" % (destination_floor, self.callbacks.current_floor)
            if destination_floor > self.callbacks.current_floor:
                self.callbacks.motor_direction = UP
            elif destination_floor < self.callbacks.current_floor:
                self.callbacks.motor_direction = DOWN
            elif destination_floor == self.callbacks.current_floor:
                self.requests.pop(0)

            #print 'ready...%s %s %s' % (self.callbacks.current_floor, destination_floor, self.callbacks.motor_direction)

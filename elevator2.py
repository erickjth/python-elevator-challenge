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
        reverse = direction == DOWN

        if len(self.requests) > 0:
            last_destination = self.requests[-1]
            if direction == UP:
                if last_destination['floor'] < floor:
                    if last_destination['sort'] == -1:
                        reverse = True
                elif last_destination['floor'] > floor:
                    if self.callbacks.current_floor > floor and last_destination['sort'] == 1:
                        reverse = True

            #print "| Direction %s, Destination %s, Current Floor %s, Last Destination %s, Reverse %s |" % (direction, floor, self.callbacks.current_floor, last_destination['floor'], reverse)

        self.requests.append({ "floor" : floor, "sort": sort })
        self.requests.sort(key=lambda x: (x['sort'], x['floor']), reverse=reverse)
        #print 'on Called', self.requests

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        direction = self.callbacks.motor_direction
        ignored = False
        reverse = False

        if len(self.breadcrumbs) > 0:
            direction = DOWN if self.breadcrumbs[-1]['sort'] == -1 else UP
        if floor < self.callbacks.current_floor:
            direction = DOWN
        elif floor > self.callbacks.current_floor:
            direction = UP

        if len(self.requests) > 0:
            next_destination = self.requests[0]

            if direction == UP:
                if next_destination['floor'] < floor:
                    if next_destination['sort'] == -1:
                        reverse = True
                        if self.callbacks.current_floor < floor:
                            if next_destination['floor'] + 3 != floor:
                                ignored = True
                    if self.callbacks.current_floor > floor:
                         ignored = True
                elif next_destination['floor'] >= floor:
                    if self.callbacks.current_floor >= floor:
                        ignored = True

            elif direction == DOWN:
                if next_destination['floor'] > floor:
                    if next_destination['sort'] == 1:
                        if self.callbacks.current_floor > floor:
                            ignored = True

            #print "| Direction %s Destination Floor %s Current Floor %s, Next Destination %s, Reverse %s, Ignore %s |" % (direction, floor, self.callbacks.current_floor, next_destination['floor'], reverse, ignored)
        sort = -1 if direction == DOWN else 1

        if ignored == False:
            self.requests.append({ "floor" : floor, "sort": sort })

        self.requests.sort(key=lambda x: (x['sort'], x['floor']), reverse=reverse)
        #print 'on Selected', self.requests

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        #print "On changed before: Floor ", self.callbacks.current_floor, ' on Current Requests', self.requests

        if len(self.requests) > 0:
            next_destination = self.requests[0]

            if next_destination['floor'] < self.callbacks.current_floor:
                if next_destination['sort'] == 1:
                    self.requests.sort(key=lambda x: (x['sort'], x['floor']), reverse=True)

            if self.requests[0]['floor'] == self.callbacks.current_floor:
                removed = self.requests.pop(0)
                self.breadcrumbs.append(removed)
                self.callbacks.motor_direction = None

            #print "On changed after: Floor ", self.callbacks.current_floor, ' on Current Requests', self.requests

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

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
        self.change_direction = False
        self.requests = { DOWN: [], UP: [] }
        self.breadcrumbs = []

    def floors_are_consecutive(self, a, b, c):
        min_floor = min(a, min(b, c));
        max_floor = max(a, max(b, c));
        return (max_floor - min_floor == 2 and a != b and a != c and b != c)

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        with_sort = True
        ignored = False
        all_requests = self.requests[UP] + self.requests[DOWN]

        if len(self.requests[direction]) > 0:
            last_destination = self.requests[direction][-1]

            if floor == last_destination['floor'] and direction == last_destination['direction']:
                self.requests[direction].pop()

             # Check if the floors are consecutive
            floors_are_consecutive = self.floors_are_consecutive(last_destination['floor'], self.callbacks.current_floor, floor)
            if last_destination['type'] == CALL and floors_are_consecutive == True:
                with_sort = False

        self.requests[direction].append({'floor': floor, 'type': CALL, 'direction': direction})

        if with_sort == True:
            self.requests[direction].sort(key=lambda x: x['floor'], reverse=direction == DOWN)

        #print 'Direction:', direction, ' Destination:', floor, ' Current state: ', self.requests, 'With Sort:', with_sort, ', ignored ', ignored
        #print 'on Called', self.requests

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        direction = UP # By default the elevator starts in UP
        ignored = False
        all_requests = self.requests[UP] + self.requests[DOWN]

        if len(self.breadcrumbs) > 0:
            last_destination = self.breadcrumbs[-1]
            direction = last_destination['direction']

            if self.change_direction == True:
                direction = DOWN if direction == UP else UP

        if len(self.requests[direction]) > 0:
            # Check if the floors are consecutive
            last_destination = self.requests[direction][-1]
            floors_are_consecutive = self.floors_are_consecutive(last_destination['floor'], self.callbacks.current_floor, floor)

            if direction == UP and floor <= self.callbacks.current_floor:
                ignored = True
            elif direction == DOWN and floor >= self.callbacks.current_floor:
                ignored = True
            elif last_destination['type'] == SELECT and floors_are_consecutive == True:
                ignored = True
        # elif len(self.requests[direction]) == 0 and len(self.breadcrumbs) > 0:
        #     if len(all_requests) > 0:
        #         ignored = True
        elif direction == UP and floor <= self.callbacks.current_floor:
            ignored = True
        elif direction == DOWN and floor >= self.callbacks.current_floor:
            ignored = True
        elif len(all_requests) > 0:
             ignored = True if all_requests[-1]['floor'] == floor else False

        #print 'Current floor', self.callbacks.current_floor,' Direction:', direction, ' Destination:', floor, ' Current state: ', self.requests, 'Ignored:', ignored

        if ignored == False:
            self.requests[direction].append({ 'floor' : floor, 'type' : SELECT, 'direction': direction })
            self.requests[direction].sort(key=lambda x: x['floor'], reverse=direction == DOWN)
            #print 'on Selected', self.requests

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        opened = True
        direction = self.callbacks.motor_direction

        all_requests = self.requests[UP] + self.requests[DOWN]

        if len(all_requests) > 0:
            floor = all_requests[0]['floor']
            direction = all_requests[0]['direction']

            if direction == UP and floor < self.callbacks.current_floor:
                self.requests[UP].sort(key=lambda x: x['floor'], reverse=True)

            if floor == self.callbacks.current_floor:
                self.requests[direction].pop(0)
                self.callbacks.motor_direction = None
            else:
                opened = False
        else:
            opened = False

        self.breadcrumbs.append({ 'direction': direction, 'floor': self.callbacks.current_floor, 'opened': opened,  })

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        requests = self.requests[UP] + self.requests[DOWN]

        if len(requests) > 0:
            next_destination = requests[0]['floor']
            if next_destination > self.callbacks.current_floor:
                self.callbacks.motor_direction = UP
            elif next_destination < self.callbacks.current_floor:
                self.callbacks.motor_direction = DOWN
            elif next_destination == self.callbacks.current_floor:
                self.on_floor_changed()

            self.change_direction = False
        else:
            self.change_direction = True
            #print 'ready...%s %s %s' % (self.callbacks.current_floor, destination_floor, self.callbacks.motor_direction)

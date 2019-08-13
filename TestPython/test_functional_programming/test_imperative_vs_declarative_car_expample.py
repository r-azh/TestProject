__author__ = 'R.Azh'


# A program can be made more declarative by bundling pieces of the code into functions.
# This code is written imperatively.
print('\n############### imperative #######################')

from random import random

time = 5
car_positions = [1, 1, 1]

while time:
    # decrease time
    time -= 1

    print('')
    for i in range(len(car_positions)):
        # move car
        if random() > 0.3:
            car_positions[i] += 1

        # draw car
        print('-' * car_positions[i])

print('\n############### declarative: not functional #######################')
# A functional version would be declarative. It would describe what to do, rather than how to do it.
# This technique uses functions, but it uses them as sub-routines. the code is not functional.


def move_cars():
    for i, _ in enumerate(car_positions):
        if random() > 0.3:
            car_positions[i] += 1


def draw_car(car_position):
    print('-' * car_position)


def run_step_of_race():
    global time
    time -= 1
    move_cars()


def draw():
    print('')
    for car_position in car_positions:
        draw_car(car_position)

time = 5
car_positions = [1, 1, 1]

while time:
    run_step_of_race()
    draw()

print('\n############### functional #######################')
# Remove state
# The code is still split into functions, but the functions are functional.
# First, there are no longer any shared variables.
# Second, functions take parameters.
# Third, no variables are instantiated inside functions. All data changes are done with return values.


def move_cars_(car_positions):
    return map(lambda x: x + 1 if random() > 0.3 else x,
               car_positions)


def output_car_(car_position):
    return '-' * car_position


def run_step_of_race_(state):
    return {'time': state['time'] - 1,
            'car_positions': move_cars_(state['car_positions'])}


def draw(state):
    print('')
    print('\n'.join(map(output_car_, state['car_positions'])))


def race(state):
    draw(state)
    if state['time']:
        race(run_step_of_race_(state))

race({'time': 5,
      'car_positions': [1, 1, 1]})

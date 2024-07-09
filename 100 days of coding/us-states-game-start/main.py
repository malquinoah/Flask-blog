import turtle
import pandas

screen = turtle.Screen()
screen.title('U.S. States Game')
image = 'blank_states_img.gif'
screen.addshape(image) # This is a method to add an image

turtle.shape(image) # the shape method can now take the newly added image as input


# def get_mouse_click_coor(x, y):
#     print(x,y)
#
#
# turtle.onscreenclick(get_mouse_click_coor) #onscreenclick listens for when the mouse clicks, which will then call our
# # func to pass over the x and y coordinate of that location
#
# turtle.mainloop() # Alternative way to keep our screen open even after our code finished running, opposite of exitonclick


# # states map guessing game

# data = pandas.read_csv('50_states.csv')
# on_map = []
#
# turty = turtle.Turtle()
# turty.hideturtle()
# turty.penup()
# turty.color('black')
#
# states_guessed = 0
#
# incomplete = True
#
#
# while incomplete:
#     guess = screen.textinput(f'Guess the State: {states_guessed}/50', 'What\'s a state\'s name?').title()
#
#     row = data[data['state'] == guess]
#     x_value = row['x'].iloc[0]
#     y_value = row['y'].iloc[0]
#
#     if states_guessed == 50:
#         incomplete = False
#         turty.goto(0,0)
#         turty.write(arg='You guessed all 50 states!', align='center', font=('arial', 50, 'normal'))
#
#     if guess in data['state'].to_numpy():
#         if guess not in on_map:
#             states_guessed += 1
#             turty.goto(x_value, y_value)
#             turty.write(arg=guess, align='center', font=('arial', 20, 'normal'))
#             on_map.append(guess)
#
#         else:
#             guess = screen.textinput('Guess the State', 'Try another state that you haven\'t guessed')
#             pass
#     elif guess == 'Exit':
#         incomplete = False
#     # elif guess not in data['state'].to_numpy():
#     #     screen.textinput('Guess the State', 'That\'s not one of the U.S. States')
#
# print(on_map)
#
# screen.mainloop()

data = pandas.read_csv('50_states.csv')
guessed_states = []
all_states = data['state'].tolist()

while len(guessed_states) < 50:

    answer_state = screen.textinput(title=f'{len(guessed_states)}/50 states correct', prompt='What\'s another state\'s name?').title()

    if answer_state == 'Exit':
        missing_states = [state for state in all_states if state not in guessed_states]
        break

    if answer_state in all_states:
        guessed_states.append(answer_state)
        turty = turtle.Turtle()
        turty.hideturtle()
        turty.penup()
        state_data = data[data.state == answer_state]
        turty.goto(int(state_data.x), int(state_data.y))
        turty.write(answer_state) # or turty.write(state.data.item())


columns = ['States to learn']

states_to_learn = pandas.DataFrame(missing_states, columns=columns)

states_to_learn.to_csv('States to learn.csv')




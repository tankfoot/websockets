from core import Machine


class Waze(object):
    pass


user = Waze()

states = ['first', 'second', 'third', 'fourth']

transitions = [
    {'trigger': 'navigation', 'source': 'first', 'dest': 'second'},
    {'trigger': 'navigation_cancel', 'source': 'second', 'dest': 'first'}
]


machine = Machine(model=user, states=states, transitions=transitions, initial='first')


# Test
print(user.state)
user.navigation()
print(user.state)
user.navigation_cancel()
print(user.state)
user.navigation_cancel()
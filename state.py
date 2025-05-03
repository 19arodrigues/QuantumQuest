# States are managed on the game.states stack. Typically the stack will look like this starting from the bottom: titleScreen, level, menu/levelUI

class State():
    def __init__(self, game, name):
        self.game = game
        self.prev_state = None
        self.stateName = name

    def update(self, deltaTime, actions):
        pass

    def render(self, window):
        pass

    def enterState(self):
        if len(self.game.stateStack) > 1:
            self.prev_state = self.game.stateStack[-1]
        self.game.stateStack.append(self)

    def exitState(self):
        self.game.stateStack.pop()
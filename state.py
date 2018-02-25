import shelve
import random
import sys

class State:
    def __init__(self, filename):
        self.filename = filename
        self.username = "nobody"
        self.player_position = 1
        self.wumpus_position = random.randint(2, 20)
        self.pit_position = random.randint(2, 20)
        self.bat_position = random.randint(2, 20)
        self.arrow_position = random.randint(2, 20)
        self.arrows_remaining = 3

    def load(self, username):
        self.username = username
    	current_state = None
        statedb = shelve.open(self.filename)

        try:
            current_state = statedb[self.username]
            self.player_position = current_state['player_position']
            self.wumpus_position = current_state['wumpus_position']
            self.pit_position = current_state['pit_position']
            self.bat_position = current_state['bat_position']
            self.arrow_position = current_state['arrow_position']
            self.arrows_remaining = current_state['arrows_remaining']
        except:
            self.update()
            raise
        finally:
            statedb.close()


    def get_player_position():
        return self.player_position


    def set_player_position(player_position):
        self.player_position = player_position

    def get_wumpus_position():
        return self.get_wumpus_position


    def set(self, username, state):
        statedb = shelve.open(self.filename)
        statedb[username] = { "username": "cherdt", "update": "1" }
        statedb.sync()
        statedb.close()

    def update(self):
        statedb = shelve.open(self.filename)
        statedb[self.username] = { "username": self.username, "player_position": self.player_position, "wumpus_position": self.wumpus_position, "pit_position": self.pit_position, "bat_position": self.bat_position, "arrow_position": self.arrow_position, "arrows_remaining": self.arrows_remaining }
        #statedb.sync()
        statedb.close()

    def delete(self):
        # TODO confirm self.filename is defined
        statedb = shelve.open(self.filename)
        del statedb[self.username]
        statedb.close()
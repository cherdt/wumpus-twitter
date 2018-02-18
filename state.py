import shelve

class State:
    def __init__(self, filename):
        self.filename = filename

    def get(self, username):
    	state = None
        statedb = shelve.open(self.filename)

        try:
            state = statedb[username]
        except:
        	pass
            #print(username + ' not found')
            #statedb[username] = { "username": "cherdt" }

        statedb.sync()
        statedb.close()

        return state

    def set(self, username, state):
        statedb = shelve.open(self.filename)
        statedb[username] = { "username": "cherdt", "update": "1" }
        statedb.sync()
        statedb.close()
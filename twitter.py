# this is mostly just a wrapper around the birdy
import shelve

class Twitter:
    def __init__(self, client, statedb):
        self.client = client
        self.statedb = statedb
        self.last_seen_dm = 1

    def get_last_seen_dm(self):
    	db = shelve.open(self.statedb)
    	self.last_seen_dm = db['last_seen_dm']
    	db.close()
    	return self.last_seen_dm

    def set_last_seen_dm(self, id):
    	db = shelve.open(statedb)
    	db['last_seen_dm'] = id
    	db.close()

    def favorite(self, tweet_id):
        response = self.client.api.favorites.create.post(id=str(tweet_id))

    def retweet(self, tweet_id):
        response = self.client.api.statuses.retweet.post(id=str(tweet_id))

    def update(self, tweet):
        response = self.client.api.statuses.update.post(status=str(tweet))

    def dm(self, user, message):
    	response = self.client.api.direct_messages.new.post(screen_name=str(user), text=str(message))

    def get_dms_since(self, id):
        response = self.client.api.direct_messages.get(since_id=str(id), count=1)
        return response
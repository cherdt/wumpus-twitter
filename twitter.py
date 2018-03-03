# this is mostly just a wrapper around the birdy
import shelve

class Twitter:
    def __init__(self, client, statedb):
        self.client = client
        self.statedb = statedb
        self.last_seen_dm = 1

    def get_last_seen_dm(self):
    	"""Get the most recent tweet id from the state table"""
    	db = shelve.open(self.statedb)
    	try:
    	    self.last_seen_dm = db['last_seen_dm']
    	except:
    		db['last_seen_dm'] = self.last_seen_dm
    	db.close()
    	return self.last_seen_dm

    def set_last_seen_dm(self, id):
    	"""Update the most recent tweet id in the state table to the specified id"""
    	db = shelve.open(self.statedb)
    	db['last_seen_dm'] = id
    	db.close()

    def favorite(self, tweet_id):
    	"""Favorite the specified tweet"""
        response = self.client.api.favorites.create.post(id=str(tweet_id))

    def retweet(self, tweet_id):
    	"""Retweet the specified tweet"""
        response = self.client.api.statuses.retweet.post(id=str(tweet_id))

    def update(self, tweet):
    	"""Post the specified tweet to the user's timeline"""
        response = self.client.api.statuses.update.post(status=str(tweet))

    def dm(self, user, message):
    	"""Send the specified user the specified message as a DM"""
    	response = self.client.api.direct_messages.new.post(screen_name=str(user), text=str(message))

    def get_dms_since(self, id):
    	"""Get direct messages older than the specified id"""
        response = self.client.api.direct_messages.get(since_id=str(id), count=1)
        return response

    def get_followers(self, username):
        """Get users who follow the specified screen_name"""
        response = self.client.api.followers.list.get(screen_name=username, skip_status="true", include_user_entities="false")
        return response

    def follow(self, username):
        """Follow the specified screen_name"""
        response = self.client.api.friendships.create.post(screen_name=username,follow='true')

    def follow_my_followers(self, username):
        """Follow users that follow the specified user."""
        response = self.get_followers(username)
        for follower in response.data.users:
            if not follower.following:
                self.follow(follower.screen_name.encode('ascii', 'ignore'))

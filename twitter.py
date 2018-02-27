# this is just a wrapper around the birdy

class Twitter:
    def __init__(self, client):
        self.client = client

    def favorite(self, tweet_id):
        response = self.client.api.favorites.create.post(id=str(tweet_id))

    def retweet(self, tweet_id):
        response = self.client.api.statuses.retweet.post(id=str(tweet_id))

    def update(self, tweet):
        response = self.client.api.statuses.update.post(status=str(tweet))

    def dm(self, user, message):
    	response = self.client.api.direct_messages.new.post(screen_name=str(user), text=str(message))

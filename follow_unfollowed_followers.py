import sys
from config import get_client
from birdy.twitter import UserClient
from twitter import Twitter


def main(argv):

    # Make sure we received a target user
    if len(argv) != 2:
        print "usage: python follow_unfollowed_followers.py username"
        sys.exit()

    # create twitter client
    client = get_client()

    # create Twitter...
    twitter = Twitter(client, "state")

    # follow unfollowed followers
    twitter.follow_my_followers(argv[1])


if __name__ == "__main__":
    main(sys.argv)
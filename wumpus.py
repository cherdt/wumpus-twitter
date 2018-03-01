from state import State
from board import Board
from config import get_client
from birdy.twitter import UserClient
from twitter import Twitter
import re
import random
import sys


state = State("state")
board = Board()
# create twitter client
client = get_client()
# create twitter wrapper
twitter = Twitter(client, "twitter_state")


def is_debug_mode():
    return False


def tweet(msg):
    if is_debug_mode():
        print msg
    else:
        twitter.dm(state.username, msg)


def display_moves():
    print_state()
    msg = "\nPossible moves:"
    for move in board.get_adjacent(state.player_position):
        msg += " " + str(move)
    msg += "\nYour move? (type 'help' for list of commands)"
    tweet(msg)


def get_random_event():
    msg = ""
    # decide if we're going to show a random event at all
    # if so, pick a random event
    return msg


# make the Wumpus move to an adjacent cave
def disturb_wumpus():
    # get array of positions adjacent to the wumpus
    wumpus_adjacent = board.get_adjacent(state.wumpus_position)

    # remove player position
    wumpus_adjacent.remove(state.player_position)
    # add wumpus position
    wumpus_adjacent.append(state.wumpus_position)

    # select randomly an adjacent position or the current position
    state.wumpus_position = wumpus_adjacent[random.randint(0,len(wumpus_adjacent)-1)]
    state.update()
        

# takes 1 argument, the destination
def check_position():
    # check wumpus
    if state.player_position == state.wumpus_position:
        tweet("You've been eaten by a wumpus!")
        state.delete()
        sys.exit()

    # check pit
    if state.player_position == state.pit_position:
        tweet("You fell down a pit! You died!")
        state.delete()
        sys.exit()

    # check bats
    if state.player_position == state.bat_position:
        state.player_position = random.randint(1, 20)
        state.update()
        tweet("Bats carried you away!")
        # player has moved, re-check state
        check_position()

    # check arrow
    if state.player_position == state.arrow_position:
        tweet("You found an arrow!")
        state.arrow_position = 999
        state.arrows_remaining += 1
        state.update()


# takes 1 argument, the destination
def move (v):
    if board.is_adjacent(v, state.player_position):
        state.player_position=int(v)
        state.update()
        check_position()
    else:
        tweet("Invalid move: " + v)


# takes 1 argument, the target
def shoot(v):
    target = int(v)
    if state.arrows_remaining > 0:
        if board.is_adjacent(target, state.player_position):
            if target == state.wumpus_position:
                tweet("You killed the wumpus! You WIN!")
                state.delete()
                sys.exit()
            else:
                tweet("Drats! Missed!")
                state.arrows_remaining -= 1
                if board.is_adjacent(state.wumpus_position, state.player_position):
                    disturb_wumpus()
        else:
            # Check to see if target is user's own board position
            if target == state.player_position:
                tweet("You refrain from such foolishness.")
            # Otherwise, user is targeting non-adjacent cavern
            else:
                tweet("Think you can shoot through rock walls?")
    else:
        tweet("No arrows left.")


def process_command(cmd):
    if re.search('^[0-9]+$', cmd):
        move(cmd)
    elif re.search('^[Mm][^ ]* [0-9]+$', cmd):
        match = re.search('^[Mm][^ ]* ([0-9]+)$', cmd)
        move(match.group(1))
    elif re.search('^[Ss][^ ]* [0-9]+$', cmd):
        match = re.search('^[Ss][^ ]* ([0-9]+)$', cmd)
        shoot(match.group(1))
    elif re.search('^[EeQq]', cmd):
        tweet("You retire to a comfortable life of not hunting wumpuses.")
        tweet("DM me any time to start a new game.")
        state.delete()
        sys.exit()
    else:
        print_help()


def print_help():
    tweet("Commands are:" +
          "\n- (m|move) #" +
          "\n- s|shoot #" +
          "\n- h|help" +
          "\n- q|quit")


def print_intro():

    tweet("*** HUNT THE WUMPUS ***" +
          "\n" +
          "\nYou are in a series of dark caverns." +
          "\nLike, really dark." +
          "\nYou can barely see." +
          "\n" +
          "\nThe caverns are ADA compliant." +
          "\nThey are numbered in Braille." +
          "\nWhich, somehow, you can read. Cool!")

    tweet("You are here to hunt the terrifying wumpus." +
         "\nYou'll know when he's near. You'll smell him." +
         "\nAnd look out for the bottomless pit." +
         "\nAnd did I mention the bats?" +
         "\n" +
         "\nYou have 3 arrows.")


def get_adjacent_danger():
    msg = ""

    if board.is_adjacent(state.player_position, state.wumpus_position):
        msg += "\nYou smell something awful."

    if board.is_adjacent(state.player_position, state.pit_position):
        msg += "\nYou feel a breeze."

    if board.is_adjacent(state.player_position, state.bat_position):
        msg += "\nYou hear flapping."
    
    return msg


def print_state():
    msg = "You are in cavern " + str(state.player_position) + "."
    #if is_debug_mode():
    #    msg += "\nW: " + state.wumpus_position +", P: " + state.pit_position + ", B: " + state.bat_position + ", A: " + state.arrow_position
    msg += get_random_event()
    msg += get_adjacent_danger()
    tweet(msg)


def get_commands_from_twitter():
    # Get DMs posted after the last DM we've seen
    id = twitter.get_last_seen_dm()
    response = twitter.get_dms_since(id)

    # Initialize the last DM we've seen
    newest_dm_id = id

    # for each DM, call main and pass username and DM text (command)
    for message in response.data:
        # If this ID is later than our latest ID, update the latest ID
        if message.id > int(newest_dm_id):
            newest_dm_id = int(message.id)
        # call main to process this game command
        main(['python', message.sender_screen_name.encode('ascii', 'ignore'), message.text.encode('ascii', 'ignore')])

    # Update last_seen_dm in twitter state db
    twitter.set_last_seen_dm(newest_dm_id)


def main(argv):
    # Make sure we received a target user
    if len(argv) < 2:
        if is_debug_mode():
            print "usage: python wumpus.py username [move]"
        else:
            get_commands_from_twitter()
        sys.exit()

    # Strip invalid username characters (only A-Za-z0-9_ are valid)
    username = re.sub(r'[^A-Za-z0-9_]', r'', argv[1])

    # Check for existing game/state
    try:
        state.load(username)
    except:
        print_intro()
        display_moves()
        sys.exit()

    if len(argv) < 3:
        display_moves()
        print_help()
    else:
        # Strip unexpected characters (only A-Za-z0-9 " " and "?" are valid)
        process_command(re.sub(r'[^A-Za-z0-9\?\ ]', r'',argv[2]))
        display_moves()
        sys.exit()


if __name__ == "__main__":
    main(sys.argv)

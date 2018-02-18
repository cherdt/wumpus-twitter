#!/bin/bash

is_game_in_progress () {
    grep --quiet ^$1\  .state
}

get_state () {
    local STATE=$(grep ^$1\  .state)
    USERNAME=$(echo $STATE | cut -d' ' -f1)
    PLAYER=$(echo $STATE | cut -d' ' -f2)
    WUMPUS=$(echo $STATE | cut -d' ' -f3)
    BATS=$(echo $STATE | cut -d' ' -f4)
    PIT=$(echo $STATE | cut -d' ' -f5)
    ARROW=$(echo $STATE | cut -d' ' -f6)
    ARROWS_REMAINING=$(echo $STATE | cut -d' ' -f7)
}

set_state () {
    sed -i "s/^$USERNAME\ .*/$USERNAME $PLAYER $WUMPUS $BATS $PIT $ARROW $ARROWS_REMAINING $(date -u +%s)/" .state
    echo $USERNAME $PLAYER $WUMPUS $BATS $PIT $ARROW $ARROWS_REMAINING $(date -u +%s)
}

delete_state () {
    GAMEOVER=1
    sed -i "/^$USERNAME\ .*/d" .state
}

translate_computer_to_human () {
    echo $(((($1/2)+1)+(($1%2)*10)))
}

translate_human_to_computer () {
    local SOLUTION=$((((($1-1)%10)*2)+($1/10)))
    # hack below because I haven't found a general solution
    if [ $(($1%10)) -eq 0 ]
    then
        let "SOLUTION = SOLUTION - 1"
    fi
    echo $SOLUTION
}

display_moves () {
    local MOVES=''
    for NODE in $*
    do
        MOVES="$(translate_computer_to_human $1) $MOVES"
        shift
    done
    echo "Possible moves: $(echo $MOVES | tr ' ' '\n' | sort -n | paste -d' ' -s)"
}

random_event () {
    if [ $(seq 1 2 | shuf -n 1) -eq 1 ]
    then
        echo "$(shuf -n 1 random)"
    fi
}

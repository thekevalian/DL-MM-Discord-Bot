# DL-MM-Discord-Bot
A discord bot for matchmaking (still in development)

Motivation:
Playing Deadlock is much more fun with pick & bans systems where all players communicate and their is strategy. No more random comps, but now with strategic play. The goal of this bot is two part:

1) Be able to easily view information about your current rank and match
    1. See the games of your last n matches (Teammates, Enemies, Game Stats)
    2. See simple hero stats (Best Heroes ...)
    3. Build the backbone for part 2

2) Create a matchmaking system that would work like the following:
    1. Users enter a voice channel called "Queue"
    2. The users in this channel are entered to a queue, where some matchmaking algorithm will account for:
        - player hero pool (Player Mains)
        - player ranks (Player Rank - still deciding if internal rank or existing ranking system will be used)
        - player playstyle (Support, Carry, ...)
    3. The teams created by matchmaking are moved to 2 different voice channels where a pick & ban system website will be linked
        - A discord alternative to this can be made in the future
    4. After both teams are ready, a new custom match will be create where both teams can join

The 2nd part will definitely be the most difficult, but hopefully we'll make progress.

To generate Protobuf Bindings:
1. run `python genbindings.py`
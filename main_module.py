﻿# This is the main game file and it will be deliberately short.
import libtcodpy as libtcod # "The Doryen Library" v1.5.1 Source: https://bitbucket.org/libtcod/libtcod
# classes.py - Here are the classes shared between modules (Tile, Object and Rect).
# component.py - The game components are defined here.
# ai. py - Artificial Inteligence classes.
import cartographer # This handles the map object (tecniaclly a class but it deserves special treatment).
# demographic.py - Functions to generate creatures and items and populate areas.
import render # All related to displaying stuff on the screen.
import get_input # Self explainatory.
import globals # Here live the global functions and objects (player, map, object list, etc.).

# Start the game screen.
render.init_screen()

# Start new game.
globals.init_player('new')
globals.init_map('new')
#globals.init_map('new', map_function=cartographer.make_dungeon)
globals.set_game_state('playing')
globals.init_game_msgs('new')
player_action = None
globals.message('You were bored, you craved adventure and due to your total lack of common sense and reckless impulsive behavior you came here, to some strange ruins half a world away from what you call civilization!', libtcod.light_cyan)
globals.message('Did you at least told somebody what you where up to?', libtcod.crimson)
globals.message('Well, its kinda late for that.', libtcod.light_purple)


# Start user interface.
render.init_ui()

# Main loop.
while not libtcod.console_is_window_closed():
  render.all(globals.player())
  libtcod.console_flush()
  globals.player().fighter.check_state()
  player_action = get_input.handle_keys(globals.player())
  for object in globals.objects():
    render.clear(object)
  if player_action == 'exit':
    break
  if globals.get_game_state() == 'playing' and player_action != 'didnt-take-turn':
    for object in globals.objects():
      if object.fighter:
        object.fighter.check_state()
      if object.ai:
        object.ai.take_turn()

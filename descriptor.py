import libtcodpy as libtcod
import engine
import classes
import combat
import ai
import render
import glob
import os

def creature_chances():
  chances = {}
  chances['snake'] = 40
  chances['orc'] = 40
  chances['troll'] = from_dungeon_level([[15, 3], [30, 5], [60, 7]])
  return chances

def creatures(id, x, y):
  if id == 'player':
    creature_component = classes.Creature(faction='player', hp=100, defense=1, power=4, sight=7, poison_resist=30, xp_bonus=350, lvl_base=200, lvl_factor=150, inv_max=26, death_function=player_death)
    ai_component = ai.PlayerControlled()
    creature = classes.Object(0, 0, '@', 'player', libtcod.white, blocks=True, creature=creature_component, ai=ai_component)
  elif id == 'snake':
    creature_component = classes.Creature(faction='wild', hp=10, defense=0, power=3, sight=15, poison_resist=80, xp_bonus=20, lvl_base=20, lvl_factor=15, death_function=monster_death, nat_atk_effect=inflict_poison)
    ai_component = ai.BasicMonster()
    creature = classes.Object(x, y, 's', 'snake', libtcod.darker_red, blocks=True, creature=creature_component, ai=ai_component)
  elif id == 'orc':
    creature_component = classes.Creature(faction='dungeon', hp=20, defense=0, power=4, sight=10, poison_resist=20, xp_bonus=35, lvl_base=40, lvl_factor=20, death_function=monster_death)
    ai_component = ai.BasicMonster()
    creature = classes.Object(x, y, 'o', 'orc', libtcod.desaturated_green, blocks=True, creature=creature_component, ai=ai_component)
  elif id == 'troll':
    creature_component = classes.Creature(faction='dungeon', hp=30, defense=2, power=8, sight=5, poison_resist=30, xp_bonus=100, lvl_base=200, lvl_factor=150, death_function=monster_death)
    ai_component = ai.BasicMonster()
    creature = classes.Object(x, y, 'T', 'troll', libtcod.darker_green, blocks=True, creature=creature_component, ai=ai_component)
  return creature

def player_death(player, attacker):
  if attacker is not None: render.message('You were killed by ' + attacker.name.capitalize() + '!', libtcod.red)
  else: render.message('You died of severe battle wounds.', libtcod.red)
  player.ai.state = 'dead'
  player.char = '%'
  player.color = libtcod.dark_red
  player.blocks = False
  player.name = 'remains of ' + player.name
  player.send_to_back()
  try:
    os.remove('savegame')
  except:
    return
  for f in glob.glob('lvl*'):
    os.remove(f)

def monster_death(monster, attacker):
#  eq = [piece for piece in monster.creature.equipment.values() if piece is not None]
#  for obj in eq:
#    obj.equipment.dequip(monster)
#  for obj in monster.creature.inventory:
#    obj.item.drop(monster)
  if attacker.ai is not None: render.message(monster.name.capitalize() + ' was killed by ' + attacker.name.capitalize() + '!', libtcod.orange)
  else: render.message(monster.name.capitalize() + ' died of severe battle wounds.', libtcod.orange)
  monster.char = '%'
  monster.color = libtcod.dark_red
  monster.blocks = False
  monster.creature = None
  monster.ai = None
  monster.name = 'remains of ' + monster.name
  monster.send_to_back()

def item_chances():
  chances = {}
#  chances['possess'] = 5
  chances['bow'] = 5
  chances['arrow'] = 10
  chances['throwing knife'] = from_dungeon_level([[10, 2]])
  chances['dagger'] = 10
  chances['machete'] = from_dungeon_level([[10, 2]])
  chances['sword'] = from_dungeon_level([[10, 3]])
  chances['heal'] = 35
  chances['lightning'] = from_dungeon_level([[25, 4]])
  chances['fireball'] =  from_dungeon_level([[25, 6]])
  chances['confuse'] =   from_dungeon_level([[10, 2]])
  return chances

def items(id, x, y):
  if id == 'fireball':
    item_component = classes.Item(1, use_function=scroll)
    spell_component = classes.Spell(power=25, spell_range =3 , effect=combat.cast_fireball)
    item = classes.Object(x, y, chr(151), 'scroll of fireball', libtcod.red, item=item_component, spell=spell_component)
  elif id == 'lightning':
    item_component = classes.Item(1, use_function=scroll)
    spell_component = classes.Spell(power=40, spell_range =5 , effect=combat.cast_lightning)
    item = classes.Object(x, y, chr(151), 'scroll of lightning bolt', libtcod.light_yellow, item=item_component, spell=spell_component)
  elif id == 'confuse':
    item_component = classes.Item(1, use_function=scroll)
    spell_component = classes.Spell(power=10, spell_range =5 , effect=combat.cast_confuse)
    item = classes.Object(x, y, chr(151), 'scroll of confusion', libtcod.purple, item=item_component, spell=spell_component)
  elif id == 'heal':
    item_component = classes.Item(1, use_function=scroll)
    spell_component = classes.Spell(power=40, effect=combat.cast_heal)
    item = classes.Object(x, y, chr(144), 'healing potion', libtcod.violet, item=item_component, spell=spell_component)
#  elif id == 'possess':
#    item_component = classes.Item(1, use_function=scroll)
#    spell_component = classes.Spell(power=10, spell_range =5 , effect=combat.cast_possess)
#    item = classes.Object(0, 0, chr(151), 'scroll of possession', libtcod.green, item=item_component, spell=spell_component)
  elif id == 'sword':
    equipment_component = classes.Equipment(slot='hand', power_bonus = 3)
    item = classes.Object(x, y, chr(148), 'sword', libtcod.sky, equipment=equipment_component)
  elif id == 'machete':
    equipment_component = classes.Equipment(slot='hand', power_bonus = 2)
    item = classes.Object(x, y, chr(148), 'machete', libtcod.gray, equipment=equipment_component)
  elif id == 'dagger':
    equipment_component = classes.Equipment(slot='hand', power_bonus = 1)
    item = classes.Object(x, y, chr(150), 'dagger', libtcod.silver, equipment=equipment_component)
  elif id == 'throwing knife':
    item_component = classes.Item(1, projectile_bonus = 2, use_function=combat.projectile)
    item = classes.Object(x, y, chr(150), 'throwing knife', libtcod.light_blue, item=item_component)
  elif id == 'bow':
    equipment_component = classes.Equipment(slot='hand', ammo='arrow', power_bonus = 1)
    item = classes.Object(x, y, chr(146), 'bow', libtcod.dark_gray, equipment=equipment_component)
  elif id == 'arrow':
    item_component = classes.Item(5, ammo='arrow', projectile_bonus = 1)
    item = classes.Object(x, y, chr(147), 'arrow', libtcod.dark_gray, item=item_component)
  return item

def inflict_poison(attacker, target):
  if libtcod.random_get_int(0, 1, 100) > target.creature.poison_resist:
    target.creature.status = 'poison'
    target.creature.status_inflictor = attacker
    if target == engine.state().player: 
      render.message(target.name.capitalize() + ' has been poisoned by ' + attacker.name + '.', libtcod.purple)
    if attacker == engine.state().player:
      render.message(attacker.name.capitalize() + ' has poisoned ' + target.name + '.', libtcod.fuchsia)

def scroll(owner, caster):
  if owner.spell.effect(owner, caster) == 'cancelled': return 'cancelled'

def from_dungeon_level(table):
  for (value, level) in reversed(table):
    if engine.state().d_level >= level:
      return value
  return 0
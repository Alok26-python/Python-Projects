import random

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import item

fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# white Magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# create item
potion = item("Potion", "potion", "Heals 50HP", 50)
hipotion = item("Hipotion", "potion", "Heals 100 HP", 100)
superpotion = item("Superpotion", "potion", "Heals 1000 HP", 1000)
elixir = item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
megaelixir = item("MegaElixir", "elixir", "Fully restores pary's HP/MP", 9999)

grenade = item("Grenade", "attack", "Deals 500 damage", 500)
player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_magic = [fire, meteor, curaga]
player_item = [{"item": potion, "quantity": 15},
               {"item": hipotion, "quantity": 5},
               {"item": superpotion, "quantity": 5},
               {"item": elixir, "quantity": 5},
               {"item": megaelixir, "quantity": 5},
               {"item": grenade, "quantity": 5}]
# Inline instantiation
player1 = Person("Valos:", 3260, 132, 300, 34, player_magic, player_item)
player2 = Person("Nick :", 4610, 188, 311, 34, player_magic, player_item)
player3 = Person("Robox:", 3089, 174, 288, 34, player_magic, player_item)

players = [player1, player2, player3]
# print("Damage is:", player.generate_damage())
# print("Damage is:", player.generate_damage())
# print("Damage is:", player.generate_damage())
# print("Spell Damage is:", player.generate_spell_damage(0))
# print("Spell Damage is:", player.generate_spell_damage(1))
# print("Spell Damage is:", player.generate_spell_damage(2))
enemy1 = Person("Imp  :", 1250, 130, 560, 325, enemy_magic, [])
enemy2 = Person("Magus:", 11200, 201, 525, 25, enemy_magic, [])
enemy3 = Person("Imp  :", 1250, 130, 560, 325, enemy_magic, [])

enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("====================")
    print(bcolors.BOLD + "Name                   HP                                     MP" + bcolors.ENDC)
    for player in players:
        # print("\n\n")
        player.get_stats()
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()
    print("\n")

    for player in players:
        player.choose_action()
        choice = input("    Choose action:")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace("  :", "") + " for", dmg, "points of damage")
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace("  :", "") + " has died")
                del enemies[enemy]
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic:")) - 1

            if magic_choice == -1:
                continue
            # new code
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough MO\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for " + str(magic_dmg) + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to" + enemies[enemy].name.replace("  :", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace("  :", "") + " has died")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            item_choice = int(input("    Choose items : ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left...." + "\n")
                continue
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print("\n" + bcolors.OKGREEN + item.name + " heals for " + str(item.prop) + "HP" + bcolors.ENDC)

            if item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print("\n" + bcolors.FAIL + item.name + " deals " + str(item.prop) + " points of Damage to " + enemies[
                    enemy].name.replace("  :", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace("  :", "") + " has died")
                    del enemies[enemy]

            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print("\n" + bcolors.OKGREEN + item.name + " Fully restores HP/MP " + bcolors.ENDC)

    total_enemy_hp = 0
    total_players_hp = 0
    for enemy in enemies:
        total_enemy_hp += enemy.get_hp()
    for player in players:
        total_players_hp += player.get_hp()

    if total_enemy_hp <= 0:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False
    elif total_players_hp == 0:
        print(bcolors.FAIL + "Your Enemy Has Defeated You" + bcolors.ENDC)
        running = False

    print("\n")
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            target = random.randrange(0, 3)
            pdmg = enemy.generate_damage()
            players[target].take_damage(pdmg)
            print(bcolors.FAIL + enemy.name.replace(":", "") + " Attacks " + players[target].name.replace(" :", "") + " for", pdmg,
                  "points of damage.")

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            # print ("Enemy Chose",spell, "damage is ",magic_dmg)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(
                    bcolors.FAIL  + spell.name + " heals " + enemy.name.replace("  :", "") + " for " + str(magic_dmg) + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + enemy.name.replace("  :", "") + "'s " + spell.name + " deals",
                      str(magic_dmg),
                      "points of damage to" + players[target].name.replace("  :", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace("  :", "") + " has died")
                    del players[target]

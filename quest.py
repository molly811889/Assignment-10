from colorama import Fore
from item import make_item

class QuestManager:
    def __init__(self, player):
        self.player = player

    def show(self):
        print(Fore.YELLOW + "\n=== QUEST LOG ===")
        steps = [
            "Speak with Elder Rowan in the village.",
            "Defeat a Goblin and recover the ward key.",
            "Find the Sunstone in the Forest.",
            "Return to Elder Rowan, then defeat the Ashen Dragon."
        ]
        for i, step in enumerate(steps):
            status = "DONE" if self.player.main_quest_step > i else "ACTIVE" if self.player.main_quest_step == i else "LOCKED"
            print(f"Main {i+1} [{status}]: {step}")
        print("Side quest - Herbalist: collect a Mana Crystal and speak to the Herbalist.")
        print("Status:", "Complete" if self.player.side_quests.get("herbs") else "Incomplete")
        print("Side quest - Village Guard: defeat two monsters and speak to the Guard.")
        print("Status:", "Complete" if self.player.side_quests.get("wolves") else "Incomplete")

    def interact(self, npc_key):
        if npc_key == "elder":
            if self.player.main_quest_step == 0:
                print("Main quest started: restore the wards and save Emberfall.")
                self.player.main_quest_step = 1
            elif self.player.main_quest_step == 1 and self.player.monsters_defeated >= 1:
                print("You have proven yourself. Search the Forest for the Sunstone.")
                self.player.main_quest_step = 2
            elif self.player.main_quest_step == 2 and any(i["name"] == "Sunstone" for i in self.player.inventory.items):
                self.player.inventory.items = [i for i in self.player.inventory.items if i["name"] != "Sunstone"]
                self.player.main_quest_step = 3
                print("The Sunstone restores the ward. The Ashen Dragon awaits in the Ruins!")
            elif self.player.main_quest_step >= 3:
                print("The final task remains: defeat the Ashen Dragon.")
        elif npc_key == "herbalist" and not self.player.side_quests["herbs"]:
            if any(i["name"] == "Mana Crystal" for i in self.player.inventory.items):
                self.player.inventory.items = [i for i in self.player.inventory.items if i["name"] != "Mana Crystal"]
                self.player.side_quests["herbs"] = True
                self.player.gold += 20
                self.player.gain_xp(40)
                self.player.inventory.add(make_item("potion"))
                print(Fore.GREEN + "Herbalist quest complete: 20 gold, 40 XP, and a potion!")
            else:
                print("Herbalist quest: bring me a Mana Crystal from a Wraith.")
        elif npc_key == "guard" and not self.player.side_quests["wolves"]:
            if self.player.monsters_defeated >= 2:
                self.player.side_quests["wolves"] = True
                self.player.gold += 25
                self.player.gain_xp(50)
                print(Fore.GREEN + "Guard quest complete: 25 gold and 50 XP!")
            else:
                print("Guard quest: defeat any two monsters and report back.")
        elif npc_key == "merchant":
            print("The shop is open from the Shop menu.")
        elif npc_key == "scholar":
            print("Scholar's advice: skills have different effects and cooldowns. Prepare before the boss.")

    def on_monster_defeated(self, monster_key):
        if self.player.main_quest_step == 1 and self.player.monsters_defeated >= 1:
            print(Fore.YELLOW + "Quest update: return to Elder Rowan.")
        if monster_key == "ashen_dragon":
            self.complete_main_quest()

    def complete_main_quest(self):
        self.player.main_quest_step = 4

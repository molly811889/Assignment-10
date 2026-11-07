from colorama import Fore

class Skill:
    name = "Skill"
    description = "A basic skill."
    cost = 0
    cooldown = 1

    def apply(self, player):
        raise NotImplementedError("Skill subclasses must implement apply().")

class Fireball(Skill):
    name = "Fireball"
    description = "Increase your next attack by 15."
    cost = 20
    cooldown = 2

    def apply(self, player):
        player.attack += 15
        print(Fore.YELLOW + "Fireball power surges through you. Attack increased by 15.")

class Heal(Skill):
    name = "Heal"
    description = "Restore 30 HP."
    cost = 15
    cooldown = 3

    def apply(self, player):
        old = player.hp
        player.hp = min(player.max_hp, player.hp + 30)
        print(Fore.GREEN + f"Heal restored {player.hp - old} HP.")

class Shield(Skill):
    name = "Shield"
    description = "Gain 5 armor for the next combat hit."
    cost = 25
    cooldown = 2

    def apply(self, player):
        player.equipped_armor += 5
        print(Fore.CYAN + "Shield raised. Armor increased by 5.")

SKILL_LIBRARY = {c.name: c for c in (Fireball, Heal, Shield)}

def skill_from_dict(name):
    return SKILL_LIBRARY[name]()

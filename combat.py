from colorama import Fore
from skill import skill_from_dict

class Combat:
    def __init__(self, player, save_callback=None):
        self.player = player
        self.save_callback = save_callback

    def fight(self, monster):
        print(Fore.RED + f"\nA {monster.name} appears!")
        while monster.hp > 0 and self.player.hp > 0:
            print(f"\nYour HP {self.player.hp}/{self.player.max_hp} | {monster.name} HP {monster.hp}/{monster.max_hp}")
            print("1 Attack  2 Use skill  3 Use potion  4 Run")
            choice = input("> ").strip()
            if choice == "1":
                damage = self.player.attack + self.player.equipped_weapon_bonus
                monster.hp -= damage
                print(Fore.GREEN + f"You deal {damage} damage.")
            elif choice == "2":
                if not self.player.learned_skills:
                    print("You have no learned skills.")
                    continue
                for i, name in enumerate(self.player.learned_skills, 1):
                    print(f"{i}. {name} (cooldown {self.player.cooldowns.get(name, 0)})")
                try:
                    n = int(input("Skill number (0 cancels): "))
                    if n == 0:
                        continue
                    if not 1 <= n <= len(self.player.learned_skills):
                        raise ValueError
                    name = self.player.learned_skills[n - 1]
                    if self.player.cooldowns.get(name, 0) > 0:
                        print("Skill is on cooldown.")
                        continue
                    skill = skill_from_dict(name)
                    skill.apply(self.player)
                    self.player.cooldowns[name] = skill.cooldown
                except ValueError:
                    print("Enter a valid number.")
                    continue
            elif choice == "3":
                if not self.player.inventory.use_item(self.player, item_type="potion"):
                    continue
            elif choice == "4":
                if monster.name == "Ashen Dragon":
                    print("You cannot flee from the final boss.")
                    continue
                print("You escaped from combat.")
                return False
            else:
                print("Invalid choice.")
                continue
            if monster.hp <= 0:
                break
            damage = max(1, monster.special_move(self.player) - self.player.equipped_armor)
            self.player.hp = max(0, self.player.hp - damage)
            print(Fore.RED + f"{monster.name} deals {damage} damage.")
            for key in self.player.cooldowns:
                self.player.cooldowns[key] = max(0, self.player.cooldowns[key] - 1)
            if self.save_callback:
                self.save_callback()
        if self.player.hp <= 0:
            return False
        print(Fore.GREEN + f"You defeated {monster.name}!")
        self.player.gain_xp(monster.xp_reward)
        return True

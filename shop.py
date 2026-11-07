from colorama import Fore
from item import make_item

class Shop:
    STOCK = ["potion", "iron_sword", "leather_armor"]

    def visit(self, player):
        print(Fore.YELLOW + f"\n=== MERCHANT SHOP | Gold: {player.gold} ===")
        for i, key in enumerate(self.STOCK, 1):
            item = make_item(key)
            print(f'{i}. {item["name"]} — {item["price"]} gold: {item["description"]}')
        print("0. Leave shop")
        try:
            choice = int(input("Buy which item? "))
            if choice == 0:
                return
            if not 1 <= choice <= len(self.STOCK):
                raise ValueError
            item = make_item(self.STOCK[choice - 1])
            if player.gold < item["price"]:
                print(Fore.RED + "Not enough gold.")
                return
            player.gold -= item["price"]
            player.inventory.add(item)
            print(Fore.GREEN + f'Purchased {item["name"]}.')
        except ValueError:
            print(Fore.RED + "Enter a valid shop number.")

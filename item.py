class Item:
    def __init__(self, name, item_type, price, description, **effects):
        self.name = name
        self.type = item_type
        self.price = price
        self.description = description
        self.effects = effects

    def to_dict(self):
        return {"name": self.name, "type": self.type, "price": self.price,
                "description": self.description, **self.effects}

def make_item(key):
    catalog = {
        "potion": Item("Health Potion", "potion", 10, "Restore up to 35 HP.", heal=35),
        "iron_sword": Item("Iron Sword", "weapon", 30, "Adds 5 attack.", attack_bonus=5),
        "leather_armor": Item("Leather Armor", "armor", 25, "Reduces incoming damage by 3.", armor_bonus=3),
        "mana_crystal": Item("Mana Crystal", "quest", 0, "A shimmering crystal prized by scholars."),
        "dragon_scale": Item("Dragon Scale", "quest", 0, "Proof that the Ashen Dragon was defeated.")
    }
    if isinstance(key, dict):
        return Item(key["name"], key["type"], key.get("price", 0), key.get("description", ""),
                    **{k: v for k, v in key.items() if k not in ("name", "type", "price", "description")})
    return catalog[key].to_dict()

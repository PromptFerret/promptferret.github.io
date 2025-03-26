embed
<drac2>
COMMAND = "!pm"
TITLE = "Pet Handler"
DESCRIPTION = "A **pet manager** made by **PromptFerret**. I accept gifts of gp, karma, dtp, magic items and sessions 🙃🌟🐕"
OUTPUT = "" #f"No action taken. Use `{COMMAND} help` for command details."
COLOR = "white"
THUMBNAIL = "https://promptferret.github.io/assets//promptferret_small.jpg"

#!------------------------- start maps --------------------------#

color_map = {
    "beige": "#F5F5DC",
    "black": "#000000",
    "blue": "#0000FF",
    "brown": "#A52A2A",
    "chocolate": "#D2691E",
    "coral": "#FF7F50",
    "crimson": "#DC143C",
    "cyan": "#00FFFF",
    "dark_gray": "#333333",
    "deep_blue": "#00008B",
    "forest_green": "#228B22",
    "gold": "#FFD700",
    "gray": "#808080",
    "green": "#008000",
    "indigo": "#4B0082",
    "ivory": "#FFFFF0",
    "lavender": "#E6E6FA",
    "light_gray": "#D3D3D3",
    "lime": "#00FF00",
    "magenta": "#FF00FF",
    "maroon": "#800000",
    "mint": "#98FF98",
    "navy": "#000080",
    "olive": "#808000",
    "orange": "#FFA500",
    "orchid": "#DA70D6",
    "peach": "#FFDAB9",
    "pink": "#FFC0CB",
    "plum": "#DDA0DD",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#FF0000",
    "salmon": "#FA8072",
    "sea_green": "#2E8B57",
    "silver": "#C0C0C0",
    "sky_blue": "#87CEEB",
    "tan": "#D2B48C",
    "teal": "#008080",
    "turquoise": "#40E0D0",
    "violet": "#EE82EE",
    "white": "#FFFFFF",
    "yellow": "#FFFF00"
}


superscript_map = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
    "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
    "+": "⁺", "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾",
    "!": "ᵎ", "?": "ˀ",

    "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ", "e": "ᵉ",
    "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ⁱ", "j": "ʲ",
    "k": "ᵏ", "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ",
    "p": "ᵖ", "q": "𐑞", "r": "ʳ", "s": "ˢ", "t": "ᵗ",
    "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ", "z": "ᶻ",

    "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ",
    "F": "ᶠ", "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ",
    "K": "ᴷ", "L": "ᴸ", "M": "ᴹ", "N": "ᴺ", "O": "ᴼ",
    "P": "ᴾ", "Q": "𐑞", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ"
}


subscript_map = {
    "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
    "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉",
    "+": "₊", "-": "₋", "=": "₌", "(": "₍", ")": "₎",
    "!": "﹗", "?": "﹖"
}

check_map = {
    # Raw Ability Checks (short)
    "str": "str",
    "dex": "dex",
    "con": "con",
    "int": "int",
    "wis": "wis",
    "cha": "cha",

    # Raw Ability Checks (long)
    "strength": "str",
    "dexterity": "dex",
    "constitution": "con",
    "intelligence": "int",
    "wisdom": "wis",
    "charisma": "cha",


    # Strength-based Skills
    "athletics": "str",

    # Dexterity-based Skills
    "acrobatics": "dex",
    "sleight_of_hand": "dex",
    "stealth": "dex",

    # Intelligence-based Skills
    "arcana": "int",
    "history": "int",
    "investigation": "int",
    "nature": "int",
    "religion": "int",

    # Wisdom-based Skills
    "animal_handling": "wis",
    "insight": "wis",
    "medicine": "wis",
    "perception": "wis",
    "survival": "wis",

    # Charisma-based Skills
    "deception": "cha",
    "intimidation": "cha",
    "performance": "cha",
    "persuasion": "cha",
}


save_map = {
    "strength": "str",
    "dexterity": "dex",
    "constitution": "con",
    "intelligence": "int",
    "wisdom": "wis",
    "charisma": "cha"
}
#!------------------------- end maps --------------------------#


#!------------------------- start schemas --------------------------#
pet_schema = {
    "name": None,
    "species": None,
    "description": "No description set. Use `!pet set description <value>` to set one.",
    "color":"#333333",
    "cr": None,
    "size": None,
    "type": None,
    "alignment": None,
    "ac": None,
    "initiative": None,
    "hp": {
        "max": None,
        "current": None,
        "temp": None
    },
    "stats": {
        "str": None,
        "dex": None,
        "con": None,
        "int": None,
        "wis": None,
        "cha": None
    },
    "proficiency": [],
    "expertise": [],
    "speed": [],
    "senses": [],
    "traits": [],
    "condition": [],
    "resist": [],
    "immune": [],
    "skills": {},
    "actions": {},
    "items": {},
    "thumbnail": None,
    "source": None
}

item_stat_schema = {
    "str": None,
    "dex": None,
    "con": None,
    "int": None,
    "wis": None,
    "cha": None,
    "initiative": None,
    "ac": None,
    "hp_max": None,
    "hp_temp": None,
    "save_str": None,
    "save_dex": None,
    "save_con": None,
    "save_int": None,
    "save_wis": None,
    "save_cha": None,
    "ground_speed": None,
    "fly_speed": None,
    "swim_speed": None,
    "climb_speed": None,
    "attack_bonus": None,
    "damage_bonus": None,
    # "spell_attack_bonus": None, # !! FUTURE PERHAPS !!
    # "spell_dc": None, # !! FUTURE PERHAPS !!
    "resist": [],
    "immune": [],
    # "darkvision": None,
    # "blindsight": None,
    # "senses" None, # !! FUTURE PERHAPS !!
    "passive_perception": None,
    "passive_insight": None,
    "passive_investigation": None,
    "luck_bonus": None,
    # "ignore_nonmagical_damage": False # !! FUTURE PERHAPS !!
}

skill_schema = {
    "name": None,
    "bonus": None
}


action_schema = {
    "name": None,
    "hit_roll": "1d20",
    "hit_modifier": "+0",
    "damage_roll": "1d10",
    "damage_modifier": "+0",
    "damage_type": "Undefined",
    "range": "Melee",
    "target": "Single Target",
    "description": "No description set. Use `!pet action edit <name> description <value>` to set one."
}


item_schema = {
    "name": None,
    "quantity": 0,
    "effect": {
        "stats": {}, # Such as stats.dex +1 when attuned
        "extra_effects": [] # Stuff that does not effect any values or roles, such as "you gain advantage on perception checks"
    },
    "active": False,
    "worn": False,
    "attuned": False,
    "description": None
}
#!------------------------- start schemas --------------------------#


# -----------------------------------------------------------------------#
#  Internal functions, these functions are used for basic functionality  #
# -----------------------------------------------------------------------#
def debug(data):
    return None, {"DESCRIPTION": data, "COLOR": color_map["orange"]}  # Output in orange to draw attention to the debug


def arg_processor(args):
    return {"command": args[0].lower() if args else None, **{str(i): arg for i, arg in enumerate(args[1:], start=1)}}


def deepcopy(obj):  # deepcopy does not exist in drac2, fake it till you make it
    return load_json(dump_json(obj))


def delete(dictionary, key): # del does not exist in drac2, fake it till you make it
    return {k: v for k, v in dictionary.items() if k != key}


def isinstance(obj, _type):  # isinstance does not exist in drac2, fake it till you make it
    if _type == dict:
        try:
            return deepcopy(obj) == obj  # If it survives serialization, it's a dict
        except:
            return False  # If JSON conversion fails, it's not a dictionary
    return False  # We only support dict checks for now


def sanitize_string_or_error(value, max_length=15):
    if not value:
        return None, {"DESCRIPTION": "⚠️ Error: Input is required.", "COLOR": color_map["red"]}

    # Convert to lowercase and replace spaces with underscores
    sanitized = value.lower().replace(" ", "_")

    # Allow only letters, numbers, underscores, and dashes
    if not all(char.isalnum() or char in ["_", "-"] for char in sanitized):
        return None, {"DESCRIPTION": "⚠️ Error: Input can only contain letters, numbers, underscores (_), and dashes (-).", "COLOR": color_map["red"]}

    # Enforce length limit
    if len(sanitized) > max_length:
        return None, {"DESCRIPTION": f"⚠️ Error: Input must be **{max_length} characters or fewer**.", "COLOR": color_map["red"]}

    return sanitized, None  # ✅ Return sanitized value and no error


def to_proper(value):
    return " ".join(word.capitalize() for word in value.split("_"))


def get_modifiers(attr, pet):
    """
    Returns a list of dictionaries for modifiers affecting a given attribute.
    Each modifier includes a source and value.
    """
    mods = []
    for item_key, item in pet.get("items", {}).items():
        if not item.get("active") and not item.get("worn") and not item.get("attuned"):
            continue  # Skip inactive items

        effect = item.get("effect", {})
        stats = effect.get("stats", {})

        if attr in stats and stats[attr] is not None:
            mods.append({
                "source": f"item.{item_key}",
                "value": stats[attr]
            })

    return mods


def roll_modifier(attr, pet):
    """
    Calculates the total modifier for a given attribute.
    Returns (total, [modifiers])
    """
    mods = get_modifiers(attr, pet)
    total = sum(m["value"] for m in mods)

    return total, mods


def explain_modifiers(mods):
    return ", ".join(f"{m['value']:+d} from {to_proper(m['source'])}" for m in mods)


def effective_stat(attr, base_value, pet):
    """
    Calculates the effective stat value from base and items,
    and returns the modifier and a readable breakdown.
    """
    mods = get_modifiers(attr, pet)

    # Check for overrides (e.g., item sets STR to 19)
    overrides = [m["value"] for m in mods if isinstance(m["value"], int) and m["value"] >= 15 and base_value < m["value"]]
    effective_value = max(overrides) if overrides else base_value

    mod = (effective_value - 10) // 2
    breakdown = f"{to_proper(attr)} ({effective_value}) → {mod:+d} modifier"

    return mod, breakdown


def get_stat_info(attr, pet, check_key=None):
    base = pet.get("stats", {}).get(attr, 10)
    mods = get_modifiers(attr, pet)

    # Check for stat override (like item sets DEX to 19)
    overrides = [m["value"] for m in mods if isinstance(m["value"], int) and m["value"] >= 15 and base < m["value"]]
    effective = max(overrides) if overrides else base

    base_mod = (effective - 10) // 2
    item_bonus, item_mods = roll_modifier(attr, pet)

    prof_bonus = 2
    is_proficient = False
    is_expert = False
    prof_applied = 0
    override_value = None
    breakdown_lines = []

    if check_key:
        # Check for manual override in skills
        override_value = pet.get("skills", {}).get(check_key)

        if override_value is None:
            # Check for proficiency/expertise if no override
            if check_key in pet.get("expertise", []):
                is_expert = True
                prof_applied = prof_bonus * 2
            elif check_key in pet.get("proficiency", []):
                is_proficient = True
                prof_applied = prof_bonus

    total_modifier = override_value if override_value is not None else base_mod + prof_applied
    breakdown = f"{to_proper(attr)} ({effective}) → {total_modifier:+d} modifier"

    if override_value is not None:
        breakdown_lines.append(f"- {override_value:+d} manual override")
    else:
        breakdown_lines.append(f"- {base_mod:+d} base")
        if prof_applied:
            prof_source = "Expertise" if is_expert else "Proficiency"
            breakdown_lines.append(f"- {prof_applied:+d} from {prof_source}")
        if item_bonus:
            breakdown_lines.append(f"- {item_bonus:+d} from Items")

    display = breakdown + ("\n" + "\n".join(breakdown_lines) if breakdown_lines else "")

    return {
        "attr": attr,
        "base": base,
        "effective": effective,
        "modifier": total_modifier,
        "mods": item_mods,
        "prof_bonus": prof_bonus,
        "is_proficient": is_proficient,
        "is_expert": is_expert,
        "override": override_value,
        "display": display
    }



def get_character_or_error():
    ch = character()
    return ch, None if ch else (None, {"DESCRIPTION": "⚠️ Error: Unable to locate character. Please ensure you have an active character.", "COLOR": color_map["red"]})  # Red for failure


def get_pets_or_error():
    ch, error = get_character_or_error()
    if error:
        return None, error
    custom_pets = ch.get_cvar("custom_pets", "{}")  # Default to '{}'
    try:
        pets = load_json(custom_pets)  # Ensure it's properly parsed
    except:
        return None, {"DESCRIPTION": "⚠️ Error: Failed to decode pets data. Reset it using `!pet purge`.", "COLOR": color_map["red"]}

    return pets, None  # ✅ Always return pets without treating an empty dict as an error


def get_pet_or_error(pet_name):
    pets, error = get_pets_or_error()
    if error:
        return None, error
    pet = pets.get(pet_name)
    return pet, None if pet is not None else {"DESCRIPTION": f"⚠️ Error: Pet '{pet_name}' not found. Use 'list' to see available pets.", "COLOR": color_map["red"]}


def pet_exists(pet_key):
    pets, error = get_pets_or_error()
    if error:
        return False
    return pet_key in pets


def save_pets(pets):
    ch, error = get_character_or_error()
    if error:
        return error
    ch.set_cvar("custom_pets", dump_json(pets))
    return {"DESCRIPTION": "🧸 Pets saved successfully.", "COLOR": color_map["green"]}  # Green for success


def save_pet(pet_key, pet_data):
    pets, error = get_pets_or_error()
    if error and pets is None:
        pets = {}  # Only initialize if `pets` is actually None
    elif error:
        return error

    if not isinstance(pets, dict):
        return {"DESCRIPTION": "⚠️ Error: Pet data corrupted. Try using `!pet purge`.", "COLOR": color_map["red"]}

    pets[pet_key] = pet_data
    return save_pets(pets)


def create_pet(pet_key, pet_name=None):
    if not pet_name:
        pet_name = pet_key
    if pet_exists(pet_key):
        return {"DESCRIPTION": f"⚠️ Error: Pet '{pet_key}' already exists.", "COLOR": color_map["red"]}  # Red for failure

    pet = deepcopy(pet_schema)  # Create a new pet from the schema
    pet["name"] = pet_name

    result = save_pet(pet_key, pet)
    if result.get("DESCRIPTION") == "Pets saved successfully.":
        return {"TITLE": "Success!", "DESCRIPTION": f"🧸 Pet '{pet_key}' adopted successfully with name '{pet_name}'!", "COLOR": color_map["green"]}  # Green for success
    else:
        return result


# -----------------------------------------------------------------------#
#      handle functions, these functions handle commands on trigger      #
# -----------------------------------------------------------------------#


#!------------------------- start tbd --------------------------#
def tbd(arg_data):
    return {"DESCRIPTION": "⚠️ Error: Unknown command or command not implemented yet.", "COLOR": color_map["red"]}  # Red for failure
#!------------------------- start tbd --------------------------#


#!------------------------- start handle_action --------------------------#
def handle_action(arg_data):
    action_type = arg_data.get("1")

    # Get current pet
    ch, error = get_character_or_error()
    if error:
        return error

    current_pet_key = ch.get_cvar("current_pet")
    if not current_pet_key:
        return {"DESCRIPTION": "⚠️ Error: No pet selected. Use `!pm select <key>` first.", "COLOR": color_map["red"]}

    pet, error = get_pet_or_error(current_pet_key)
    if error:
        return error

    # Show help/info page if no action_type provided
    if not action_type:
        actions = pet.get("actions", {})
        actions_display = (
            "\n".join(
                f"- **{to_proper(a)}**: {details.get('description', 'No description.')}"
                for a, details in actions.items()
            ) if actions else "No actions available."
        )

        usage = (
            f"**Usage:**\n"
            f"- `{COMMAND} action add <name>`\n"
            f"- `{COMMAND} action edit <name> <field> <value>`\n"
            f"- `{COMMAND} action delete <name>`"
        )

        return {
            "TITLE": f"⚔️ Actions for {pet['name']}",
            "DESCRIPTION": f"{actions_display}\n\n{usage}",
            "COLOR": color_map["blue"]
        }

    # Existing Logic continues unchanged below here
    if action_type not in {"add", "delete", "edit"}:
        return {"DESCRIPTION": "⚠️ Error: Invalid action type. Use `add`, `delete`, or `edit`.", "COLOR": color_map["red"]}

    action_name = arg_data.get("2")
    if not action_name:
        return {"DESCRIPTION": "⚠️ Error: Action name is required. Example: `!pm action add Bite`", "COLOR": color_map["red"]}

    action_name, error = sanitize_string_or_error(action_name)
    if error:
        return error

    if "actions" not in pet:
        pet["actions"] = {}

    if action_type == "add":
        if action_name in pet["actions"]:
            return {"DESCRIPTION": f"⚠️ Error: Action `{action_name}` already exists.", "COLOR": color_map["orange"]}

        pet["actions"][action_name] = deepcopy(action_schema)
        pet["actions"][action_name]["name"] = action_name

        result = save_pet(current_pet_key, pet)
        if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
            return {"TITLE": "Success!", "DESCRIPTION": f"🛠️ Action `{action_name}` added.", "COLOR": color_map["green"]}
        else:
            return result

    elif action_type == "delete":
        if action_name not in pet["actions"]:
            return {"DESCRIPTION": f"⚠️ Error: Action `{action_name}` not found.", "COLOR": color_map["orange"]}

        pet["actions"] = delete(pet["actions"], action_name)

        result = save_pet(current_pet_key, pet)
        if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
            return {"TITLE": "Success!", "DESCRIPTION": f"🗑️ Action `{action_name}` deleted.", "COLOR": color_map["green"]}
        else:
            return result

    elif action_type == "edit":
        if action_name not in pet["actions"]:
            return {"DESCRIPTION": f"⚠️ Error: Action `{action_name}` not found.", "COLOR": color_map["orange"]}

        action_attr = arg_data.get("3")
        value = " ".join(arg_data.get(str(i), "") for i in range(4, len(arg_data))).strip()

        if not action_attr or not value:
            return {"DESCRIPTION": "⚠️ Error: You must specify an attribute and value. Example: `!pm action edit Bite damage_roll 2d8+3`", "COLOR": color_map["red"]}

        if action_attr not in action_schema:
            return {"DESCRIPTION": f"⚠️ Error: `{action_attr}` is not a valid action attribute.", "COLOR": color_map["red"]}

        if action_attr in {"hit_modifier", "damage_modifier"}:
            if not (value.lstrip("+-").isdigit() and (value.startswith("+") or value.startswith("-"))):
                return {"DESCRIPTION": f"⚠️ Error: `{action_attr}` must be a number with a `+` or `-` sign (e.g., `+2`, `-1`, `+0`).", "COLOR": color_map["red"]}
            value = f"{int(value):+d}"

        pet["actions"][action_name][action_attr] = value

        result = save_pet(current_pet_key, pet)
        if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
            return {"TITLE": "Success!", "DESCRIPTION": f"✍️ `{action_name}.{action_attr}` updated to `{value}`.", "COLOR": color_map["green"]}
        else:
            return result
#!------------------------- start handle_action --------------------------#


#!------------------------- start handle_attack --------------------------#
def handle_attack(arg_data):
    attack_name = arg_data.get("1")

    ch, error = get_character_or_error()
    if error:
        return error

    current_pet_key = ch.get_cvar("current_pet")
    if not current_pet_key:
        return {"DESCRIPTION": "⚠️ Error: No pet selected. Use `!pm select <key>` first.", "COLOR": color_map["red"]}

    pet, error = get_pet_or_error(current_pet_key)
    if error:
        return error

    # Info/help display if no attack_name given
    if not attack_name:
        actions = pet.get("actions", {})
        attacks_display = (
            "\n".join(
                f"- **{to_proper(a)}** (Damage: {details.get('damage_roll', 'None')}, Type: {details.get('damage_type', 'Unknown')})"
                for a, details in actions.items()
            ) if actions else "No attacks available."

        )

        usage = (
            f"**Usage:**\n"
            f"- `{COMMAND} attack <name>` (Normal roll)\n"
            f"- `{COMMAND} attack <name> adv` (Advantage)\n"
            f"- `{COMMAND} attack <name> dis` (Disadvantage)\n"
            f"- `{COMMAND} attack <name> <custom roll>` (Custom roll, e.g. `1d20+5`)\n\n"
            f"**Available Attacks:**\n{attacks_display}"
        )

        return {
            "TITLE": f"⚔️ Attacks for {pet['name']}",
            "DESCRIPTION": usage,
            "COLOR": color_map["blue"]
        }

    # Existing logic continues here, no changes to current functionality
    attack_name, sanitize_error = sanitize_string_or_error(attack_name)
    if sanitize_error:
        return sanitize_error

    if attack_name not in pet["actions"]:
        return {"DESCRIPTION": f"⚠️ Error: Attack `{attack_name}` not found. Use `!pm action add {attack_name}` to create it.", "COLOR": color_map["red"]}

    attack = pet["actions"][attack_name]

    roll_type = arg_data.get("2", "").lower()
    hit_modifier = attack.get("hit_modifier", "+0")

    # Handle normal, advantage, disadvantage, and custom rolls correctly
    if roll_type == "adv":
        attack_roll = f"2d20kh1{hit_modifier}"
    elif roll_type == "dis":
        attack_roll = f"2d20kl1{hit_modifier}"
    elif roll_type:  # Custom rolls
        attack_roll = roll_type
    else:  # Default roll
        attack_roll = f"1d20{hit_modifier}"

    attack_result = vroll(attack_roll)

    damage_roll = attack.get("damage_roll", "0")
    damage_modifier = attack.get("damage_modifier", "+0")
    total_damage_roll = f"{damage_roll}{damage_modifier}" if damage_roll != "0" else "0"
    damage_result = vroll(total_damage_roll)

    attack_output = (
        f"🎯 {to_proper(attack_name)} Attack\n"
        f"🎲 **Attack Roll:** {attack_result}\n"
        f"💥 **Damage:** {damage_result} {attack.get('damage_type', '')}\n"
        f"🎯 **Range:** {attack.get('range', 'Melee')}\n"
        f"🎯 **Target:** {attack.get('target', 'Single Target')}\n"
        f"📜 **Description:** {attack.get('description', 'No description.')}"
    )

    return {"TITLE": f"🗡️ {pet['name']} Attacks!", "DESCRIPTION": attack_output, "COLOR": color_map["orange"]}
#!------------------------- start handle_attack --------------------------#


#!------------------------- start handle_adopt --------------------------#
def handle_adopt(arg_data):
    pet_key = arg_data.get("1")

    # Ensure pet_key exists
    if not pet_key:
        return {"DESCRIPTION": "⚠️ Error: Pet key is required. Format: `!pm adopt <key> [name]`", "COLOR": color_map["red"]}

    # Validate and format the pet key
    pet_key, error = sanitize_string_or_error(pet_key)
    if error:
        return error  # Return error if validation fails

    # Concatenate all remaining arguments for pet_name (if any), otherwise use pet_key
    pet_name = " ".join(arg_data.get(str(i), "") for i in range(2, len(arg_data))) or pet_key

    return create_pet(pet_key, pet_name)
#!------------------------- end handle_adopt --------------------------#


#!------------------------- start handle_check --------------------------#
def handle_check(arg_data):
    check_key = arg_data.get("1")
    roll_type = arg_data.get("2", "").lower()

    ch, error = get_character_or_error()
    if error:
        return error

    current_pet_key = ch.get_cvar("current_pet")
    if not current_pet_key:
        return {"DESCRIPTION": "⚠️ Error: No pet selected. Use `!pm select <key>` first.", "COLOR": color_map["red"]}

    pet, error = get_pet_or_error(current_pet_key)
    if error:
        return error

    # If no check_key provided, display available checks and usage
    if not check_key:
        available_checks = ", ".join(check_map.keys())
        usage = (
            f"**Usage:**\n"
            f"- `{COMMAND} check <check>` (Normal roll)\n"
            f"- `{COMMAND} check <check> adv` (Advantage)\n"
            f"- `{COMMAND} check <check> dis` (Disadvantage)\n"
            f"- `{COMMAND} check <check> <custom roll>` (Custom roll)\n\n"
            f"**Available Checks:**\n{available_checks}"
        )

        return {
            "TITLE": f"🧪 Checks for {pet['name']}",
            "DESCRIPTION": usage,
            "COLOR": color_map["blue"]
        }

    if check_key not in check_map:
        return {"DESCRIPTION": f"⚠️ Error: `{check_key}` is not a recognized check.", "COLOR": color_map["red"]}

    attr = check_map[check_key]
    stat_info = get_stat_info(attr, pet, check_key=check_key)
    mod = stat_info["modifier"]

    if roll_type == "adv":
        roll_expr = f"2d20kh1{mod:+d}"
    elif roll_type == "dis":
        roll_expr = f"2d20kl1{mod:+d}"
    elif roll_type:  # Custom roll
        roll_expr = roll_type
    else:
        roll_expr = f"1d20{mod:+d}"

    roll_result = vroll(roll_expr)

    title = f"🧪 Check: {to_proper(check_key)}"
    desc = f"Rolling {to_proper(check_key)} check: `{roll_expr}`\n{roll_result}\n\n**Effective Stat:** {stat_info['display']}"

    result = {
        "TITLE": title,
        "DESCRIPTION": desc,
        "COLOR": color_map["green"]
    }

    if pet.get("thumbnail"):
        result["THUMBNAIL"] = pet["thumbnail"]

    return result

#!------------------------- end handle_check --------------------------#


#!------------------------- end handle_help --------------------------#
def handle_help(arg_data):
    help_text = (
        f"📌 **Basic Commands:**\n"
        f"- `!pm adopt <key> [name]` → Adopt a new pet.\n"
        f"- `!pm release <key> YES` → Release a pet (**permanent**).\n"
        f"- `!pm list` → List all adopted pets.\n"
        f"- `!pm select <key>` → Set a pet as active.\n\n"

        f"🛠️ **Modifying Your Pet:**\n"
        f"- `!pm set <field> <value>` → Modify basic stats.\n"
        f"  - Example: `!pm set hp.max 100`\n"
        f"  - Example: `!pm set ac 17`\n\n"

        f"⚔️ **Managing Conditions & Resistances:**\n"
        f"- `!pm condition <+|-><name>` → Add/Remove/Toggle conditions.\n"
        f"- `!pm resist <+|-><type>` → Add/Remove/Toggle resistances.\n"
        f"- `!pm immune <+|-><type>` → Add/Remove/Toggle immunities.\n"
        f"  - Example: `!pm condition +Prone`\n"
        f"  - Example: `!pm resist -Fire`\n"
        f"  - Example: `!pm immune Cold`\n\n"

        f"📦 **Advanced Features (Coming Soon!):**\n"
        f"- Inventory, Skills, Actions, and more!"
    )

    return {"TITLE": f"🛠️ **Pet Manager Help** 🛠️\n\n", "DESCRIPTION": help_text, "COLOR": color_map["blue"]}
#!------------------------- end handle_help --------------------------#


#!------------------------- start handle_list --------------------------#
def handle_list(arg_data):
    pets, error = get_pets_or_error()
    if error:
        return error

    if not pets:
        return {"DESCRIPTION": "⚠️ Error: You have no pets. Use `!pm adopt <key> [name]` to adopt one.", "COLOR": color_map["red"]}

    ch, ch_error = get_character_or_error()
    if ch_error:
        return ch_error

    current_pet = ch.get_cvar("current_pet")

    pet_list = "\n".join(
        f"{'***' if key == current_pet else ''}{key} - {pet['name']}{'***' if key == current_pet else ''}\n"
        f"(CR:{pet.get('cr', '—')}) - {pet.get('species', 'Unknown Species')} - {pet.get('size', 'Unknown')}, {pet.get('type', 'Unknown')}\n"
        f"HP: {pet['hp'].get('current', '?')}/{pet['hp'].get('max', '?')} ({pet['hp'].get('temp', 0)}) | AC: {pet.get('ac', '?')}"
        + (f" ({pet.get('ac_source')})" if pet.get('ac_source') else "") + "\n"
        f"Conditions: {', '.join(to_proper(c) for c in pet.get('condition', [])) if pet.get('condition') else 'None'}\n"
        for key, pet in pets.items()
    )

    return {"TITLE": "🧸 Your Pets", "DESCRIPTION": pet_list, "COLOR": color_map["rebeccapurple"]}
#!------------------------- end handle_list --------------------------#


#!------------------------- start handle_purge --------------------------#
def handle_purge(arg_data):
    # Check for confirmation argument
    confirmation = arg_data.get("1")
    if confirmation != "YES":
        return {"DESCRIPTION": f"⚠️ Error: You must type `{COMMAND} purge YES` in **all caps** to confirm.", "COLOR": color_map["red"]}  # Red for failure

    # Get character reference
    ch, error = get_character_or_error()
    if error:
        return error  # Return error if no active character

    # Delete pet-related data
    ch.delete_cvar("current_pet")
    ch.delete_cvar("custom_pets")

    return {"TITLE": "‼️ Pet Data Purged!", "DESCRIPTION": "All pet data has been **permanently deleted**.", "COLOR": color_map["green"]}  # Green to indicate a drastic action
#!------------------------- end handle_purge --------------------------#


#!------------------------- start handle_release --------------------------#
def handle_release(arg_data):
    pet_key = arg_data.get("1")

    # Check for confirmation argument
    confirmation = arg_data.get("2")
    if confirmation != "YES":
        return {"DESCRIPTION": f"⚠️ Error: You must type `{COMMAND} release <key> YES` in **all caps** to confirm.", "COLOR": color_map["red"]}  # Red for failure

    # Validate and format the pet key
    pet_key, error = sanitize_string_or_error(pet_key)
    if error:
        return error  # Return error if validation fails

    # Ensure pet_key exists
    if not pet_key:
        return {"DESCRIPTION": "⚠️ Error: Pet key is required. Format: `!pm release <key>`", "COLOR": color_map["red"]}

    # Get the pets
    pets, error = get_pets_or_error()
    if error:
        return error  # Return error if pets not found

    # Get character to check current pet
    ch, ch_error = get_character_or_error()
    if ch_error:
        return ch_error

    current_pet = ch.get_cvar("current_pet")

    # If deleting the current pet, remove it from cvars
    if current_pet == pet_key:
        ch.delete_cvar("current_pet")

    # Delete the pet
    pets = delete(pets, pet_key)

    # Save the pets
    result = save_pets(pets)
    if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
        return {"TITLE": "Success!", "DESCRIPTION": f"🧸 Pet '{pet_key}' released successfully!", "COLOR": color_map["green"]}  # Green for success
    else:
        return result
#!------------------------- end handle_release --------------------------#


#!------------------------- start handle_select --------------------------#
def handle_select(arg_data):
    pet_key = arg_data.get("1")

    # Validate and format the pet key
    pet_key, error = sanitize_string_or_error(pet_key)
    if error:
        return error  # Return error if validation fails

    # Ensure pet_key exists
    if not pet_key:
        return {"DESCRIPTION": "⚠️ Error: Pet key is required. Format: `!pm select <key>`", "COLOR": color_map["red"]}

    # Get the pet
    pet, error = get_pet_or_error(pet_key)
    if error:
        return error  # Return error if pet not found

    # Get character reference
    ch, error = get_character_or_error()
    if error:
        return error  # Return error if no active character

    ch.set_cvar("current_pet", pet_key)

    return {"TITLE": "Success!", "DESCRIPTION": f"🧸 '{pet['name']}' is now the active pet!", "COLOR": color_map["green"]}  # Green for success
#!------------------------- end handle_select --------------------------#


#!------------------------- end handle_set --------------------------#
def handle_set(arg_data):
    key_path = arg_data.get("1")
    value = " ".join(arg_data.get(str(i), "") for i in range(2, len(arg_data))).strip()

    # Ensure a key and value are provided
    if not key_path or not value:
        return {"DESCRIPTION": "⚠️ Error: You must provide a valid key and value. Example: `!pm set hp.max 100`", "COLOR": color_map["red"]}

    # Get current pet
    ch, error = get_character_or_error()
    if error:
        return error  # Return error if no active character

    current_pet_key = ch.get_cvar("current_pet")
    if not current_pet_key:
        return {"DESCRIPTION": "⚠️ Error: No pet selected. Use `!pm select <key>` first.", "COLOR": color_map["red"]}

    pet, error = get_pet_or_error(current_pet_key)
    if error:
        return error  # Return error if pet data is missing or corrupted

    # Split key path and determine category
    keys = key_path.split(".")
    root_key = keys[0]

    # Skip processing for ignored keys (handled by a different command)
    ignored_keys = {"speed", "senses", "traits", "condition", "resist", "immune", "skills", "actions", "items"}
    if root_key in ignored_keys:
        return {"DESCRIPTION": f"⚠️ Error: `{root_key}` cannot be modified with this command., use `!pm {root_key}` instead.", "COLOR": color_map["red"]}

    # Validate against pet_schema
    # Prevent setting `hp` directly
    if root_key == "hp" and len(keys) == 1:
        return {"DESCRIPTION": "⚠️ Error: HP must be modified using `hp.max`, `hp.current`, or `hp.temp`.", "COLOR": color_map["red"]}

    # Validate against pet_schema
    current_schema = pet_schema
    for key in keys:
        if key not in current_schema:
            return {"DESCRIPTION": f"⚠️ Error: '{key}' is not a valid field in `pet_schema`.", "COLOR": color_map["red"]}
        current_schema = current_schema[key] if isinstance(current_schema, dict) else None


    # Traverse pet data, creating missing structures if valid
    data = pet
    for k in keys[:-1]:  # Traverse until the second-to-last key
        if k not in data:
            data[k] = {}  # Create structure if missing
        data = data[k]

    last_key = keys[-1]

    # Convert numeric values when possible
    if isinstance(current_schema, (int, float)) or current_schema is None:
        if value.isdigit():
            value = int(value)
        elif value.replace(".", "", 1).isdigit():
            value = float(value)

    # Assign the value
    data[last_key] = value

    # Save the updated pet
    result = save_pet(current_pet_key, pet)
    if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
        return {"TITLE": "Success!", "DESCRIPTION": f"🧸 `{key_path}` updated to `{value}` for `{pet['name']}`.", "COLOR": color_map["green"]}
    else:
        return result
#!------------------------- end handle_set --------------------------#


#!------------------------- end handle_show --------------------------#
def handle_show(arg_data):
    # Get current pet
    ch, error = get_character_or_error()
    if error:
        return error  # Return error if no active character

    current_pet_key = ch.get_cvar("current_pet")
    if not current_pet_key:
        return {"DESCRIPTION": "⚠️ Error: No pet selected. Use `!pm select <key>` first.", "COLOR": color_map["red"]}

    pet, error = get_pet_or_error(current_pet_key)
    if error:
        return error  # Return error if pet data is missing or corrupted

    # Auto-calculate stat modifiers
    def calc_mod(score):
        """ Returns the correct ability modifier based on score. Defaults to 10 if None. """
        try:
            score = int(score) if score is not None else 10  # Default to 10 if missing
        except ValueError:
            score = 10  # Fallback if parsing fails
        return (score - 10) // 2


    # Basic Info
    size = pet.get("size", "Unknown")
    type_ = pet.get("type", "Unknown")
    alignment = pet.get("alignment", "Unaligned")
    species = pet.get("species", "Unknown")

    # Defensive Stats
    ac = pet.get("ac", "?")
    initiative = pet.get("initiative", "0")
    ac_source = f" ({pet.get('ac_source')})" if pet.get("ac_source") else ""
    hp_max = pet["hp"].get("max", "?")
    hp_current = pet["hp"].get("current", "?")
    hp_temp = pet["hp"].get("temp", "0")
    hp_display = f"{hp_current}/{hp_max} ({hp_temp})"

    # Speed & Senses
    speed = ", ".join(pet["speed"]) if pet["speed"] else "None"
    senses = ", ".join(pet["senses"]) if pet["senses"] else "None"

    # Stats
    stats = pet.get("stats", {})
    stats_display = f"```STR {stats.get('str', 10):>2} ({calc_mod(stats.get('str', 10)):+d}), " \
                    f"DEX {stats.get('dex', 10):>2} ({calc_mod(stats.get('dex', 10)):+d}), " \
                    f"CON {stats.get('con', 10):>2} ({calc_mod(stats.get('con', 10)):+d})\n" \
                    f"INT {stats.get('int', 10):>2} ({calc_mod(stats.get('int', 10)):+d}), " \
                    f"WIS {stats.get('wis', 10):>2} ({calc_mod(stats.get('wis', 10)):+d}), " \
                    f"CHA {stats.get('cha', 10):>2} ({calc_mod(stats.get('cha', 10)):+d})```"

    # Saving Throws
    saves_display = ", ".join(
        f"{stat.upper()} {calc_mod(stats.get(stat, 10)):+d}"
        for stat in ["str", "dex", "con", "int", "wis", "cha"]
    )

    # Ability Checks (same as raw stat modifiers)
    ability_checks_display = saves_display

    # Skills
    skills_display = ", ".join(
        f"{to_proper(skill)} {bonus:+d}" for skill, bonus in pet["skills"].items()
    ) if pet["skills"] else "None"

    # Conditions, Resistances, Immunities
    conditions_display = ", ".join(to_proper(cond) for cond in pet["condition"]) if pet["condition"] else "None"
    resistances_display = ", ".join(to_proper(res) for res in pet["resist"]) if pet["resist"] else "None"
    immunities_display = ", ".join(to_proper(imm) for imm in pet["immune"]) if pet["immune"] else "None"

    # Traits
    traits_display = "\n".join(
        f"**{to_proper(trait)}:** {desc}" for trait, desc in pet["traits"].items()
    ) if pet["traits"] else "(FUTURE USE)"

    # Actions
    actions_display = "\n".join(
        f" * **{to_proper(name)}**\n"
        f"   * *Melee Weapon Attack:* {action.get('hit_roll', '1d20')}{action.get('hit_modifier', '+0')} "
        f"   * to hit, {action.get('range', 'Melee')}, one target.\n"
        f"   * *Hit:* {action.get('damage_roll', '0')}{action.get('damage_modifier', '+0')} {action.get('damage_type', 'Undefined')}. "
        for name, action in pet["actions"].items()
    ) if pet["actions"] else "None"

    DESCRIPTION = ""

    # Construct Description
    DESCRIPTION += f"**Type:** {species}\n"
    DESCRIPTION += f"{size} {type_}, {alignment}\n"
    DESCRIPTION += f"**Armor Class:** {ac}{ac_source}  \n"
    DESCRIPTION += f"**Initiative:** {initiative}  \n"
    DESCRIPTION += f"**Current HP:** {hp_display}  \n"
    # DESCRIPTION += f"**Speed:** {speed}\n"
    DESCRIPTION += f"**Stats:**\n{stats_display}\n"
    DESCRIPTION += f"**Saving Throws:** {saves_display}\n"
    DESCRIPTION += f"**Ability Checks:** {ability_checks_display}\n"
    # DESCRIPTION += f"**Skills:** {skills_display}\n"
    # DESCRIPTION += f"**Senses:** {senses}\n"
    DESCRIPTION += f"**Conditions:** {conditions_display}\n"
    DESCRIPTION += f"**Resistances:** {resistances_display}\n"
    DESCRIPTION += f"**Immunities:** {immunities_display}\n"
    # DESCRIPTION += f"**Traits:**\n{traits_display}\n"
    DESCRIPTION += f"**Actions:**\n{actions_display}\n"

    # Embed Data
    embed_data = {
        "TITLE": f"🧸 {pet['name']}",
        "DESCRIPTION": DESCRIPTION,
        "COLOR": color_map["rebeccapurple"]
    }

    # If a thumbnail exists, include it
    if pet.get("thumbnail"):
        embed_data["THUMBNAIL"] = pet["thumbnail"]

    return embed_data
#!------------------------- end handle_show --------------------------#


#!------------------------- start handle_skills --------------------------#
def handle_skills(arg_data):
    # Combine check and save maps for validation
    valid_skills = set(check_map.keys()) | set(save_map.keys())

    # Get subcommand: add, edit, delete
    subcommand = arg_data.get("1", "").lower()

    if subcommand not in {"add", "edit", "delete"}:
        # If no subcommand or invalid, show current skills and usage
        ch, error = get_character_or_error()
        if error:
            return error

        current_pet_key = ch.get_cvar("current_pet")
        if not current_pet_key:
            return {"DESCRIPTION": "⚠️ Error: No pet selected. Use `!pm select <key>` first.", "COLOR": color_map["red"]}

        pet, error = get_pet_or_error(current_pet_key)
        if error:
            return error

        skills = pet.get("skills", {})
        if not skills:
            skills_display = "None"
        else:
            skills_display = ", ".join(f"**{to_proper(skill)}** {bonus:+d}" for skill, bonus in skills.items())

        usage = (
            "**Usage:**\n"
            "`!pm skills add <skill> <bonus>`\n"
            "`!pm skills edit <skill> <new bonus>`\n"
            "`!pm skills delete <skill>`"
        )

        return {
            "TITLE": "📘 Current Skills",
            "DESCRIPTION": f"{skills_display}\n\n{usage}",
            "COLOR": color_map["blue"]
        }

    # Sanitize skill name
    skill_name = arg_data.get("2")
    if not skill_name:
        return {"DESCRIPTION": f"⚠️ Error: You must specify a skill name.", "COLOR": color_map["red"]}

    sanitized_name, error = sanitize_string_or_error(skill_name)
    if error:
        return error

    if sanitized_name not in valid_skills:
        return {"DESCRIPTION": f"⚠️ Error: `{sanitized_name}` is not a valid skill or ability.\n"
                f"Valid options: `{', '.join(sorted(valid_skills))}`",
                "COLOR": color_map["red"]}

    # Get current pet
    ch, error = get_character_or_error()
    if error:
        return error

    current_pet_key = ch.get_cvar("current_pet")
    if not current_pet_key:
        return {"DESCRIPTION": "⚠️ Error: No pet selected. Use `!pm select <key>` first.", "COLOR": color_map["red"]}

    pet, error = get_pet_or_error(current_pet_key)
    if error:
        return error

    if "skills" not in pet:
        pet["skills"] = {}

    # ADD
    if subcommand == "add":
        if sanitized_name in pet["skills"]:
            return {"DESCRIPTION": f"⚠️ Error: `{sanitized_name}` already exists. Use `edit` to change it.", "COLOR": color_map["orange"]}

        try:
            bonus = int(arg_data.get("3"))
        except:
            return {"DESCRIPTION": "⚠️ Error: You must provide a numeric bonus value.", "COLOR": color_map["red"]}

        pet["skills"][sanitized_name] = bonus
        result = save_pet(current_pet_key, pet)
        return {"TITLE": "Success!", "DESCRIPTION": f"✨ Skill `{to_proper(sanitized_name)}` added with bonus `{bonus:+d}`.", "COLOR": color_map["green"]}

    # EDIT
    elif subcommand == "edit":
        if sanitized_name not in pet["skills"]:
            return {"DESCRIPTION": f"⚠️ Error: `{sanitized_name}` does not exist. Use `add` first.", "COLOR": color_map["orange"]}

        try:
            bonus = int(arg_data.get("3"))
        except:
            return {"DESCRIPTION": "⚠️ Error: You must provide a numeric bonus value.", "COLOR": color_map["red"]}

        pet["skills"][sanitized_name] = bonus
        result = save_pet(current_pet_key, pet)
        return {"TITLE": "Success!", "DESCRIPTION": f"✍️ Skill `{to_proper(sanitized_name)}` updated to `{bonus:+d}`.", "COLOR": color_map["green"]}

    # DELETE
    elif subcommand == "delete":
        if sanitized_name not in pet["skills"]:
            return {"DESCRIPTION": f"⚠️ Error: `{sanitized_name}` not found.", "COLOR": color_map["orange"]}

        pet["skills"] = delete(pet["skills"], sanitized_name)
        result = save_pet(current_pet_key, pet)
        return {"TITLE": "Success!", "DESCRIPTION": f"🗑️ Skill `{to_proper(sanitized_name)}` removed.", "COLOR": color_map["green"]}
#!------------------------- end handle_skill --------------------------#


#!------------------------- start handle_toggle_list --------------------------#
def handle_toggle_list(arg_data):
    list_map = {
        "condition": "condition",
        "resist": "resist",
        "immune": "immune",
        "prof": "proficiency",
        "proficiency": "proficiency",
        "exp": "expertise",
        "expertise": "expertise"
    }

    # Ensure a valid command type
    list_type = arg_data.get("command")
    if list_type not in list_map:
        return {"DESCRIPTION": "⚠️ Error: Invalid command. Use `condition`, `resist`, `immune`, `prof`, or `expertise`.", "COLOR": color_map["red"]}

    # Get current pet
    ch, error = get_character_or_error()
    if error:
        return error

    current_pet_key = ch.get_cvar("current_pet")
    if not current_pet_key:
        return {"DESCRIPTION": "⚠️ Error: No pet selected. Use `!pm select <key>` first.", "COLOR": color_map["red"]}

    pet, error = get_pet_or_error(current_pet_key)
    if error:
        return error

    # If no argument provided, display current list and usage
    raw_name = arg_data.get("1")
    if not raw_name:
        key = list_map[list_type]
        current_list = pet.get(key, [])

        current_display = ", ".join(to_proper(name) for name in current_list) if current_list else "None active."

        usage = (
            f"**Usage:**\n"
            f"• `{COMMAND} {list_type} +<name>` (Add)\n"
            f"• `{COMMAND} {list_type} -<name>` (Remove)\n"
            f"• `{COMMAND} {list_type} <name>` (Toggle)\n\n"
            f"**Currently active:** {current_display if current_list else 'None active.'}"
        )

        return {
            "TITLE": f"📋 {to_proper(list_type)} for {pet['name']}",
            "DESCRIPTION": usage,
            "COLOR": color_map["blue"]
        }

    # Detect + / - operator
    operation = None
    if raw_name[0] in {"+", "-"}:
        operation = raw_name[0]
        raw_name = raw_name[1:].strip()

    # Sanitize input
    sanitized_name, error = sanitize_string_or_error(raw_name)
    if error:
        return error

    # Validate input if prof/expertise
    if list_type in {"prof", "proficiency", "exp", "expertise"}:
        valid_keys = set(check_map.keys()) | set(save_map.keys())
        if sanitized_name not in valid_keys:
            return {
                "DESCRIPTION": f"⚠️ Error: `{sanitized_name}` is not a valid skill or ability.\n"
                f"Valid options: `{', '.join(sorted(valid_keys))}`",
                "COLOR": color_map["red"]
            }

    # Get the actual list and apply operation
    list_key = list_map[list_type]
    if key not in pet:
        pet[key] = []

    pet_list = pet[key]

    if operation == "+":
        if sanitized_name not in pet_list:
            pet_list.append(sanitized_name)
            action = "added to"
        else:
            return {"DESCRIPTION": f"⚠️ `{sanitized_name}` is already in `{list_type}`.", "COLOR": color_map["orange"]}

    elif operation == "-":
        if sanitized_name in pet_list:
            pet_list.remove(sanitized_name)
            action = "removed from"
        else:
            return {"DESCRIPTION": f"⚠️ `{sanitized_name}` is not in `{list_type}`.", "COLOR": color_map["orange"]}

    else:
        if sanitized_name in pet_list:
            pet_list.remove(sanitized_name)
            action = "removed from"
        else:
            pet_list.append(sanitized_name)
            action = "added to"

    result = save_pet(current_pet_key, pet)
    if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
        return {
            "TITLE": "Success!",
            "DESCRIPTION": f"🧸 `{sanitized_name}` {action} `{list_type}`.",
            "COLOR": color_map["green"]
        }
    else:
        return result
#!------------------------- end handle_toggle_list --------------------------#






# -----------------------------------------------------------------------#
#                  Command map and process flow control                  #
# -----------------------------------------------------------------------#

commands = {
    "action": handle_action,
    "add": tbd,
    "adopt": handle_adopt,
    "attack": handle_attack,
    "check": handle_check,
    "condition": handle_toggle_list,
    "debug": tbd,
    "exp": handle_toggle_list,
    "expertise": handle_toggle_list,
    "export": tbd,
    "help": handle_help,
    "immune": handle_toggle_list,
    "import": tbd,
    "list": handle_list,
    "prof": handle_toggle_list,
    "proficiency": handle_toggle_list,
    "purge": handle_purge,
    "release": handle_release,
    "resist": handle_toggle_list,
    "select": handle_select,
    "set": handle_set,
    "show": handle_show,
    "skills": handle_skills,
    "status": tbd,
}

# Now call the function
arg_data = arg_processor(&ARGS&)

command = arg_data.get("command")

result = commands[command](arg_data) if command in commands else tbd(arg_data)

# OUTPUT = f"{arg_data}"


# Merge result with the pre-existing variables
if isinstance(result, dict):
    TITLE = result.get("TITLE", TITLE)
    DESCRIPTION = result.get("DESCRIPTION", DESCRIPTION)
    OUTPUT = result.get("OUTPUT", OUTPUT)
    COLOR = result.get("COLOR", COLOR)
else:
    # Ensure result is a tuple with at least one valid dictionary
    result_dict = result[1] if isinstance(result, tuple) and len(result) > 1 and isinstance(result[1], dict) else {}

    DESCRIPTION = result_dict.get("DESCRIPTION", DESCRIPTION)
    OUTPUT = result_dict.get("OUTPUT", OUTPUT)
    COLOR = result_dict.get("COLOR", COLOR)

# Check if a pet is selected and has a thumbnail
ch, error = get_character_or_error()
if not error:
    current_pet_key = ch.get_cvar("current_pet")
    if current_pet_key:
        pet, pet_error = get_pet_or_error(current_pet_key)
        if not pet_error and pet.get("thumbnail"):
            THUMBNAIL = pet["thumbnail"]

</drac2>
-title "{{TITLE}}"
-desc "{{DESCRIPTION}}"
-f "{{OUTPUT}}"
-color "{{COLOR}}"
-thumb "{{THUMBNAIL}}"

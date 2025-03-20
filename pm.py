embed
<drac2>
COMMAND = "!pm"
TITLE = "Pet Handler"
DESCRIPTION = "A **pet manager** made by **PromptFerret**. I accept gifts of gp, karma, dtp, magic items and sessions 🙃🌟🐕"
OUTPUT = "" #f"No action taken. Use `{COMMAND} help` for command details."
COLOR = "white"

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
    "initiative": None,
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
    "worn": False,
    "attuned": False,
    "description": None
}


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
    # Ensure an action type is provided (add, delete, edit)
    action_type = arg_data.get("1")
    if action_type not in {"add", "delete", "edit"}:
        return {"DESCRIPTION": "⚠️ Error: Invalid action type. Use `add`, `delete`, or `edit`.", "COLOR": color_map["red"]}

    # Ensure an action name is provided
    action_name = arg_data.get("2")
    if not action_name:
        return {"DESCRIPTION": "⚠️ Error: Action name is required. Example: `!pm action add Bite`", "COLOR": color_map["red"]}

    # Sanitize the action name
    action_name, error = sanitize_string_or_error(action_name)
    if error:
        return error  # Return sanitization error if invalid

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

    # Ensure the actions dictionary exists
    if "actions" not in pet:
        pet["actions"] = {}

    # Handle "add" action
    if action_type == "add":
        if action_name in pet["actions"]:
            return {"DESCRIPTION": f"⚠️ Error: Action `{action_name}` already exists.", "COLOR": color_map["orange"]}

        # Create new action from schema
        pet["actions"][action_name] = deepcopy(action_schema)
        pet["actions"][action_name]["name"] = action_name

        # return debug(pet)

        result = save_pet(current_pet_key, pet)
        if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
            return {"TITLE": "Success!", "DESCRIPTION": f"🛠️ Action `{action_name}` added.", "COLOR": color_map["green"]}
        else:
            return result

    # Handle "delete" action
    elif action_type == "delete":
        if action_name not in pet["actions"]:
            return {"DESCRIPTION": f"⚠️ Error: Action `{action_name}` not found.", "COLOR": color_map["orange"]}

        # Remove the action
        pet["actions"] = delete(pet["actions"], action_name)

        result = save_pet(current_pet_key, pet)
        if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
            return {"TITLE": "Success!", "DESCRIPTION": f"🗑️ Action `{action_name}` deleted.", "COLOR": color_map["green"]}
        else:
            return result

    # Handle "edit" action
    elif action_type == "edit":
        if action_name not in pet["actions"]:
            return {"DESCRIPTION": f"⚠️ Error: Action `{action_name}` not found.", "COLOR": color_map["orange"]}

        # Ensure an attribute and value are provided
        action_attr = arg_data.get("3")
        value = " ".join(arg_data.get(str(i), "") for i in range(4, len(arg_data))).strip()

        if not action_attr or not value:
            return {"DESCRIPTION": "⚠️ Error: You must specify an attribute and value. Example: `!pm action edit Bite damage_roll 2d8+3`", "COLOR": color_map["red"]}

        # Validate attribute against action_schema
        if action_attr not in action_schema:
            return {"DESCRIPTION": f"⚠️ Error: `{action_attr}` is not a valid action attribute.", "COLOR": color_map["red"]}

        # Assign the value
        # Ensure proper formatting for numeric modifiers
        if action_attr in {"hit_modifier", "damage_modifier"}:
            if not (value.lstrip("+-").isdigit() and (value.startswith("+") or value.startswith("-"))):
                return {"DESCRIPTION": f"⚠️ Error: `{action_attr}` must be a number with a `+` or `-` sign (e.g., `+2`, `-1`, `+0`).", "COLOR": color_map["red"]}
            value = f"{int(value):+d}"  # Ensure proper sign formatting

        # Assign the value
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

    # Ensure an attack name is provided
    if not attack_name:
        return {"DESCRIPTION": "⚠️ Error: You must specify an attack name. Example: `!pm attack claw`", "COLOR": color_map["red"]}

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

    # Ensure attack exists
    attack_name, sanitize_error = sanitize_string_or_error(attack_name)
    if sanitize_error:
        return sanitize_error

    if attack_name not in pet["actions"]:
        return {"DESCRIPTION": f"⚠️ Error: Attack `{attack_name}` not found. Use `!pm action add {attack_name}` to create it.", "COLOR": color_map["red"]}

    attack = pet["actions"][attack_name]

    # Get roll type (default is normal attack roll)
    roll_type = arg_data.get("2", "").lower()

    # Determine attack roll formula
    hit_modifier = attack.get("hit_modifier", "+0")  # Ensure it's always a string

    if roll_type == "adv":
        attack_roll = f"2d20kh1{hit_modifier}"
    elif roll_type == "dis":
        attack_roll = f"2d20kl1{hit_modifier}"
    elif roll_type:  # If a roll is provided, assume it's a custom roll
        attack_roll = roll_type
    else:  # Default to normal attack roll
        attack_roll = f"1d20{hit_modifier}"

    attack_result = vroll(attack_roll)

    # Get damage roll
    damage_roll = attack.get("damage_roll", "0")
    damage_modifier = attack.get("damage_modifier", "+0")  # Ensure correct sign
    total_damage_roll = f"{damage_roll}{damage_modifier}" if damage_roll != "0" else "0"

    damage_result = vroll(total_damage_roll)

    # Format attack output
    attack_output = (
        f"🎲 **Attack Roll:** {attack_result}\n"
        f"💥 **Damage:** {damage_result} {attack.get('damage_type', '')}\n"
        f"🎯 **Range:** {attack.get('range', 'Melee')}\n"
        f"🎯 **Target:** {attack.get('target', 'Single Target')}\n"
        f"📜 **Description:** {attack.get('description', 'No description.')}"
    )

    return {"TITLE": f"🗡️ {to_proper(attack_name)} Attack", "DESCRIPTION": attack_output, "COLOR": color_map["red"]}

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


#!------------------------- start handle_toggle_list --------------------------#
def handle_toggle_list(arg_data):
    list_map = {
        "condition": "condition",
        "resist": "resist",
        "immune": "immune"
    }

    # Ensure a valid command type
    list_type = arg_data.get("command")
    if list_type not in list_map:
        return {"DESCRIPTION": "⚠️ Error: Invalid command. Use `condition`, `resist`, or `immune`.", "COLOR": color_map["red"]}

    # Get operation and name
    raw_name = arg_data.get("1")

    # Ensure a name is provided
    if not raw_name:
        return {"DESCRIPTION": "⚠️ Error: You must specify a name. Example: `!pm condition +Prone`", "COLOR": color_map["red"]}

    # Determine operation: extract `+` or `-`, or toggle if missing
    operation = None
    if raw_name[0] in {"+", "-"}:
        operation = raw_name[0]  # Get "+" or "-"
        raw_name = raw_name[1:].strip()  # Remove the symbol from the name

    # Sanitize the name
    sanitized_name, error = sanitize_string_or_error(raw_name)
    if error:
        return error  # Return sanitization error if invalid

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

    # Ensure the list exists in pet data
    list_key = list_map[list_type]
    if list_key not in pet:
        pet[list_key] = []  # Initialize if missing

    pet_list = pet[list_key]

    # Determine if we're adding, removing, or toggling
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

    else:  # Toggle mode (no + or - provided)
        if sanitized_name in pet_list:
            pet_list.remove(sanitized_name)
            action = "removed from"
        else:
            pet_list.append(sanitized_name)
            action = "added to"

    # Save updated pet
    result = save_pet(current_pet_key, pet)
    if result.get("DESCRIPTION") == "🧸 Pets saved successfully.":
        return {"TITLE": "Success!", "DESCRIPTION": f"🧸 `{sanitized_name}` {action} `{list_type}`.", "COLOR": color_map["green"]}
    else:
        return result

#!------------------------- end handle_toggle_list --------------------------#






# -----------------------------------------------------------------------#
#                  Command map and process flow control                  #
# -----------------------------------------------------------------------#

commands = {
    "action": handle_action,
    "attack": handle_attack,
    "add": tbd,
    "adopt": handle_adopt,
    "condition": handle_toggle_list,
    "debug": tbd,
    "export": tbd,
    "help": handle_help,
    "immune": handle_toggle_list,
    "import": tbd,
    "list": handle_list,
    "purge": handle_purge,
    "release": handle_release,
    "resist": handle_toggle_list,
    "select": handle_select,
    "set": handle_set,
    "show": tbd,
    "status": tbd,
}

# Now call the function
arg_data = arg_processor(&ARGS&)

command = arg_data.get("command")

result = commands[command](arg_data) if command in commands else tbd(arg_data)

# Merge result with the pre-existing variables
if isinstance(result, dict):
    TITLE = result.get("TITLE", TITLE)
    DESCRIPTION = result.get("DESCRIPTION", DESCRIPTION)
    OUTPUT = result.get("OUTPUT", OUTPUT)
    COLOR = result.get("COLOR", COLOR)
else:
    OUTPUT = result[1]["DESCRIPTION"]
    COLOR = result[1]["COLOR"]

</drac2>
-title "{{TITLE}}"
-desc "{{DESCRIPTION}}"
-f "{{OUTPUT}}"
-color "{{COLOR}}"

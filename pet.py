embed
<drac2>
TITLE = "Pet Handler"
DESCRIPTION = "A **pet manager** made by **PromptFerret**. I accept gifts of gp, karma, dtp, magic items and sessions 🙃🌟🐕"
OUTPUT = "No action taken. Use 'help' for command details."
COLOR = "#ffffff"

pet_schema = {
    "name": "Unnamed",
    "species": "Unknown",
    "description": "No description set. Use `!pet set description <value>` to set one.",
    "color": "#333333",
    "cr":'?',
    "size": "Undefined",
    "type": "Undefined",
    "alignment": "Undefined",
    "ac": 0,
    "hp": {"max": 0,"current": 0,"temp": 0},
    "status": [],
    "speed": {},
    "stats": {"str": 0,"dex": 0,"con": 0,"int": 0,"wis": 0,"cha": 0},
    "skills": "No skills set.",
    "senses": "No senses listed.",
    "traits": {},
    "actions": {},
    "thumbnail": "",
    "source":""
}

action_schema = {
    "name": "",
    "description": "Undefined",
    "attack_roll": "Undefined",
    "hit_roll":"Undefined"
}

# Get the current Avrae character
ch=character()
current_pet = ch.get_cvar("current_pet", None)

def arg_processor(args):
    return {"command": args[0].lower() if args else None, **{str(i): arg for i, arg in enumerate(args[1:], start=1)}}

def clean_and_validate_shortcut(shortcut):
    # Clean up shortcut (lowercase and replace spaces with underscores)
    shortcut_cleaned = shortcut.lower().replace(" ", "_")

    # Validate the shortcut (alphanum, underscores, hyphens check)
    if not all(char.isalnum() or char in ["_", "-"] for char in shortcut_cleaned) or len(shortcut_cleaned) > 10:
        return None, {"DESCRIPTION": f"Error: Invalid shortcut '{shortcut}'. Shortcuts must be alphanumeric, underscores (_), hyphens (-), and at most 10 characters.","color": "#ff0000"}  # Red for failure

    return shortcut_cleaned, None

def isinstance(obj, _type):
    """Custom isinstance replacement using JSON serialization."""
    if _type == dict:
        try:
            return load_json(dump_json(obj)) == obj  # If it survives serialization, it's a dict
        except:
            return False  # If JSON conversion fails, it's not a dictionary
    return False  # We only support dict checks for now


def tbd(arg_data):
    # Pull all arguments except the command itself
    args = {key: value for key, value in arg_data.items() if key != 'command'}
    # Format args neatly as a string
    args_display = "\n".join([f"{key}: {value}" for key, value in args.items()]) if args else "No arguments provided."

    # Fetch custom pets stored in the character/guild variable and handle missing/empty values
    custom_pets = ch.get_cvar("custom_pets", "{}")
    # Load pet data
    custom_pets = load_json(ch.get_cvar("custom_pets", "{}"))

    # Format a cleaner pet summary
    if custom_pets:
        pet_summary = "\n".join([
            f"**{name}** - {data.get('type', 'Unknown')} | HP: {data.get('hp', {}).get('current', 0)}/{data.get('hp', {}).get('max', 0)} | AC: {data.get('ac', 0)}"
            for name, data in custom_pets.items()])
    else:
        pet_summary = "No custom pets defined."

    custom_pets_display = pet_summary

    # Return a structured dictionary including args and pets summary
    return {"DESCRIPTION": f"Command '{arg_data.get('command')}' is not yet implemented.\n\nArguments:\n{args_display}\n\nCustom Pets:\n{custom_pets_display}","color": "#ffaaaa"}   # Soft red to indicate lack of implementation



def handle_create(arg_data):
    shortcut = arg_data.get("1")
    if not shortcut:
        return {"DESCRIPTION": "Error: You must specify a shortcut. Format: `!pet create <shortcut> [name]`","color": "#ff0000"}  # Red for failure

    # Clean and validate the shortcut
    shortcut_cleaned, error = clean_and_validate_shortcut(shortcut)
    if error:
        return error

    # Get the name, if provided, otherwise use the unmodified shortcut
    name = " ".join(arg_data.get(str(i)) for i in range(2, len(arg_data)) if arg_data.get(str(i)))
    name = name or shortcut

    # Load existing custom pets
    custom_pets = load_json(ch.get_cvar("custom_pets", {}))

    # Check if shortcut already exists
    if shortcut_cleaned in custom_pets:
        return {"DESCRIPTION": f"Error: A pet with shortcut '{shortcut}' already exists.","color": "#ff0000"}  # Red for failure

    # Add the new pet schema to custom pets
    new_pet = pet_schema.copy()
    new_pet["name"] = name
    custom_pets[shortcut_cleaned] = new_pet

    # Save the updated custom pets back to the cvar
    ch.set_cvar("custom_pets", dump_json(custom_pets))

    return {"TITLE": "Success!","DESCRIPTION": f"Pet '{shortcut}' created successfully with name '{name}'!","OUTPUT": f"Shortcut: {shortcut_cleaned}, Name: {name}","color": "#00ff00", } # Green for success

def handle_list(arg_data):
    # Load existing custom pets
    custom_pets = load_json(ch.get_cvar("custom_pets", "{}"))

    # Provide feedback if no pets are stored
    if not custom_pets:
        return {"DESCRIPTION": "No pets found. Use `!pet help` to see how to use this program.","color": "#ff0000"}  # Red for failure

    # Format a list of pets with their relevant details
    pet_summary = "\n".join([
        f"**{key}** - {data.get('name', 'Unnamed')}\n"
        f"**(CR:{data.get('cr')})** - {data.get('species')} - {data.get('size')}, {data.get('type')}\n"
        f"HP: {data.get('hp', {}).get('current', 0)}/{data.get('hp', {}).get('max', 0)} | AC: {data.get('ac', 0)} | Status: {', '.join(data.get('status', [])) or 'None'}\n"
        for key, data in custom_pets.items()
    ])

    # Return the formatted list of pets
    return {"DESCRIPTION": f"**Your Pets:**\n\n{pet_summary}","color": "#00ff00"}  # Green for success


def get_pet_or_error(shortcut_cleaned):
    """Loads a pet by shortcut, validates existence, and converts it into an object."""
    # Load existing custom pets
    custom_pets = load_json(ch.get_cvar("custom_pets", "{}"))

    # Check if the shortcut exists
    pet_data = custom_pets.get(shortcut_cleaned)

    if pet_data is None:
        return None, {"DESCRIPTION": f"Error: A pet with shortcut '{shortcut_cleaned}' does not exist.", "color": "#ff0000"}

    return pet_data, None  # Now we are sure it's a dictionary

def handle_select(arg_data):
    shortcut = arg_data.get("1")
    if not shortcut:
        return {"DESCRIPTION": "Error: You must specify a shortcut. Format: `!pet select <shortcut>`", "color": "#ff0000"}

    # Clean and validate the shortcut
    shortcut_cleaned, error = clean_and_validate_shortcut(shortcut)
    if error:
        return error

    # Load the pet (if it exists), otherwise return an error
    active_pet, error = get_pet_or_error(shortcut_cleaned)
    if error:
        return error

    # Save the selected pet as the current pet
    ch.set_cvar("current_pet", shortcut_cleaned)

    return {"TITLE": "Success!","DESCRIPTION": f"Pet '{shortcut_cleaned} - {active_pet.get('name', 'Unknown')}' is awake and ready for action!","OUTPUT": f"Active pet changed to: {shortcut_cleaned}","color": "#00ff00",}  # Green for success



def handle_set(arg_data):
    """Handles setting attributes for the currently active pet."""
    shortcut_cleaned = ch.get_cvar("current_pet")

    if not shortcut_cleaned:
        return {"DESCRIPTION": "Error: No pet is currently selected. Use `!pet select <shortcut>` first.", "color": "#ff0000"}

    # Load the active pet
    active_pet, error = get_pet_or_error(shortcut_cleaned)
    if error:
        return error

    # Ensure both key and value are provided
    key = arg_data.get("1")
    value = " ".join(arg_data.get(str(i)) for i in range(2, len(arg_data)) if arg_data.get(str(i)))

    if not key or not value:
        return {"DESCRIPTION": "Error: You must provide both a key and a value. Format: `!pet set <key> <value>`", "color": "#ff0000"}

    # Prevent modifications to restricted fields
    restricted_keys = ["speed", "traits", "actions"]
    if key.split(".")[0] in restricted_keys:
        return {"DESCRIPTION": f"Error: You cannot modify `{key}`.", "color": "#ff0000"}

    # Validate that the key exists in pet_schema
    keys = key.split(".")
    pet_data = pet_schema  # Start checking from the schema template

    for k in keys[:-1]:  # Traverse through all but the last key
        if k not in pet_data:
            return {"DESCRIPTION": f"Error: `{k}` is not a valid attribute in the pet schema.", "color": "#ff0000"}

        pet_data = pet_data[k]  # Move deeper into the schema

        # Ensure pet_data is still a dictionary
        try:
            if not isinstance(load_json(dump_json(pet_data)), dict):
                return {"DESCRIPTION": f"Error: `{k}` is not a valid nested category.", "color": "#ff0000"}
        except:
            return {"DESCRIPTION": f"Error: `{k}` is not a valid nested category.", "color": "#ff0000"}

    final_key = keys[-1]
    if final_key not in pet_data:
        return {"DESCRIPTION": f"Error: `{final_key}` is not a valid attribute in the pet schema.", "color": "#ff0000"}

    # Now that we know the key is valid, apply the change
    active_pet[final_key] = int(value) if value.isdigit() else value  # Convert to int if applicable

    # Save updated pet data
    custom_pets = load_json(ch.get_cvar("custom_pets", "{}"))
    custom_pets[shortcut_cleaned] = active_pet
    ch.set_cvar("custom_pets", dump_json(custom_pets))

    return {
        "TITLE": "Success!",
        "DESCRIPTION": f"Updated `{key}` to `{value}` for pet `{shortcut_cleaned}`.",
        "color": "#00ff00",
    }


def handle_purge(arg_data):
    """Completely removes pet-related character variables, requiring explicit confirmation."""

    # Check for confirmation argument
    confirmation = arg_data.get("1")
    if confirmation != "YES":
        return {
            "DESCRIPTION": "Error: You must type `!pet purge YES` in all caps to confirm.",
            "color": "#ff0000",  # Red for failure
        }

    # Properly delete pet-related variables
    ch.delete_cvar("current_pet")
    ch.delete_cvar("custom_pets")

    return {
        "TITLE": "Success!",
        "DESCRIPTION": "All pet data has been permanently deleted.",
        "color": "#ff0000",  # Red to indicate a drastic action
    }












def handle_import(arg_data):
    """Imports a pet using the schema as a base, then updates only the provided fields."""

    # Ensure at least two arguments (shortcut + key-value data)
    if len(arg_data) < 2:
        return {
            "DESCRIPTION": "Error: You must provide a shortcut and pet data in key-value format.\nExample:\n`!pet import moo-mochi name: Moo-Mochi species: Armored Saber-Toothed Tiger`",
            "color": "#ff0000",
        }

    # Extract the shortcut (first argument)
    shortcut = arg_data.get("1")
    if not shortcut:
        return {
            "DESCRIPTION": "Error: Missing pet shortcut.\nExample:\n`!pet import moo-mochi name: Moo-Mochi species: Armored Saber-Toothed Tiger`",
            "color": "#ff0000",
        }

    # Rebuild key-value data from remaining arguments (preserve multi-word values)
    raw_data = " ".join([arg_data.get(str(i), "") for i in range(2, len(arg_data))]).strip()

    # Validate input data
    if not raw_data:
        return {
            "DESCRIPTION": "Error: Missing pet data.\nUse key-value format: `!pet import moo-mochi name: Moo-Mochi species: Tiger ac: 17`",
            "color": "#ff0000",
        }

    # **Parse the input data into key-value pairs**
    parsed_data = {}
    current_key = None
    current_value = []

    for entry in raw_data.split(" "):
        if ":" in entry:
            if current_key:
                parsed_data[current_key] = " ".join(current_value).strip()
            current_key, value = entry.split(":", 1)
            current_key = current_key.strip()
            current_value = [value.strip()]
        else:
            current_value.append(entry.strip())

    if current_key:
        parsed_data[current_key] = " ".join(current_value).strip()

    # **Load base pet schema and prepare pet data**
    new_pet = load_json(dump_json(pet_schema))  # Deep copy to avoid schema issues

    # Function to safely convert numeric values
    def safe_int(value, default=0):
        return int(value) if value.isdigit() else default

    # Function to update nested fields
    def update_nested_field(parent_key, field, value):
        if parent_key in new_pet and isinstance(new_pet[parent_key], dict):
            new_pet[parent_key][field] = safe_int(value, new_pet[parent_key].get(field, ""))

    # **Update pet data with provided values**
    for key, value in parsed_data.items():
        if key in new_pet:
            new_pet[key] = safe_int(value, new_pet[key]) if key in ["ac", "cr"] else value
        elif key.startswith("hp_"):
            update_nested_field("hp", key.split("_")[1], value)
        elif key.startswith("stats_"):
            update_nested_field("stats", key.split("_")[1], value)

    # Load existing pets
    custom_pets = load_json(ch.get_cvar("custom_pets", "{}"))

    # Check if the shortcut already exists
    if shortcut in custom_pets:
        return {
            "DESCRIPTION": f"Error: A pet with shortcut `{shortcut}` already exists. Use another shortcut or delete the existing one first.",
            "color": "#ff0000",
        }

    # Save the new pet
    custom_pets[shortcut] = new_pet
    ch.set_cvar("custom_pets", dump_json(custom_pets))

    # **Format a clean output message (without full JSON dump)**
    pet_summary = f"**Name:** {new_pet['name']}\n" \
                  f"**Species:** {new_pet['species']}\n" \
                  f"**AC:** {new_pet['ac']} | **HP:** {new_pet['hp']['current']}/{new_pet['hp']['max']}\n" \
                  f"**STR:** {new_pet['stats']['str']} | **DEX:** {new_pet['stats']['dex']} | **CON:** {new_pet['stats']['con']}\n" \
                  f"**INT:** {new_pet['stats']['int']} | **WIS:** {new_pet['stats']['wis']} | **CHA:** {new_pet['stats']['cha']}\n" \
                  f"**Skills:** {new_pet['skills']}\n" \
                  f"**Senses:** {new_pet['senses']}"

    return {
        "TITLE": "Success!",
        "DESCRIPTION": f"Pet `{shortcut}` imported successfully with provided attributes!\n\n{pet_summary}",
        "color": "#00ff00"  # Green for success
    }







def handle_export(arg_data):
    """Exports a pet's data in the special key-value format used for importing."""

    # Ensure a pet shortcut is provided
    shortcut = arg_data.get("1")
    if not shortcut:
        return {
            "DESCRIPTION": "Error: You must specify a pet to export. Use `!pet export <shortcut>`.",
            "color": "#ff0000",
        }

    # Load existing pets
    custom_pets = load_json(ch.get_cvar("custom_pets", "{}"))

    # Check if the pet exists
    pet_data = custom_pets.get(shortcut)
    if not pet_data:
        return {
            "DESCRIPTION": f"Error: No pet found with the shortcut `{shortcut}`.",
            "color": "#ff0000",
        }

    # **Convert to key-value format**
    export_data = [f"!pet import {shortcut}"]  # Start with the import command

    for key, value in pet_data.items():
        # **Handle dictionaries like hp, stats, traits, and actions**
        if isinstance(value, dict):
            try:
                test_dict = load_json(dump_json(value))  # JSON test to check if it's a dict
                if test_dict == value:
                    for sub_key, sub_value in value.items():
                        if sub_value:  # Skip empty values
                            export_data.append(f"{key}_{sub_key}: {sub_value}")
                else:
                    if value:  # Skip empty values
                        export_data.append(f"{key}: {value}")
            except:
                if value:  # Skip empty values
                    export_data.append(f"{key}: {value}")
        elif isinstance(value, list):
            if value:  # Only add if the list isn't empty
                export_data.append(f"{key}: {', '.join(map(str, value))}")
        else:
            if value:  # Skip empty fields
                export_data.append(f"{key}: {value}")

    # Join into a clean output format
    export_output = "\n".join(export_data)

    return {
        "TITLE": "Pet Export",
        "DESCRIPTION": f"Here is the exportable data for `{shortcut}`.",
        "color": "#00ff00",  # Green for success
        "OUTPUT": f"```\n{export_output}\n```"
    }












# Now call the function
arg_data = arg_processor(&ARGS&)

command = arg_data.get("command")

commands = {
    "help": tbd,
    "create": handle_create,
    "list": handle_list,
    "select":handle_select,
    "add":tbd,
    "set":handle_set,
    "status":tbd,
    "delete":tbd,
    "debug":tbd,
    "show":tbd,
    "purge":handle_purge,
    "import":handle_import,
    "export":handle_export,
}

result = commands[command](arg_data) if command in commands else {
    "DESCRIPTION": "Invalid command. Use 'help' for guidance.",
    "color": "#ff0000",  # Red for failure
}

# Merge result with the pre-existing variables
TITLE = result.get("TITLE", TITLE)
DESCRIPTION = result.get("DESCRIPTION", DESCRIPTION)
OUTPUT = result.get("OUTPUT", OUTPUT)
COLOR = result.get("color", COLOR)




</drac2>
-title "{{TITLE}}"
-desc "{{DESCRIPTION}}"
-f "{{OUTPUT}}"
-color "{{COLOR}}"
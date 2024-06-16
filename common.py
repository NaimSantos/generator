## Basic data structures and common names/variable used in the generation
import re
import os

def print_lines(lines):
    for line in lines:
        print(line)

class InputStruct:
    def __init__(self, outputfile='', producttype=0, card_set=0, urls=''):
            self.outputfile = outputfile
            self.producttype = producttype
            self.card_set = card_set
            self.outputfile = outputfile

class Table_DatasObject:
    def __init__(self, password=1, ot=0, alias=0, setcode=0, cardtype=1, atk=0, defense=0, level=0, race=0, attribute=0, category=0):
        self.password = password
        self.ot = ot
        self.alias = alias
        self.setcode = setcode
        self.cardtype = cardtype
        self.atk = atk
        self.defense = defense
        self.level = level
        self.race = race
        self.attribute = attribute
        self.category = category

class Table_TextsObject:
    def __init__(self, password=1, name='Default Card Name', desc='Default card text', str1='', str2='', str3='', str4='', str5='', str6='', str7='', str8='', str9='', str10='', str11='', str12='', str13='', str14='', str15='', str16=''):
        self.password = password
        self.name = name
        self.desc = desc
        self.str1 = str1
        self.str2 = str2
        self.str3 = str3
        self.str4 = str4
        self.str5 = str5
        self.str6 = str6
        self.str7 = str7
        self.str8 = str8
        self.str9 = str9
        self.str10 = str10
        self.str11 = str11
        self.str12 = str12
        self.str13 = str13
        self.str14 = str14
        self.str15 = str15
        self.str16 = str16

TYPE_MONSTER     = 0x1
TYPE_SPELL       = 0x2
TYPE_TRAP        = 0x4
TYPE_NORMAL      = 0x10
TYPE_EFFECT      = 0x20
TYPE_FUSION      = 0x40
TYPE_RITUAL      = 0x80
TYPE_TRAPMONSTER = 0x100
TYPE_SPIRIT      = 0x200
TYPE_UNION       = 0x400
TYPE_GEMINI      = 0x800
TYPE_TUNER       = 0x1000
TYPE_SYNCHRO     = 0x2000
TYPE_TOKEN       = 0x4000
TYPE_MAXIMUM     = 0x8000
TYPE_QUICKPLAY   = 0x10000
TYPE_CONTINUOUS  = 0x20000
TYPE_EQUIP       = 0x40000
TYPE_FIELD       = 0x80000
TYPE_COUNTER     = 0x100000
TYPE_FLIP        = 0x200000
TYPE_TOON        = 0x400000
TYPE_XYZ         = 0x800000
TYPE_PENDULUM    = 0x1000000
TYPE_SPSUMMON    = 0x2000000
TYPE_LINK        = 0x4000000
TYPE_SKILL       = 0x8000000
TYPE_ACTION      = 0x10000000
TYPE_PLUS        = 0x20000000
TYPE_MINUS       = 0x40000000
TYPE_ARMOR       = 0x80000000
ATTRIBUTE_EARTH  = 0x1
ATTRIBUTE_WATER  = 0x2
ATTRIBUTE_FIRE   = 0x4
ATTRIBUTE_WIND   = 0x8
ATTRIBUTE_LIGHT  = 0x10
ATTRIBUTE_DARK   = 0x20
ATTRIBUTE_DIVINE = 0x40
RACE_WARRIOR          = 0x1
RACE_SPELLCASTER      = 0x2
RACE_FAIRY            = 0x4
RACE_FIEND            = 0x8
RACE_ZOMBIE           = 0x10
RACE_MACHINE          = 0x20
RACE_AQUA             = 0x40
RACE_PYRO             = 0x80
RACE_ROCK             = 0x100
RACE_WINGEDBEAST      = 0x200
RACE_PLANT            = 0x400
RACE_INSECT           = 0x800
RACE_THUNDER          = 0x1000
RACE_DRAGON           = 0x2000
RACE_BEAST            = 0x4000
RACE_BEASTWARRIOR     = 0x8000
RACE_DINOSAUR         = 0x10000
RACE_FISH             = 0x20000
RACE_SEASERPENT       = 0x40000
RACE_REPTILE          = 0x80000
RACE_PSYCHIC          = 0x100000
RACE_DIVINE           = 0x200000
RACE_CREATORGOD       = 0x400000
RACE_WYRM             = 0x800000
RACE_CYBERSE          = 0x1000000
RACE_ILLUSION         = 0x2000000
RACE_CYBORG           = 0x4000000
RACE_MAGICALKNIGHT    = 0x8000000
RACE_HIGHDRAGON       = 0x10000000
RACE_OMEGAPSYCHIC     = 0x20000000
RACE_CELESTIALWARRIOR = 0x40000000
RACE_GALAXY           = 0x80000000
RACE_YOKAI            = 0x4000000000000000
LINK_MARKER_BOTTOM_LEFT  = 0x1
LINK_MARKER_BOTTOM       = 0x2
LINK_MARKER_BOTTOM_RIGHT = 0x4
LINK_MARKER_LEFT         = 0x8
LINK_MARKER_RIGHT        = 0x20
LINK_MARKER_TOP_LEFT     = 0x40
LINK_MARKER_TOP          = 0x80
LINK_MARKER_TOP_RIGHT    = 0x100

def ReturnMonsterTypeFromString(fulltype):
    typ=TYPE_MONSTER
    if "Normal" in fulltype:
        typ=typ|TYPE_NORMAL
    if "Effect" in fulltype:
        typ=typ|TYPE_EFFECT
    if "Fusion" in fulltype:
        typ=typ|TYPE_FUSION
    if "Ritual" in fulltype:
        typ=typ|TYPE_RITUAL
    if "Spirit" in fulltype:
        typ=typ|TYPE_SPIRIT
    if "Union" in fulltype:
        typ=typ|TYPE_UNION
    if "Gemini" in fulltype:
        typ=typ|TYPE_GEMINI
    if "Tuner" in fulltype:
        typ=typ|TYPE_TUNER
    if "Synchro" in fulltype:
        typ=typ|TYPE_SYNCHRO
    if "Flip" in fulltype:
        typ=typ|TYPE_FLIP
    if "Toon" in fulltype:
        typ=typ|TYPE_TOON
    if "Xyz" in fulltype:
        typ=typ|TYPE_XYZ
    if "Pendulum" in fulltype:
        typ=typ|TYPE_PENDULUM
    if "Link" in fulltype:
        typ=typ|TYPE_LINK
    if "Maximum" in fulltype:
        typ=typ|TYPE_MAXIMUM
    return typ

def ReturnRaceFromString(fulltype):
    rac= 0
    if "Warrior" in fulltype:
        rac=rac|RACE_WARRIOR
    if "Spellcaster" in fulltype:
        rac=rac|RACE_SPELLCASTER
    if "Fairy" in fulltype:
        rac=rac|RACE_FAIRY
    if "Fiend" in fulltype:
        rac=rac|RACE_FIEND
    if "Zombie" in fulltype:
        rac=rac|RACE_ZOMBIE
    if "Machine" in fulltype:
        rac=rac|RACE_MACHINE
    if "Aqua" in fulltype:
        rac=rac|RACE_AQUA
    if "Pyro" in fulltype:
        rac=rac|RACE_PYRO
    if "Rock" in fulltype:
        rac=rac|RACE_ROCK
    if "Winged Beast" in fulltype:
        rac=rac|RACE_WINGEDBEAST
    if "Plant" in fulltype:
        rac=rac|RACE_PLANT
    if "Insect" in fulltype:
        rac=rac|RACE_INSECT
    if "Thunder" in fulltype:
        rac=rac|RACE_THUNDER
    if "Dragon" in fulltype:
        rac=rac|RACE_DRAGON
    if "Beast" in fulltype:
        rac=rac|RACE_BEAST
    if "Beast Warrior" in fulltype:
        rac=rac|RACE_BEASTWARRIOR
    if "Dinosaur" in fulltype:
        rac=rac|RACE_DINOSAUR
    if "Fish" in fulltype:
        rac=rac|RACE_FISH
    if "Sea Serpent" in fulltype:
        rac=rac|RACE_SEASERPENT
    if "Reptile" in fulltype:
        rac=rac|RACE_REPTILE
    if "Psychic" in fulltype:
        rac=rac|RACE_PSYCHIC
    if "Divine" in fulltype:
        rac=rac|RACE_DIVINE
    if "Creator God" in fulltype:
        rac=rac|RACE_CREATORGOD
    if "Wyrm" in fulltype:
        rac=rac|RACE_WYRM
    if "Cyberse" in fulltype:
        rac=rac|RACE_CYBERSE
    if "Illusion" in fulltype:
        rac=rac|RACE_ILLUSION
    if "Cyborg" in fulltype:
        rac=rac|RACE_CYBORG
    if "Magical Knight" in fulltype:
        rac=rac|RACE_MAGICALKNIGHT
    if "High Dragon" in fulltype:
        rac=rac|RACE_HIGHDRAGON
    if "Omega Psychic" in fulltype:
        rac=rac|RACE_OMEGAPSYCHIC
    if "Celestial Warrior" in fulltype:
        rac=rac|RACE_CELESTIALWARRIOR
    if "Galaxy" in fulltype:
        rac=rac|RACE_GALAXY
    return rac

def ReturnLinkFromString(string):
    #Assumption: the number of link markers is the number of commas separating them plus 1
    total = string.count(',')
    return total+1

def ReturnPassCodeFromBaseSet(setbase, input_string):
    pattern = r"(?:EN|JP)(\d{3})"
    match = re.search(pattern, input_string)
    if match:
        return int(setbase + match.group(1))
    else:
        return 0

def ReturnLinkMarkerFromString(string):
    marker = 0
    if "Bottom-Left" in string:
        marker=marker|LINK_MARKER_BOTTOM_LEFT
    if "Bottom-Center" in string:
        marker=marker|LINK_MARKER_BOTTOM
    if "Bottom-Right" in string:
        marker=marker|LINK_MARKER_BOTTOM_RIGHT
    if "Middle-Left" in string:
        marker=marker|LINK_MARKER_LEFT
    if "Middle-Right" in string:
        marker=marker|LINK_MARKER_RIGHT
    if "Top-Left" in string:
        marker=marker|LINK_MARKER_TOP_LEFT
    if "Top-Center" in string:
        marker=marker|LINK_MARKER_TOP
    if "Top-Right" in string:
        marker=marker|LINK_MARKER_TOP_RIGHT
    return marker

def ReturnSTTypeFromString(fulltype,propertytype):
    typ=0
    #Major Card Types:
    if "Spell" in fulltype:
        typ=typ|TYPE_SPELL
    elif "Trap" in fulltype:
        typ=typ|TYPE_TRAP
    
    #Specialized card types (type_normal should not be added)
    if "Quick-Play" in propertytype:
        typ=typ|TYPE_QUICKPLAY
    if "Continuous" in propertytype:
        typ=typ|TYPE_CONTINUOUS
    if "Ritual" in propertytype:
        typ=typ|TYPE_RITUAL
    if "Field" in propertytype:
        typ=typ|TYPE_FIELD
    if "Counter" in propertytype:
        typ=typ|TYPE_COUNTER
    if "Equip" in propertytype:
        typ=typ|TYPE_EQUIP
    return typ

def ReturnAttributeFromString(string):
    att=0
    if "EARTH" in string:
        att=att|ATTRIBUTE_EARTH
    if "WATER" in string:
        att=att|ATTRIBUTE_WATER
    if "FIRE" in string:
        att=att|ATTRIBUTE_FIRE
    if "WIND" in string:
        att=att|ATTRIBUTE_WIND
    if "LIGHT" in string:
        att=att|ATTRIBUTE_LIGHT
    if "DARK" in string:
        att=att|ATTRIBUTE_DARK
    if "DIVINE" in string:
        att=att|ATTRIBUTE_DIVINE
    return att

def ReturnArchetypeFromString(string):
    arche=0
    #TODO
    return arche

def format_text(input_text):
    # A proper newline
    input_text = re.sub(r'<br\s*/?>', '\n', input_text)
    # Find and treat the hyperlinks
    def process_match(match):
        inner_text = match.group(1)
        # Check for text delimited by |, which is part of the html tag
        if '|' in inner_text:
            processed_text = inner_text.split('|', 1)[1]
        else:
            processed_text = inner_text

        return processed_text

    # Replace [[ ... ]] , then remove [[ and ]] and '' (two single quote marks)
    input_text = re.sub(r'\[\[(.*?)\]\]', lambda match: process_match(match), input_text)
    input_text = re.sub(r'\[\[|\]\]', '', input_text)
    input_text = input_text.replace("''", '')

    return input_text.strip()

def FormatOCGCardToEdoproText(source_text, materials, pend_effect):
    source_text=format_text(source_text)
    pend_effect=format_text(pend_effect)
    materials=format_text(materials)
    return pend_effect + materials + source_text

def FormatRushCardToEdoproText(cardinfo):
    effect=format_text(cardinfo.get('lore', ''))
    req=format_text(cardinfo.get('requirement', ''))
    materials=format_text(cardinfo.get('materials', ''))
    sum_con=format_text(cardinfo.get('summoning_condition', ''))
    maximum_atk = cardinfo.get('maximum_atk', '')
    effect_types= cardinfo.get('effect_types', '')
    efftype=''
    if "Continuous" in effect_types:
        efftype = "[CONTINUOUS EFFECT]"
    elif "Multi-Choice" in effect_types:
        efftype = "[MULTI-CHOICE EFFECT]"
    else:
        efftype = "[EFFECT]"

    if maximum_atk:
        maximum_atk = "MAXIMUM ATK = " + maximum_atk + '\n'
    if materials :
        materials = materials + '\n\n'
    if sum_con :
        sum_con = sum_con + '\n\n'
    if req :
        req = "[REQUIREMENT]\n" + req + '\n'
    
    return maximum_atk + materials + sum_con + req + efftype + '\n' + effect

def FormatCardName(pagetitle):
    replacements = {
        '_': ' ',
        '(Rush Duel)': '(Rush)',
        '(L)': '[L]',
        '(R)': '[R]'
    }
    output_string = pagetitle
    for old, new in replacements.items():
        output_string = output_string.replace(old, new)

    return output_string

def GenerateLevelWithPScale(lvl,scale):
    level = int(lvl.strip())
    lscale = int(scale.strip())
    rscale = lscale
    return ((lscale << 24) | (rscale << 16) | (level & 0xff))

def convert_to_integer_or_return_original(string):
    try:
        number = int(string)
        return number
    except ValueError:
        return string

def delete_file(filename):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, filename)
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            return f"File '{filename}' deleted successfully."
        except Exception as e:
            return f"Error deleting file '{filename}': {e}"
    else:
        return f"File '{filename}' not found in the current directory."

def append_cdb(filename):
    if not filename.endswith('.cdb'):
        filename += '.cdb'
    return filename

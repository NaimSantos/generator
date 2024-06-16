from common import *
import requests
import wikitextparser as wtp
from urllib.parse import urlparse, unquote

#Global Variables:
requested_fields=["name", "attribute", "card_type", "property", "types", "level", "atk", "def", "password", "lore", "archseries", "pendulum_scale", "pendulum_effect", "link_arrows", "ocg_status", "tcg_status", "materials", "rank", "summoned_by", 'jp_sets', "requirement", "effect_types", "summoning_condition", "rush_duel_status", "maximum_atk", "kr_sets"]

mainurl = 'https://yugipedia.com/api.php'
useragent = {
    'User-Agent': 'TextRegeneratorFromLink'
}
a=1

def Get_Page_Title_From_Url(url):
    parsed_url = urlparse(url)
    if parsed_url.path.startswith('/wiki/'):
        return unquote(parsed_url.path.split('/wiki/')[1])
    return None

def Get_Page_Content_By_Title(page_title):
    executionparparams = {
        'action': 'query',
        'titles': page_title,
        'prop': 'revisions',
        'rvprop': 'content',
        'format': 'json'
    }
    response = requests.get(mainurl, headers=useragent, params=executionparparams)
    if response.status_code == 200:
        data = response.json()
        pages = data['query']['pages']
        return next(iter(pages.values()))['revisions'][0]['*']  # Get the page content
    else:
        print(f"Error: {response.status_code}")
        return None

def Extract_Card_Info(page_content):
    parsed_wikitext = wtp.parse(page_content)
    templates = parsed_wikitext.templates

    card_info = {}
    for template in templates:
        print("The name of this table is ", template.name.strip())
        if template.name.strip() == 'CardTable2':
            for arg in template.arguments:
                for key in requested_fields:
                    if arg.name.strip() == key:
                        card_info[key] = arg.value.strip()
            break
    return card_info

def Extract_All_Card_Info(page_content):
    parsed_wikitext = wtp.parse(page_content)
    templates = parsed_wikitext.templates
    card_info = {}
    for template in templates:
        if template.name.strip() == 'CardTable2':
            for arg in template.arguments:
                card_info[arg.name.strip()] = arg.value.strip()
            break
    return card_info

def Print_Full_Card_Info(page_content):
    parsed_wikitext = wtp.parse(page_content)
    templates = parsed_wikitext.templates
    for template in templates:
        if template.name.strip() == 'CardTable2':
            print("Full card information:")
            for arg in template.arguments:
                print(f"{arg.name.strip()}: {arg.value.strip()}")
            break

def Get_Data_From_Page(url,printinfo="False"):
    page_title = Get_Page_Title_From_Url(url)
    card_info = None

    if page_title:
        page_content = Get_Page_Content_By_Title(page_title)
        if page_content:
            card_info = Extract_All_Card_Info(page_content)
            if card_info:
                if printinfo=='Full':
                    print("\nCard information (full):")
                    Print_Full_Card_Info(page_content)
                elif printinfo=='Partial':
                    print("\nCard information:")
                    for key, value in card_info.items():
                        print(f"{key}: {value}")
            else:
                print("No card information found.")
        else:
            print("No content found for the page.")
    else:
        print("Invalid Yugipedia page URL.")
    return card_info,page_title

def GenerateDataFromCardInfo(cardinfo,pagetitle,baseID,producttype):
    texts=Table_TextsObject()
    data=Table_DatasObject()

    ##Name and passcode
    texts.name = FormatCardName(pagetitle)

    source_set=''
    if 'jp_sets' in cardinfo:
        source_set=cardinfo['jp_sets']
    elif 'en_sets' in cardinfo:
        source_set=cardinfo['en_sets']
    elif 'kr_sets' in cardinfo:
        source_set=cardinfo['kr_sets']


    producttype=int(producttype.strip())
    if producttype==1:
        if 'password' in cardinfo:
            print("The card password is :")
            print(cardinfo['password'])
            data.password=int(cardinfo['password'].strip())
            texts.password=int(cardinfo['password'].strip())
    elif producttype==2:
        if baseID>0:
            temp_password=ReturnPassCodeFromBaseSet(str(baseID), source_set)
            data.password=temp_password
            texts.password=temp_password
    elif producttype==3:
        if baseID>0:
            temp_password=ReturnPassCodeFromBaseSet(str(baseID), source_set)
            data.password=temp_password
            texts.password=temp_password

    print(f"Generating card {data.password} ({texts.name})")

    ##Card text (effects, materials, pendulum text, if any):
    source_text = cardinfo['lore']
    materials = ''
    if 'materials' in cardinfo:
        materials=cardinfo['materials']

    if producttype==3:
        texts.desc = FormatRushCardToEdoproText(cardinfo)
    else:
        pend_effect = ''
        if 'pendulum_effect' in cardinfo:
            pend_effect=cardinfo['pendulum_effect']
        texts.desc = FormatOCGCardToEdoproText(source_text, materials, pend_effect)

    ##OTs
    ot = 3 #Assumes by default an official card released in all regions
    if producttype==3 :
        if 'rush_duel_status' in cardinfo:
            ot=0x300 #Rush pre-release
        else:
            ot=0x200 #Rush released
    if producttype==2: 
        if 'ocg_status' in cardinfo:
            ot=0x101 # TCG, pre-release
        elif 'tcg_status' in cardinfo:
            ot=0x102 # OCG, pre-release
    data.ot = ot

    ##Monster cards
    if 'types' in cardinfo:
        #ATTACK:
        atkvalue=int(cardinfo['atk'].strip())
        if atkvalue == '?' :
            atkvalue = -2
        data.atk=atkvalue

        #DEFENSE:
        defvalue = 0
        if 'def' in cardinfo:
            defvalue=int(cardinfo['def'].strip())
            if defvalue == '?' :
                defvalue = -2
        elif 'link_arrows' in cardinfo:
            defvalue = ReturnLinkMarkerFromString(cardinfo['link_arrows'])
        data.defense=defvalue

        ##Level, Ranks, Links:
        newlevel=1
        if 'rank' in cardinfo:
            newlevel=int(cardinfo['rank'].strip())
        elif 'link_arrows' in cardinfo:
            newlevel = ReturnLinkFromString(cardinfo['link_arrows'])
        elif 'pendulum_scale' in cardinfo:
            newlevel = GenerateLevelWithPScale(cardinfo['level'], cardinfo['pendulum_scale'])
        elif 'level' in cardinfo:
            newlevel=int(cardinfo['level'].strip())
        data.level = newlevel

        #ATTRIBUTE:
        data.attribute= ReturnAttributeFromString(cardinfo['attribute'])

        #RACES
        data.race = ReturnRaceFromString(cardinfo['types'])

        #CARD TYPE:
        monster_type = ReturnMonsterTypeFromString(cardinfo['types'])
        if 'summoned_by' in cardinfo:
            monster_type=monster_type|TYPE_TOKEN
        data.cardtype=monster_type

        ##ARCHETYPES:
        if 'archseries' in cardinfo:
            data.setcode = ReturnArchetypeFromString(cardinfo['archseries'])
    ##Spell and Trap cards
    elif 'card_type' in cardinfo:
        data.cardtype = ReturnSTTypeFromString(cardinfo['card_type'],cardinfo['property'])
    else:
        print("Unknown Card Type. Using default card information.")

    return texts,data
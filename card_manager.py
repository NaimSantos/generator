from common import *
import requests
import wikitextparser as wtp
from urllib.parse import urlparse, unquote
import logging
import os
import json

mainurl = 'https://yugipedia.com/api.php'
useragent = {
    'User-Agent': 'SingleCardGenerator'
}

def GetPageTitleFromUrl(url):
    parsed_url = urlparse(url)
    if parsed_url.path.startswith('/wiki/'):
        return unquote(parsed_url.path.split('/wiki/')[1])
    return None

def GetPageContentFromPageTitle(page_title):
    executionparparams = {
        'action': 'query',
        'titles': page_title,
        'prop': 'revisions',
        'rvprop': 'content',
        'format': 'json'
    }
    try:
        response = requests.get(mainurl, headers=useragent, params=executionparparams)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)

        if response.status_code == 200:
            data = response.json()
            #SaveJsonToFile(data, f"{page_title}_content.json")
            pages = data['query']['pages']
            return next(iter(pages.values()))['revisions'][0]['*']
        else:
            logging.error(f"Unexpected response code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return None

def SaveJsonToFile(data, file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    return file_path

def ExtractCardInfo(page_content):
    parsed_wikitext = wtp.parse(page_content)
    templates = parsed_wikitext.templates
    card_info = {}
    for template in templates:
        if template.name.strip() == 'CardTable2':
            for arg in template.arguments:
                card_info[arg.name.strip()] = arg.value.strip()
            break
    return card_info

def PrintFullCardInfo(page_content):
    parsed_wikitext = wtp.parse(page_content)
    templates = parsed_wikitext.templates
    for template in templates:
        if template.name.strip() == 'CardTable2':
            print("Full card information:")
            for arg in template.arguments:
                print(f"{arg.name.strip()}: {arg.value.strip()}")
            break

def GetCardInfoAndPageTitle(url, printinfo="False"):
    page_title = GetPageTitleFromUrl(url)
    card_info = None

    if page_title:
        page_content = GetPageContentFromPageTitle(page_title)
        if page_content:
            card_info = ExtractCardInfo(page_content)
            if card_info:
                if printinfo:
                    PrintFullCardInfo(page_content)
            else:
                print("No card information found.")
        else:
            print("No content found for the page.")
    else:
        print("Invalid Yugipedia page URL.")
    return card_info,page_title


def FillCardObjectFromCardInfo(cardinfo, pagetitle, baseID, producttype):
    cardobject=CardObject()

    ##Card name
    cardobject.name = GenerateCardNameFromPageTitle(pagetitle)


    producttype=int(producttype.strip()) #1= TCG/OCG released, 2= Unreleased, 3 = Rush

    ##Passcode:
    if baseID:
        #If it is an official released card, it has a passcode
        if producttype==1 and ('password' in cardinfo):
                cardobject.password=int(cardinfo['password'].strip())
        source_set=''
        if 'jp_sets' in cardinfo:
            source_set=cardinfo['jp_sets']
        elif 'en_sets' in cardinfo:
            source_set=cardinfo['en_sets']
        elif 'kr_sets' in cardinfo:
            source_set=cardinfo['kr_sets']
        #If it is unreleased, generate a passcode from the base set + its position in the set
        if producttype==2 or producttype==3:
            if baseID>0:
                cardobject.password=CreatePasscodeFromBaseset(str(baseID), source_set)
    elif producttype==1: 
        if 'password' in cardinfo:
            cardobject.password=int(cardinfo['password'].strip())
    print(f"Generating card {cardobject.password} ({cardobject.name})")

    ##Card text (effects, materials, pendulum text,etc. Rush cards have more fields so they are handled accordingly)
    if producttype==3:
        cardobject.desc = GenerateFormatedRushCardText(cardinfo)
    else:
        cardobject.desc = GenerateFormatedOCGCardText(cardinfo)

    ##OT field in the database
    ot = 3 #Assumes by default an official card released in all regions
    if producttype==3 :
        if (cardinfo['misc']) and ("Legend Card" in cardinfo['misc']):
            if 'rush_duel_status' in cardinfo:
                ot=0x700                      # Rush legend pre-release
            else:
                ot=0x600                      # Rush legend released
        elif 'rush_duel_status' in cardinfo:  # This tag says it is a Rush pre-release
            ot=0x300                          # Rush/Pre-release
        else:
            ot=0x200                          # Rush
    if producttype==2:
        if 'ocg_status' in cardinfo: 
            ot=0x101                          # OCG, pre-release
        elif 'tcg_status' in cardinfo:
            ot=0x102                          # TCG, pre-release
    cardobject.ot = ot

    ## Monster cards
    if 'types' in cardinfo:
        #ATTACK:
        atkvalue=int(cardinfo['atk'].strip())
        if atkvalue == '?' :
            atkvalue = -2
        cardobject.atk=atkvalue

        #DEFENSE:
        defvalue = 0
        if 'def' in cardinfo:
            defvalue=int(cardinfo['def'].strip())
            if defvalue == '?' :
                defvalue = -2
        elif 'link_arrows' in cardinfo:
            defvalue = GetLinkMarkersAsInteger(cardinfo['link_arrows'])
        cardobject.defense=defvalue

        ##Level, Ranks, Links:
        newlevel=1
        if 'rank' in cardinfo:
            newlevel=int(cardinfo['rank'].strip())
        elif 'link_arrows' in cardinfo:
            newlevel = GetLinkRatingAsInteger(cardinfo['link_arrows'])
        elif 'pendulum_scale' in cardinfo:
            newlevel = GenerateLevelWithPScale(cardinfo)
        elif 'level' in cardinfo:
            newlevel=int(cardinfo['level'].strip())
        cardobject.level = newlevel

        #ATTRIBUTE:
        cardobject.attribute= GetAttributeAsInteger(cardinfo['attribute'])

        #RACES
        cardobject.race = GetRaceAsInteger(cardinfo['types'])

        #CARD TYPE:
        monster_type = GetMonsterTypeAsInteger(cardinfo['types'])
        if 'summoned_by' in cardinfo:
            monster_type=monster_type|TYPE_TOKEN
        cardobject.cardtype=monster_type

        ##ARCHETYPES:
        if 'archseries' in cardinfo:
            cardobject.setcode = GenerateArchetype(cardinfo['archseries'])
    ##Spell and Trap cards
    elif 'card_type' in cardinfo:
        cardobject.cardtype = GetSpellTrapTypeAsInteger(cardinfo['card_type'],cardinfo['property'])
    else:
        print("Unknown Card Type. Using default card information.")

    return cardobject


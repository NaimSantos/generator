from common import *
import sqlite3

def CreateNewDatabase(filename):
    cdb = sqlite3.connect(filename)
    cursor = cdb.cursor()
    # edopro's database structure has 2 tables: 'texts' and datas
    cursor.execute('''CREATE TABLE IF NOT EXISTS texts (id integer primary key, name text, desc text,
                                                        str1 text, str2 text, str3 text, str4 text,
                                                        str5 text, str6 text, str7 text, str8 text,
                                                        str9 text, str10 text, str11 text, str12 text,
                                                        str13 text, str14 text, str15 text, str16 text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS datas (id integer primary key, ot integer, alias integer,
                                                        setcode integer, type integer, atk integer, def integer,
                                                        level integer, race integer, attribute integer, category integer)''')
    cdb.commit()
    cdb.close()

def InsertIntoDatabase(filename, obj):
    cdb = sqlite3.connect(filename)
    cursor = cdb.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS texts (id integer primary key, name text, desc text,
                                                        str1 text, str2 text, str3 text, str4 text,
                                                        str5 text, str6 text, str7 text, str8 text,
                                                        str9 text, str10 text, str11 text, str12 text,
                                                        str13 text, str14 text, str15 text, str16 text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS datas (id integer primary key, ot integer, alias integer,
                                                        setcode integer, type integer, atk integer, def integer,
                                                        level integer, race integer, attribute integer, category integer)''')
    
    #Inserir exemplos na tabela:

    cursor.execute('''INSERT INTO texts (id, name, desc, str1, str2, str3, str4, str5, str6, str7, str8, str9, str10, str11, str12, str13, str14, str15, str16)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (obj.password, obj.name, obj.desc, obj.str1, obj.str2, obj.str3, obj.str4, obj.str5, obj.str5, obj.str7,
                      obj.str8, obj.str9, obj.str10, obj.str11, obj.str12, obj.str13, obj.str14, obj.str15, obj.str16))

    cdb.commit()
    cursor.execute('''INSERT INTO datas (id, ot, alias, setcode, type, atk, def, level, race, attribute, category)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (obj.password, obj.ot, obj.alias, obj.setcode, obj.cardtype, obj.atk, obj.defense, obj.level, obj.race, obj.attribute, obj.category))
    cdb.commit()
    cdb.close()
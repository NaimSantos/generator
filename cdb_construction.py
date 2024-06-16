from common import *
import sqlite3


def create_new_database(filename):
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

def insert_into_database(filename, obj1, obj2):
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
                      (obj1.password, obj1.name, obj1.desc, obj1.str1, obj1.str2, obj1.str3, obj1.str4,
                      obj1.str5, obj1.str5, obj1.str7, obj1.str8, obj1.str9, obj1.str10,
                      obj1.str11, obj1.str12, obj1.str13, obj1.str14, obj1.str15, obj1.str16))

    cdb.commit()
    cursor.execute('''INSERT INTO datas (id, ot, alias, setcode, type, atk, def, level, race, attribute, category)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (obj2.password, obj2.ot, obj2.alias, obj2.setcode, obj2.cardtype, obj2.atk, obj2.defense, obj2.level, obj2.race, obj2.attribute, obj2.category))
    cdb.commit()
    cdb.close()
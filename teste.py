from datetime import date
from storm.locals import *
import getpass
import hashlib
import pickle
import sys
import psycopg2

class Person(object):
    __storm_table__ = "login"
    id = Int(primary=True)
    username = unicode()
    password = unicode()

class Post(object):
    __storm_table__ = "post"
    post_id = Int(primary=True)
    user_id = Int
    header = unicode()
    password = unicode()

def schema():
    
    store.execute("DROP TABLE IF EXISTS login CASCADE")
    store.execute("DROP TABLE IF EXISTS post CASCADE")
    store.execute("DROP TABLE IF EXISTS texto CASCADE")

    store.execute("CREATE TABLE login (id serial PRIMARY KEY,"
                                       "username VARCHAR UNIQUE,"
                                       "password VARCHAR)", noresult=True)
    store.execute("CREATE TABLE post (post_id serial PRIMARY KEY,"
                                      "user_id INT References login(id),"
                                      "header VARCHAR UNIQUE,"
                                      "day DATE)", noresult=True)
    store.execute("CREATE TABLE texto (text_id serial PRIMARY KEY,"
                                       "post_id INT References post(post_id),"
                                       "conteudo TEXT)", noresult=True)
    store.commit()

def cadastrar():
    person = Person()
    login = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    password_check = getpass.getpass("Insert the password again: ")
    encrypted_password = hashlib.md5(password).hexdigest()
    person.name = login
    person.password = encrypted_password
    store.add(person)
    store.commit()

#print sys.argv, __name__
if __name__ == '__main__':
    operacao = sys.argv[1]
    database = create_database("postgres://luisoishi@anthem/stoq_luis_teste")
    store = Store(database)
    if operacao == '-c':
        cadastrar()
    elif operacao == '-e':
        example()
    elif operacao == '-i':
        insert()
    elif operacao == '-l':
        listar()
    elif operacao == '-t':
        teste()
    elif operacao == '-s':
        schema()
    else:
	    print operacao," isnt a invalid argument"

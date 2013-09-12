#TODO terminar o insert(), fazer o listar() e fazer testes
from datetime import date
import getpass
import hashlib
import sys

import psycopg2
from storm.locals import Int, create_database, Store, Unicode
from storm.tracer import debug

#debug(True)
class Person(object):
    __storm_table__ = "login"
    id = Int(primary=True)
    username = Unicode()
    password = Unicode()

class Post(object):
    __storm_table__ = "post"
    id = Int(primary=True)
    user_id = Int
    header = Unicode()
    password = Unicode()

class Texto(object):
    __storm_table__ = "texto"
    id = Int(primary=True)
    post_id = Int(primary=False)
    conteudo = Unicode()

def schema():
    
    store.execute("DROP TABLE IF EXISTS login CASCADE")
    store.execute("DROP TABLE IF EXISTS post CASCADE")
    store.execute("DROP TABLE IF EXISTS texto CASCADE")

    store.execute("CREATE TABLE login (id serial PRIMARY KEY,"
                                       "username VARCHAR UNIQUE,"
                                       "password VARCHAR)", noresult=True)
    store.execute("CREATE TABLE post (id serial PRIMARY KEY,"
                                      "user_id INT References login(id),"
                                      "header VARCHAR UNIQUE,"
                                      "day DATE)", noresult=True)
    store.execute("CREATE TABLE texto (id serial PRIMARY KEY,"
                                       "post_id INT References post(id),"
                                       "conteudo TEXT)", noresult=True)
    store.commit()

def cadastrar():
    person = Person()
    login = unicode(raw_input("Username: "))
    search = store.find(Person, username=login).one()
    if search is not None:
        print "Username",login,"already exists"
        return
    password = getpass.getpass("Password: ")
    password_check = getpass.getpass("Insert the password again: ")
    if password != password_check:
        print "passwords dont match"
        return
    encrypted_password = hashlib.md5(password).hexdigest()
    person.username = login
    person.password = unicode(encrypted_password)
    store.add(person)
    store.commit()

def insert():
    print "===============Login==============="
    person = Person()
    
    texto = Texto()
    login = unicode(raw_input("Username: "))
    search = store.find(Person, username=login).one()
    if search is  None:
        print "Username",login,"does not exists"
        return
    password = unicode(getpass.getpass("Password: "))
    encrypted_password = hashlib.md5(password).hexdigest()
    row = store.find(Person, username=login).one()
    if row.password != encrypted_password:
        print "Username and/or Password invalid"
        return
    
    user_id = row.id
    post = Post()
    print "==========Insertion mode=========="
    print "Welcome", login
    title = unicode(raw_input("Header: "))
    search = store.find(Post, header=title).one()
    if search is not None:
        print "Header", title, "already in use"
        return
    dia = unicode(date.today())
    post.user_id = user_id
    post.head = title
    post.day = dia
    store.add(post)
    store.flush()
    text = unicode(raw_input("Post: "))
    
#    texto = Texto()
#    texto.conteudo = text
#    texto.post_id = 
#    cur.execute("SELECT post_id FROM post WHERE header = %s",(title,))
#    row = cur.fetchone()
#    post_id = row[0]
#    cur.execute("INSERT INTO texto(post_id, conteudo) VALUES(%s,%s)",
#                (post_id,text))




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

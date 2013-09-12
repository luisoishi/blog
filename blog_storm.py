#first, import python modules
from datetime import date
import getpass
import hashlib
import sys

#second, import non-python modules, always in alphabetical order
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
    user_id = Int()
    header = Unicode()
    day = Unicode()

class Texto(object):
    __storm_table__ = "texto"
    id = Int(primary=True)
    post_id = Int()
    conteudo = Unicode()

def cadastrar():
    person = Person()
    print "=========================Register========================="
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
    encrypted_password = unicode(hashlib.md5(password).hexdigest())
    person.username = login
    person.password = encrypted_password
    store.add(person)
    store.commit()

def insert():
    print "=========================Login========================="
    person = Person()
    login = unicode(raw_input("Username: "))
    person_search = store.find(Person, username=login).one()
    if person_search is  None:
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
    header_search = store.find(Post, header=title).one()
    if header_search is not None:
        print "Header", title, "already in use"
        return
    dia = unicode(date.today())
    post.user_id = row.id
    post.header = title
    post.day = dia
    store.add(post)
    store.flush

    texto = Texto()
    text = unicode(raw_input("Post: "))
    search = store.find(Post, header=title).one()
    texto.conteudo = text
    texto.post_id = search.id
    store.add(texto)
    store.commit()

def listar():
    result = store.find((Person, Post, Texto),
                             (Person.id == Post.user_id),
                             (Post.id == Texto.post_id))
    for row in result:
        print "============================================================"
        print "Title:", row[1].header
        print "Opened at:" , row[1].day
        print "Owner:",row[0].username
        print "------------------------------------------------------------"
        print row[2].conteudo
        print "============================================================"

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
                                      "day VARCHAR)", noresult=True)
    store.execute("CREATE TABLE texto (id serial PRIMARY KEY,"
                                       "post_id INT References post(id),"
                                       "conteudo TEXT)", noresult=True)
    store.commit()

#print sys.argv, __name__
if __name__ == '__main__':
    operacao = sys.argv[1]
    database = create_database("postgres://luis@localhost/stoq_luis_teste")
    store = Store(database)
    if operacao == '-c':
        cadastrar()
    elif operacao == '-e':
        example()
    elif operacao == '-i':
        insert()
    elif operacao == '-l':
        listar()
    elif operacao == '-s':
        schema()
    else:
	    print operacao," isnt a invalid argument"

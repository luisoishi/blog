import sys
from datetime import date
import pickle
import hashlib
import getpass

def schema():
    conn = psycopg2.connect("dbname=blog user=luis")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS login CASCADE")
    cur.execute("CREATE TABLE login (user_id serial PRIMARY KEY,"
                                     "username varchar(30) UNIQUE,"
                                     "password varchar(20))")
    cur.execute("DROP TABLE IF EXISTS post CASCADE")
    cur.execute("CREATE TABLE post (post_id serial,"
                                    "user_id int references login(user_id),"
                                    "header varchar(30),"
                                    "texto text )")

    conn.commit()
    cur.close()
    conn.close()

def cadastrar():
    conn = psycopg2.connect("dbname=blog user=luis")
    cur = conn.cursor()
    autenticado = 0
    login = raw_input("Username: ")
    senha = getpass.getpass("Password: ")
    password_check = getpass.getpass("Insert the password again: ")
    if senha == password_check:
        try:
            cur.execute("INSERT INTO login (username,password) VALUES(%s, %s)",(login, senha))
        except psycopg2.IntegrityError:
            print "Username" ,login, "already in use"
    else:
        print "password didnt match"
    conn.commit()
    cur.close()
    conn.close()

def insert():
    print "==========Insertion mode=========="
    print
    login = raw_input("username: ")
    senha = getpass.getpass("password: ")
    autenticado = 0
    with open('user.txt', 'r') as user_file:
        try:
            lista = pickle.load(user_file)
        #When user.txt is empty
        except EOFError:
            lista = []

        for user in lista:
            if user['username'] == login:
                autenticado = 1

    if autenticado == 1:
    	print "Welcome",  login
        title = raw_input("Header: ")
        text = raw_input("Post: ")
        dia = unicode(date.today())
        post = {"data": dia, "title": title, "text":text, "user":login}
        #when dados.txt is empty
        with open('dados.txt', 'r') as arquivo:
            try:
                lista = pickle.load(arquivo)
            except EOFError:
                lista = []
			
        with open('dados.txt', 'w') as arquivo:
            lista.append(post)
            pickle.dump(lista, arquivo)
            arquivo.close()

    else:
        print "login and/or password invalid"

    user_file.close()
    
def listar():
    print "==========List Mode==========\n"
    post = []
    with open('dados.txt', 'r') as arquivo:
        try:
            lista = pickle.load(arquivo)
            for post in lista:
                print
                print post["title"], "opened at",post["data"], "as", post["user"]
                print "-------------------------------------"
                print post["text"]
                print "====================================="
        except EOFError:
            print "Empty file!"
        arquivo.close()


    
def teste():
    teste = getpass.getpass("Password")
    teste2 = getpass.getpass("password check")
    if teste == teste2:
        print "igual"

#print sys.argv, __name__
if __name__ == '__main__':
    if sys.argv[1] == '-i':
        insert()

    elif sys.argv[1] == '-l':
        listar()

    elif sys.argv[1] == '-c':
        cadastrar()

    elif sys.argv[1] == '-t':
        teste()

    else:
	print sys.argv[1]," isnt a invalid argument"

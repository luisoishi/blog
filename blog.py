import sys
from datetime import date
import pickle
import hashlib
import getpass
import psycopg2

def schema():
    conn = psycopg2.connect("dbname=blog user=luis")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS login CASCADE")
    cur.execute("CREATE TABLE login (user_id serial PRIMARY KEY,"
                                     "username varchar(40) UNIQUE,"
                                     "password varchar(35))")
    cur.execute("DROP TABLE IF EXISTS post CASCADE")
    cur.execute("CREATE TABLE post (post_id serial,"
                                    "user_id int references login(user_id),"
                                    "header varchar(30) PRIMARY KEY,"
                                    "day date )")
    cur.execute("DROP TABLE IF EXISTS texto CASCADE")
    cur.execute("CREATE TABLE texto (texto_id serial,"
                                     "header varchar(30) references post(header),"
                                     "conteudo text )")

    conn.commit()
    cur.close()
    conn.close()

def cadastrar():
    conn = psycopg2.connect("dbname=blog user=luis")
    cur = conn.cursor()
    autenticado = 0
    print "===============Register==============="
    login = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    password_check = getpass.getpass("Insert the password again: ")
    encrypted_password = hashlib.md5(password).hexdigest()
    if password == password_check:
        try:
            cur.execute("INSERT INTO login (username,password) VALUES(%s, %s)",
                        (login, encrypted_password))
        except psycopg2.IntegrityError:
            print "Username" ,login, "already in use"
    else:
        print "password didnt match"

    conn.commit()
    cur.close()
    conn.close()

def insert():
    print "===============Login==============="
    login = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    encrypted_password = hashlib.md5(password).hexdigest()
    conn = psycopg2.connect("dbname=blog user=luis")
    cur = conn.cursor()
    autenticado = 0
    cur.execute("SELECT user_id,username,password FROM login where username = %s",
                (login,))
    row = cur.fetchone()
    if row != None and login == row[1] and encrypted_password == row[2]:
        user_id =row[0]
        autenticado = 1
    else:
        print "Username and/or Password invalid"

    if autenticado == 1:
        print "==========Insertion mode=========="
        print "Welcome", login
        title = raw_input("Header: ")
        text = raw_input("Post: ")
        dia = unicode(date.today())
        cur.execute("INSERT INTO post(user_id,header,day) VALUES (%s,%s,%s)",
                    (user_id,title,dia))
        cur.execute("INSERT INTO texto(header, conteudo) VALUES(%s,%s)",
                    (title,text))

    conn.commit()
    cur.close()
    conn.close()

def listar():
    conn = psycopg2.connect("dbname=blog user=luis")
    cur = conn.cursor()
    cur.execute("SELECT post.header,day,username, conteudo "
                "FROM login, post, texto "
                "WHERE post.user_id = login.user_id AND "
                "texto.header = post.header")
    for row in cur.fetchall():
        print "============================================================"
        print "Title:",row[0]
        print "Opened at:", row[1]
        print "Owner:",row[2]
        print "------------------------------------------------------------"
        print row[3]
        print "============================================================"

    conn.commit()
    cur.close()
    conn.close()

def teste():
    conn = psycopg2.connect("dbname=blog user=luis")
    cur = conn.cursor()
    cur.execute("SELECT header,day,username,conteudo FROM login,post,texto")
    for row in cur.fetchall():
        print "============================================================"
        print "Title:",row[0]
        print "Opened at:", row[1]
        print "Owner:",row[2]
        print "------------------------------------------------------------"
        print row[3]
        print "============================================================"

    conn.commit()
    cur.close()
    conn.close()
#print sys.argv, __name__
if __name__ == '__main__':
    operacao = sys.argv[1]
    if operacao == '-c':
        cadastrar()
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

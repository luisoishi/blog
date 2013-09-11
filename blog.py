from datetime import date
import getpass
import hashlib
import pickle
import sys
import psycopg2

def cadastrar():
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
            conn.commit()
        except psycopg2.IntegrityError:
            print "Username" ,login, "already in use"
            return
    else:
        print "password didnt match"

    cur.close()
    conn.close()

def example():
    cur.execute("INSERT INTO login (username, password)"
                "VALUES ('luisoishi','3858f62230ac3c915f300c664312c63f')")
    cur.execute("INSERT INTO login (username, password)"
                "VALUES ('luis','acbd18db4cc2f85cedef654fccc4a4d8')")
    cur.execute("INSERT INTO login (username, password)"
                "VALUES ('oishi','37b51d194a7513e45b56f6524f2d51f2')")
    cur.execute("INSERT INTO post (user_id, header, day)"
                "VALUES (1, 'h1', now())")
    cur.execute("INSERT INTO post (user_id, header, day)"
                "VALUES (2, 'h2', now())")
    cur.execute("INSERT INTO post (user_id, header, day)"
                "VALUES (3, 'h3', now())")
    cur.execute("INSERT INTO post (user_id, header, day)"
                "VALUES (2, 'h4', now())")
    cur.execute("INSERT INTO post (user_id, header, day)"
                "VALUES (1, 'h5', now())")
    cur.execute("INSERT INTO texto (post_id, conteudo)"
                "VALUES (1, 't1')")
    cur.execute("INSERT INTO texto (post_id, conteudo)"
                "VALUES (2, 't2')")
    cur.execute("INSERT INTO texto (post_id, conteudo)"
                "VALUES (3, 't3')")
    cur.execute("INSERT INTO texto (post_id, conteudo)"
                "VALUES (4, 't4')")
    cur.execute("INSERT INTO texto (post_id, conteudo)"
                "VALUES (5, 't5')")
    
    conn.commit()
    cur.close()
    conn.close()


def insert():
    print "===============Login==============="
    login = raw_input("Username: ")
    password = getpass.getpass("Password: ")
    encrypted_password = hashlib.md5(password).hexdigest()
    autenticado = 0
    cur.execute("SELECT user_id,username,password FROM login WHERE username = %s",
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
        try:
            cur.execute("INSERT INTO post(user_id,header,day) VALUES (%s,%s,%s)",
                        (user_id,title,dia))
            conn.commit()
        except psycopg2.IntegrityError:
            print "Title", title,"already in use"
            return

        cur.execute("SELECT post_id FROM post WHERE header = %s",(title,))
        row = cur.fetchone()
        post_id = row[0]
        cur.execute("INSERT INTO texto(post_id, conteudo) VALUES(%s,%s)",
                    (post_id,text))
    conn.commit()
    cur.close()
    conn.close()

def listar():
    cur.execute("select header,day,username, conteudo "
                "FROM login, post, texto "
                "WHERE login.user_id = post.user_id AND "
                "post.post_id = texto.post_id")
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

def schema():
    cur.execute("DROP TABLE IF EXISTS login CASCADE")
    cur.execute("DROP TABLE IF EXISTS post CASCADE")
    cur.execute("DROP TABLE IF EXISTS texto CASCADE")

    cur.execute("CREATE TABLE login (user_id serial PRIMARY KEY,"
                                     "username varchar(40) UNIQUE,"
                                     "password varchar(35))")
    cur.execute("CREATE TABLE post (post_id serial PRIMARY KEY,"
                                    "user_id int references login(user_id),"
                                    "header varchar(30) UNIQUE,"
                                    "day date )")
    cur.execute("CREATE TABLE texto (texto_id serial,"
                                     "post_id int references post(post_id),"
                                     "conteudo text )")

    conn.commit()
    cur.close()
    conn.close()


def teste():
    username = raw_input("Username: ")
    cur.execute("SELECT post.header, day, username, conteudo "
                "FROM login, post, texto "
                "WHERE post.user_id = login.user_id AND "
                "texto.post_id = post.post_id AND "
                "username = %s", (username,))
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
    conn = psycopg2.connect("dbname=luis_blog user=luisoishi")
    cur = conn.cursor()
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

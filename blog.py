import sys
from datetime import date
import pickle
import hashlib
import getpass

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

def cadastrar():
    username = raw_input("Insert user name: ")
    password = getpass.getpass("Password:")
    password_check = getpass.getpass("Insert the password again: ")
    user = {"username": username, "password":password}
    if password == password_check:
        #When user.txt is empty
        with open('user.txt', 'r') as user_file:
            try:
                lista = pickle.load(user_file)
            except EOFError:
                lista = []
        with open('user.txt', 'w') as user_file:
            sign_up = {'username': username, 'password': password}
            lista.append(sign_up)
            pickle.dump(lista, user_file)
            print "User created sucessfully"
    else:
        print "passwords dont match"

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

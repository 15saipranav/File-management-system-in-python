"""
Initialization of Client
"""
import asyncio

ISSUED = ''
def startServer():
    """
    this function is responsibale for taking choice for login and register
    """
    print('******* welcome to file management system *******')
    while True:
        print('1 : Login ')
        print('2 : Register ')
        choice = input('Enter Choice(1,2): ')
        if choice == '1':
            result = login()
            return result
        elif choice == '2':
            result = register()
            return result
        print('Invalid Input ')

def responses(message):
    """
    messages that need to be sent to the server are filtered
    for client commands.
    """
    split_message = message.split(' ', 1)
    command = split_message[0]
    count_arguments = len(split_message)
    global ISSUED
    if command == 'commands':
        if count_arguments == 1:
            c_file = open('commands.txt', 'r')
            content = c_file.read()
            print(content)
            return False
        elif count_arguments == 2:
            argument = split_message[1]
            if argument == 'issued':
                print(ISSUED)
                return False
            elif argument == 'clear':
                ISSUED = ''
                print('Cleared')
                return False
            print('Invalid command')
            return False
        print('invalid arguments')
        return False
    ISSUED += str('\n'+message)
    return True

def login():
    """
    this functions inputs login credential and combines them into an argument
    """
    print(':):):):)Login:):):):):)')
    user_name = input('User Name : ')
    password = input('Password : ')
    result = str(f'login {user_name} {password}')
    return result

def register():
    """
    this functions inputs registeration details and combines them into an argument
    """
    print(':-:-:- Register :-:-:-')
    user_name = input('Create User Name : ')
    password = input('Create Password : ')
    result = str(f'register {user_name} {password}')
    return result

async def tcp__client():
    """
    this functions initilases connection with the server
    """
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 4444)
    message = ''

    while True:
        request = startServer()
        writer.write(request.encode())
        data = await reader.read(10000)
        message = data.decode()
        if message == 'sucessfull':
            print('successfully logged in ')
            break
        elif message == 'Created':
            print('New user Created')
            break
        elif message == 'exist':
            print('User has already logged in ')
            print('Try again with new Username ')
            continue
        elif message == 'failed':
            print('Error occured while login ')
            print('Try Again')
            continue
        elif message == 'invalid':
            print('provide correct input')
            continue
        elif message == '     user loggedin':
            print('Same user logged in from another client')
            continue
        else:
            print('Error occured, try Again ')
            continue
    print('Hint:- By entering "commands" you can play with the server ')
    while True:
        message = input(':->')

        if message == 'quit':
            writer.write(message.encode())
            break
        elif message == '':
            continue
        reply = responses(message)
        if reply:
            writer.write(message.encode())
            data = await reader.read(10000)
            print(f'{data.decode()}')
    print('Connection closed')
    writer.close()

try:
    asyncio.run(tcp__client())
except ConnectionRefusedError:
    print(':( server connection failed:(')
import os
import asyncio
import signal
from logic import UserList
class ServerClass:
    """ [server class which executes the methods coreponding to the server]
    """
    def __init__(self):
        """Initialises all the attributes
        """
        self.user_name = ''
        self.pwd = ''
        self.rot_directory = os.getcwd()
        self.curnt_directory = ''
        self.message = ''

    def find_user(self, user_name) -> str:
        """find_user [checks whether the user is in the logfile if exist returns
        unname already exist or returns error message ]
        Arguments:
            user_name {[str]} -- [Getting user_name for checking the user exist or not]
        Returns:
            [str] -- [error!!]
        """
        file  = 'userlog.txt'
        filename = str(f'{self.rot_directory}\\{file}')
        with open(filename, 'r') as o_file:
            num_lines = o_file.readlines()
            line = sum(1 for everyline in num_lines)
            var = 0
            num = []
            name = []
            for  var in range(line):
                file = num_lines[var].strip()
                div = file.find(',')
                num.append(div)
                name.append(file[:num[var]])
            if user_name in name:
                # print('user_name')
                return 'exist'
            return 'error occured'
    def initiate(self):
        """initiate [sending user_names pwds and directories to the client]
        """
        self.client = UserList(
            self.user_name,
            self.pwd,
            self.curnt_directory,
            self.rot_directory)
    def remove_user(self):
        """remove_user [erases the user_name present in the file after closing the connection]
        """
        path = os.path.join(self.rot_directory, 'loginlog.txt')
        with open(path, 'r') as new_file:
            lines = new_file.readlines()
            for i in range(len(lines)):
                if self.user_name in lines[i]:
                    pos = i
        new_file.close()
        new_file = open(path, 'w')
        for i in range(len(lines)):
            if pos != i:
                new_file.writelines(lines[i])
        new_file.close()

    def print_message(self, message :str) -> str:
        """print_message [returns the splitted message with responses]
        Arguments:
            message {[str]} -- [stores the splitted message]
        Returns:
            [string] -- [returns the split message separated by ',']
        """
        self.message = message
        message = self.message.split(' ', 2)
        print('message split: ', message)
        result = self.commands(message)
        print('message split reply: ', result)
        return result

    def create_folder(self, user_name):
        """create_folder [creates the folder respected to user_name]
        Arguments:
            user_name {[str]} -- [user_name for creating a folder with the name]
        """
        path = os.path.join(self.rot_directory, user_name)
        # print(path)
        os.mkdir(path)
        self.user_log(path, user_name)


    def dump_pwd(self, user_name) -> str:
        """dump_pwd [fetching pwd from a file]
        Arguments:
            user_name {[str]} -- [for checking  the pwd of the user ]

        Returns:
            str -- [checks whether the pwd is correct or not from the response]
        """
        user_data = 'userlog.txt'
        user_file = open(user_data, 'r')
        u_line = user_file.readlines()
        # print(u_line)
        user_names = []
        user_pwd = []
        for i in u_line:
            file = i.strip().split(",", 1)
            user_names.append(file[0])
            user_pwd.append(file[1])
        # print(user_names, user_pwd)
        for j in range(0, len(user_names)):
            if user_name == user_names[j]:
                user_creds = user_pwd[j]
                return user_creds
        user_creds = 'failed'
        return user_creds

    def login(self, message) -> str:
        """login [checks whether the pwd and user_name is correct or not]
        Arguments:
            message {[str]} -- [checks for the response from dump_pwd]

        Returns:
            str -- [returns sucessfull if the pwd is present else returns failed]
        """
        user_name = message[1]
        login_data = open('loginlog.txt', 'r')
        fileread = login_data.read()
        if user_name in fileread:
            return "   user loggedin"
        pwd = message[2]
        msg = self.dump_pwd(user_name)
        if msg == 'failed':
            return 'failed'
        try:
            if msg == pwd:
                w_d=os.path.join(self.rot_directory,user_name)
                self.curnt_directory = w_d
                self.user_name = user_name
                self.pwd = pwd
                self.initiate()
                self.writing_file(self.rot_directory, 'loginlog.txt', self.user_name)
                return'sucessfull'
            else:
                return 'failed'
        except:
            return 'failed'

    def writing_file(self, info, filename, inp):
        """writing_file [This method takes the filename, info, and input
        to modify a file in a directory]
        Arguments:
            info {[str]} -- [takes the information of the folder]
            filename {[str]} -- [takes the given folder name by the user from logic file]
            inp {[str]} -- [This attribute takes the input given by the user]
        """
        filename = str(f'{info}\\{filename}')
        inp = inp
        f_l = open(filename,'a+')
        data = [inp,'\n']
        f_l.writelines(data)
        f_l.close()
    def register(self, user_name, pwd):
        """register [This method registers the user.]
        Arguments:
            user_name {[str]} -- [Stores user_name given by the user]
            pwd {[str]} -- [Stores the pwd given by the user]
        """
        filepath = str(f'{self.rot_directory}\\userlog.txt')
        file = open(filepath,'a+')
        user_data = str(f'{user_name},{pwd}\n')
        file.writelines(user_data)
        file.close()
        self.create_folder(user_name)

    def user_register(self) -> str:
        """user_register [This method initiates the registration process for the user.]
        Returns:
            str -- [returns the response from the login method]
        """
        message = self.message.split(' ' ,3)
        user_name = message[1]
        pwd = message[2]
        reply = self.find_user(user_name)
        try:
            if reply == 'exist':
                return reply
        except NameError as  n_e:
            return n_e
        self.register(user_name, pwd)
        message = ['login', user_name, pwd]
        response = self.login(message)
        # print(response)
        return response

    def user_log(self, directory, user_name):
        """user_log [This method appends the users who are registered into userlog.txt file.]
        Arguments:
            directory {[str]} -- [This argument stores the directory created by the user while registering.]
            user_name {[str]} -- [This argument stores the user_name given by the user.]
        """
        filename = str(f'{directory}\\log.txt')
        file = open(filename, "w")
        data = user_name
        user_data = [data, "\n"]
        file.writelines(user_data)
        file.close()
    def commands(self, message) -> str:
        """commands [This method stores the commands which are redirected for the server
        and completes the respected action of string.]

        Arguments:
            message {str} -- [Stores the message which redirects the specific action]

        Returns:
            str -- [Returns error when the message is not redirected to respective action.]
        """
        command = message[0]
        # print(command)
        if self.user_name == '':
            if command == "login":
                try:
                    response = self.login(message)
                except IOError:
                    response = 'error occured while login'
                return response
            if command == 'register':
                try:
                    response = self.user_register()
                except IOError:
                    response = 'error occured while registering'
                return response
        elif command == 'create_folder':
            try:
                folder_name = message[1]
                response = self.client.create_folder(folder_name)
                # print(response)
            except IOError:
                response = 'error occured while creation of folder'
            return response
        elif command == "list":
            try:
                response = self.client.content_list()
                assert response is not None
            except AssertionError:
                response = " files created "
            except:
                response='error occured'
            return response
        elif command == "change_folder":
            try:
                response = self.client.change_folder(message[1])
            except Exception:
                response = 'error occured while modyfying the directory'
            return response
        elif command == "read_file":

            try:
                response = self.client.read_file(message[1])
            except Exception:
                response = 'error occured while reading the file'
            return response
        elif command == 'write_file':
            try:
                folder = message[1]
            except IndexError:
                reply = 'invalid Argument'
                return reply
            try:
                iput_data = message[2]
                reply = self.client.write_file(folder, iput_data)
            except IndexError:
                reply = self.client.write_file(folder)
            except Exception:
                reply = 'error occured while modyfying the file'
            return reply
        else:
            return "Input is inavlid"

"""A key signal to a command prompt to exit from the
deadlock or infinte loops which can be done by pressing ctrl+c"""
signal.signal(signal.SIGINT, signal.SIG_DFL)
CLIENT_DICTIONARY = {}
async def server_handler(reader, writer):
    """server_handler [To handle server-side connections from the client.]
    Arguments:
        reader {[str]} -- [To get reponses from the client,]
        writer {[str]} -- [To send responses to the client.]
    """
    server_addr = writer.get_extra_info('peername')
    message = f"{server_addr} connection is established."
    CLIENT_DICTIONARY[server_addr[1]] = ServerClass()
    # print(message)
    while True:
        data = await reader.read(10000)
        message = data.decode().strip()
        if message == 'quit':
            CLIENT_DICTIONARY[server_addr[1]].remove_user()
            break
        print(f"Received {message} from {server_addr}")
        reply = CLIENT_DICTIONARY[server_addr[1]].print_message(message)
        print(f"Send: {reply}")
        if reply != '' or reply != 'None':
            writer.write(reply.encode())
        else:
            reply = '.'
            writer.write(reply.encode())
        await writer.drain()
    print("Connection closed")
    writer.close()

async def main():
    """
    In this function the main program is executed
    """
    server_ip = '127.0.0.1'
    port = 4444
    logfile = open('loginlog.txt', 'w')
    logfile.close()
    server = await asyncio.start_server(
        server_handler, server_ip, port)

    server_addr = server.sockets[0].getsockname()
    print(f'Serving on {server_addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
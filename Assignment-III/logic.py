import datetime
import os
import time

class UserList:
    """ [This class runs the user commands coresponding to reply from client]
    """
    def __init__(self, username, password, c_directory, r_directory):
        """__init__ [initializing all the attributes]
        Arguments:
            username {[str]} -- [username from server]
            password {[str]} -- [password from server]
            c_directory {[str]} -- [directory to store the current working directory]
            r_directory {[type]} -- [directory where the users are created]
        """
        self.username = username
        self.password = password
        self.c_directory = c_directory
        self.r_directory = r_directory
        self.r_file = " "
        self.firstpoint = 0

    def content_list(self):
        file_path = self.c_directory
        dirs = os.listdir(os.getcwd())  # lists all files and folders
        for file in dirs:
            print(file)

    def create_folder(self, filename):
        """create_folder [creating a folder from a server]
        Arguments:
            filename {[str]} -- [filename that need to be created]

        Returns:
            [str] -- [returns whether the folder is created or not]
        """
        try:
            path = os.path.join(self.c_directory, filename)
            os.mkdir(path)
        except IOError:
            response = 'failed to create folder'
            return response
        response = 'folder created'
        return response

    def write_file(self, filename, message=None):
        """write_file [writing a file if the file is not present it creates and writes the file]
        Arguments:
            filename {[str]} -- [It stores the filename which need to written]

        Keyword Arguments:
            message {[str]} -- [Input given by the user to write in a file] (default: {None})

        Returns:
            [str] -- [returns whther the file created or edited]
        """
        path = os.path.join(self.c_directory, filename)
        if message == None:
            with open(path, 'w')  as file:
                file.close()
                response = 'file cleared'
                return response
        else:
            with  open(path, 'a') as file:
                data = [message, '\n']
                file.writelines(data)
                file.close()
                response = 'file edited'
                return response

    def read_file(self, filename):
        """read_file [reads and displays the file present in a directory]
        Arguments:
            filename {[str]} -- [It stores the filename to read the whole file]

        Returns:
            [str] -- [returns whether the is created or closed]
        """
        if filename is None:
            if self.r_file != '':
                self.r_file = ''
                response = 'file  is closed'
                return response
            response = 'wrong argument'
            return response
        path = os.path.join(self.c_directory, filename)
        try:
            if os.path.exists(path):
                if self.r_file == filename:
                    self.firstpoint += 100
                    reply = self.file_loc(path, self.firstpoint)
                    return reply
                self.r_file = filename
                self.firstpoint = 0
                reply = self.file_loc(path, self.firstpoint)
                return reply
            reply = 'no such file exist'
            return reply
        except FileNotFoundError:
            reply = 'given file is a folder'
            return reply
        except:
            reply = 'error occured'
            return reply

    def change_folder(self, filename):
        """change_folder [changes the current working directory into given directory]
        Arguments:
            filename {[str]} -- [stores the filename which folder directory to be changed]

        Returns:
            [str] -- [returns whether the file is changed or not present in directory]
        """
        path = (self.r_directory)[::-1]
        num = path.find('\\')+1
        final_path = path[num:][::-1]
        inp = '..'
        try:
            if filename == inp:
                rev = (self.c_directory)[::-1]
                num = rev.find('\\')+1
                new_path = rev[num:][::-1]
                if new_path == final_path:
                    return 'Access denied'
                self.c_directory = (new_path)
                reply = 'directory changed to : '+self.c_directory
                return reply
            directory = os.path.join(self.c_directory, filename)
            if os.path.isdir(directory):
                if self.c_directory == self.r_directory:
                    if filename == self.username:
                        self.c_directory = directory
                        reply = 'directory changed to : '+self.c_directory
                        return reply
                    else:
                        reply = 'Access denied'
                        return reply
                self.c_directory = directory
                reply = 'directory changed to : '+self.c_directory
                return reply
            else:
                return 'File not found'
        except Exception as error:
            return error

    def file_input(self, info, filename, input_str):
        """file_input [Inputs the given with response given by the client]
        Arguments:
            info {[str]} -- [stores the root directory of the client]
            filename {[type]} -- [stores the filename of the client]
            input_str {[type]} -- [stores the filename from the client]
        """
        filename = str(f'{info}\\{filename}')
        file = open(filename, 'a')
        user_info = [input_str, "\n"]
        file.writelines(user_info)
        file.close()

    def file_loc(self, filename, firstpoint):
        """file_loc [This method genarates the file location in a directory]
        Arguments:
            filename {[str]} -- [directory of the file to find its location]
            firstpoint {[int]} -- [stores the first 100 lines of the file]
        Returns:
            [str] -- [returns the whole lines in a given file]
        """
        begin = firstpoint+100
        file = open(filename, 'r')
        response = file.read()
        if begin >= len(response):
            self.firstpoint = 0
        return str(response[firstpoint:begin])

    def userlog(self, directory):
        """userlog [creates the userlog.txt file to store the username]
        Arguments:
            directory {[str]} -- [directory which stores the path of cureent working directory]
        """
        file_name = str(f'{directory}\\log.txt')
        file = open(file_name, 'w')
        data = self.username
        uinfo = [data, '/n']
        file.writelines(uinfo)
        file.close()












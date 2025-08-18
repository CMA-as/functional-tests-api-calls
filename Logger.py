import sys

class Logger:
    def __init__(self, filename):
        self.file = open(filename,'w', encoding='utf-8')
        self.stdout = sys.stdout

    def write(self, message):
        self.stdout.write(message)
        self.file.write(message)

    def flush(self):
        self.stdout.flush()
        self.file.flush()

    def log_user_input(self,user_input):
        self.file.write(user_input + '\n')
        self.file.flush()


from threading import Thread
from mail.mail_server import check_mail
from time import sleep


class MailThread(Thread):
    '''
    Create a thread that fetches email on pop3 settings. It will keep running
    until you stop the thread by calling <threadname>.stop().

    TODO: change email while running
    '''
    def __init__(self, sleep_time, server, port, email, password):
        ''' Constructor. '''
        Thread.__init__(self)
        self.running = True
        self.sleep_time = sleep_time
        self.server = server
        self.port = port
        self.email = email
        self.password = password

    def run(self):
        while (self.running):
            print("Checking", self.email + ". On thread " + self.getName())
            check_mail(self.server, self.port, self.email, self.password)
            print("sleeping", self.sleep_time)
            sleep(self.sleep_time)
            #self.running = False
        print("Stopped fetching mail on thread: " + self.getName() + " email: " + self.email)

    def stop(self):
        '''
        Stop Thread
        '''
        self.running = False

    def update(self, sleep_time=None, server=None, port=None, email=None, password=None):
        if (sleep_time != None):
            self.sleep_time = sleep_time
        if (server != None):
            self.server = server
        if (port != None):
            self.port = port
        if (email != None):
            self.email = email
        if (password != None):
            self.password = password

# Run following code when the program starts
if __name__ == '__main__':
    '''
    Example of how you start a thread and then remove it
    '''
    # Declare objects of MyThread class
    myThreadOb1 = MailThread(10, 'pop.gmail.com', '995', 'uvapsetest@gmail.com', 'stephanandrea')
    myThreadOb1.setName('Thread 1')

    # Start running the threads!
    myThreadOb1.start()
    sleep(60)

    # Stop the thread
    myThreadOb1.stop()

    print('Main Terminating...')

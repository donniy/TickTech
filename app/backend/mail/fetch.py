from threading import Thread
from mail.mail_server import check_mail
from time import sleep


class MailThread(Thread):

    '''
    Create a thread that fetches email on pop3 settings. It will keep running
    until you stop the thread by calling <threadname>.stop().

    TODO: change email while running
    '''
    global threads
    threads = []

    def __init__(self, sleep_time, server, port, email, password, course_id):
        ''' Constructor. '''
        Thread.__init__(self)
        self.running = True
        self.sleep_time = sleep_time
        self.server = server
        self.port = port
        self.email = email
        self.password = password
        self.course_id = course_id
        threads.append(self)

    def run(self):
        while (self.running):
            print("Checking", self.email + ". On thread " + self.getName())
            check_mail(self.server, self.port, self.email, self.password,
                       self.course_id)
            print("sleeping", self.sleep_time)
            sleep(self.sleep_time)
        print("Stopped fetching mail on thread: " + self.getName() +
              " email: " + self.email)

    def stop(self):
        '''
        Stop Thread
        '''
        self.running = False
        threads.remove(self)
        print("Stopping thead:", self.getName())

    def update(self, sleep_time=None, server=None, port=None, email=None,
               password=None):
        if sleep_time is not none:
            self.sleep_time = sleep_time
        if server is not none:
            self.server = server
        if port is not none:
            self.port = port
        if email is not none:
            self.email = email
        if password is not none:
            self.password = password

    def print_threads():
        print(threads)
        for t in threads:
            print(t.getName())

    def exist_thread_courseid(course_id):
        for thread in threads:
            if (thread.getName() == course_id):
                return thread
        return None

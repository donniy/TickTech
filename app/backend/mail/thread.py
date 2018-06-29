from mail.mail_server import checkMail
from threading import Thread
from time import sleep


class MailThread(Thread):
    '''
    Create a thread that fetches email on pop3 server. It will keep running
    until you stop the thread by calling <threadname>.stop().
    '''
    global threads
    threads = []

    def __init__(self, sleep_time, server, port, email, password, course_id):
        '''
        Constructor to initialize the thread.
        '''
        Thread.__init__(self)
        self.course_id = course_id
        self.email = email
        self.firstRun = True
        self.password = password
        self.port = port
        self.running = True
        self.sleep_time = sleep_time
        self.server = server
        threads.append(self)

    def run(self):
        '''
        Start fetching mail from a server on a thread.
        '''
        while (self.running):
            print("--- Checking email ---", self.email,
                  ". On thread ",  self.getName())
            checkMail(self.server, self.port, self.email,
                      self.password, self.course_id)
            print("Sleeping for ", self.sleep_time,  " seconds.")
            sleep(self.sleep_time)

        print("--- Stopped fetching mail on thread: ", self.getName(),
              " email: ", self.email, " ---")

    def stop(self):
        '''
        Stop a running thread.
        '''
        self.running = False
        threads.remove(self)

    def update(self, sleep_time=None, server=None,
               port=None, email=None, password=None):
        '''
        Update a running thread.
        '''
        if sleep_time is not None:
            self.sleep_time = sleep_time
        if server is not None:
            self.server = server
        if port is not None:
            self.port = port
        if email is not None:
            self.email = email
        if password is not None:
            self.password = password

    def print_threads():
        '''
        Helper function to print all threads for debugging purposes.
        '''
        print(threads)
        for t in threads:
            print(t.getName())

    def existThreadCourseID(courseid):
        '''
        Helper function to match a thread to a course id.
        '''
        for thread in threads:
            if (thread.getName() == courseid):
                return thread
        return None

    def existThreadEmail(email):
        '''
        Helper function to match a thread to an email address.
        '''
        for thread in threads:
            if (thread.email == email):
                return True
        return False

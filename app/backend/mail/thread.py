from threading import Thread
from mail.mail_server import checkMail
from time import sleep


class MailThread(Thread):

    '''
    Create a thread that fetches email on pop3 server. It will keep running
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
        self.firstRun = True

    def run(self):
        print("***** STARTED MAIL THREAD ******")
        # result = checkMail(self.server, self.port, self.email,
        #                     self.password, self.course_id)
        # if (result == 1):
        # Something went wrong
        #     print("Something went wrong, stop thread" + self.getName())
        #     self.stop()
        # else:
        #     print("Succes!\n\n")
        #     result = requests.post('http://localhost:5000/api/email', "nothing")
        #     print(result)
        #     print("made post request")
        # notify somehow

        while (self.running):
            print("Checking", self.email + ". On thread " + self.getName())
            checkMail(self.server, self.port, self.email,
                      self.password, self.course_id)
            print("Sleeping for ", self.sleep_time, " seconds.")
            sleep(self.sleep_time)

        print("Stopped fetching mail on thread: ", self.getName(),
              " email: ", self.email)

    def stop(self):
        '''
        Stop Thread
        '''
        self.running = False
        threads.remove(self)

    def force_fetch(self):
        print("Checking", self.email + ". On thread " + self.getName())
        checkMail(self.server, self.port, self.email,
                  self.password, self.course_id)

    def update(self, sleep_time=None, server=None,
               port=None, email=None, password=None):
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
        print(threads)
        for t in threads:
            print(t.getName())

    def exist_thread_courseid(course_id):
        for thread in threads:
            if (thread.getName() == course_id):
                return thread
        return None

    def exist_thread_email(email):
        for thread in threads:
            if (thread.email == email):
                return True
        return False

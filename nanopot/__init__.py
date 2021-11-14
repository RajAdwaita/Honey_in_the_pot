import logging
import threading
from socket import socket, timeout

# BIND_IP = "0.0.0.0"
# we will accept the BIND_IP as a configurable parameter


class HoneyPot(object):

    def __init__(self, bind_ip, ports, log_filepath):
        # doing a sanity check for the number of ports
        if len(ports) < 1:
            raise Exception("No ports provided")

        # STORING ALL THE DATA
        self.bind_ip = bind_ip  # BIND_IP
        self.ports = ports
        self.log_filepath = log_filepath  # storing log filepath
        self.listener_threads = {}  # a dictionary to store the listener threads
        self.logger = self.prepare_logger()

        # displaying message to console
        self.logger.info("HoneyPot initializing...")
        self.logger.info("Ports %s " % self.ports)
        self.logger.info("Log filepath %s " % self.log_filepath)

    def handle_connection(self, client_socket, port, ip, remote_port):
        self.logger.info("Connection received: %s: %s:%d" %
                         (port, ip, remote_port))  # add ip and port to log
        # add timeout to socket (15 seconds) timer for 15 seconds
        client_socket.settimeout(15)
        try:

            data = client_socket.recv(64)  # add buffer size to socket
            self.logger.info("Data received: %s: %s:%d: %s" %  # display data received from intruder console
                             (port, ip, remote_port, data))  # add ip and port to log

            # display this message to control when an intruder  tries to pass any message
            client_socket.send("Access Denied.\n".encode(
                'utf8'))  # send a string encoded in utf8
        except timeout:
            # if timeout occurs then it catches the exception and then  display this message to control when an intruder  tries to pass any message

            pass  # just pass in case of exception do not do anything
        client_socket.close()  # close the connection

        # if there are no ports to listen to, it will start a new port and listen to it using start_listening() function
    def start_new_listener_thread(self, port):
        listener = socket()  # add socket type to socket
        listener.bind((self.bind_ip, int(port)))  # add bind ip to socket
        listener.listen(5)  # add backlog to socket

        # for each port we are listening to, we are creating a new thread to listen to that port
        while True:  # whenever we get a client start a new thread
            client, addr = listener.accept()  # accepts the next incoming connection
            client_handler = threading.Thread(
                target=self.handle_connection, args=(client, port, addr[0], addr[1]))
            #  add ip and port to thread

            client_handler.start()  # stop_listening(self):

            # in the start listening() function we are creating a newe listener

    def start_listening(self):  # add port to start_listening
        for port in self.ports:  # go through each port in ports
            self.listener_threads[port] = threading.Thread(  # we are storing a new thread in listeners_thread dictionary
                target=self.start_new_listener_thread, args=(port,))  # the args is a tuple of ports to be passed to the target function
            # from here we know what port it is listening to

            # start the thread and they are all listening to the ports
            self.listener_threads[port].start()

    def run(self):  # add port to run
        self.start_listening()

    def prepare_logger(self):  # add log filepath to logger

        # we are setting up logging to file and console

        logging.basicConfig(level=logging.DEBUG,  # add log level to logger (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                            # create a format for the log and add it to handlers
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%s',
                            # add log filepath to filename in basicConfig call above (logging.basicConfig)
                            filename=self.log_filepath,
                            filemode='w')  # add filemode to logger file config (w) to overwrite file each time the program is run (a) to append to file each time the program is run
        logger = logging.getLogger(__name__)  # add logger name to logger
        console_handler = logging.StreamHandler()  # add console handler to logger

        # add console handler level to logger
        console_handler.setLevel(logging.DEBUG)

        logger.addHandler(console_handler)  # add console handler to logger
        return logger

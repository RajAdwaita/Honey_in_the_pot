import logging
import threading
from socket import socket, timeout

# BIND_IP = "0.0.0.0"


class HoneyPot(object):

    def __init__(self, bind_ip, ports, log_filepath):
        # doing a sanity check for the number of ports
        if len(ports) < 1:
            raise Exception("No ports provided")

        self.bind_ip = bind_ip  # BIND_IP
        self.ports = ports
        self.log_filepath = log_filepath
        self.listener_threads = {}
        self.logger = self.prepare_logger()

        self.logger.info("HoneyPot initializing...")
        self.logger.info("Ports %s " % self.ports)
        self.logger.info("Log filepath %s " % self.log_filepath)

    def handle_connection(self, client_socket, port, ip, remote_port):
        self.logger.info("Connection received: %s: %s:%d" %
                         (port, ip, remote_port))  # TODO: add ip and port to log
        client_socket.settimeout(15)  # TODO: add timeout to socket
        try:

            data = client_socket.recv(64)  # TODO: add buffer size to socket
            self.logger.info("Data received: %s: %s:%d: %s" %
                             (port, ip, remote_port, data))  # TODO: add ip and port to log

            client_socket.send("Access Denied.\n".encode('utf8'))
        except timeout:

            pass
        client_socket.close()

    def start_new_listener_thread(self, port):
        listener = socket()  # TODO: add socket type to socket
        listener.bind((self.bind_ip, int(port)))  # TODO: add bind ip to socket
        listener.listen(5)  # TODO: add backlog to socket
        while True:
            client, addr = listener.accept()
            client_handler = threading.Thread(
                target=self.handle_connection, args=(client, port, addr[0], addr[1]))  # TODO: add ip and port to thread

            client_handler.start()  # stop_listening(self):

    def start_listening(self):  # add port to start_listening
        for port in self.ports:  # go through each port in ports
            self.listener_threads[port] = threading.Thread(  # TODO: add port to thread
                target=self.start_new_listener_thread, args=(port,))

            self.listener_threads[port].start()

    def run(self):  # TODO: add port to run
        self.start_listening()

    def prepare_logger(self):  # TODO: add log filepath to logger

        # we are setting up logging to file and console

        logging.basicConfig(level=logging.DEBUG,  # add log level to logger (DEBUG, INFO, WARNING, ERROR, CRITICAL)
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

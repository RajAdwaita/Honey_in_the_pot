import logging
import threading
from socket import socket, timeout

# BIND_IP = "0.0.0.0"


class HoneyPot(object):

    def __init__(self, bind_ip, ports, log_filepath):
        if len(ports) < 1:
            # print("No ports provided")
            raise Exception("No ports provided")

        self.bind_ip = bind_ip
        self.ports = ports
        self.log_filepath = log_filepath
        self.listener_threads = {}
        self.logger = self.prepare_logger()

        self.logger.info("HoneyPot initializing...")
        self.logger.info("Ports %s " % self.ports)
        self.logger.info("Log filepath %s " % self.log_filepath)

        # self.logger = self.prepare_logger()

        # for port in ports:
        #     print("Going to listen on %s " % port)

    def handle_connection(self, client_socket, port, ip, remote_port):
        self.logger.info("Connection received: %s: %s:%d" %
                         (port, ip, remote_port))
        client_socket.settimeout(15)
        try:

            data = client_socket.recv(64) 
            self.logger.info("Data received: %s: %s:%d: %s" %
                             (port, ip, remote_port, data))

            client_socket.send("Access Denied.\n".encode('utf8'))
        except timeout:

            pass
        client_socket.close()

    def start_new_listener_thread(self, port):
        listener = socket()
        listener.bind((self.bind_ip, int(port)))
        listener.listen(5)
        while True:
            client, addr = listener.accept()
            client_handler = threading.Thread(
                target=self.handle_connection, args=(client, port, addr[0], addr[1]))

            client_handler.start()

    def start_listening(self):
        for port in self.ports:
            self.listener_threads[port] = threading.Thread(
                target=self.start_new_listener_thread, args=(port,))

            self.listener_threads[port].start()

    def run(self):
        self.start_listening()

    def prepare_logger(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%s',
                            filename=self.log_filepath,
                            filemode='w')
        logger = logging.getLogger(__name__)
        # self.logger.addHandler(logging.StreamHandler())
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        logger.addHandler(console_handler)
        return logger

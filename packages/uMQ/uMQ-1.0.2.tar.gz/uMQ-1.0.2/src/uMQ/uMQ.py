"""
    Author: Arash Roshanineshat
    Date: April 2021
    Description: A minimal and reliable JSON MQ library!
    License: MIT
"""

import json
import socket
import threading


"""
Sets the buffer size. for larger packets, a larger buffer size makes 
the process of transmission faster and might prevent overloading of buffer.
For smaller packets, 1024 is usally enough. Choose one of:
1024
2048
4096
and so on to 2**n
"""
BUFFER_SIZE = 1024

"""
Endianness. 'little' endian is default but you can set it to 'big'. 
server and clients MUST use the same endiannes. better to leave it 
as default.
"""
ENDIANNESS = 'little'

DEBUG = False

class uMQ_Socket(object):
    
    def __init__ (self):
        self.sock = socket.socket(socket.AF_INET, 
                                  socket.SOCK_STREAM)     
                
        self.cCs  = [] #client Count stack. 
        
        self.C_index = 0
        
        self.event_callback = threading.Event()
        
    """
        This is the onClose callback function so that the client will be removed
        from the Stack
    """   
    def __remove_from_list(self, C_id):
        if DEBUG:
            print("Removing a client")
        for index, Client in enumerate(self.cCs):
            if Client.get_C_id () == C_id:
                self.cCs.pop(index)
                
    """
        This function increments the client ID
    """           
    def increment_C_id(self):
        if DEBUG:
            print("Adding a client")
        self.C_index = self.C_index + 1
    
    """
        Act as a client and wait for the connections
    """
    def connect (self, ip_address, port):
        if DEBUG:
            print("The socket is now a client. Trying to connect to the server.")
        if (self.sock.fileno() == -1):
            self.sock = socket.socket(socket.AF_INET, 
                                  socket.SOCK_STREAM)   
        self.ip_address = ip_address
        self.port       = port
        
        self.sock.connect((self.ip_address, self.port))
        
        self.__add_socket(self.sock)
    
    """
        Returns the number of connected clients
    """
    def get_clients_count(self):
        return len(self.cCs)
    
    """
        Act as a server and wait for the connections
    """
    def server (self, ip_address, port):
        if DEBUG:
            print("The socket is now a server. Listening for the clients.")
            print(f"Listening on {ip_address}, port {port}")
        if (self.sock.fileno() == -1):
            self.sock = socket.socket(socket.AF_INET, 
                                  socket.SOCK_STREAM)   
    
        self.ip_address = ip_address
        self.port       = port
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        self.sock.bind ((self.ip_address, self.port))
        self.sock.listen(5)
        
        self.st = threading.Thread(target=self.__server_listener)
        self.st.start()
    
    """
        if any of the clients have any data, it will return true,
        otherwise false
    """
    def data_available(self):
        for connected_client in self.cCs:
            if connected_client.get_nmbr_pkts() >0:
                return True
        return False
    
    """
        get the next packet in the list and return it
    """
    def get_next_pkt(self):
        for connected_client in self.cCs:
            if connected_client.get_nmbr_pkts() >0:
                return connected_client.get_pkt()
        return False
    
    def __add_socket(self, C):
        
        new_endpoint = uMQ_EndPoint(C, 
                                     self.C_index, 
                                     self.__remove_from_list,
                                     self.event_callback)
        
        self.cCs.append(new_endpoint)
        self.increment_C_id()
    
    def __server_listener(self):
        while True:
            C, addr = self.sock.accept()
            if DEBUG:
                print(f"New connection received from: {addr[0]}:{addr[1]}")
            self.__add_socket(C)

    """
        This function will send the data to the server
    """
    def send_all(self, data):
        data_b = data.encode('ascii')
        data_size = len(data_b).to_bytes(4, byteorder=ENDIANNESS)
        dta = bytearray()
        dta.extend(data_size)
        dta.extend(data_b)
        
        for C in self.cCs:
            C.send_json(dta)    

    """
        waiting for any event. it is a blocking function
    """
    def hold(self):
        self.event_callback.wait()

    """
        Clearing the flag.
    """
    def Clear(self):
        self.event_callback.clear()

"""
    uMQ endpoint should not be needed by user. 
    the uMQ socket takes care of it.
"""
class uMQ_EndPoint(object):
    def __init__ (self, sock, C_id, on_close_Callback, event_callback):
    
        self.sock = sock
        self.st   = threading.Thread(target=self.EndPoint_worker)
        
        self._IncomingData_FIFO = []
        self.processed_packets = []
        self._C_id = C_id
        
        self.event_callback = event_callback
        
        self.on_close_Callback = on_close_Callback
        
        ###State Machine
        self.Packet_State       = 0
        
        self.STATE_PACKET_SIZE  = 0
        self.STATE_LOADING_PKT  = 1
        
        self.crnt_state         = self.STATE_PACKET_SIZE
        self.crnt_packet_data   = bytearray()
        
        self.crnt_pkt_size_byte = []
        self.crnt_pkt_size = 0
        ################
    
        self.st.start()
        
        
    
    def get_nmbr_pkts(self):
        return len(self.processed_packets)
        
    def get_pkt(self):
        return self.processed_packets.pop(0)
    
    def get_C_id (self):
        return self._C_id
        
        
    def EndPoint_worker(self):
        while True:    
            incoming_data = self.sock.recv(BUFFER_SIZE)
            if not incoming_data:
                ##Connection Lost
                if DEBUG:
                    print ("Connection lost")
                break
            else:
                ## new data coming
                if DEBUG:
                    print ("Incoming data")
                self._IncomingData_FIFO.extend(incoming_data)
                self.Process_Bytes()

        #Close the socket                
        self.sock.close()
        self.on_close_Callback(self.get_C_id()) # remove itself from the list of Clients
        self.event_callback.set() #call the event callback


    def send_json(self, data):
        if DEBUG:
            print ("Sending data")
        self.sock.send(data)

    """
        Next function implements a state machine to separate packets   
        uMQ MUST receive json string.
    """ 
    def Process_Bytes(self):
        while len(self._IncomingData_FIFO) > 0:
            if   self.crnt_state == self.STATE_PACKET_SIZE:
                self.crnt_pkt_size_byte.append(self._IncomingData_FIFO.pop(0))
                if len(self.crnt_pkt_size_byte) == 4:
                    self.crnt_pkt_size = int.from_bytes(self.crnt_pkt_size_byte, byteorder=ENDIANNESS, signed=False)
                    self.crnt_state  = self.STATE_LOADING_PKT #loading the next state, the size is loaded
                    self.crnt_pkt_size_byte.clear()
                    
            elif self.crnt_state == self.STATE_LOADING_PKT :
                self.crnt_packet_data.append(self._IncomingData_FIFO.pop(0))
                if len(self.crnt_packet_data) == self.crnt_pkt_size:
                    json_string = self.crnt_packet_data
                    self.processed_packets.append (json.loads(json_string))
                    self.crnt_packet_data.clear()
                    self.crnt_state = self.STATE_PACKET_SIZE
                    self.event_callback.set() #call the event callback
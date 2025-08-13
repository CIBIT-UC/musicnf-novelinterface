# Class with methods to communicate with TBV network plugin

# These are the variables:
# host, port, rSocket, rInputReqStream, rOutputReqStream,
# eSocket, eInputReqStream, eOutputReqStream,
# inChann, buffer, array
        
# These are the methods:
# __init__, createConnection, closeConnection, query, queryVolumeData,
# sendRequest, getMessage, getVolumeDataMessage, decodeMessage

import struct
import socket
import time
import numpy as np

class TBVClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.rSocket = None
        self.rOutputReqStream = None
        self.rInputReqStream = None
        self.inChann = None
        self.array = None
        self.buffer = None

    def create_connection(self):
        # Open request socket
        self.rSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rSocket.settimeout(2.0)
        self.rSocket.connect((self.host, self.port))

        # Input and output stream from the socket
        self.rOutputReqStream = self.rSocket.makefile('wb')
        self.rInputReqStream = self.rSocket.makefile('rb')

        # Channel and buffer setup
        BUFFER_SIZE = 1024 * 1024 * 2  # 2MB
        self.array = np.zeros(BUFFER_SIZE, dtype=np.int8)
        self.buffer = memoryview(self.array)

        # Send request and get message
        rOK = self.send_request('Request Socket')
        rOK, message = self.get_message()

        print(f' --- request socket open: {rOK}\n\n')
    
    def close_connection(self):
        # Close request socket
        self.rOutputReqStream.close()
        self.rInputReqStream.close()
        self.rSocket.close()

        print(' --- request socket closed\n\n')

    def byte_to_num(self, byte_array, byteorder='big'):
        return int.from_bytes(byte_array, byteorder=byteorder)

    def num_to_byte(self, num, length, byteorder='big'):
        return num.to_bytes(length, byteorder=byteorder)

    def send_request(self, request, output=None):
        if output is None:
            output = []

        ok = True

        try:
            # Create message with request

            # Char to byte
            request_bytes = request.encode('utf-8') + b'\x00'

            # Length of the request (4 bytes)
            request_length = self.num_to_byte(len(request_bytes), 4)

            # Add request parameters
            output_var = bytearray()
            for item in output:
                output_var.extend(self.num_to_byte(item, 4))

            # Length of the message
            message_size = self.num_to_byte(
                len(request_bytes) + len(request_length) + len(output_var),
                8
            )

            # Complete message to send to the server
            to_send = message_size + request_length + request_bytes + output_var

            # Send message using output stream
            self.rOutputReqStream.write(to_send)
            self.rOutputReqStream.flush()

        except Exception as e:
            print(f'Error: {e}')
            ok = False

        return ok

    def get_message(self):
        HEADER_MSG_SIZE = 8
        requestOk = True
        response = b''
        counter = 0

        try:
            # Read message size
            while True:
                bytes_available = self.rSocket.recv(HEADER_MSG_SIZE, socket.MSG_PEEK)
                if len(bytes_available) >= HEADER_MSG_SIZE:
                    break
                time.sleep(0.1)
                #print('waiting...')
                counter += 1
                if counter > 5:
                    requestOk = False
                    return requestOk, response

            msg_size = bytearray()
            for _ in range(HEADER_MSG_SIZE):
                msg_size.append(self.rSocket.recv(1)[0])

            msg_size = self.byte_to_num(msg_size)
            #print(f'\n - message size - {msg_size}')

            # Read the actual message
            counter = 0
            message = bytearray()
            while len(message) < msg_size:
                chunk = self.rSocket.recv(msg_size - len(message))
                message.extend(chunk)
                time.sleep(0.1)
                #print('waiting...')
                counter += 1
                if counter > 5:
                    requestOk = False
                    return requestOk, response

            #print(f'\n - message received - {message}')

            # Decode the message
            request_size, request, response = self.decode_message(message)

        except Exception as e:
            print(f'Error: {e}')
            requestOk = False

        return requestOk, response

    def get_volume_data_message(self, request):
        HEADER_MSG_SIZE = 8
        requestOk = True
        response = b''
        counter = 0

        try:
            # Read message size
            while True:
                bytes_available = self.rSocket.recv(HEADER_MSG_SIZE, socket.MSG_PEEK)
                if len(bytes_available) > HEADER_MSG_SIZE:
                    break
                time.sleep(0.1)
                #print('waiting...')
                counter += 1
                if counter > 5:
                    requestOk = False
                    return requestOk, response

            msg_size = bytearray()
            for _ in range(HEADER_MSG_SIZE):
                msg_size.append(self.rSocket.recv(1)[0])

            msg_size = self.byte_to_num(msg_size)
            #print(f'\n - message size - {msg_size}')

            message = bytearray()
            bytes_read_total = 0

            while bytes_read_total < msg_size:
                bytes_read = self.rInputReqStream.readinto(self.buffer)
                bytes_read_total += bytes_read
                temp_message = self.buffer[:bytes_read].tobytes()
                message.extend(temp_message)
                self.buffer[:] = b'\x00' * len(self.buffer)
                if bytes_read == 0 or bytes_read_total >= msg_size:
                    break

            # Decode the message
            request_size, request, response = self.decode_message(message)

        except Exception as e:
            print(f'Error: {e}')
            requestOk = False

        return requestOk, response

    def decode_message(self, message):
        def byte_to_num(byte_array):
            return int.from_bytes(byte_array, byteorder='big')

        # Extract request size
        request_size = byte_to_num(message[:4])
        message = message[4:]

        # Extract request
        request = message[:request_size].decode('utf-8')
        message = message[request_size:]

        # The response is the remaining part of the message
        response = message

        return request_size, request, response

    def query(self, request, outputs=None):
        if outputs is None:
            outputs = []

        aOK = 0
        message = b''

        try:
            # Send request
            rOK = self.send_request(request, outputs)
        except Exception as e:
            print(f'Error: {e}')
            rOK = 0
            aOK = 0
            return rOK, aOK, message

        try:
            # If request rOK - wait for answer from server
            if rOK:
                aOK, message = self.get_message()
            else:
                print(f' --- request {request} WAS NOT sent.')
        except Exception as e:
            print(f'Error: {e}')
            rOK = 1
            aOK = 0
            message = b''

        return rOK, aOK, message

    def query_volume_data(self, request, outputs=None):
        if outputs is None:
            outputs = []

        aOK = 0
        message = b''

        try:
            # Send request
            rOK = self.send_request(request, outputs)
        except Exception as e:
            print(f'Error: {e}')
            rOK = 0
            aOK = 0
            return rOK, aOK, message

        try:
            # If request rOK - wait for answer from server
            if rOK:
                aOK, message = self.get_volume_data_message(request)
            else:
                print(f' --- request {request} WAS NOT sent.')
        except Exception as e:
            print(f'Error: {e}')
            rOK = 1
            aOK = 0
            message = b''

        return rOK, aOK, message

# Example usage
if __name__ == "__main__":
    conn = TBVClient('192.168.6.72', 55555)
    conn.create_connection()
    rOK, aOK, message = conn.query('tGetWatchFolder')
    print(f'rOK: {rOK}, aOK: {aOK}, message: {message}')

    if rOK and aOK:
        # convert to int and print message
        print(f' --- message: {int.from_bytes(message, byteorder="big")}')


    conn.close_connection()
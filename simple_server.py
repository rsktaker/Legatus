# rsk-machine

# Description: Personal API endpoint to process write and read requests to message bins - perfect for INDIRECT communication between servers
# Created By: Ruchir Kavulli (https://github.com/rsktaker) & Rochan Kavulli (https://github.com/RochanK)



# Single threaded server by default, handles requests one at a time!
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import dotenv

dotenv.load_dotenv()

#XXX: DO I need to do global for these two?
admin_password = os.getenv('admin_password')
admin_name = os.getenv('admin_name')

mess_bins = [{'id':0, 'name': 'commander-bin', 'messages': [] }]
id_counter = 0


class SimpleHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        global mess_bins, id_counter
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = post_data.decode('utf-8')
        password = self.headers.get('pass')

        # If bin is not a valid integer, set it to None
        bin = self.headers.get('bin')
        if bin is not None:
            try:
                bin = int(bin)
            except ValueError:
                bin = None  

        if self.path == '/create-messbin':
            # Create message bin:
            # 'message' is message bin name

            mess_bins.append({})
            id_counter = id_counter + 1
            mess_bins[-1]['id'] = id_counter
            mess_bins[-1]['name'] = message
            mess_bins[-1]['messages'] = []

            rb_data = f'Message bin {id_counter} created with name {message} (*_*).\n'.encode()

        elif self.path == '/messbin':
            # Write to a message bin:
            # Data sent is message. Header contains bin number.

            if (bin is None) or not isinstance(bin, int):
                rb_data = b'Use an existing bin number (*_*)\n'
            elif bin == 0:
                rb_data = f'WARNING: You are not allowed here (*_*)\nThis bin is property of {admin_name}.\n'.encode()
            else:
                for bin_dict in mess_bins:
                    if bin_dict['id'] == bin:
                        bin_dict['messages'].append(message)
                        
                        # Retrieve the last 10 messages (or fewer if not available)
                        chatLogs = ''
                        for i in range(1, 11):
                            try:
                                chatLogs += bin_dict['messages'][-i] + "\n\n"
                            except IndexError:
                                break
                        
                        if chatLogs.strip() == message:
                            rb_data = f'Message stored in message bin {bin} (*_*)\n\nBin logs empty.\n'.encode()
                        else:
                            rb_data = f'Message stored in message bin {bin} (*_*)\n-------------------------------------------------\n\nBin {bin} logs (Max 10):\n{chatLogs}-------------------------------------------------\n\n'.encode()
                        break
                else:
                    rb_data = b'Use an existing bin number (*_*).\n'
        
        elif self.path == '/clear-all':
            # Clear all message bins:
            # Requires "password" to be admin password

            if (password == admin_password):
                mess_bins = [{'id':0, 'name': 'commander-bin', 'messages': [] }]
                rb_data = f'Welcome {admin_name} (*_*)\nAll message bins cleared. Commander bin initialized.\n'.encode()
                id_counter = 0
            else:
                rb_data = 'You are not the commander (*_*)\n'.encode()

        elif self.path == '/commander-bin':
            # Write to commander-bin
            # Data is 'message' and header contains password

            if password == admin_password:
                mess_bins[0]['messages'].append(message)
                chatLogs = ''
                for i in range(1, 11):
                    try:
                        chatLogs += mess_bins[0]['messages'][-i] + "\n\n"
                    except IndexError:
                        break 
                
                if chatLogs.strip() == message:
                    rb_data = f'Welcome {admin_name} (*_*)\n\nMessage stored in commander bin.\nCommander bin logs empty.\n'.encode()
                else:
                    rb_data = f'Message stored in commander bin (*_*)\n-------------------------------------------------\n\nCommander bin logs (Max 10):\n{chatLogs}-------------------------------------------------\n\n'.encode()
            else:
                rb_data = 'You are not the commander (*_*)\n'.encode()

        else:
            rb_data = """
            Welcome to the Message Bin API (*_*)

            Public Endpoints:
            1. POST /create-messbin - Create a new message bin
                Headers:
                - None
                Body:
                - The name of the message bin (string)
            
            2. POST /messbin - Write a message to a bin
                Headers:
                - bin: The ID of the bin (integer)
                Body:
                - The message to store (string)
            
            3. GET /messbin - Read messages from a bin
                Headers:
                - bin: The ID of the bin (integer)
            

            Commander Endpoints:
            4. POST /clear-all - Clear all message bins
                Headers:
                - pass: Admin password (string)
            
            5. POST /commander-bin - Write to commander bin
                Headers:
                - pass: Admin password (string)
                Body:
                - The message to store (string)
            
            6. GET /commander-bin - Read messages from the commander bin
                Headers:
                - pass: Admin password (string)

            """.encode()
                

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(rb_data)

    def do_GET(self):
        global mess_bins, id_counter
        password = self.headers.get('pass')
        # If bin is not a valid integer, set it to None
        bin = self.headers.get('bin')
        if bin is not None:
            try:
                bin = int(bin)
            except ValueError:
                bin = None  

        if self.path == '/messbin':
            # Read a message bin:
            # Header contains bin number.

            if (bin is None) or not isinstance(bin, int):
                rb_data = b'Use an existing bin number (*_*).\n'
            elif bin == 0:
                rb_data = f'WARNING: You are not allowed here (*_*)\nThis bin is property of {admin_name}.\n'.encode()
            else:
                for bin_dict in mess_bins:
                    if bin_dict['id'] == bin:                       
                        # Retrieve the last 10 messages (or fewer if not available)
                        chatLogs = ''
                        for i in range(1, 11):
                            try:
                                chatLogs += bin_dict['messages'][-i] + "\n\n"
                            except IndexError:
                                break  # Stop if there are fewer than i messages

                        if chatLogs == '':
                            rb_data = f'Bin logs empty (*_*)\n'.encode()
                        else:
                            rb_data = f'Reading {bin_dict['name']} (*_*)\n-------------------------------------------------\n\nBin {bin} logs (Max 10):\n\n{chatLogs}\n-------------------------------------------------\n\n'.encode()
                        break
                else:
                    # If no matching bin is found
                    rb_data = b'Use an existing bin number (*_*).\n'
        elif self.path == '/commander-bin':
            # Read commander-bin
            # Header contains password

            if password == admin_password:
                chatLogs = ''
                for i in range(1, 11):
                    try:
                        chatLogs += mess_bins[0]['messages'][-i] + "\n\n"
                    except IndexError:
                        break 
                
                if chatLogs == '':
                    rb_data = f'Welcome {admin_name} (*_*)\nCommander bin logs empty.\n'.encode()
                else:
                    rb_data = f'Reading commander bin (*_*)\n-------------------------------------------------\n\nCommander bin logs (Max 10):\n{chatLogs}\n-------------------------------------------------\n\n'.encode()
            else:
                rb_data = 'You are not the commander (*_*)\n'.encode()
        else:
            rb_data = """
            Welcome to the Message Bin API (*_*)

            Public Endpoints:
            1. POST /create-messbin - Create a new message bin
                Headers:
                - None
                Body:
                - The name of the message bin (string)
            
            2. POST /messbin - Write a message to a bin
                Headers:
                - bin: The ID of the bin (integer)
                Body:
                - The message to store (string)
            
            3. GET /messbin - Read messages from a bin
                Headers:
                - bin: The ID of the bin (integer)
            

            Commander Endpoints:
            4. POST /clear-all - Clear all message bins
                Headers:
                - pass: Admin password (string)
            
            5. POST /commander-bin - Write to commander bin
                Headers:
                - pass: Admin password (string)
                Body:
                - The message to store (string)
            
            6. GET /commander-bin - Read messages from the commander bin
                Headers:
                - pass: Admin password (string)

            """.encode()
            
        

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(rb_data)


if __name__ == "__main__":
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, SimpleHandler)
    print("Server running on port 8080...")
    httpd.serve_forever()

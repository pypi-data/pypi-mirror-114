class cmds:
    """Proccess commands and yield the correct output.\n
     Add a command with cmds.add("command") """
    def __init__(self, debug=True):
        self.pairs = []
        self.debug = debug

    def add(self, command: str, func):
        """
        Add command to cmds. Call command with cmds.call("name")"""
        self.pairs.append((command, func))

    def send_socket(self, command: str,ip: str="localhost", port: int=80, packet_size: int=1024, *args, **kwargs):
        import socket, pickle
        from datetime import datetime
        """
        Create a socket connection to send commands over the network.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                response = {
                    'date': str(datetime.now()),
                    'content':{
                        'function': command,
                        'args': {
                            
                        }
                    }
                }
                for item in kwargs:
                    var_name = str(item)
                    var_value = str(kwargs.get(item))
                    response['content']['args'][var_name] = var_value

                # pack response
                s.connect((ip, port))
                s.sendall(pickle.dumps(response))
                data = s.recv(packet_size)
                return pickle.loads(data)
        except Exception as e:
            print(f"[ERR] Data not sent due to an execption\n\n{e}")

    
    def start_socket(self, ip: str="localhost", port: int=80, packet_size: int=1024):
        import socket, pickle
        from datetime import datetime
        """
        Create a socket to receive commands over the network.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip, port))
            while True:
                s.listen()
                try:
                    conn, addr = s.accept()
                except:
                    print(f"[ERR - {datetime.now()}] Initial connection failed at conn, addr = s.accept()")
                    continue
                print(f"[{datetime.now()}] Connection from {addr[0]}:{addr[1]}")
                with conn:
                    while True:
                        try:
                            data = conn.recv(packet_size)
                            if not data:
                                break
                            dat = pickle.loads(data)
                        except:
                            print(f"[ERR - {datetime.now()}] Malformed data was sent")
                            continue
                        try:
                            if type(dat) == dict:
                                args_list = dat['content']['args']
                                if self.is_valid_function(dat['content']['function']):
                                    output = self.call(dat['content']['function'], args_list)

                                    response = {
                                        'date': str(datetime.now()),
                                        'content':{
                                            'response': output[0],
                                            'output': output[1]
                                        }
                                    }

                                    conn.sendall(pickle.dumps(response))
                                    print(f"[{datetime.now()}] RESPONDED WITH: {response}")
                                else:
                                    response = {
                                        'date': str(datetime.now()),
                                        'content':{
                                            'response': 'BAD',
                                            'output': 'Invalid function name'
                                        }
                                    }

                                    conn.sendall(pickle.dumps(response))
                                    print(f"[{datetime.now()}] RESPONDED WITH: {response}")

                            else:
                                response = {
                                    'date': str(datetime.now()),
                                    'content':{
                                        'response': 'BAD',
                                        'output': 'Invalid form body'
                                    }
                                }
                                
                                conn.sendall(pickle.dumps(response))
                                print(f"[{datetime.now()}] RESPONDED WITH: {response}")
                            break
                        except:
                            print(f"[ERR - {datetime.now()}] Data couldnt be sent back to client")
                            continue



    def is_valid_function(self, fname: str):
        for item in self.pairs:
            if item[0] == fname:
                return True
        return False


    def call(self, func_name: str, arg_dict, **kwargs):
        """
        \nMake sure you name your variables with names that do not conflict with other segments of the code\n
        \n\nReserved variable names:\n
        func_name: str\n
        self: self\n\n
        \nReturns type: tuple\n
        """
        valid = False
        output = None
        for cmd in self.pairs:
            if cmd[0] == func_name:
                try:
                    output = ("GOOD", cmd[1](**arg_dict))
                except Exception as e:
                    output = ('BAD', str(e))
                valid = True
                break
        
        if not valid:
            if self.debug == True:
                print("Invalid function name")
            else:
                raise Exception("Invalid function name: Could not find function with name")
        return output
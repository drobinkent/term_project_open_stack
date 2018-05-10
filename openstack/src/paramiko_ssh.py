import threading, paramiko
import GLOBAL_CONFIG as global_config

class ssh:
    shell = None
    client = None
    transport = None

    def __init__(self, address, username, password = None,commands= ["ls"]):
        self.address = address
        self.username = username
        self.password = password
        self.state = global_config.IDOL_STATE
        print("Connecting to server on ip", str(address) + ".")
        key = paramiko.RSAKey.from_private_key_file(global_config.SSH_KEY_PATH)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        #self.client.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)
        self.client.connect(address,port = 22, username=username,  pkey = key)
        #self.client.connect(address,port = 22, username=username, password=password)
        self.commands = commands
        self.print_output = True
        self.thread = threading.Thread(target=self.process)
        self.thread.daemon = True
        self.thread.start()

    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()

    def openShell(self):
        self.shell = self.client.invoke_shell()

    def sendShell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")
    
    def get_state(self):
        return self.state

    def process(self):
        self.state = global_config.WORKING_STATE
        for cmnd in self.commands:
            stdin, stdout, stderr = self.client.exec_command(cmnd)
            print("Result of ",cmnd," is follwoing ")
            # print("STDIN is : ",stdin)
            # print("stdout is : ",stdout)
            # print("stderr is : ",stderr)
            for line in stdout:
                print(self.address +"..." + line.strip('\n'))
        self.client.close()
        self.state = global_config.FINISHED_STATE



        
            
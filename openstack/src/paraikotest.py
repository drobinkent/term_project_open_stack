import paramiko_ssh as paramiko_ssh




connection = paramiko_ssh.ssh("131.123.39.73", "drobin", "ppa05060")
connection.openShell()
while True:
    command = input('$ ')
    if command.startswith(" "):
        command = command[1:]
    connection.sendShell(command)
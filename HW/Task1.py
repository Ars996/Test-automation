import subprocess

def check_command_output(command, text):
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        return text in output
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

command = "ls"
text = "file.txt"
result = check_command_output(command, text)
print(result)
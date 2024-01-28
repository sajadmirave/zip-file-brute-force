import subprocess
import concurrent.futures
import sys
from colorama import init,Fore
import os

init()

is_password_find = False
cracked_password = ""
output_file = 'crack.txt'
password_list = 'passlist.txt'
zip_file_path = r"info.zip" # target file

colors = {
    "RED":Fore.RED,
    "BLUE":Fore.BLUE,
    "CYAN":Fore.CYAN,
    "MAGENTA":Fore.MAGENTA,
    "WHITE":Fore.WHITE,
    "YELLOW":Fore.YELLOW,
    "GREEN":Fore.GREEN
}

def help_meun():
    print("""
        --target:  target file
        --password-list: password list
        --output: save cracked password
          """)

def checking_string_template(text):
    print(colors['WHITE'] +'[',end='')
    print(colors["RED"] + '-', end='')
    print(colors['WHITE'] + ']', end=' ')
    print(colors['YELLOW'] + f"Checking For: {text}",end='')
    print(colors['WHITE'] + ' | ',end='')
    print(colors['RED'] + 'Failed')
    
def success_string_template(text):
    global is_password_find
    global cracked_password
    
    is_password_find = True
    cracked_password = text
    
    print(colors['WHITE'] +'[',end='')
    print(colors["GREEN"] + '+', end='')
    print(colors['WHITE'] + ']', end=' ')
    print(colors['GREEN'] + f"Successfully verified the password: {text}")    

# check password
# params: str password - the password readed from passlist
def check_password(password,zip_file_path):
    global is_password_find
    if is_password_find:
        return

    # command for check password 
    command = r'"tools/7z.exe" t -p{} "{}"'.format(password, zip_file_path)
            
    # Redirect standard output and error to a pipe and discard it
    return_code = subprocess.call(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
   # try each password 
    if return_code == 0:
        success_string_template(password)
        return True
    elif return_code == 2:
        checking_string_template(password)
    else:
        print(f"Error: 7-Zip returned a non-zero exit code {return_code}")


def main():
    global password_list
    global zip_file_path
    buffer_size = 8192 # buffer size for read faster

    # open password list
    with open(password_list, 'r') as file:
        passwords = file.read(buffer_size).splitlines()

    with concurrent.futures.ThreadPoolExecutor() as executorr:
        futures = [executorr.submit(check_password,password,zip_file_path) for password in passwords]
           
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            
            if is_password_find:
                break

    os.system(f'echo {cracked_password} > {output_file}')
    print(colors['MAGENTA'] + f'password saved in {output_file} file')

    
if __name__ == '__main__':
    options = sys.argv[1:]

    # show help menu
    if options and options[0] == '-h':
        help_meun()
        sys.exit()

    # check option and config
    for index,option in enumerate(options):
        if option == '--target':
            zip_file_path = options[index + 1]

        if option == '--password-list':
            password_list = options[index + 1]
        
        if option == '--output':
            output_file = options[index + 1]    

    main()
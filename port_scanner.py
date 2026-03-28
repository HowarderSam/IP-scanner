import socket
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
import threading
import time
import os

init(autoreset=True)

print_lock = threading.Lock()
open_ports = []
closed_ports = []

GREEN = "\033[1;92m"
WHITE = "\033[97m"
RESET = "\033[0m"

def MainColor(text):
    start_color = (5, 168, 5)  
    end_color = (118, 255 ,118)

    num_steps = 9

    colors = []
    for i in range(num_steps):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        g = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        b = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((r, g, b))
    
    colors += list(reversed(colors[:-1]))  
    
    gradient_chars = '┴┼┘┤└┐─┬├┌└│]░▒░▒█▓▄▌▀()'
    
    def text_color(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
       
    lines = text.split('\n')
    num_colors = len(colors)
    
    result = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char in gradient_chars:
                color_index = (i + j) % num_colors
                color = colors[color_index]
                result.append(text_color(*color) + char + "\0330m")
            else:
                result.append(char)
        if i < len(lines) - 1:
            result.append('\n')
    
    return ''.join(result)



def MainColor2(text):
    start_color = (5, 168, 5)  
    end_color = (118, 255 ,118)

    num_steps = 9

    colors = []
    for i in range(num_steps):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // (num_steps - 1)
        g = start_color[1] + (end_color[1] - start_color[1]) * i // (num_steps - 1)
        b = start_color[2] + (end_color[2] - start_color[2]) * i // (num_steps - 1)
        colors.append((r, g, b))
    
    colors += list(reversed(colors[:-1]))  
    
    def text_color(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"
       
    lines = text.split('\n')
    num_colors = len(colors)
    
    result = []
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            color_index = (i + j) % num_colors
            color = colors[color_index]
            result.append(text_color(*color) + char + "\033[0m")
        
        if i < len(lines) - 1:
            result.append('\n')
    
    return ''.join(result)




def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host, port))

            with print_lock:
                if result == 0:
                    open_ports.append(port)
                    print(GREEN + f"[OPEN  ] Port {port}"+ RESET) 
                else:
                    closed_ports.append(port)
                    print(WHITE + f"[CLOSED] Port {port}"+ RESET)

                time.sleep(0.03)
    except:
        pass

def run_scan():
    os.system("cls")

    target = input(GREEN+ "Type IP or website: " +RESET)

    try:
        host = socket.gethostbyname(target)
        print(GREEN+f"\n[+] Scanning: {host}\n"+RESET)
    except socket.gaierror:
        print("Wrong adress.")
        input("Enter to return to menu...")
        return

    try:
        start_port = int(input(MainColor2("Starting port: ")))
        end_port = int(input(MainColor2("Ending port: ")))
    except ValueError:
        print("Input error.")
        input("Enter to return to menu...")
        return

    open_ports.clear()
    closed_ports.clear()

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=40) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, host, port)

    duration = round(time.time() - start_time, 2)

    print(MainColor2("\n====== SCAN COMPLETE ======"))
    print(WHITE + f"OPEN PORTS ({len(open_ports)}): {sorted(open_ports)}"+ RESET)
    print(GREEN + f"CLOSED PORTS: {len(closed_ports)}"+ RESET)
    print(GREEN +f"Time: {duration} seconds"+ RESET)

    input("\nPress Enter to return to menu...")

def main():
    while True:
        os.system("cls")
        print(MainColor2('''                              

   ___           __    ____                          
  / _ \___  ____/ /_  / __/______ ____  ___  ___ ____
 / ___/ _ \/ __/ __/ _\ \/ __/ _ `/ _ \/ _ \/ -_) __/
/_/   \___/_/  \__/ /___/\__/\_,_/_//_/_//_/\__/_/   
                                                     
                              
                              '''))
        print(MainColor2("╔══════════════════════╗"))
        print(MainColor2("║        MENU          ║"))
        print(MainColor2("╠══════════════════════╣"))
        print(MainColor2("║ [1] Full scan        ║"))
        print(MainColor2("║ [0] Exit             ║"))
        print(MainColor2("╠══════════════════════╣"))
        print(MainColor2("║  Made by Sam Howard  ║"))
        print(MainColor2("╚══════════════════════╝"))
 



        choice = input("\nSelect option: ")

        if choice == "1":
            run_scan()
        elif choice == "0":
            print("\nExiting...")
            time.sleep(0.5)
            break
        else:
            print("Invalid option.")
            time.sleep(1)

if __name__ == "__main__":
    main()

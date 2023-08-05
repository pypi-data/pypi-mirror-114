import os
import subprocess
import sys
from os import system
from installult import git , install , package_name

startup = input(
    "1) Generate StringSession \n2) Install Ultroid\n\nWhat Would you like to do? (1,2) : "
)

try:
    startup = int(startup)
except TypeError:
    print("Not a Valid Input...")

if startup == 1:
    subprocess.run(["bash", "resources/session/session.sh"], check=True)
elif startup == 2:
    global useros
    useros = input("In Which OS are you installing (windows/ubuntu/debian/arch) : ")
    if useros == "ubuntu" or "debian":
        if useros == "ubuntu":
            print("You Have Chosen Ubuntu Distribution")
        else:
            print("You Have Chosen Debian Distribution")
        print("Running Local Setup To Install Ultroid")
        git("clone", "https://github.com/TeamUltroid/Ultroid", "-b", "main")
        system("clear")
        print("Git Repo Has Been Cloned Succesfully")
        os.chdir("Ultroid")
        with open(".env", "w") as f:
            print("Enter the Following Details For Setting Up Ultroid :-")
            app_id = input("API_ID = ")
            api_hash = input("API_HASH = ")
            session = input("SESSION = ")
            redis_uri = input("REDIS_URI = ")
            redis_pass = input("REDIS_PASSWORD = ")
            f.write("API_ID=" + app_id + "\n")
            f.write("API_HASH=" + api_hash + "\n")
            f.write("SESSION=" + session + "\n")
            f.write("REDIS_URI=" + redis_uri + "\n")
            f.write("REDIS_PASSWORD=" + redis_pass + "\n")
            f.close
        print("Installing Requirements.. This may Take a While")
        install("requirements.txt")
        subprocess.run(["wget", "https://git.io/JnZPE"], check=True)
        install("JnZPE")
        system("clear")
        print("Requirements Installed Successfully")
        subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)
        print("Installation of Ultroid Has Completed Successfully")
        ultstart = input("Do you want to start Ultroid now ? (y/n)")
        if ultstart == "y":
            os.execl(sys.executable, sys.executable, "-m", "pyUltroid")
        else:
            print("Ok No Problem.")
    elif useros == "arch":
        print("You Have Chosen Arch Distribution")
        print("Running Local Setup To Install Ultroid")
        git("clone", "https://github.com/TeamUltroid/Ultroid", "-b", "main")
        system("clear")
        print("Git Repo Has Been Cloned Succesfully")
        os.chdir("Ultroid")
        with open(".env", "w") as f:
            print("Enter the Following Details For Setting Up Ultroid :-")
            app_id = input("API_ID = ")
            api_hash = input("API_HASH = ")
            session = input("SESSION = ")
            redis_uri = input("REDIS_URI = ")
            redis_pass = input("REDIS_PASSWORD = ")
            f.write("API_ID=" + app_id + "\n")
            f.write("API_HASH=" + api_hash + "\n")
            f.write("SESSION=" + session + "\n")
            f.write("REDIS_URI=" + redis_uri + "\n")
            f.write("REDIS_PASSWORD=" + redis_pass + "\n")
            f.close
        print("Installing Requirements.. This may Take a While")
        install("requirements.txt")
        subprocess.run(["wget", "https://git.io/JnZPE"], check=True)
        install("JnZPE")
        system("clear")
        print("Requirements Installed Successfully")
        subprocess.run(["sudo", "pacman", "-S", package_name, "-y"], check=True)
        system("clear")
        print("Installed FFmPEg Successfully")
        print("Installation of Ultroid Has Completed Successfully")
        ultstart = input("Do you want to start Ultroid now ? (y/n)")
        if ultstart == "y":
            os.execl(sys.executable, sys.executable, "-m", "pyUltroid")
        else:
            print("Ok No Problem.")
    elif useros == "windows":
        print("You have Chosen Windows Distributuion")
        print("Running Local Setup To Install Ultroid")
        git("clone", "https://github.com/TeamUltroid/Ultroid", "-b", "main")
        os.chdir("Ultroid")
        with open(".env", "w") as f:
            print("Enter the Following Details For Setting Up Ultroid :-")
            app_id = input("API_ID = ")
            api_hash = input("API_HASH = ")
            session = input("SESSION = ")
            redis_uri = input("REDIS_URI = ")
            redis_pass = input("REDIS_PASSWORD = ")
            f.write("API_ID=" + app_id + "\n")
            f.write("API_HASH=" + api_hash + "\n")
            f.write("SESSION=" + session + "\n")
            f.write("REDIS_URI=" + redis_uri + "\n")
            f.write("REDIS_PASSWORD=" + redis_pass + "\n")
            f.close
        print("Installing Requirements.. This may Take a While")
        install("requirements.txt")
        subprocess.run(["wget", "https://git.io/JnZPE"], check=True)
        install("JnZPE")
        print(
            "If You want you use Youtube Video and Audio Downloader then FFMPEG is nesscary Please Google 'How to install ffmpeg on windows 10' if you dont want to use then You are good to go"
        )
        print("Installation of Ultroid Has Completed Successfully")
        ultstart = input("Do you want to start Ultroid now ? (y/n)")
        if ultstart == "y":
            os.execl(sys.executable, sys.executable, "-m", "pyUltroid")
        else:
            print("Ok No Problem.")
    else:
        print(
            "Please Enter Proper Distribution or Contact @UltroidSupport for installing on other distributions"
        )

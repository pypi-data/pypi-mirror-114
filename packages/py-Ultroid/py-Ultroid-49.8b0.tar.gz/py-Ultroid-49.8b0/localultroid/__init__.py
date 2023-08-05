import os
import subprocess
import sys


def git(*args):
    return subprocess.check_call(["git"] + list(args))


def install(package):
    return subprocess.check_call(
        [sys.executable, "-m", "pip3", "install", "-r", package]
    )


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
package_name = "ffmpeg"
subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)
print("Installation of Ultroid Has Completed Successfully")
if input("Do you want to start Ultroid now ? (y/n)") == y:
    os.execl(sys.executable, sys.executable, "-m", "pyUltroid")
else:
    print("Ok No Problem.")

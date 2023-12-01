import urllib
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import certifi
import ssl
import subprocess
import platform

# Program args
ANDROID_HOME = "."
SDK_TOOLS_VERSION = "10406996"
COMMAND_LINE_TOOLS_URL = ("https://dl.google.com/android/repository/commandlinetools-linux-"
                          + SDK_TOOLS_VERSION
                          + "_latest.zip")

# Unix SDK manager variable setup
SDK_MANAGER_PATH = ANDROID_HOME + "/cmdline-tools/bin/sdkmanager"
SDK_MANAGER_BASE_COMMAND = SDK_MANAGER_PATH + " --sdk_root=" + ANDROID_HOME

# Sdk Manager args
SDK_MAN_ARG_LIST = "--list"
SDK_MAN_ARG_LICENSES = "--licenses"
SDK_MAN_ARG_INSTALL = "--install"
SDK_MAN_ARG_INSTANT_APP = "'extras;google;instantapps'"

# Unix tasks
UNIX_CHMOD_STEP = "chmod +x " + SDK_MANAGER_PATH
SDK_MANAGER_LICENSE_AGREEMENT = "yes | " + SDK_MANAGER_BASE_COMMAND + " " + SDK_MAN_ARG_LICENSES
SDK_MAN_INSTALL_PLATFORM_TOOLS = SDK_MANAGER_BASE_COMMAND + " " + SDK_MAN_ARG_INSTALL + " " + "platform-tools"
SDK_MANAGER_INSTANT_APP_SETUP = SDK_MANAGER_BASE_COMMAND + " " + SDK_MAN_ARG_INSTANT_APP


def light_forge():
    print("Lighting Forge")
    tasks = build_task_list(build_command_list())
    download_and_unzip(COMMAND_LINE_TOOLS_URL, ANDROID_HOME)
    launch_tasks(tasks)


def download_and_unzip(url, extract_to='.'):
    http_response = urllib.request.Request(url)
    print("Zip File Download Started")
    with urllib.request.urlopen(http_response, context=ssl.create_default_context(cafile=certifi.where())) as response:
        zipfile = ZipFile(BytesIO(response.read()))
        print("Zip File Downloaded")
        zipfile.extractall(path=extract_to)
        print("Zip File Extracted")


def launch_tasks(tasks: [subprocess]):
    try:
        print("Starting " + str(len(tasks)) + " tasks")
        for task in tasks:
            print(task)
        print("All Tasks complete")
    except subprocess.CalledProcessError as e:
        print(f"Task Error: {e}")


def build_task_list(command_list: [str]):
    task_list = []
    for command in command_list:
        task = subprocess.run(
            command,
            shell=True,
            capture_output=False,
            text=True,
            check=True
        )
        task_list.append(task)
    return task_list


def build_command_list():
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        unix_commands = [
            UNIX_CHMOD_STEP,
            SDK_MANAGER_LICENSE_AGREEMENT,
            SDK_MAN_INSTALL_PLATFORM_TOOLS,
            SDK_MANAGER_INSTANT_APP_SETUP
        ]
        return unix_commands


if __name__ == '__main__':
    light_forge()

import urllib
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import constants as const
import certifi
import ssl
import subprocess
import platform


def download_cmd_tools(cmd_line_version: str, android_home: str):
    url = get_commandline_url(cmd_line_version)
    download_and_unzip(url, android_home)


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


def build_command_list(android_home: str):
    if is_unix():
        unix_commands = get_unix_setup_commands(android_home)
        return unix_commands


def get_unix_setup_commands(android_home: str):
    # Unix SDK manager variable setup
    SDK_MANAGER_PATH = android_home + "/cmdline-tools/bin/sdkmanager"
    SDK_MANAGER_BASE_COMMAND = SDK_MANAGER_PATH + " --sdk_root=" + android_home

    # Unix tasks
    UNIX_CHMOD_STEP = const.UNIX_CHMOD + " " + SDK_MANAGER_PATH
    SDK_MANAGER_LICENSE_AGREEMENT = const.YES_PIPE + " " + SDK_MANAGER_BASE_COMMAND + " " + const.SDK_MAN_ARG_LICENSES
    SDK_MAN_INSTALL_PLATFORM_TOOLS = SDK_MANAGER_BASE_COMMAND + " " + const.SDK_MAN_ARG_INSTALL + " " + const.PLATFORM_TOOLS
    SDK_MANAGER_INSTANT_APP_SETUP = SDK_MANAGER_BASE_COMMAND + " " + const.SDK_MAN_ARG_INSTANT_APP

    return [
        UNIX_CHMOD_STEP,
        SDK_MANAGER_LICENSE_AGREEMENT,
        SDK_MAN_INSTALL_PLATFORM_TOOLS,
        SDK_MANAGER_INSTANT_APP_SETUP
    ]


def get_commandline_url(cmdline_tools_version):
    commandline_url = ""

    if is_mac():
        commandline_url = (const.CMD_LINE_URL_BASE + const.MAC + "-"
                           f"{cmdline_tools_version}" + const.LATEST_ZIP)

    if is_linux():
        commandline_url = (const.CMD_LINE_URL_BASE + const.LINUX + "-"
                           f"{cmdline_tools_version}" + const.LATEST_ZIP)

    elif is_windows():
        commandline_url = (const.CMD_LINE_URL_BASE + const.WINDOWS + "-"
                           f"{cmdline_tools_version}" + const.LATEST_ZIP)
    return commandline_url


def is_mac():
    return platform.system().lower() == const.DARWIN


def is_linux():
    return platform.system().lower() == const.LINUX


def is_unix():
    return is_mac() or is_linux()


def is_windows():
    return platform.system().lower() == const.WINDOWS

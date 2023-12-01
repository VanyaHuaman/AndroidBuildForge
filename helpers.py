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
    with urllib.request.urlopen(
            http_response,
            context=ssl.create_default_context(cafile=certifi.where())
    ) as response:
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


def build_command_list(android_home: str, android_platform_tools_version: str, build_tools_version: str):
    if is_unix():
        unix_commands = get_unix_setup_commands(android_home, android_platform_tools_version, build_tools_version)
        return unix_commands


def get_unix_setup_commands(android_home: str, android_platform_tools_version: str, build_tools_version: str):
    # Unix SDK manager variable setup
    sdk_manager_path = android_home + const.UNIX_SDK_MAN_PATH_END
    sdk_manager_base_command = sdk_manager_path + const.SPACE + const.SDK_MAN_ARG_SDK_ROOT + android_home

    # Unix tasks
    unix_chmod_step = const.UNIX_CHMOD + const.SPACE + sdk_manager_path

    sdk_manager_build_tools = (sdk_manager_base_command +
                               const.SPACE +
                               f"'{const.BUILD_TOOLS}"
                               f"{build_tools_version}'")

    sdk_manager_license_agreement = (const.YES_PIPE +
                                     const.SPACE +
                                     sdk_manager_base_command +
                                     const.SPACE +
                                     const.SDK_MAN_ARG_LICENSES)
    sdk_man_install_platform_tools = (sdk_manager_base_command +
                                      const.SPACE +
                                      const.SDK_MAN_ARG_INSTALL +
                                      const.SPACE +
                                      const.PLATFORM_TOOLS)
    sdk_manager_plat_tool_android_version = (sdk_manager_base_command +
                                             const.SPACE +
                                             f"'{const.PLATFORM_TOOLS_ANDROID}{android_platform_tools_version}'")
    sdk_manager_instant_app_setup = (sdk_manager_base_command +
                                     const.SPACE +
                                     const.SDK_MAN_ARG_INSTANT_APP)

    return [
        unix_chmod_step,
        sdk_manager_build_tools,
        sdk_man_install_platform_tools,
        sdk_manager_plat_tool_android_version,
        sdk_manager_instant_app_setup,
        sdk_manager_license_agreement
    ]


def get_commandline_url(cmdline_tools_version):
    commandline_url = ""

    if is_mac():
        commandline_url = (const.CMD_LINE_URL_BASE + const.MAC + const.DASH +
                           f"{cmdline_tools_version}" + const.LATEST_ZIP)

    if is_linux():
        commandline_url = (const.CMD_LINE_URL_BASE + const.LINUX + const.DASH +
                           f"{cmdline_tools_version}" + const.LATEST_ZIP)

    elif is_windows():
        commandline_url = (const.CMD_LINE_URL_BASE + const.WINDOWS + const.DASH +
                           f"{cmdline_tools_version}" + const.LATEST_ZIP)
    return commandline_url


def generate_build_tool_version_string(build_tool_version: str):
    return build_tool_version + const.BUILD_TOOLS_ZEROS


def is_mac():
    return platform.system().lower() == const.DARWIN


def is_linux():
    return platform.system().lower() == const.LINUX


def is_unix():
    return is_mac() or is_linux()


def is_windows():
    return platform.system().lower() == const.WINDOWS

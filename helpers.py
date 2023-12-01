import os
import urllib
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import constants as const
import certifi
import ssl
import subprocess
import platform


def check_for_sdk_manager():
    if not is_sdk_manager_installed():
        download_cmd_tools(const.CMD_TOOLS_VERSION)


def download_cmd_tools(cmd_line_version: str):
    url = get_commandline_url(cmd_line_version)
    download_and_unzip(f"{const.COMMAND_LINE_TOOLS.title()} version:{cmd_line_version}", url, get_android_home())


def download_and_unzip(name: str, url: str, extract_to='.'):
    http_response = urllib.request.Request(url)
    print(f"{name} Download Started")
    with urllib.request.urlopen(
            http_response,
            context=ssl.create_default_context(cafile=certifi.where())
    ) as response:
        zipfile = ZipFile(BytesIO(response.read()))
        print(f"{name} Downloaded")
        zipfile.extractall(path=extract_to)
        print(f"{name} Extracted")


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
    if is_unix():
        unix_commands = get_unix_setup_commands()
        return unix_commands


def get_unix_setup_commands():
    command_list = []
    sdk_manager_path = get_sdk_manager_path()
    sdk_manager_base_command = sdk_manager_path + const.SPACE + const.SDK_MAN_ARG_SDK_ROOT + get_android_home()

    # Unix tasks
    if not is_sdkmanager_executable():
        unix_chmod_step = const.UNIX_CHMOD + const.SPACE + sdk_manager_path
        command_list.append(unix_chmod_step)

    if not is_build_tool_version_installed(const.INITIAL_BUILD_TOOL_VERSION):
        sdk_manager_build_tools = (const.YES_PIPE +
                                   const.SPACE +
                                   sdk_manager_base_command +
                                   const.SPACE +
                                   f"'{const.BUILD_TOOLS}"
                                   f"{const.INITIAL_BUILD_TOOL_VERSION}'")
        command_list.append(sdk_manager_build_tools)

    sdk_man_install_platform_tools = (sdk_manager_base_command +
                                      const.SPACE +
                                      const.SDK_MAN_ARG_INSTALL +
                                      const.SPACE +
                                      const.PLATFORM_TOOLS)
    command_list.append(sdk_man_install_platform_tools)

    sdk_manager_instant_app_setup = (sdk_manager_base_command +
                                     const.SPACE +
                                     const.SDK_MAN_ARG_INSTANT_APP)
    command_list.append(sdk_manager_instant_app_setup)

    sdk_manager_license_agreement = (const.YES_PIPE +
                                     const.SPACE +
                                     sdk_manager_base_command +
                                     const.SPACE +
                                     const.SDK_MAN_ARG_LICENSES)
    command_list.append(sdk_manager_license_agreement)

    return command_list


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


def is_android_home_set():
    return get_android_home() is not None


def is_build_tool_version_installed(version_code: str):
    build_tool_path = get_build_tool_path(version_code)
    return os.path.exists(build_tool_path)


def is_sdk_manager_installed():
    return os.path.isfile(get_sdk_manager_path())


def is_mac():
    return platform.system().lower() == const.DARWIN


def is_linux():
    return platform.system().lower() == const.LINUX


def is_unix():
    return is_mac() or is_linux()


def is_windows():
    return platform.system().lower() == const.WINDOWS


def get_android_home():
    return os.getenv(const.ANDROID_HOME)


def get_sdk_manager_path():
    if is_unix():
        return (f"{get_android_home()}"
                f"{const.UNIX_SDK_MAN_PATH_END}")


def get_build_tool_path(version_code: str):
    if is_unix():
        return f"{get_android_home()}{const.UNIX_BUILD_TOOLS_PATH_BASE}{version_code}"


def is_sdkmanager_executable():
    return os.access(get_sdk_manager_path(), os.X_OK)

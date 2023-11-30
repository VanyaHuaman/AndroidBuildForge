import urllib
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import certifi
import ssl
import subprocess


ANDROID_HOME = "."

SDK_TOOLS_VERSION = "10406996"
COMMAND_LINE_TOOLS_URL = ("https://dl.google.com/android/repository/commandlinetools-linux-"
                          + SDK_TOOLS_VERSION
                          + "_latest.zip")
SDK_MANAGER_LOCATION = ANDROID_HOME + "cmdline-tools/bin/sdkmanager"

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    download_and_unzip(COMMAND_LINE_TOOLS_URL, ANDROID_HOME)
    launchSdkManager()


def download_and_unzip(url, extract_to='.'):
    http_response = urllib.request.Request(url)
    print("Zip File Download Started")
    with urllib.request.urlopen(http_response, context=ssl.create_default_context(cafile=certifi.where())) as response:
        zipfile = ZipFile(BytesIO(response.read()))
        print("Zip File Downloaded")
        zipfile.extractall(path=extract_to)
        print("Zip File Extracted")

def launchSdkManager(buildVersion=""):
    result = subprocess.run([SDK_MANAGER_LOCATION, "--install platform-tools extras;google;instantapps"], shell=True, capture_output=True, text=True)
    print(result.stdout)
    print("Sdk Manager setup complete")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
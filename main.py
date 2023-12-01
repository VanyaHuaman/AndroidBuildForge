import os
import helpers

# Program args
ANDROID_HOME = os.getenv('ANDROID_HOME')
CMD_TOOLS_VERSION = "10406996"
INITIAL_BUILD_TOOL_VERSION = "34.0.0"


def light_forge():
    print("Lighting Forge")
    helpers.download_cmd_tools(CMD_TOOLS_VERSION, ANDROID_HOME)
    commands = helpers.build_command_list(ANDROID_HOME, INITIAL_BUILD_TOOL_VERSION)
    tasks = helpers.build_task_list(commands)
    helpers.launch_tasks(tasks)


if __name__ == '__main__':
    light_forge()

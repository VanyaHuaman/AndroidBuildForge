import helpers


def light_forge():
    print("Lighting Forge")
    helpers.check_for_sdk_manager()
    commands = helpers.build_command_list()
    tasks = helpers.build_task_list(commands)
    helpers.launch_tasks(tasks)


if __name__ == '__main__':
    if helpers.is_android_home_set():
        light_forge()
    else:
        print("ERROR: ANDROID_HOME ENV VAR IS NOT SET")

import forge_helpers as helpers


def light_forge():
    print("Lighting Forge")
    helpers.check_for_sdk_manager()
    commands = helpers.build_command_list()
    tasks = helpers.build_task_list(commands)
    helpers.accept_win_license()
    helpers.launch_tasks(tasks)


if __name__ == '__main__':
    if not helpers.is_java_home_set():
        print("ERROR: ANDROID_HOME ENV VAR IS NOT SET")
    elif not helpers.is_android_home_set():
        print("ERROR: ANDROID_HOME ENV VAR IS NOT SET")
    else:
        light_forge()

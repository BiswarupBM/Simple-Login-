def list_all_commands(group):
    all = [group]
    for name in group.list_commands(None):
        command = group.get_command(None, name)
        try:
            subcommands = list_all_commands(command)
            all.extend(subcommands)
        except AttributeError:
            all.append(command)
    return all

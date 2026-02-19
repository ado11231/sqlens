from cli import CLI
import shlex

cli = CLI()

commands = {
    "load": cli.load,
    "query": cli.query,
    "tables": cli.tables,
    "drop": cli.drop,
    "reset": cli.reset,
    "files": cli.files,
    "add": cli.add,
    "remove": cli.remove
}


print("Welcome to SQLen!")
print("List of Commands")
print("Commands: add | remove | load | query | drop | files | tables | exit")

while True:
    user_input = input("> ")

    parts = shlex.split(user_input)
    if not parts:
        continue

    command = parts[0].lower()
    args = parts[1:]

    if command == "exit":
        print("Goodbye")
        break
    elif command == "query":
        print("Enter Query Mode. Type 'back' to return ")
        cli.tables()
        while True:
            sql = input("SQL> ")
            if sql.lower() == "back":
                break
            cli.query(sql)
    elif command in commands:
        try:
            commands[command](*args)
        except TypeError:
            print(f"{command} requires arguements")
        except Exception as e:
            print(f"Error: {e}")
    else:
        try:
            cli.query(user_input)
        except Exception as e:
            print(f"Error: {e}")








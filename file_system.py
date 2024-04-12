from directory import Directory
from file import File
class FileSystem:
    def __init__(self):
        self.root = Directory("/")
        self.current_directory = self.root

    def mkdir(self, path):
        parts = self.split_path(path)
        if not parts:
            print("Usage: mkdir <directory_path>")
            return
        
        dir_name = parts[-1]
        parent_dir = self.get_directory(parts[:-1])

        if not parent_dir:
            print(f"Directory '{path}' not found")
            return

        if dir_name in parent_dir.children:
            print(f"Directory '{dir_name}' already exists")
            return
        
        new_dir = Directory(dir_name, parent_dir)
        parent_dir.add_child(new_dir)

    def cd(self, path):
        if not path:
            print("Usage: cd <directory_path>")
            return

        if path == "/":
            self.current_directory = self.root
            return

        if path == "..":
            if self.current_directory == self.root:
                print("Already at the root directory")
            else:
                self.current_directory = self.current_directory.get_parent()
            return

        parts = self.split_path(path)
        target_dir = self.get_directory(parts)

        if not target_dir:
            print(f"Directory '{path}' not found")
            return

        self.current_directory = target_dir

    def ls(self, path="."):
        if path == ".":
            target_dir = self.current_directory
        else:
            parts = self.split_path(path)
            target_dir = self.get_directory(parts)

        if not target_dir:
            print(f"Directory '{path}' not found")
            return

        if not target_dir.children:
            print("(empty)")
        else:
            for name in target_dir.children:
                print(name)

    def touch(self, path):
        parts = self.split_path(path)
        if not parts:
            print("Usage: touch <file_path>")
            return
        
        file_name = parts[-1]
        parent_dir = self.get_directory(parts[:-1])

        if not parent_dir:
            print(f"Directory '{path}' not found")
            return

        if file_name in parent_dir.children:
            print(f"File '{file_name}' already exists")
            return
        
        parent_dir.add_child(File(file_name))

    def echo(self, args):
        if len(args) < 3 or args[-2] != ">":
            print("Usage: echo <text> > <file_name>")
            return

        text = " ".join(args[:-2])
        file_name = args[-1]

        if file_name not in self.current_directory.children:
            print(f"File '{file_name}' not found")
            return

        quoted_text = " ".join(args[:-2])
        self.current_directory.children[file_name].content = quoted_text.strip('"')

    def cat(self, path):
        parts = self.split_path(path)
        if not parts:
            print("Usage: cat <file_path>")
            return
            
        file_name = parts[-1]
        parent_dir = self.get_directory(parts[:-1])

        if not parent_dir:
            print(f"Directory '{path}' not found")
            return

        if file_name not in parent_dir.children:
            print(f"File '{file_name}' not found")
            return

        file_content = parent_dir.children[file_name].content
        print(file_content)

    def mv(self, src, dest):
        src_parts = self.split_path(src)
        dest_parts = self.split_path(dest)

        src_dir = self.get_directory(src_parts[:-1])
        dest_dir = self.get_directory(dest_parts[:-1])

        if not src_dir or not dest_dir:
            print("Invalid source or destination path")
            return
        
        file_name = src_parts[-1]

        if file_name not in src_dir.children:
            print(f"File '{file_name}' not found")
            return
        
        dest_dir.add_child(src_dir.children[file_name])
        src_dir.remove_child(file_name)

    def cp(self, src, dest):
        src_parts = self.split_path(src)
        dest_parts = self.split_path(dest)

        src_dir = self.get_directory(src_parts[:-1])
        dest_dir = self.get_directory(dest_parts[:-1])

        if not src_dir or not dest_dir:
            print("Invalid source or destination path")
            return
        
        file_name = src_parts[-1]

        if file_name not in src_dir.children:
            print(f"File '{file_name}' not found")
            return
        
        dest_dir.add_child(File(file_name, src_dir.children[file_name].content))

    def rm(self, path):
        parts = self.split_path(path)
        if not parts:
            print("Usage: rm <file_or_directory_path>")
            return
        
        item_name = parts[-1]
        parent_dir = self.get_directory(parts[:-1])

        if not parent_dir:
            print(f"Directory '{path}' not found")
            return

        if item_name not in parent_dir.children:
            print(f"File or directory '{item_name}' not found")
            return
        
        parent_dir.remove_child(item_name)

    def split_path(self, path):
        if not path:
            return []
        
        if path == "/":
            return []

        parts = path.strip("/").split("/")
        if path.startswith("/"):
            return parts
        else:
            return self.current_directory.name.split("/") + parts

    def get_directory(self, parts):
        current_dir = self.root

        for part in parts:
            if part == "":
                continue
            elif part == "..":
                if current_dir == self.root:
                    continue
                current_dir = current_dir.get_parent()
            elif part in current_dir.children:
                current_dir = current_dir.children[part]
            else:
                return None
        
        return current_dir

    def run_interactive_shell(self):
        while True:
            command = input(f"{self.current_directory.name}> ").strip()
            if command.lower() == "exit":
                print("Exiting...")
                break
            self.execute_command(command)

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return
        
        command_name = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        if command_name == "mkdir":
            self.mkdir(*args)
        elif command_name == "cd":
            self.cd(*args)
        elif command_name == "ls":
            self.ls(*args)
        elif command_name == "touch":
            self.touch(*args)
        elif command_name == "echo":
            self.echo(args)
        elif command_name == "cat":
            self.cat(*args)
        elif command_name == "mv":
            if len(args) < 2:
                print("Usage: mv <source_path> <destination_path>")
                return
            src_path, dest_path = args
            self.mv(src_path, dest_path)
        elif command_name == "cp":
            if len(args) < 2:
                print("Usage: cp <source_path> <destination_path>")
                return
            src_path, dest_path = args
            self.cp(src_path, dest_path)
        elif command_name == "rm":
            self.rm(*args)
        else:
            print(f"Unrecognized command: {command_name}")
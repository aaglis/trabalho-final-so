import time
import random
import matplotlib.pyplot as plt

BLOCK_SIZE = 512

class Block:
    def _init_(self, data=''):
        self.data = data
        self.next = None

class File:
    def _init_(self, name):
        self.name = name
        self.size = 0
        self.first_block = None

class Directory:
    def _init_(self, name):
        self.name = name
        self.children = {}

root = Directory('/')
current_dir = root

def find_directory(path):
    parts = path.strip('/').split('/')
    dir_ptr = root
    for part in parts:
        if part and part in dir_ptr.children and isinstance(dir_ptr.children[part], Directory):
            dir_ptr = dir_ptr.children[part]
        else:
            return None
    return dir_ptr

def mkdir(name):
    if name not in current_dir.children:
        current_dir.children[name] = Directory(name)

def touch(name):
    if name not in current_dir.children:
        current_dir.children[name] = File(name)

def ls():
    print(" ".join(current_dir.children.keys()))

def cd(name):
    global current_dir
    if name == '..':
        current_dir = root
    elif name in current_dir.children and isinstance(current_dir.children[name], Directory):
        current_dir = current_dir.children[name]

def write(filename, content):
    if filename not in current_dir.children:
        return
    f = current_dir.children[filename]
    f.size = len(content)
    blocks = []
    for i in range(0, len(content), BLOCK_SIZE):
        block = Block(content[i:i+BLOCK_SIZE])
        blocks.append(block)
    for i in range(len(blocks)-1):
        blocks[i].next = blocks[i+1]
    f.first_block = blocks[0] if blocks else None

def cat(filename):
    if filename not in current_dir.children:
        return
    f = current_dir.children[filename]
    ptr = f.first_block
    content = ''
    while ptr:
        content += ptr.data
        ptr = ptr.next
    return content

def mv(filename, target_path):
    if filename not in current_dir.children:
        return
    target_dir = find_directory(target_path)
    if not target_dir:
        return
    target_dir.children[filename] = current_dir.children.pop(filename)

def rm(name):
    if name in current_dir.children:
        del current_dir.children[name]

def stat(name):
    if name not in current_dir.children:
        return
    item = current_dir.children[name]
    if isinstance(item, File):
        blocks = []
        ptr = item.first_block
        while ptr:
            blocks.append(ptr)
            ptr = ptr.next
        print(f"Arquivo: {name}")
        print(f"Tamanho: {item.size} bytes")
        print(f"Blocos usados: {len(blocks)}")
        print(f"Encadeamento: {' -> '.join(str(id(b))[-4:] for b in blocks)}")
    elif isinstance(item, Directory):
        print(f"Diretório: {name} (contém {len(item.children)} itens)")

# Prompt interativo

def prompt():
    global current_dir
    while True:
        cmd = input("$ ").strip()
        if cmd == "exit":
            break
        elif cmd.startswith("mkdir "):
            mkdir(cmd[6:])
        elif cmd.startswith("touch "):
            touch(cmd[6:])
        elif cmd == "ls":
            ls()
        elif cmd.startswith("cd "):
            cd(cmd[3:])
        elif cmd.startswith("write "):
            parts = cmd[6:].split(" ", 1)
            if len(parts) == 2:
                write(parts[0], parts[1].strip('"'))
        elif cmd.startswith("cat "):
            content = cat(cmd[4:])
            if content:
                print(content)
        elif cmd.startswith("mv "):
            parts = cmd[3:].split(" ")
            if len(parts) == 2:
                mv(parts[0], parts[1])
        elif cmd.startswith("rm "):
            rm(cmd[3:])
        elif cmd.startswith("stat "):
            stat(cmd[5:])
        elif cmd == "help":
            print("mkdir <nome>, touch <nome>, ls, cd <nome>/.., write <arquivo> \"conteudo\", cat <arquivo>, mv <arquivo> <dir>, rm <nome>, stat <nome>, exit")
        else:
            print("Comando inválido. Digite 'help' para ajuda.")

if _name_ == "_main_":
    prompt()

from filesystem.path_utils import resolve_path
from filesystem.symlink_utils import resolve_symlink
from filesystem.inode import Inode
import shlex

def ln(shell, args):
    parts = shlex.split(args)
    if not parts or len(parts) < 2:
        print("Uso: ln [-s] <alvo> <link>")
        return
    if parts[0] == "-s":
        if len(parts) != 3:
            print("Uso: ln -s <alvo> <link>")
            return
        target_path, link_name = parts[1], parts[2]
        if link_name in shell.cwd.children:
            print("Já existe um arquivo ou diretório com esse nome.")
            return
        shell.cwd.children[link_name] = Inode(link_name, False, True, target_path)
        print(f"Link simbólico '{link_name}' criado, apontando para '{target_path}'")
    else:
        if len(parts) != 2:
            print("Uso: ln <alvo> <link>")
            return
        target_name, link_name = parts
        if link_name in shell.cwd.children:
            print("Já existe um arquivo ou diretório com esse nome.")
            return
        target_inode = resolve_path(shell, target_name, True)
        if not target_inode or target_inode.is_directory or target_inode.is_symlink:
            print("Não é possível criar hard link para esse tipo.")
            return
        shell.cwd.children[link_name] = target_inode
        target_inode.link_count += 1
        print(f"Hard link '{link_name}' criado (total de links: {target_inode.link_count})")


from filesystem.inode import Inode
from filesystem.path_utils import resolve_path
from filesystem.symlink_utils import resolve_symlink

def mkdir(shell, name):
    if not name:
        print("Uso: mkdir <nome>")
        return
    if name in shell.cwd.children:
        print("Já existe um arquivo ou diretório com esse nome.")
    else:
        shell.cwd.children[name] = Inode(name, True)

def ls(shell, show_inode=False):
    for name, inode in sorted(shell.cwd.children.items()):
        tipo = "📁" if inode.is_directory else ("🔗" if inode.is_symlink else "📄")
        inode_str = f"[inode: {inode.id}] " if show_inode else ""
        if inode.is_symlink:
            target = resolve_symlink(inode, shell)
            status = " (quebrado)" if not target else f" -> {inode.symlink_target}"
        else:
            status = ""
        print(f"{inode_str}{tipo} {name}{status}")

def cd(shell, name):
    if not name:
        shell.cwd = shell.root
        shell.path = [shell.root]
        shell._update_prompt()
        return

    name = name.strip()

    if name == "..":
        if len(shell.path) > 1:
            shell.path.pop()
            shell.cwd = shell.path[-1]
            shell._update_prompt()
        return

    inode = resolve_path(shell, name)
    if not inode:
        print("Diretório não encontrado.")
        return
    if not inode.is_directory:
        print("Não é um diretório.")
        return

    if name.startswith("/"):
        components = name.split("/")[1:]
        shell.path = [shell.root]
        current = shell.root
        for comp in components:
            if comp in current.children:
                current = current.children[comp]
                if current.is_symlink:
                    current = resolve_symlink(current, shell)
                    if not current:
                        print("Link simbólico quebrado.")
                        return
                shell.path.append(current)
        shell.cwd = shell.path[-1]
    else:
        shell.cwd = inode
        shell.path.append(shell.cwd)

    shell._update_prompt()

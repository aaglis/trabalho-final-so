
import shlex
from filesystem.path_utils import resolve_path
from filesystem.symlink_utils import resolve_symlink
import os

def touch(shell, name):
    if not name:
        print("Uso: touch <nome>")
        return
    if name in shell.cwd.children:
        print("Já existe um arquivo ou diretório com esse nome.")
    else:
        from filesystem.inode import Inode
        shell.cwd.children[name] = Inode(name, False)

def write(shell, args):
    parts = shlex.split(args)
    if len(parts) < 2:
        print("Uso: write <arquivo> \"conteúdo\"")
        return
    name, content = parts[0], parts[1]
    inode = resolve_path(shell, name, follow_symlinks=False)
    if not inode:
        print("Arquivo não encontrado.")
        return
    if inode.is_symlink:
        inode = resolve_symlink(inode, shell)
        if not inode:
            print("Link simbólico quebrado - não é possível escrever.")
            return
    if inode.is_directory:
        print("Não é possível escrever em um diretório.")
        return
    inode.data_blocks = [content[i:i+4] for i in range(0, len(content), 4)]
    inode.size = len(content)

def cat(shell, name):
    if not name:
        print("Uso: cat <arquivo>")
        return
    inode = resolve_path(shell, name, follow_symlinks=False)
    if not inode:
        print("Arquivo não encontrado.")
        return
    if inode.is_symlink:
        inode = resolve_symlink(inode, shell)
        if not inode:
            print("Link simbólico quebrado - não é possível ler.")
            return
    if inode.is_directory:
        print("Não é possível ler um diretório.")
        return
    print("".join(inode.data_blocks))

def rm(shell, name):
    name = name.strip()
    if name not in shell.cwd.children:
        print("Arquivo ou diretório não encontrado.")
        return

    inode = shell.cwd.children[name]

    if inode.is_symlink:
        del shell.cwd.children[name]
        print(f"Link simbólico '{name}' removido.")
    else:
        inode.link_count -= 1
        del shell.cwd.children[name]

        if inode.link_count <= 0:
            print(f"Inode '{name}' removido completamente (sem mais links).")
        else:
            print(f"Link '{name}' removido, inode ainda tem {inode.link_count} link(s).")

def mv(shell, args):
    parts = shlex.split(args)
    if len(parts) != 2:
        print("Uso: mv <origem> <destino>")
        return

    source_path, target_path = parts

    source_inode = resolve_path(shell, source_path, follow_symlinks=False)
    if not source_inode:
        print("Arquivo de origem não encontrado.")
        return

    # Diretório onde está o arquivo de origem
    source_dir_path = os.path.dirname(source_path) or "."
    source_dir = resolve_path(shell, source_dir_path, follow_symlinks=True)
    source_name = os.path.basename(source_path)

    if source_name not in source_dir.children:
        print("Arquivo de origem não encontrado no diretório pai.")
        return

    # Verifica se destino é um diretório
    target_inode = resolve_path(shell, target_path, follow_symlinks=True)
    if target_inode and target_inode.is_directory:
        new_name = source_name
        target_dir = target_inode
    else:
        target_dir_path = os.path.dirname(target_path) or "."
        new_name = os.path.basename(target_path)
        target_dir = resolve_path(shell, target_dir_path, follow_symlinks=True)
        if not target_dir or not target_dir.is_directory:
            print("Diretório de destino inválido.")
            return

    if new_name in target_dir.children:
        print("Já existe um arquivo ou diretório com esse nome no destino.")
        return

    # Mover: remove do diretório de origem, adiciona ao destino
    inode_to_move = source_dir.children.pop(source_name)
    target_dir.children[new_name] = inode_to_move

def stat(shell, name):
    if not name:
        print("Uso: stat <arquivo>")
        return

    inode = resolve_path(shell, name, follow_symlinks=False)
    if not inode:
        print("Arquivo ou diretório não encontrado.")
        return

    real_inode = resolve_symlink(inode, shell) if inode.is_symlink else inode

    print(f"Inode: {inode.id}")
    print(f"Nome: {inode.name}")
    print(f"Tipo: {'Link simbólico' if inode.is_symlink else ('Diretório' if real_inode.is_directory else 'Arquivo')}")
    if inode.is_symlink:
        print(f"Aponta para: {inode.symlink_target}")
        print(f"Status do link: {'quebrado' if not real_inode else 'válido'}")
    print(f"Tamanho: {real_inode.size} bytes")
    print(f"Links: {real_inode.link_count}")
    if not real_inode.is_directory:
        print(f"Blocos de dados: {real_inode.data_blocks}")
    else:
        print(f"Contém {len(real_inode.children)} itens")


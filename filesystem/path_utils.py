
def resolve_path(shell, path, follow_symlinks=True):
    if not path:
        return None
    if path == ".":
        return shell.cwd
    if path == "..":
        return shell.path[-2] if len(shell.path) > 1 else shell.root

    if path.startswith("/"):
        components = path.split("/")[1:]
        current = shell.root
    else:
        components = path.split("/")
        current = shell.cwd

    for comp in components:
        if not comp or comp == ".":
            continue
        if comp == "..":
            current = shell.path[-2] if len(shell.path) > 1 else shell.root
            continue
        if comp in current.children:
            inode = current.children[comp]
            if inode.is_symlink and follow_symlinks:
                from .symlink_utils import resolve_symlink
                resolved = resolve_symlink(inode, shell)
                if not resolved:
                    return None
                current = resolved
            else:
                current = inode
        else:
            return None
        if not current.is_directory and comp != components[-1]:
            return None
    return current

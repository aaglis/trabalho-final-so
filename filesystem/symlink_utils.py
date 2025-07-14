
def resolve_symlink(inode, shell, follow=True):
    if not inode or not inode.is_symlink or not follow:
        return inode

    target_path = inode.symlink_target
    return shell.resolve_path(target_path, follow_symlinks=True)

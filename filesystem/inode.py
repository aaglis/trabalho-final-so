
import uuid

class Inode:
    def __init__(self, name, is_directory, is_symlink=False, symlink_target=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.is_directory = is_directory
        self.is_symlink = is_symlink
        self.symlink_target = symlink_target
        self.size = 0
        self.data_blocks = []
        self.children = {} if is_directory else None
        self.link_count = 1 if not is_symlink else 0

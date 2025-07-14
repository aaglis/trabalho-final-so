
import cmd
from filesystem.inode import Inode
from filesystem.commands import file_ops, dir_ops, link_ops
from filesystem.path_utils import resolve_path

class FileSystemShell(cmd.Cmd):
    intro = "Bem-vindo ao simulador de sistema de arquivos com i-nodes! Digite 'help' para ajuda."
    prompt = "/ > "

    def __init__(self):
        super().__init__()
        self.root = Inode("/", True)
        self.cwd = self.root
        self.path = [self.root]

    def resolve_path(self, path, follow_symlinks=True):
        from filesystem.path_utils import resolve_path
        return resolve_path(self, path, follow_symlinks)

    def _update_prompt(self):
        self.prompt = "/" + "/".join(inode.name for inode in self.path[1:]) + " > "

    def do_ls(self, arg):
        dir_ops.ls(self, show_inode=(arg.strip() == "-i"))

    def do_mkdir(self, arg):
        dir_ops.mkdir(self, arg.strip())

    def do_touch(self, arg):
        file_ops.touch(self, arg.strip())

    def do_write(self, arg):
        file_ops.write(self, arg)

    def do_cat(self, arg):
        file_ops.cat(self, arg.strip())

    def do_ln(self, arg):
        link_ops.ln(self, arg)

    def do_rm(self, arg):
        file_ops.rm(self, arg.strip())

    def do_mv(self, arg):
        file_ops.mv(self, arg)

    def do_cd(self, arg):
        dir_ops.cd(self, arg.strip())

    def do_stat(self, arg):
        file_ops.stat(self, arg.strip())

    def do_metrics(self, arg):
        from filesystem.metrics import gerar_metricas
        gerar_metricas(self)

    def do_benchmark(self, arg):
        from filesystem.benchmark import benchmark
        benchmark(self)

    def do_exit(self, arg):
        print("Saindo do sistema de arquivos.")
        return True

    def emptyline(self):
        pass

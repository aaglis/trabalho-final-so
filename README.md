
# Simulador de Sistema de Arquivos com i-nodes

Este é um simulador interativo de sistema de arquivos baseado em i-nodes, com comandos semelhantes aos do terminal Linux.

## Comandos disponíveis

- `mkdir <nome>`: cria um diretório
- `touch <nome>`: cria um arquivo vazio
- `ls`: lista o conteúdo do diretório atual
- `cd <nome>` / `cd ..`: navega entre diretórios
- `write <arquivo> "conteúdo"`: escreve conteúdo no arquivo
- `cat <arquivo>`: mostra o conteúdo do arquivo
- `mv <arquivo> <diretório>`: move um arquivo para um diretório
- `rm <nome>`: remove um arquivo ou diretório
- `stat <nome>`: exibe informações do inode do item
- `debug`: mostra a árvore inteira de inodes
- `exit`: encerra o simulador

## Execução

```bash
python3 file_system_shell.py
```

## Exemplo de uso

```bash
mkdir docs
cd docs
touch exemplo.txt
write exemplo.txt "ola mundo"
cat exemplo.txt
stat exemplo.txt
cd ..
debug
exit
```

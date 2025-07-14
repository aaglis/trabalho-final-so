# filesystem/metrics.py
import matplotlib.pyplot as plt

def _coletar_inodes(inode, dados):
    if inode.is_directory:
        dados['diretorios'] += 1
        for filho in inode.children.values():
            _coletar_inodes(filho, dados)
    elif inode.is_symlink:
        dados['symlinks'] += 1
        dados['tamanhos_symlinks'].append(len(inode.symlink_target or ""))
    else:
        dados['arquivos'] += 1
        dados['tamanhos_arquivos'].append(inode.size)
        dados['nomes_arquivos'].append(inode.name)
        dados['blocos'].append(len(inode.data_blocks))

def gerar_metricas(shell):
    dados = {
        'diretorios': 0,
        'arquivos': 0,
        'symlinks': 0,
        'tamanhos_arquivos': [],
        'tamanhos_symlinks': [],
        'nomes_arquivos': [],
        'blocos': []
    }
    _coletar_inodes(shell.root, dados)

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # Gráfico 1: contagem por tipo
    axs[0].bar(['Arquivos', 'Diretórios', 'Symlinks'],
               [dados['arquivos'], dados['diretorios'], dados['symlinks']],
               color=['skyblue', 'lightgreen', 'orange'])
    axs[0].set_title("Contagem de Inodes por Tipo")

    # Gráfico 2: distribuição de tamanhos
    axs[1].hist(dados['tamanhos_arquivos'], bins=10, color='blue', alpha=0.7)
    axs[1].set_title("Distribuição de Tamanhos de Arquivos")
    axs[1].set_xlabel("Tamanho (bytes)")
    axs[1].set_ylabel("Frequência")

    # Gráfico 3: top N arquivos por tamanho
    top_n = sorted(zip(dados['nomes_arquivos'], dados['tamanhos_arquivos']),
                   key=lambda x: x[1], reverse=True)[:5]
    if top_n:
        nomes, tamanhos = zip(*top_n)
        axs[2].bar(nomes, tamanhos, color='purple')
        axs[2].set_title("Top 5 Maiores Arquivos")
        axs[2].set_ylabel("Tamanho (bytes)")
        axs[2].tick_params(axis='x', rotation=45)
    else:
        axs[2].set_title("Sem arquivos para mostrar")

    plt.tight_layout()
    plt.savefig("metricas.png")
    print("Gráfico salvo como 'metricas.png'")

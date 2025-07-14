# filesystem/benchmark.py
import time
import matplotlib.pyplot as plt
from filesystem.inode import Inode

def medir_tempo(func, *args):
    inicio = time.perf_counter()
    func(*args)
    fim = time.perf_counter()
    return fim - inicio

def benchmark(shell):
    resultados = {
        'create': [],
        'write': [],
        'read': [],
        'delete': []
    }

    from filesystem.commands import file_ops

    for i in range(10):
        filename = f"teste_{i}.txt"

        # Medir criação
        tempo_create = medir_tempo(file_ops.touch, shell, filename)
        resultados['create'].append(tempo_create)

        # Medir escrita
        tempo_write = medir_tempo(file_ops.write, shell, f"{filename} \"{'x'*1000}\"")
        resultados['write'].append(tempo_write)

        # Medir leitura
        tempo_read = medir_tempo(file_ops.cat, shell, filename)
        resultados['read'].append(tempo_read)

        # Medir deleção
        tempo_rm = medir_tempo(file_ops.rm, shell, filename)
        resultados['delete'].append(tempo_rm)

    # Mostrar gráfico
    labels = list(resultados.keys())
    valores = [sum(resultados[chave])/len(resultados[chave]) for chave in labels]

    plt.bar(labels, valores, color=["blue", "green", "orange", "red"])
    plt.title("Tempo médio por operação (em segundos)")
    plt.ylabel("Tempo médio (s)")
    plt.savefig("benchmark.png")
    print("📈 Benchmark final salvo como 'benchmark.png'")

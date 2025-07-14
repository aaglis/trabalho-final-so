import time
import matplotlib.pyplot as plt
from filesystem.commands import file_ops
from filesystem.commands import dir_ops

def medir_tempo(func, *args):
    inicio = time.perf_counter()
    func(*args)
    fim = time.perf_counter()
    return fim - inicio

def benchmark(shell):
    resultados = {
        'create': [],
        'write': [],
        'mv': [],
        'read': [],
        'delete': []
    }

    # Criar diretório de destino para mv
    if "destino" not in shell.cwd.children:
        dir_ops.mkdir(shell, "destino")

    for i in range(10):
        nome = f"arquivo_{i}.txt"
        destino = f"destino/{nome}"

        # 1. Criação
        tempo = medir_tempo(file_ops.touch, shell, nome)
        resultados['create'].append(tempo)

        # 2. Escrita
        tempo = medir_tempo(file_ops.write, shell, f'{nome} "dados-{i*1000}"')
        resultados['write'].append(tempo)

        # 3. Move para /destino
        tempo = medir_tempo(file_ops.mv, shell, f"{nome} {destino}")
        resultados['mv'].append(tempo)

        # 4. Leitura (no destino)
        tempo = medir_tempo(file_ops.cat, shell, f"{destino}")
        resultados['read'].append(tempo)

        # 5. Deleção (no destino)
        tempo = medir_tempo(file_ops.rm, shell, nome if nome in shell.cwd.children else destino.split("/")[-1])
        resultados['delete'].append(tempo)

    # Gráfico: tempo médio por operação
    labels = list(resultados.keys())
    tempos_medios = [sum(resultados[k]) / len(resultados[k]) for k in labels]

    plt.bar(labels, tempos_medios, color=['blue', 'green', 'orange', 'purple', 'red'])
    plt.title("⏱️ Tempo médio por operação")
    plt.ylabel("Tempo (segundos)")
    plt.savefig("benchmark.png")
    print("📈 Benchmark completo salvo como 'benchmark.png'")

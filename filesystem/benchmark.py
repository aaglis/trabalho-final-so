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

    if "destino" not in shell.cwd.children:
        dir_ops.mkdir(shell, "destino")

    for i in range(10):
        nome = f"arquivo_{i}.txt"
        destino = f"destino/{nome}"

        tempo = medir_tempo(file_ops.touch, shell, nome)
        resultados['create'].append(tempo)

        tempo = medir_tempo(file_ops.write, shell, f'{nome} "dados-{i*1000}"')

        tempo = medir_tempo(file_ops.mv, shell, f"{nome} {destino}")
        resultados['mv'].append(tempo)

        tempo = medir_tempo(file_ops.cat, shell, f"{destino}")
        resultados['read'].append(tempo)

        tempo = medir_tempo(file_ops.rm, shell, nome if nome in shell.cwd.children else destino.split("/")[-1])
        resultados['delete'].append(tempo)

    labels = list(resultados.keys())
    tempos_medios = [sum(resultados[k]) / len(resultados[k]) for k in labels]

    plt.bar(labels, tempos_medios, color=['blue', 'green', 'orange', 'purple', 'red'])
    plt.title("⏱️ Tempo médio por operação")
    plt.ylabel("Tempo (segundos)")
    plt.savefig("benchmark.png")
    print("📈 Benchmark completo salvo como 'benchmark.png'")

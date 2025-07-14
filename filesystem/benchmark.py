import time
import matplotlib.pyplot as plt
from filesystem.commands import file_ops, dir_ops

def medir_tempo(func, *args):
    try:
        inicio = time.perf_counter()
        func(*args)
        fim = time.perf_counter()
        return fim - inicio
    except Exception as e:
        print(f"Erro em {func.__name__}: {e}")
        return None

def benchmark(shell):
    resultados = {}

    nome = "realista.txt"
    conteudo = "x" * 1_000  # 1MB 1_000_000

    resultados['create'] = medir_tempo(file_ops.touch, shell, nome)
    resultados['write'] = medir_tempo(file_ops.write, shell, f'{nome} "{conteudo}"')

    if "destino" not in shell.cwd.children:
        dir_ops.mkdir(shell, "destino")
    resultados['mv_superficial'] = medir_tempo(file_ops.mv, shell, f"{nome} destino/{nome}")

    shell.do_cd("/")
    caminho = []
    for letra in "abcdefghij":
        caminho.append(letra)
        if letra not in shell.cwd.children:
            dir_ops.mkdir(shell, letra)
        shell.do_cd(letra)

    caminho_profundo = "/".join(caminho)
    resultados['mv_profundo'] = medir_tempo(file_ops.mv, shell, f"/destino/{nome} {caminho_profundo}/{nome}")

    resultados['read'] = medir_tempo(file_ops.cat, shell, f"{caminho_profundo}/{nome}")

    labels = list(resultados.keys())
    tempos = [resultados[k] for k in labels]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, tempos, color=['blue', 'green', 'orange', 'cyan', 'purple', 'red'])
    plt.title("⏱️ Benchmark realista (usando i-nodes)")
    plt.ylabel("Tempo (segundos)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("benchmark_realista.png")
    print("📊 Benchmark realista salvo como 'benchmark_realista.png'")

    for k, v in resultados.items():
        print(f"{k:>15}: {v:.6f} segundos")

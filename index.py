import pandas as pd
import random
from functools import cmp_to_key

# Comparator para ordenar arestas por peso (terceiro elemento da sublista)
def comparator(a, b):
    return a[2] - b[2]

# Estrutura de Dados Disjoint Set Union (DSU)
class DSU:
    def __init__(self, n):
        # Array pai para nós de 0 a n-1
        self.parent = list(range(n))
        self.rank = [1] * n # Usado para otimização de união por rank

    def find(self, i):
        # Encontra o representante (raiz) do conjunto ao qual i pertence
        # com compressão de caminho
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, x, y):
        # Une os conjuntos que contêm x e y
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x != root_y: # Só une se estiverem em conjuntos diferentes
            # União por rank para manter a árvore DSU mais plana
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            return True # União realizada
        return False # Já estavam no mesmo conjunto

# Algoritmo de Kruskal para encontrar a MST
def kruskals_mst(num_total_vertices, edge_list):
    # Ordena todas as arestas pelo peso em ordem crescente
    # Usar sorted() cria uma nova lista ordenada, não modifica a original no lugar.
    # A chave de ordenação lambda item: item[2] é mais idiomática em Python 3
    # do que cmp_to_key para simples ordenação por um elemento.
    # Mas cmp_to_key com seu 'comparator' funciona bem.
    sorted_edge_list = sorted(edge_list, key=cmp_to_key(comparator))
    
    # Inicializa DSU para o número total de vértices (espera-se que os IDs dos nós
    # em edge_list já estejam remapeados para 0 até num_total_vertices-1)
    dsu = DSU(num_total_vertices)
    
    mst_cost = 0
    mst_edge_count = 0
    
    for node1, node2, weight in sorted_edge_list:
        # node1 e node2 devem ser IDs de nós remapeados (0 a num_total_vertices-1)
        if dsu.find(node1) != dsu.find(node2): # Se não formam ciclo
            dsu.union(node1, node2)
            mst_cost += weight
            mst_edge_count += 1
            # A MST terá num_total_vertices - 1 arestas se o grafo for conectado
            if mst_edge_count == num_total_vertices - 1:
                break # MST completa encontrada
    
    # Verificação caso o grafo não seja conectado ou num_total_vertices esteja incorreto
    if mst_edge_count < num_total_vertices - 1 and num_total_vertices > 0:
        print(f"Aviso: A MST encontrou apenas {mst_edge_count} arestas, mas esperava {num_total_vertices - 1} para {num_total_vertices} vértices.")
        print("Isso pode indicar que o grafo não é conectado ou o número de vértices está impreciso.")
        
    return mst_cost

# --- Script Principal ---

# 1. Lendo os dados do arquivo
try:
    # Assume que dados.csv tem colunas separadas por espaço e sem cabeçalho.
    # As colunas representam: node_origem node_destino
    data_df = pd.read_csv("dados.csv", sep=" ", header=None)
    data_df.columns = ["node1_orig", "node2_orig"] # Nomes para as colunas
except FileNotFoundError:
    print("Erro: O arquivo 'dados.csv' não foi encontrado. Verifique o caminho.")
    exit()
except Exception as e:
    print(f"Erro ao ler 'dados.csv': {e}")
    exit()

# 2. Determinar características dos nós e preparar arestas
all_node_ids_in_file = set(data_df["node1_orig"].unique()).union(set(data_df["node2_orig"].unique()))

if not all_node_ids_in_file:
    print("Erro: Nenhum nó encontrado no arquivo de dados.")
    exit()

min_id_from_file = min(all_node_ids_in_file)
max_id_from_file = max(all_node_ids_in_file)
actual_num_distinct_nodes = len(all_node_ids_in_file) # Número total de nós únicos

print(f"IDs dos nós no arquivo variam de {min_id_from_file} a {max_id_from_file}.")
print(f"Número de nós distintos encontrados: {actual_num_distinct_nodes}.")

# Para o DSU e Kruskal, os nós precisam ser 0-indexados (0 a N-1).
# Se os nós no arquivo são 1-indexados (1 a N), precisamos remapeá-los.
id_offset = 0
if min_id_from_file == 1 and max_id_from_file == actual_num_distinct_nodes:
    print("Detectado: Nós parecem ser 1-indexados (1 a N). Remapeando para 0 a N-1.")
    id_offset = 1
elif min_id_from_file == 0 and max_id_from_file == actual_num_distinct_nodes - 1:
    print("Detectado: Nós parecem ser 0-indexados (0 a N-1). Nenhum remapeamento de ID necessário.")
else:
    # Para outros casos (ex: IDs esparsos ou começando de um número > 1),
    # uma estratégia de mapeamento mais robusta (usando um dicionário de mapeamento) seria necessária.
    # Por simplicidade, se não for 0-indexado, tentamos um offset simples.
    if min_id_from_file != 0:
        print(f"Aviso: IDs dos nós não são estritamente 0-indexados ou 1-indexados contíguos.")
        print(f"Tentando remapear subtraindo {min_id_from_file} de cada ID.")
        id_offset = min_id_from_file


kruskal_edges = []
original_weight = 0
for _, row in data_df.iterrows():
    source_orig = int(row["node1_orig"])
    destination_orig = int(row["node2_orig"])
    weight = random.randint(1, 100) # Peso aleatório atribuído

    # Remapeia IDs se necessário
    remapped_source = source_orig - id_offset
    remapped_destination = destination_orig - id_offset
    
    kruskal_edges.append([remapped_source, remapped_destination, weight])
    original_weight+=weight

# 3. Executar o algoritmo de Kruskal
# O número de vértices para Kruskal é o número total de nós distintos.
num_vertices_for_kruskal = actual_num_distinct_nodes


average_price_per_meter = 2

if num_vertices_for_kruskal > 0:
    print(f"\nExecutando o algoritmo de Kruskal com {num_vertices_for_kruskal} vértices.")
    print(f"Os IDs dos nós foram processados para estarem no intervalo [0, {num_vertices_for_kruskal-1}].")
    
    total_mst_cost = kruskals_mst(num_vertices_for_kruskal, kruskal_edges)
    cost_economized = original_weight - total_mst_cost
    print(f"Custo total da Árvore Geradora Mínima (MST): {total_mst_cost}")
    print(f"Custo total do grafo: {original_weight}")
    print(f"Custo total economizado: {cost_economized}")
    print(f"Valor economizado R$: {cost_economized * average_price_per_meter}")
else:
    print("Nenhum vértice para processar para a MST.")

# O seu dicionário 'graph' original não era usado diretamente por Kruskal.
# Se você precisar dele para outros propósitos (ex: visualização com Pyvis),
# construa-o usando os IDs remapeados (ou originais, dependendo da sua necessidade).
# Exemplo de construção do 'graph' (adjacência) com IDs remapeados:
# adj_list_graph = {}
# for n1, n2, w in kruskal_edges: # Usando arestas com IDs já remapeados
#     adj_list_graph.setdefault(n1, []).append((n2, w))
#     adj_list_graph.setdefault(n2, []).append((n1, w)) # Para grafo não direcionado
# print("\nExemplo de lista de adjacência (primeiros 5 nós):")
# for i, (node, neighbors) in enumerate(adj_list_graph.items()):
#     if i < 5:
#         print(f"Nó {node}: {neighbors}")
#     else:
#         break
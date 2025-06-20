import pandas as pd
import heapq  # Importa a biblioteca para a fila de prioridade (min-heap)
import time   # Importa a biblioteca para medir o tempo de execução

# --- Constantes ---
COST_PER_METER = 2.0  # Exemplo: R$ 2,00 por metro de cabo/estrada

# ... (A classe DSU continua exatamente a mesma) ...
class DSU:
    """
    Implementação da estrutura de dados Disjoint Set Union (DSU) ou Union-Find.
    Utiliza otimizações de compressão de caminho e união por rank para alta eficiência.
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            return True
        return False

def kruskals_mst(num_vertices, edge_list):
    """
    Executa o algoritmo de Kruskal para encontrar a Árvore Geradora Mínima (MST).
    Args:
        num_vertices (int): O número total de vértices no grafo.
        edge_list (list): Uma lista de arestas, onde cada aresta é [u, v, peso].
    Returns:
        tuple: (custo_total_mst, arestas_da_mst)
    """
    sorted_edge_list = sorted(edge_list, key=lambda item: item[2])
    dsu = DSU(num_vertices)
    mst_cost = 0
    mst_edges = []
    for node1, node2, weight in sorted_edge_list:
        if dsu.union(node1, node2):
            mst_cost += weight
            mst_edges.append([node1, node2, weight])
            if len(mst_edges) == num_vertices - 1:
                break
    return mst_cost, mst_edges

# --- NOVA FUNÇÃO: ALGORITMO DE PRIM ---
def prims_mst(num_vertices, adj_list):
    """
    Executa o algoritmo de Prim para encontrar a Árvore Geradora Mínima (MST).
    Utiliza uma fila de prioridade (min-heap) para eficiência.
    Args:
        num_vertices (int): O número total de vértices no grafo.
        adj_list (dict): Uma lista de adjacência do grafo. {vértice: [(vizinho, peso), ...]}
    Returns:
        tuple: (custo_total_mst, arestas_da_mst)
    """
    if num_vertices == 0:
        return 0, []

    # Fila de prioridade (min-heap) para armazenar as arestas a serem consideradas.
    # Formato: (peso, vértice_origem, vértice_destino)
    min_heap = []
    
    # Conjunto para rastrear os vértices já incluídos na MST
    visited = set()
    
    mst_cost = 0
    mst_edges = []
    
    # Começa o algoritmo a partir do vértice 0 (poderia ser qualquer um)
    start_vertex = 0
    visited.add(start_vertex)
    
    # Adiciona todas as arestas do vértice inicial à fila de prioridade
    for neighbor, weight in adj_list.get(start_vertex, []):
        heapq.heappush(min_heap, (weight, start_vertex, neighbor))

    # O loop continua até que a MST esteja completa
    while min_heap and len(visited) < num_vertices:
        weight, u, v = heapq.heappop(min_heap)
        
        # Se o vértice de destino já foi visitado, esta aresta cria um ciclo. Pule.
        if v not in visited:
            visited.add(v)
            mst_cost += weight
            mst_edges.append([u, v, weight])
            
            # Adiciona as arestas do novo vértice 'v' à fila de prioridade
            for next_neighbor, next_weight in adj_list.get(v, []):
                if next_neighbor not in visited:
                    heapq.heappush(min_heap, (next_weight, v, next_neighbor))
    
    return mst_cost, mst_edges


def main():
    """
    Função principal que executa o fluxo completo e compara os algoritmos.
    """
    # --- 1. Leitura dos dados ---
    try:
        data_df = pd.read_csv("dados.csv", sep=" ", header=None)
        data_df.columns = ["node1_orig", "node2_orig", "peso"]
    except FileNotFoundError:
        print("Erro: O arquivo 'dados.csv' não foi encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler 'dados.csv': {e}")
        return

    # --- 2. Processamento de Nós e Arestas ---
    all_node_ids = set(data_df["node1_orig"]).union(set(data_df["node2_orig"]))
    if not all_node_ids:
        print("Erro: Nenhum nó encontrado no arquivo de dados.")
        return
        
    num_vertices = len(all_node_ids)
    map_id_to_idx = {original_id: i for i, original_id in enumerate(all_node_ids)}

    edge_list = []
    # Criação da lista de adjacência para o algoritmo de Prim
    adj_list = {i: [] for i in range(num_vertices)}
    original_total_weight = 0

    for _, row in data_df.iterrows():
        source_orig, dest_orig, weight = int(row["node1_orig"]), int(row["node2_orig"]), float(row["peso"])
        
        remapped_source = map_id_to_idx[source_orig]
        remapped_dest = map_id_to_idx[dest_orig]

        # Para Kruskal
        edge_list.append([remapped_source, remapped_dest, weight])
        
        # Para Prim (grafo não direcionado)
        adj_list[remapped_source].append((remapped_dest, weight))
        adj_list[remapped_dest].append((remapped_source, weight))
        
        original_total_weight += weight
    
    print(f"Dados carregados: {num_vertices} vértices e {len(edge_list)} arestas.")
    
    # --- 3. Execução e Comparação dos Algoritmos ---
    if num_vertices > 0:
        
        # --- Executando Kruskal ---
        start_time = time.time()
        kruskal_cost, _ = kruskals_mst(num_vertices, edge_list)
        kruskal_time = time.time() - start_time
        
        # --- Executando Prim ---
        start_time = time.time()
        prim_cost, _ = prims_mst(num_vertices, adj_list)
        prim_time = time.time() - start_time

        # --- 4. Apresentação dos Resultados ---
        print("\n--- Tabela Comparativa de Resultados ---")
        print("="*40)
        print(f"Custo da Rede Original: {original_total_weight:,.2f} m")
        print("-"*40)
        print("Algoritmo de Kruskal:")
        print(f"  - Custo da MST: {kruskal_cost:,.2f} m")
        print(f"  - Tempo de Execução: {kruskal_time:.6f} segundos")
        print("-"*40)
        print("Algoritmo de Prim:")
        print(f"  - Custo da MST: {prim_cost:,.2f} m")
        print(f"  - Tempo de Execução: {prim_time:.6f} segundos")
        print("="*40)
        
        # Validação cruzada dos resultados
        if abs(kruskal_cost - prim_cost) < 1e-9: # Usar tolerância para floats
            print("\n[SUCESSO] Validação: Ambos os algoritmos encontraram o mesmo custo de MST.")
        else:
            print("\n[AVISO] Validação: Os custos da MST são diferentes. Verifique as implementações.")

        cost_saved = original_total_weight - kruskal_cost # Usa um dos custos, já que são iguais
        percentage_saved = (cost_saved / original_total_weight) * 100 if original_total_weight > 0 else 0

        print(f"\nEconomia total com a MST: {cost_saved:,.2f} m ({percentage_saved:.2f}%)")
        print(f"Valor financeiro economizado: R$ {cost_saved * COST_PER_METER:,.2f}")
    else:
        print("Nenhum vértice para processar.")


if __name__ == "__main__":
    main()

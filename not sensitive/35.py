

def dijkstra(graph, start, goal):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    heap = [(distance, node) for node, distance in distances.items()]
    heapq.heapify(heap)
    predecessors = {node: None for node in graph.nodes}
    while heap:
        distance, node = heapq.heappop(heap)
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = predecessors[node]
            return path[::-1]
        for neighbor in graph.edges[node]:
            new_distance = distance + graph.distances[(node, neighbor)]
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = node
                heap = [(distance, node) for node, distance in distances.items()]
                heapq.heapify(heap)

start = (0, 0)
goal = (90, 90)	
path = dijkstra(graph, start, goal)
print(path)


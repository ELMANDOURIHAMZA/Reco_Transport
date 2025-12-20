import networkx as nx
import osmnx as ox
import os

# Get the path to the data directory relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
graph_path = os.path.join(project_root, "data", "city_map.graphml")

# Global variable to cache the graph
G = None
_graph_loading = False

def load_graph():
    """Load the graph lazily when first needed."""
    global G, _graph_loading
    
    if G is not None:
        return G
        
    if _graph_loading:
        return None
        
    _graph_loading = True
    print(f"Loading graph from: {graph_path}")
    try:
        G = ox.load_graphml(graph_path)
        print(f"Graph loaded successfully: {len(G.nodes)} nodes, {len(G.edges)} edges")
        _graph_loading = False
        return G
    except Exception as e:
        print(f"Error loading graph: {e}")
        _graph_loading = False
        return None

def calculate_route(start_coords, end_coords):
    # Load graph on first use
    graph = load_graph()
    
    if graph is None:
        print("ERROR: Graph not loaded")
        return [], 0

    try:
        print(f"Calculating route: start={start_coords}, end={end_coords}")
        orig_node = ox.distance.nearest_nodes(graph, X=start_coords[1], Y=start_coords[0])
        dest_node = ox.distance.nearest_nodes(graph, X=end_coords[1], Y=end_coords[0])

        print(f"Nodes found: orig={orig_node}, dest={dest_node}")
        route = nx.shortest_path(graph, orig_node, dest_node, weight='length')

        path_coords = [(graph.nodes[n]['y'], graph.nodes[n]['x']) for n in route]

        # Calculate total distance in meters (sum of 'length' edge weights)
        distance = 0
        for i in range(len(route) - 1):
            edge_data = graph.get_edge_data(route[i], route[i+1])
            # edge_data can be a dict with multiple keys (multi-graph), take the first edge
            if edge_data:
                if isinstance(edge_data, dict):
                    edge = list(edge_data.values())[0]
                else:
                    edge = edge_data
                distance += edge.get('length', 0)

        result_path = [f"{lat},{lng}" for lat, lng in path_coords]
        result_distance = distance / 1000  # Convert to km
        print(f"Route calculated: {len(result_path)} points, {result_distance:.2f} km")
        return result_path, result_distance

    except Exception as e:
        print(f"Error calculating route: {e}")
        import traceback
        traceback.print_exc()
        return [], 0

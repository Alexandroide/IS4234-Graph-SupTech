import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any, List


class GraphAnalyzerCIDM:
    def __init__(self, graph_file: str) -> None:
        """
        Initialize the graph from a JSON file.

        Parameters
        ----------
        graph_file : str
            Path to the JSON file containing the graph data.
        """
        self.graph_file: str = graph_file
        self.G: nx.DiGraph = nx.DiGraph()
        self.load_graph()
        
    def load_graph(self) -> None:
        """Load graph data from JSON and create a NetworkX graph."""
        with open(self.graph_file, "r") as f:
            graph_data: Dict[str, Any] = json.load(f)
        
        # Add nodes with weights
        for node_id, node_data in graph_data.items():
            self.G.add_node(node_id, **node_data["weights"])
        
        # Add edges with operational reliance as weight
        for node_id, node_data in graph_data.items():
            for target_id, edge_weight in node_data["edges"].items():
                self.G.add_edge(node_id, target_id, weight=edge_weight)
    
    def visualize(
        self,
        min_size: int = 100,
        max_size: int = 2000,
        edge_scale: float = 10.0,
        layout: str = "spring",
        seed: int = 42
    ) -> None:
        """Visualize the graph with node sizes, colors, and edge widths."""
        globals_list: List[float] = [self.G.nodes[n]["global"] for n in self.G.nodes]
        min_val, max_val = min(globals_list), max(globals_list)
        node_sizes = [
            min_size + (val - min_val) / (max_val - min_val) * (max_size - min_size)
            for val in globals_list
        ]
        
        node_colors: List[float] = [self.G.nodes[n]["societal"] for n in self.G.nodes]
        edge_widths: List[float] = [self.G[u][v]["weight"] * edge_scale for u, v in self.G.edges]
        
        # Choose layout
        if layout == "spring":
            pos = nx.spring_layout(self.G, k=0.5, seed=seed)
        elif layout == "circular":
            pos = nx.circular_layout(self.G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(self.G)
        else:
            raise ValueError("Unsupported layout type")
        
        # Draw graph
        plt.figure(figsize=(12, 12))
        nx.draw_networkx_nodes(
            self.G, pos, node_size=node_sizes, node_color=node_colors,
            cmap=plt.cm.viridis, alpha=0.8
        )
        nx.draw_networkx_edges(
            self.G, pos, width=edge_widths, alpha=0.6,
            arrowstyle="-|>", arrowsize=15
        )
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="black")
        plt.title(
            "Company Dependency Graph\n"
            "Node size = Global criticality, Edge width = Operational reliance"
        )
        plt.colorbar(
            plt.cm.ScalarMappable(cmap=plt.cm.viridis),
            label="Societal criticality"
        )
        plt.axis("off")
        plt.show()
    
    def centrality(self) -> Dict[str, float]:
        """Compute degree centrality."""
        return nx.degree_centrality(self.G)
    
    def shortest_path(self, source: str, target: str) -> List[str]:
        """Compute shortest path from source to target (weighted by edge weight)."""
        return nx.shortest_path(self.G, source=source, target=target, weight='weight')
    
    def summary(self) -> None:
        """Print a quick summary of the graph."""
        print(f"Nodes: {self.G.number_of_nodes()}, Edges: {self.G.number_of_edges()}")
        print("Nodes with attributes:", list(self.G.nodes(data=True))[:5])
        print("Edges with attributes:", list(self.G.edges(data=True))[:5])
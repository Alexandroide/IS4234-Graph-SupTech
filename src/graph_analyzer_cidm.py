import json
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any, List


class GraphAnalyzerCIDM:
    """
    Executive Summary:
    -------------------
    This class provides a framework for analyzing inter-company dependencies
    in a critical infrastructure or digital supply-chain network.
    
    Each node represents a company (or service provider).
    Each directed edge represents an operational dependency (A → B means A relies on B).
    Edge weights represent reliance intensity (0–1), while node weights reflect
    each company's intrinsic importance to the economy or society.
    
    This system helps regulators or analysts identify:
      • Hidden but critical providers.
      • Systemic dependencies and cascade risks.
      • Potential regulatory supervision targets.
    """

    def __init__(self, graph_file: str) -> None:
        """Initialize the CIDM graph from a JSON file."""
        self.graph_file: str = graph_file
        self.G: nx.DiGraph = nx.DiGraph()
        self.load_graph()

    # CORE FUNCTIONALITY
    def load_graph(self) -> None:
        """Load graph data from a JSON file and construct a directed graph."""
        with open(self.graph_file, "r") as f:
            graph_data: Dict[str, Any] = json.load(f)

        # Add nodes (companies) with intrinsic weights
        for node_id, node_data in graph_data.items():
            self.G.add_node(node_id, **node_data["weights"])

        # Add edges (dependencies) with reliance weights
        for node_id, node_data in graph_data.items():
            for target_id, edge_weight in node_data["edges"].items():
                self.G.add_edge(node_id, target_id, weight=edge_weight)

    def summary(self) -> None:
        """Print an executive snapshot of the graph’s scale and structure."""
        print("=== CIDM NETWORK SUMMARY ===")
        print(f"Nodes (Companies): {self.G.number_of_nodes()}")
        print(f"Edges (Dependencies): {self.G.number_of_edges()}")

        node_attrs = list(self.G.nodes(data=True))[:5]
        edge_attrs = list(self.G.edges(data=True))[:5]

        print("\nSample Nodes (Top 5):", node_attrs)
        print("Sample Edges (Top 5):", edge_attrs)
        print("============================\n")

    # VISUALIZATION
    def visualize(
        self,
        min_size: int = 100,
        max_size: int = 2000,
        edge_scale: float = 10.0,
        layout: str = "spring",
        seed: int = 42
    ) -> None:
        """
        Visualize the network to understand structure, size, and dependencies.

        Node size  = Global criticality
        Node color = Societal criticality
        Edge width = Operational reliance
        """
        globals_list: List[float] = [self.G.nodes[n]["global"] for n in self.G.nodes]
        min_val, max_val = min(globals_list), max(globals_list)
        node_sizes = [
            min_size + (val - min_val) / (max_val - min_val) * (max_size - min_size)
            for val in globals_list
        ]

        node_colors: List[float] = [self.G.nodes[n]["societal"] for n in self.G.nodes]
        edge_widths: List[float] = [self.G[u][v]["weight"] * edge_scale for u, v in self.G.edges]

        # Layout options for better readability
        if layout == "spring":
            pos = nx.spring_layout(self.G, k=0.5, seed=seed)
        elif layout == "circular":
            pos = nx.circular_layout(self.G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(self.G)
        else:
            raise ValueError("Unsupported layout type")

        # Draw the network
        plt.figure(figsize=(12, 12))
        nx.draw_networkx_nodes(
            self.G, pos, node_size=node_sizes, node_color=node_colors,
            cmap=plt.cm.viridis, alpha=0.8
        )
        nx.draw_networkx_edges(
            self.G, pos, width=edge_widths, alpha=0.6, arrows=True,
            arrowstyle="-|>", arrowsize=15
        )
        nx.draw_networkx_labels(self.G, pos, font_size=8, font_color="black")
        plt.title(
            "Company Dependency Graph\n"
            "Node size = Global criticality, Edge width = Operational reliance"
        )
        plt.axis("off")
        plt.show()

    # ANALYTICAL METHODS
    def centrality(self) -> Dict[str, float]:
        """
        Measure: Degree Centrality
        --------------------------
        Indicates how many direct connections a company has.
        High centrality = many relationships (either dependencies or providers).
        """
        return nx.degree_centrality(self.G)

    def dependency_centrality(self) -> Dict[str, float]:
        """
        Measure: Dependency Centrality
        ------------------------------
        Quantifies how much other companies rely on a given company.
        Calculated as the sum of inbound edge weights.
        High score = key provider with many reliant clients.
        """
        centrality = {}
        for node in self.G.nodes:
            inbound_edges = self.G.in_edges(node, data=True)
            centrality[node] = sum(d["weight"] for _, _, d in inbound_edges)
        return centrality

    def systemic_importance(self) -> Dict[str, float]:
        """
        Measure: Systemic Importance Index
        ----------------------------------
        Combines dependency influence (inbound reliance)
        with intrinsic company importance (global weight).
        Identifies 'too critical to fail' nodes in the ecosystem.
        """
        dep_centrality = self.dependency_centrality()
        importance = {}
        for node in self.G.nodes:
            w_dep = dep_centrality[node]
            w_glob = self.G.nodes[node]["global"]
            importance[node] = (0.6 * w_dep) + (0.4 * w_glob)
        return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

    def simulate_failure(self, node: str, threshold: float = 0.3) -> List[str]:
        """
        Simulation: Cascading Failure Model
        -----------------------------------
        Simulates the ripple effect of a company outage.

        Any company that relies more than `threshold` on a failed company
        is considered 'failed' as well, and the effect propagates recursively.
        """
        failed = {node}
        new_failures = {node}
        while new_failures:
            next_failures = set()
            for n in new_failures:
                dependents = [src for src, tgt, d in self.G.in_edges(n, data=True) if d["weight"] >= threshold]
                next_failures.update(dependents)
            next_failures -= failed
            if not next_failures:
                break
            failed |= next_failures
            new_failures = next_failures
        return list(failed)

    def shortest_path(self, source: str, target: str) -> List[str]:
        """
        Utility: Dependency Path Finder
        -------------------------------
        Finds the shortest operational dependency path between two companies.
        Helps trace supply routes or software reliance chains.
        """
        return nx.shortest_path(self.G, source=source, target=target, weight='weight')

# TEST CODE
if __name__ == "__main__":
    # Executive Summary: Load and test a company dependency network
    analyzer = GraphAnalyzerCIDM("../data/graph_data.json")

    # 1. Overview
    analyzer.summary()

    # 2. Visual diagnostic of systemic dependencies
    analyzer.visualize()

    # 3. Identify top systemic providers
    print("\n=== SYSTEMIC IMPORTANCE RANKING ===")
    importance = analyzer.systemic_importance()
    for company, score in list(importance.items())[:10]:
        print(f"{company}: {score:.2f}")

    # 4. Simulate failure of a key company
    critical_node = list(importance.keys())[0]
    cascade = analyzer.simulate_failure(critical_node, threshold=0.3)
    print(f"\nIf {critical_node} fails, {len(cascade)} companies are impacted:")
    print(cascade)

    # 5. Example path query
    print("\nExample dependency path:")
    print(analyzer.shortest_path("COMP001", "COMP010"))

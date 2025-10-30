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
    def systemic_influence(self, damping: float = 0.85, max_iter: int = 100, tol: float = 1e-6) -> Dict[str, float]:
        """
        Compute recursive systemic influence for all companies.
        
        Each company's score is influenced by the criticality of companies that depend on it,
        weighted by dependency strength (edge weight) and propagated recursively.

        Parameters
        ----------
        damping : float
            Damping factor (like in PageRank, 0 < damping < 1)
        max_iter : int
            Maximum number of iterations
        tol : float
            Convergence tolerance

        Returns
        -------
        Dict[str, float]
            Node ID -> systemic influence score (sorted descending)
        """
        # Initialize scores with intrinsic global importance
        scores = {node: self.G.nodes[node]["global"] for node in self.G.nodes}
        
        for iteration in range(max_iter):
            new_scores = {}
            max_change = 0.0
            
            for node in self.G.nodes:
                # Sum over all inbound edges (who depends on me)
                total = sum(
                    scores[src] * d["weight"] for src, _, d in self.G.in_edges(node, data=True)
                )
                # Update with damping: preserves intrinsic node weight
                new_score = (1 - damping) * self.G.nodes[node]["global"] + damping * total
                new_scores[node] = new_score
                max_change = max(max_change, abs(new_score - scores[node]))
            
            scores = new_scores
            
            if max_change < tol:
                break
        
        # Return scores sorted descending
        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


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

    def simulate_failure_recursive(self, node: str, threshold: float = 0.3, company_file: str = "../data/company_data.json") -> List[Dict[str, str]]:
        """
        Cascading failure simulation with recursive propagation.
        Computes effective dependency along chains using multiplication of edge weights.
        """
        # Load company names
        try:
            with open(company_file, "r") as f:
                companies = json.load(f)
            id_to_name = {c["company_id"]: c["company_name"] for c in companies}
        except FileNotFoundError:
            id_to_name = {}

        failed = {node}
        # Track effective dependencies for all nodes
        effective_dep = {node: 1.0}

        changed = True
        while changed:
            changed = False
            for n in self.G.nodes:
                if n in failed:
                    continue
                # Compute max effective dependency to any failed node
                max_dep = 0.0
                for succ in self.G.successors(n):
                    if succ in effective_dep:
                        max_dep = max(max_dep, self.G[n][succ]["weight"] * effective_dep[succ])
                if max_dep >= threshold:
                    failed.add(n)
                    effective_dep[n] = max_dep
                    changed = True

        affected_list = [{"company_id": cid, "company_name": id_to_name.get(cid, "Unknown")} for cid in failed]
        return affected_list


    def get_company_info(self, company_id: str, company_file: str = "../data/company_data.json") -> dict:
        """
        Retrieve all useful information about a company given its company_id.

        Parameters
        ----------
        company_id : str
            ID of the company to retrieve.
        company_file : str
            Path to the JSON file containing company details.

        Returns
        -------
        dict
            Dictionary with all available information, or empty dict if not found.
        """
        try:
            with open(company_file, "r") as f:
                companies = json.load(f)
            for comp in companies:
                if comp.get("company_id") == company_id:
                    return comp
            print(f"Company {company_id} not found in {company_file}.")
            return {}
        except FileNotFoundError:
            print(f"File {company_file} not found.")
            return {}
        
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = GraphAnalyzerCIDM("../data/graph_data.json")

    # 1️⃣ Print graph summary
    analyzer.summary()

    # 2️⃣ Compute recursive systemic influence
    influence_scores = analyzer.systemic_influence()

    # Top 10 most systemically critical companies
    print("\nTop 10 most systemically critical companies:")
    top_companies = list(influence_scores.items())[:10]
    for i, (company, score) in enumerate(top_companies, start=1):
        print(f"{i}. {company}: {score:.2f}")

    # 3️⃣ Get detailed info for the top company
    top_company_id = top_companies[0][0]
    print(f"\n=== DETAILED INFO FOR TOP COMPANY: {top_company_id} ===")
    company_info = analyzer.get_company_info(top_company_id, company_file="../data/company_data.json")
    if company_info:
        for key, value in company_info.items():
            print(f"{key}: {value}")

    # 4️⃣ Optional: simulate failure of top company
    affected_companies = analyzer.simulate_failure(top_company_id, threshold=0.3)
    print(f"\nSimulating failure of {top_company_id}...")
    print(f"{len(affected_companies)} companies would be affected:")
    print(affected_companies)

    # 5️⃣ Optional: visualize network
    analyzer.visualize()
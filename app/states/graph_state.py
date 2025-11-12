import reflex as rx
from typing import ClassVar, TypedDict, Literal
import networkx as nx
import plotly.graph_objects as go
import random
import logging


class Node(TypedDict):
    id: str


class Link(TypedDict):
    source: str
    target: str


class GraphData(TypedDict):
    directed: bool
    multigraph: bool
    nodes: list[Node]
    links: list[Link]


class GraphState(rx.State):
    """Manages the state for the graph generator application."""

    nodes_str: str = ""
    edges_str: str = ""
    graph_type: str = "undirected"
    graph_data: GraphData | None = None
    graph_figure: go.Figure | None = None
    error_message: str = ""
    shortest_path_start: str = ""
    shortest_path_end: str = ""
    shortest_path_result: list[str] = []
    centrality_result: dict[str, float] = {}
    clustering_result: dict[str, float] = {}
    PRESETS: ClassVar[dict[str, dict[str, str]]] = {
        "social_network": {
            "nodes": "Alice, Bob, Charlie, David, Eve",
            "edges": """Alice, Bob
Alice, Charlie
Bob, Charlie
Bob, David
Charlie, David
David, Eve""",
        },
        "tree": {
            "nodes": "A, B, C, D, E, F, G",
            "edges": """A, B
A, C
B, D
B, E
C, F
C, G""",
        },
        "cycle": {
            "nodes": "1, 2, 3, 4, 5",
            "edges": """1, 2
2, 3
3, 4
4, 5
5, 1""",
        },
        "complete_graph": {
            "nodes": "X, Y, Z, W",
            "edges": """X, Y
X, Z
X, W
Y, Z
Y, W
Z, W""",
        },
    }

    @rx.var
    def graph_nodes(self) -> list[Node]:
        """Returns the list of nodes from graph_data, or an empty list."""
        if self.graph_data is None:
            return []
        return self.graph_data.get("nodes", [])

    @rx.var
    def graph_stats(self) -> dict[str, str | int | float] | None:
        """Computed statistics for the current graph."""
        if self.graph_data is None:
            return None
        try:
            G = self._create_nx_graph()
            if G is None:
                return None
            return {
                "Nodes": G.number_of_nodes(),
                "Edges": G.number_of_edges(),
                "Density": f"{nx.density(G):.4f}",
                "Avg. Clustering": f"{nx.average_clustering(G):.4f}"
                if self.graph_type == "undirected"
                else "N/A",
            }
        except Exception as e:
            logging.exception(f"Error calculating graph stats: {e}")
            return None

    def _create_nx_graph(self) -> nx.Graph | nx.DiGraph | None:
        """Helper to create a NetworkX graph from state variables."""
        try:
            nodes = [n.strip() for n in self.nodes_str.split(",") if n.strip()]
            edge_list = []
            for line in self.edges_str.strip().split("""
"""):
                parts = [p.strip() for p in line.split(",") if p.strip()]
                if len(parts) == 2:
                    edge_list.append(tuple(parts))
            G = nx.DiGraph() if self.graph_type == "directed" else nx.Graph()
            G.add_nodes_from(nodes)
            G.add_edges_from(edge_list)
            return G
        except Exception as e:
            logging.exception(f"Error creating networkx graph: {e}")
            return None

    def _generate_plotly_figure(self, G: nx.Graph | nx.DiGraph) -> go.Figure:
        """Generates a Plotly figure for the graph visualization."""
        pos = nx.spring_layout(G, seed=42)
        edge_x, edge_y = ([], [])
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1, color="#888"),
            hoverinfo="none",
            mode="lines",
        )
        node_x, node_y, node_text = ([], [], [])
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            hoverinfo="text",
            text=node_text,
            textposition="bottom center",
            marker=dict(showscale=False, color="#9333ea", size=15, line_width=2),
        )
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=5, r=5, t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e5e7eb"),
            ),
        )
        return fig

    @rx.event
    def handle_submit(self, form_data: dict):
        """Handles the form submission, generates the graph, and redirects."""
        self.nodes_str = (form_data.get("nodes_str") or "").strip()
        self.edges_str = (form_data.get("edges_str") or "").strip()
        self.graph_type = form_data.get("graph_type", "undirected")
        if not self.nodes_str or not self.edges_str:
            return rx.toast.error("Nodes and Edges cannot be empty.")
        G = self._create_nx_graph()
        if G is None:
            return rx.toast.error(
                "Failed to parse graph data. Check your input format."
            )
        graph_dict = nx.node_link_data(
            G, source="source", target="target", name="id", key="key", edges="links"
        )
        self.graph_data = {
            "directed": graph_dict.get("directed", False),
            "multigraph": graph_dict.get("multigraph", False),
            "nodes": graph_dict.get("nodes", []),
            "links": graph_dict.get("links", []),
        }
        self.graph_figure = self._generate_plotly_figure(G)
        self.error_message = ""
        self.shortest_path_result = []
        self.centrality_result = {}
        self.clustering_result = {}
        return rx.redirect("/graph")

    @rx.event
    def load_preset(self, preset_name: str):
        """Loads a predefined graph data preset into the form."""
        if preset_name in self.PRESETS:
            preset = self.PRESETS[preset_name]
            self.nodes_str = preset["nodes"]
            self.edges_str = preset["edges"]
            return rx.toast.info(
                f"Loaded '{preset_name.replace('_', ' ').title()}' preset."
            )

    @rx.event
    def calculate_shortest_path(self):
        """Calculates the shortest path between two selected nodes."""
        if not self.shortest_path_start or not self.shortest_path_end:
            return rx.toast.warning("Please select both start and end nodes.")
        G = self._create_nx_graph()
        if G is None:
            return
        try:
            path = nx.shortest_path(G, self.shortest_path_start, self.shortest_path_end)
            self.shortest_path_result = path
        except (nx.NetworkXNoPath, nx.NodeNotFound) as e:
            logging.exception(f"Shortest path not found: {e}")
            self.shortest_path_result = []
            return rx.toast.error("No path found between the selected nodes.")

    @rx.event
    def calculate_centrality(self):
        """Calculates the degree centrality for all nodes."""
        G = self._create_nx_graph()
        if G is None:
            return
        self.centrality_result = nx.degree_centrality(G)
        return rx.toast.success("Calculated Degree Centrality.")

    @rx.event
    def calculate_clustering(self):
        """Calculates the clustering coefficient for all nodes."""
        G = self._create_nx_graph()
        if G is None or self.graph_type == "directed":
            return rx.toast.warning(
                "Clustering can only be calculated for undirected graphs."
            )
        self.clustering_result = nx.clustering(G)
        return rx.toast.success("Calculated Clustering Coefficient.")

    @rx.event
    def on_load_graph(self):
        """Checks if graph data exists on page load and regenerates figure if needed."""
        if self.graph_data is None:
            return rx.redirect("/")
        if self.graph_figure is None:
            G = nx.node_link_graph(
                self.graph_data, directed=self.graph_type == "directed"
            )
            if G:
                self.graph_figure = self._generate_plotly_figure(G)
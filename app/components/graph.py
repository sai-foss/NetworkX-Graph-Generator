import reflex as rx
from reflex.components.plotly import plotly
from app.states.graph_state import GraphState


def result_table(title: str, data: rx.Var[dict]) -> rx.Component:
    """A component to display algorithm results in a table."""
    return rx.el.div(
        rx.el.h4(title, class_name="font-semibold text-purple-200 mb-2"),
        rx.el.div(
            rx.foreach(
                data.entries(),
                lambda item: rx.el.div(
                    rx.el.span(item[0], class_name="font-medium text-gray-300"),
                    rx.el.span(
                        item[1].to(float).to_string(),
                        class_name="text-purple-300 font-mono",
                    ),
                    class_name="flex justify-between items-center text-sm p-2 rounded-md bg-white/5",
                ),
            ),
            class_name="space-y-1 max-h-60 overflow-y-auto pr-2",
        ),
        class_name="p-4 bg-black/20 rounded-xl",
    )


def graph_sidebar() -> rx.Component:
    """The sidebar for graph controls and metrics."""
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon(tag="arrow-left", class_name="mr-2"),
                "New Graph",
                href="/",
                class_name="inline-flex items-center px-4 py-2 text-sm font-semibold text-purple-200 bg-white/10 rounded-lg hover:bg-white/20 transition-colors mb-6",
            ),
            rx.el.div(
                rx.el.h3(
                    "Graph Statistics", class_name="text-lg font-bold text-white mb-3"
                ),
                rx.cond(
                    GraphState.graph_stats,
                    rx.el.div(
                        rx.foreach(
                            GraphState.graph_stats.entries(),
                            lambda item: rx.el.div(
                                rx.el.span(
                                    item[0], class_name="font-medium text-gray-400"
                                ),
                                rx.el.span(
                                    item[1].to_string(),
                                    class_name="font-semibold text-white",
                                ),
                                class_name="flex justify-between items-center py-2 border-b border-white/10",
                            ),
                        ),
                        class_name="text-sm",
                    ),
                    rx.el.p("No stats available.", class_name="text-gray-400"),
                ),
                class_name="mb-8 p-4 bg-black/20 rounded-xl",
            ),
            rx.el.div(
                rx.el.h3(
                    "Graph Algorithms", class_name="text-lg font-bold text-white mb-4"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h4(
                            "Shortest Path",
                            class_name="font-semibold text-purple-200 mb-3",
                        ),
                        rx.el.div(
                            rx.el.select(
                                rx.foreach(
                                    GraphState.graph_nodes,
                                    lambda node: rx.el.option(
                                        node["id"], value=node["id"]
                                    ),
                                ),
                                placeholder="Start Node",
                                on_change=GraphState.set_shortest_path_start,
                                class_name="bg-white/10 text-white rounded-md w-full text-sm p-2 border-none focus:ring-2 focus:ring-purple-500",
                            ),
                            rx.el.select(
                                rx.foreach(
                                    GraphState.graph_nodes,
                                    lambda node: rx.el.option(
                                        node["id"], value=node["id"]
                                    ),
                                ),
                                placeholder="End Node",
                                on_change=GraphState.set_shortest_path_end,
                                class_name="bg-white/10 text-white rounded-md w-full text-sm p-2 border-none focus:ring-2 focus:ring-purple-500",
                            ),
                            class_name="grid grid-cols-2 gap-2 mb-3",
                        ),
                        rx.el.button(
                            "Find Path",
                            on_click=GraphState.calculate_shortest_path,
                            class_name="w-full text-sm py-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors",
                        ),
                        rx.cond(
                            GraphState.shortest_path_result.length() > 0,
                            rx.el.div(
                                rx.el.p(
                                    "Path:", class_name="text-xs text-gray-400 mb-1"
                                ),
                                rx.el.p(
                                    GraphState.shortest_path_result.join(" → "),
                                    class_name="text-center font-mono text-sm bg-black/30 p-2 rounded-md",
                                ),
                                class_name="mt-3",
                            ),
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Calculate Degree Centrality",
                            on_click=GraphState.calculate_centrality,
                            class_name="w-full text-sm py-2 mb-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors",
                        ),
                        rx.cond(
                            GraphState.centrality_result.keys().length() > 0,
                            result_table(
                                "Degree Centrality", GraphState.centrality_result
                            ),
                        ),
                        rx.el.button(
                            "Calculate Clustering Coefficient",
                            on_click=GraphState.calculate_clustering,
                            class_name="w-full text-sm py-2 mt-4 mb-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors",
                        ),
                        rx.cond(
                            GraphState.clustering_result.keys().length() > 0,
                            result_table(
                                "Clustering Coefficient", GraphState.clustering_result
                            ),
                        ),
                        class_name="space-y-2",
                    ),
                    class_name="space-y-4",
                ),
                class_name="p-4 bg-black/20 rounded-xl",
            ),
            class_name="p-6",
        ),
        class_name="w-96 h-screen bg-gray-900/80 backdrop-blur-sm border-r border-white/10 overflow-y-auto shrink-0",
    )


def graph_display() -> rx.Component:
    """The main view for displaying the generated graph."""
    return rx.el.div(
        rx.cond(
            GraphState.graph_figure,
            plotly(data=GraphState.graph_figure, class_name="w-full h-full"),
            rx.el.div(
                rx.el.p("No graph generated. ", class_name="text-gray-400"),
                rx.el.a(
                    "Go back to create one.",
                    href="/",
                    class_name="text-purple-400 hover:underline",
                ),
                class_name="flex items-center justify-center w-full h-full text-lg",
            ),
        ),
        class_name="flex-1 h-screen bg-transparent",
    )


def graph_page() -> rx.Component:
    """The page for displaying the graph and its metrics."""
    return rx.el.div(
        graph_sidebar(),
        graph_display(),
        class_name="flex w-full h-screen font-['Roboto'] bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white",
    )
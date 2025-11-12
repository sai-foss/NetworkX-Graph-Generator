import reflex as rx
from app.states.graph_state import GraphState


def preset_button(label: str, preset_name: str) -> rx.Component:
    """A reusable button for loading a data preset."""
    return rx.el.button(
        label,
        on_click=lambda: GraphState.load_preset(preset_name),
        type="button",
        class_name="px-3 py-1.5 text-xs font-medium text-purple-700 bg-purple-100 rounded-full hover:bg-purple-200 transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2",
    )


def graph_form() -> rx.Component:
    """The main input form for generating the graph."""
    return rx.el.div(
        rx.el.h1(
            "Graph Data Generator",
            class_name="text-3xl font-bold text-center text-gray-800 mb-2",
        ),
        rx.el.p(
            "Input your graph data or use a preset to get started.",
            class_name="text-center text-gray-500 mb-8",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.label(
                        "Nodes",
                        html_for="nodes_str",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.textarea(
                        id="nodes_str",
                        name="nodes_str",
                        placeholder="e.g., A, B, C, D",
                        default_value=GraphState.nodes_str,
                        key=f"nodes-{GraphState.nodes_str}",
                        class_name="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl transition-shadow duration-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent focus:shadow-lg shadow-sm hover:shadow-md",
                        rows=3,
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Edges",
                        html_for="edges_str",
                        class_name="block text-sm font-semibold text-gray-700 mb-2",
                    ),
                    rx.el.textarea(
                        id="edges_str",
                        name="edges_str",
                        placeholder="""e.g., A, B
B, C
C, D""",
                        default_value=GraphState.edges_str,
                        key=f"edges-{GraphState.edges_str}",
                        class_name="w-full px-4 py-3 bg-white border border-gray-200 rounded-xl transition-shadow duration-300 focus:ring-2 focus:ring-purple-500 focus:border-transparent focus:shadow-lg shadow-sm hover:shadow-md",
                        rows=5,
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Load an Example:",
                        class_name="text-sm font-semibold text-gray-700 mr-4",
                    ),
                    rx.el.div(
                        preset_button("Social Network", "social_network"),
                        preset_button("Tree", "tree"),
                        preset_button("Cycle", "cycle"),
                        preset_button("Complete", "complete_graph"),
                        class_name="flex flex-wrap gap-2 items-center",
                    ),
                    class_name="flex items-center mb-6",
                ),
                rx.el.fieldset(
                    rx.el.legend(
                        "Graph Type",
                        class_name="text-sm font-semibold text-gray-700 mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="graph_type",
                                value="undirected",
                                class_name="h-4 w-4 text-purple-600 border-gray-300 focus:ring-purple-500 cursor-pointer",
                                default_checked=True,
                            ),
                            rx.el.span("Undirected", class_name="ml-2 text-gray-700"),
                            class_name="flex items-center cursor-pointer",
                        ),
                        rx.el.label(
                            rx.el.input(
                                type="radio",
                                name="graph_type",
                                value="directed",
                                class_name="h-4 w-4 text-purple-600 border-gray-300 focus:ring-purple-500 cursor-pointer",
                            ),
                            rx.el.span("Directed", class_name="ml-2 text-gray-700"),
                            class_name="flex items-center cursor-pointer",
                        ),
                        class_name="flex items-center gap-6",
                    ),
                    class_name="mb-8",
                ),
                rx.el.button(
                    "Generate Graph",
                    rx.icon("arrow-right", class_name="ml-2"),
                    type="submit",
                    class_name="w-full flex items-center justify-center px-6 py-4 text-base font-semibold text-white bg-gradient-to-r from-purple-600 to-indigo-600 rounded-xl shadow-lg hover:shadow-xl hover:from-purple-700 hover:to-indigo-700 transition-all duration-300 transform hover:-translate-y-0.5",
                ),
            ),
            on_submit=GraphState.handle_submit,
            reset_on_submit=False,
            class_name="w-full",
        ),
        class_name="w-full max-w-2xl mx-auto bg-white/70 backdrop-blur-xl p-8 sm:p-12 rounded-2xl shadow-2xl border border-gray-100",
    )
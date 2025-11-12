import reflex as rx
from app.components.graph_form import graph_form
from app.components.graph import graph_page
from app.states.graph_state import GraphState


def index() -> rx.Component:
    """The main page of the application."""
    return rx.el.main(
        rx.el.div(
            rx.el.a(
                rx.el.div(
                    rx.icon(tag="git-graph", class_name="h-6 w-6 text-purple-200"),
                    rx.el.h2(
                        "NetworkX Visualizer",
                        class_name="font-semibold text-lg text-white",
                    ),
                    class_name="flex items-center gap-3",
                ),
                href="/",
            ),
            rx.el.div(graph_form(), class_name="w-full"),
            rx.el.p(
                "Built with ",
                rx.el.a(
                    "Reflex",
                    href="https://reflex.dev",
                    target="_blank",
                    class_name="text-purple-300 hover:text-purple-100 font-semibold",
                ),
                " & ",
                rx.el.a(
                    "NetworkX",
                    href="https://networkx.org/",
                    target="_blank",
                    class_name="text-purple-300 hover:text-purple-100 font-semibold",
                ),
                ".",
                class_name="text-center text-sm text-purple-200 mt-8",
            ),
            class_name="flex flex-col items-center justify-center min-h-screen p-4 sm:p-6 lg:p-8",
        ),
        class_name="font-['Roboto'] bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/")
app.add_page(graph_page, route="/graph", on_load=GraphState.on_load_graph)
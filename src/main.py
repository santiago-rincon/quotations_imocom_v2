from flet import (
    Page,
    SafeArea,
    run,
    Row,
    SelectionArea,
    VerticalDivider,
    Column,
    Text,
    MainAxisAlignment,
    Padding,
    ScrollMode,
    FontWeight,
    Divider,
)
from components.TopBar import TopBar
from components.LeftBar import LeftBar
from components.views.cv import CvView
from config.constants import AppConst


def main(page: Page):
    page.title = "Cotizaciones"
    page.padding = Padding(top=0, bottom=10, left=10, right=10)
    page.appbar = TopBar("Cotizaciones Imocom")
    page.add(
        SafeArea(
            key="safe_area",
            expand=True,
            content=Row(
                expand=True,
                controls=[
                    SelectionArea(content=LeftBar(AppConst.left_menu)),
                    VerticalDivider(width=1),
                    Column(
                        key="body",
                        alignment=MainAxisAlignment.START,
                        expand=True,
                        controls=[CvView()],
                        scroll=ScrollMode.AUTO,
                    ),
                ],
            ),
        ),
        Divider(height=1, color="onSurfaveVariant"),
        Row(
            controls=[
                Text(
                    "© Desarrollado por: Cristian Santiago Rincón, 2025 Imocom",
                    color="onSurfaceVariant",
                    weight=FontWeight.BOLD,
                )
            ],
            alignment=MainAxisAlignment.CENTER,
        ),
    )


run(main)

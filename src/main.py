
import flet as ft
from components.TopBar import TopBar
from components.LeftBar import LeftBar
from components.views.cv import CvView

from config.constants import AppConst


def main(page: ft.Page):
    page.title = "Cotizaciones Imocom mecanizado"
    page.padding = ft.Padding(top=0, bottom=10, left=10, right=10)
    page.appbar = TopBar("Cotizaciones Imocom")
    page.window.maximized = True
    page.add(
        ft.SafeArea(
            key="safe_area",
            expand=True,
            content=ft.Row(
                expand=True,
                controls=[
                    ft.SelectionArea(content=LeftBar(AppConst.left_menu)),
                    ft.VerticalDivider(width=1),
                    ft.Column(
                        key="body",
                        alignment=ft.MainAxisAlignment.START,
                        expand=True,
                        controls=[CvView()],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                ],
            ),
        ),
        ft.Divider(height=1, color="onSurfaveVariant"),
        ft.Row(
            controls=[
                ft.Text(
                    "© Desarrollado por: Cristian Santiago Rincón, 2025 Imocom",
                    color="onSurfaceVariant",
                    weight=ft.FontWeight.BOLD,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


ft.run(main)

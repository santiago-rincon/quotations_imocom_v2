from datetime import datetime
import flet as ft


class AppConst:
    current_date = datetime.now().strftime("%Y-%m-%d")

    quotations_types = {
        "IMPORT": "Repuestos de importación",
        "STOCK": "Repuestos en stock",
    }

    left_menu = [
        {"icon": ft.Icons.RECEIPT,
            "icon_selected": ft.Icons.RECEIPT_OUTLINED, "label": "CV"},
        {
            "icon": ft.Icons.RECEIPT_LONG,
            "icon_selected": ft.Icons.RECEIPT_LONG_OUTLINED,
            "label": "PC",
        },
        {
            "icon": ft.Icons.SETTINGS,
            "icon_selected": ft.Icons.SETTINGS_OUTLINED,
            "label": "Configuración",
        },
    ]

    settings_views = {
        "CV": "Configuraciones para el módulo de CV's",
        "PC": "Configuraciones para el módulo de PC's",
    }

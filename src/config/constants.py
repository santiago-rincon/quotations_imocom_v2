from datetime import datetime
from flet import Icons


class AppConst:
    current_date = datetime.now().strftime("%Y-%m-%d")

    currencies = {
        'COP': 'Pesos Colombianos + IVA',
        'USD': 'Dólares Americanos + IVA liquidados a la TRM del día de facturación',
        'EUR': 'Euros + IVA liquidados a la TRM del día de facturación'
    }

    quotations_types = {
        'IMPORT': 'Repuestos de importación',
        'STOCK': 'Repuestos en stock'
    }

    left_menu = [
        {
            "icon": Icons.RECEIPT,
            "icon_selected": Icons.RECEIPT_OUTLINED,
            "label": "CV"
        },
        {
            "icon": Icons.RECEIPT_LONG,
            "icon_selected": Icons.RECEIPT_LONG_OUTLINED,
            "label": "PC"
        }
    ]

    pay_types_import = {
        "50-50": "50 % Anticipo para iniciar el proceso de importación, 50% 30 días fecha factura",
        "50-CR": "50 % Anticipo para iniciar el proceso de importación, 50% contraentrega",
        "100": "100% Anticipado"
    }

    pay_types_stock = {
        "CONT": "Contado",
        "CRED": "30 días factura"
    }

    def get_final_time(quotation_type, final_time):
        title_header = ""
        f_time = ""
        if quotation_type == AppConst.quotations_types["IMPORT"]:
            title_header = "Ítem"
            f_time = f"Se estima un plazo de entrega de {final_time.strip()} semanas, tiempos estimados una vez confirmada su orden de \t\t\tcompra y el anticipo"
        elif quotation_type == AppConst.quotations_types["STOCK"]:
            title_header = "Código de artículo"
            f_time = "Stock, salvo venta previa"
        return title_header, f_time

    def get_banner_message(path, platform):
        if platform == "windows":
            return f"El archivo de cotización se creó exitosamente en: {path}.docx. ¿Desea abrirlo?"
        return f"El archivo de cotización se creó exitosamente en: {path}.docx."

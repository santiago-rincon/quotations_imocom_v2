from config.constants import AppConst


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
        return f"El archivo de cotización se creó exitosamente en: {path}.docx. ¿Desea abrir el documento?"
    return f"El archivo de cotización se creó exitosamente en: {path}.docx."

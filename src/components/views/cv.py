import flet as ft
from config.constants import AppConst
from docxtpl import DocxTemplate
from utils.utils import get_final_time, get_banner_message
import locale
import os
from re import match
from json import load as json_load

locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")


class CvView(ft.Container):
    def __init__(self):
        super().__init__()
        self.settings = self._load_settings()
        ##### Client info #####
        self.client_info = ft.Row(
            controls=[ft.Text("Información del cliente",
                              size=20, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.client_field = ft.TextField(
            label="Cliente",
            hint_text="Ingresa el nombre del cliente",
            expand=2,
            border_color="onSurfaceVariant",
        )
        self.contact_field = ft.TextField(
            label="Contacto del cliente",
            hint_text="Sra. Angela Cruz",
            expand=2,
            border_color="onSurfaceVariant",
        )
        self.cv_field = ft.TextField(
            label="Número de CV",
            prefix="CV-",
            on_change=lambda e: self._validate_number(e, True),
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.address_field = ft.TextField(
            label="Dirección",
            hint_text="Parque industrial San Jorge, Bodega 10",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.location_field = ft.TextField(
            label="Ubicación",
            hint_text="Mosquera, Cundinamarca",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.quotation_type_field = ft.DropdownM2(
            options=[
                ft.dropdownm2.Option(AppConst.quotations_types["IMPORT"]),
                ft.dropdownm2.Option(AppConst.quotations_types["STOCK"]),
            ],
            expand=1,
            hint_text="Seleccione el tipo de cotización",
            on_change=self._handle_quotation_type_aux,
            value=AppConst.quotations_types["IMPORT"],
            border_color="onSurfaceVariant",
        )
        self.row1 = ft.Row(
            controls=[self.client_field, self.contact_field, self.cv_field],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        self.row2 = ft.Row(
            controls=[
                self.address_field,
                self.location_field,
                self.quotation_type_field,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        ##### Product info #####
        self.product_title = ft.Row(
            controls=[
                ft.Text("Información del producto",
                        size=20, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.article_code_field = ft.TextField(
            label="Código del artículo",
            hint_text="G111000001",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.description_field = ft.TextField(
            label="Descripción",
            hint_text="Descripción del item",
            expand=4,
            border_color="onSurfaceVariant",
        )
        self.quantity_field = ft.TextField(
            label="Cantidad",
            hint_text="1",
            expand=1,
            on_change=self._validate_number,
            border_color="onSurfaceVariant",
        )
        self.unit_field = ft.TextField(
            label="Unidad", hint_text="UND", expand=1, border_color="onSurfaceVariant"
        )
        self.selling_price = ft.TextField(
            label="Precio de venta",
            prefix="$",
            expand=1,
            on_change=self._validate_number,
            border_color="onSurfaceVariant",
        )
        self.add_btn = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="green400",
            icon_size=27,
            tooltip="Añadir producto",
            on_click=self._add_product,
        )
        self.table_row = ft.Row(
            controls=[
                self.description_field,
                self.quantity_field,
                self.unit_field,
                self.selling_price,
                self.add_btn,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        ##### Table info product #####
        self.table_info = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Item"), numeric=True),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Fecha de envío")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Unidad")),
                ft.DataColumn(ft.Text("Precio de venta")),
                ft.DataColumn(ft.Text("Importe")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            data_row_min_height=48,
            data_row_max_height=float("inf"),
        )
        self.table_info_row = ft.Row(
            controls=[self.table_info], spacing=10, alignment=ft.MainAxisAlignment.CENTER
        )

        ##### Other data #####
        self.other_data_title = ft.Row(
            controls=[ft.Text("Otros datos", size=20,
                              weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.pay_type = ft.DropdownM2(
            options=[
                ft.dropdownm2.Option(value) for value in self.settings["pay_types_import"]
            ],
            expand=2,
            hint_text="Seleccione la forma de pago",
            border_color="onSurfaceVariant",
        )
        self.final_time = ft.TextField(
            label="Tiempo de entrega en semanas",
            hint_text="6 a 7",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.currency_field = ft.DropdownM2(
            options=[
                ft.dropdownm2.Option(value) for value in self.settings["currencies"].keys()
            ],
            expand=1,
            hint_text="Seleccione la moneda",
            border_color="onSurfaceVariant",
        )
        self.other_data_row = ft.Row(
            controls=[self.pay_type, self.final_time, self.currency_field],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        ##### Buttons #####
        self.file_picker = None
        self.send_button = ft.Row(
            controls=[
                ft.OutlinedButton(
                    content=ft.Text("Generar cotización", size=18),
                    on_click=self._handle_save_file,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=1,
        )
        self.clear_button = ft.Row(
            controls=[
                ft.OutlinedButton(
                    content=ft.Text("Limpiar campos", size=18),
                    on_click=lambda _: self._clear_fileds(),
                )
            ],
            alignment=ft.MainAxisAlignment.END,
            expand=1,
        )
        self.buttons_row = ft.Row(
            controls=[self.send_button, self.clear_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.error_text = ft.Text("Error:", color="red400")

        ##### Banner #####
        self.banner = ft.Banner(
            bgcolor="green100",
            leading=ft.Icon(ft.Icons.CHECK_CIRCLE_SHARP,
                            color="green", size=40),
            content=ft.Text(
                value="",
                color="black",
            ),
            actions=[],
        )

        self.content = ft.Column(
            controls=[
                self.client_info,
                self.row1,
                self.row2,
                self.product_title,
                self.table_row,
                self.table_info_row,
                self.other_data_title,
                self.other_data_row,
                self.buttons_row,
            ],
            expand=True,
            spacing=20,
        )

    def build(self):
        return ft.Container(content=self.content, expand=True)

    def _validate_number(self, e, is_integer=False):
        field = e.control
        is_number = match(r'^(\d+(\.\d*)?)$', field.value)
        if (not is_number):
            self.page.show_dialog(
                ft.SnackBar(ft.Text("⚠ Solo se permiten números"),
                            duration=3000)
            )
            field.value = field.value[:-1]
            self.page.update()
            return
        if is_integer and field.value[-1] == ".":
            self.page.show_dialog(
                ft.SnackBar(ft.Text("⚠ Solo se permiten números enteros"),
                            duration=3000)
            )
            field.value = field.value[:-1]
            self.page.update()
            return

    def _handle_quotation_type_aux(self):
        quotation_type = self.quotation_type_field.value
        self.table_info.rows.clear()
        if quotation_type == AppConst.quotations_types["IMPORT"]:
            self.pay_type.options = [
                ft.dropdownm2.Option(value) for value in self.settings["pay_types_import"]
            ]
            self.table_row.controls = [
                self.description_field,
                self.quantity_field,
                self.unit_field,
                self.selling_price,
                self.add_btn,
            ]
            self.table_info.columns[0].label.value = "Item"
            self.other_data_row.controls = [
                self.pay_type,
                self.final_time,
                self.currency_field,
            ]
        elif quotation_type == AppConst.quotations_types["STOCK"]:
            self.pay_type.options = [
                ft.dropdownm2.Option(value) for value in self.settings["pay_types_stock"]
            ]
            self.table_row.controls = [
                self.article_code_field,
                self.description_field,
                self.quantity_field,
                self.unit_field,
                self.selling_price,
                self.add_btn,
            ]
            self.table_info.columns[0].label.value = "Código del artículo"
            self.other_data_row.controls = [self.pay_type, self.currency_field]
        self.page.update(
            self.table_row, self.table_info_row, self.pay_type, self.other_data_row
        )

    def _clear_fileds(self):
        self.client_field.value = ""
        self.contact_field.value = ""
        self.cv_field.value = ""
        self.address_field.value = ""
        self.location_field.value = ""
        self.article_code_field.value = ""
        self.description_field.value = ""
        self.quantity_field.value = ""
        self.unit_field.value = ""
        self.selling_price.value = ""
        self.pay_type.value = ""
        self.final_time.value = ""
        self.currency_field.value = ""
        self.table_info.rows.clear()
        self.page.update()

    def _add_product(self):
        product = []
        if self.quotation_type_field.value == AppConst.quotations_types["IMPORT"]:
            id = str(len(self.table_info.rows) + 1)
        elif self.quotation_type_field.value == AppConst.quotations_types["STOCK"]:
            id = self.article_code_field.value.upper()
        product.append(id)
        description = self.description_field.value.upper()
        quantity = self.quantity_field.value
        unit = self.unit_field.value.upper()
        selling_price = self.selling_price.value
        try:
            if len(description) > 0 and len(quantity) > 0 and len(unit) > 0 and len(id) > 0 and len(selling_price) > 0:
                quantity_array = quantity.split(".")
                quantity_format = None
                if len(quantity_array) > 1:
                    quantity_format = float(quantity) if int(
                        quantity_array[1]) > 0 else int(quantity)
                else:
                    quantity_format = int(quantity)
                product.append(description)
                product.append(AppConst.current_date)
                product.append(quantity_format)
                product.append(unit)
                product.append(locale.currency(
                    float(selling_price), grouping=True))
                product.append(
                    locale.currency(quantity_format *
                                    float(selling_price), grouping=True)
                )
            else:
                raise Exception("Data incomplete")
        except Exception as E:
            print(E)
            self.page.show_dialog(
                ft.SnackBar(
                    ft.Text("⚠ Todos los campos son obligatorios"), duration=3000)
            )
            return
        self.table_info.rows.append(
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(prod, selectable=True))
                       for prod in product]
                + [
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                    icon_color="red400",
                                    icon_size=20,
                                    tooltip="Eliminar producto",
                                    on_click=self._delete_product,
                                    key=id,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )
                    )
                ]
            )
        )
        self.description_field.value = ""
        self.quantity_field.value = ""
        self.unit_field.value = ""
        self.selling_price.value = ""
        self.article_code_field.value = ""
        self.page.update()

    def _delete_product(self, e):
        deleted = False
        for row in self.table_info.rows.copy():
            if row.cells[7].content.controls[0].key == e.control.key and not deleted:
                self.table_info.rows.remove(row)
                deleted = True
                continue
            if (
                deleted
                and self.quotation_type_field.value
                == AppConst.quotations_types["IMPORT"]
            ):
                row.cells[0].content.value = int(
                    row.cells[0].content.value) - 1
        self.page.update()

    async def _handle_save_file(self, e):
        try:
            path = await ft.FilePicker().save_file(
                file_type=ft.FilePickerFileType.CUSTOM,
                file_name=f"CV-{self.cv_field.value}-{self.client_field.value.upper()}",
                allowed_extensions=["docx"],
            )
            if path is None:
                raise Exception("None")
            try:
                self.page.remove(self.error_text)
            except:
                pass
            context = {
                "client": self.client_field.value.upper().replace("&", "&amp;"),
                "cv": self.cv_field.value,
                "date": AppConst.current_date,
                "contact": self.contact_field.value.upper(),
                "address": self.address_field.value.upper(),
                "location": self.location_field.value.upper(),
                "currency": self.currency_field.value,
                "pay_type": self.pay_type.value,
                "currency_text": self.settings["currencies"][self.currency_field.value],
                "contact_imocom": self.settings["name"]["contact"].upper(),
                "job_title": self.settings["name"]["job_title"].upper(),
            }
            for value in context.values():
                if len(value) == 0:
                    raise Exception("Data incomplete")
            doc = DocxTemplate("assets/schema.docx")
            products = []
            total_send = 0
            title_header, f_time = get_final_time(
                self.quotation_type_field.value, self.final_time.value
            )
            for row in self.table_info.rows:
                product = {
                    "item": row.cells[0].content.value,
                    "description": row.cells[1].content.value,
                    "send_date": row.cells[2].content.value,
                    "quantity": row.cells[3].content.value,
                    "unit": row.cells[4].content.value,
                    "selling_price": row.cells[5].content.value,
                    "amount": row.cells[6].content.value,
                }
                total_send += locale.atof(product["amount"].strip(
                    "$").strip())
                products.append(product)
            total = total_send
            taxes = total * 0.19
            rounded = round((total + taxes) % 1, 3)
            if rounded >= 0.5:
                rounded = round(1 - rounded, 3)
            else:
                rounded = rounded * (-1)
            final_price = total + taxes + rounded
            context.update(
                {
                    "title_header": title_header,
                    "products": products,
                    "total_send": locale.currency(total_send, grouping=True),
                    "total": locale.currency(total, grouping=True),
                    "taxes": locale.currency(taxes, grouping=True),
                    "rounded": rounded,
                    "final_price": locale.currency(final_price, grouping=True),
                    "final_time": f_time,
                }
            )
            doc.render(context)
            doc.save(path + ".docx")
            self.banner.content.value = get_banner_message(
                path, self.page.platform.value
            )
            banner_controls = []
            if self.page.platform.value != "windows":
                banner_controls.append(
                    ft.TextButton(
                        content="Ok",
                        style=ft.ButtonStyle(color="blue"),
                        on_click=lambda _: self.page.pop_dialog(),
                    )
                )
            else:
                banner_controls.append(
                    ft.Row(
                        controls=[
                            ft.TextButton(
                                content="Si",
                                style=ft.ButtonStyle(color="blue"),
                                on_click=lambda _: self._open_file(path),
                            ),
                            ft.TextButton(
                                content="No",
                                style=ft.ButtonStyle(color="blue"),
                                on_click=lambda _: self.page.pop_dialog(),
                            ),
                        ],
                        expand=True,
                    )
                )

            self.banner.actions = banner_controls
            self.page.show_dialog(self.banner)
        except Exception as E:
            error = str(E)
            print(f"Error: {error}")
            if error != "None":
                self.error_text.value = f"Error: {str(E)}"
                self.page.add(self.error_text)
                self.page.update()
            self.page.show_dialog(
                ft.SnackBar(
                    ft.Text(
                        "⚠ La ventana de guardado fue cerrada, o aún faltan datos para realizar la cotización"
                    ),
                    duration=5000,
                )
            )

    def _open_file(self, path):
        try:
            os.startfile(path + ".docx")
        except Exception as E:
            print(f"Error al abrir el archivo: {E}")
            self.error_text.value = f"Error al abrir el archivo: {str(E)}"
            self.page.add(self.error_text)
        finally:
            self.page.pop_dialog()

    def _load_settings(self):
        with open("config/settings.json", "r", encoding="utf-8") as f:
            settings = json_load(f)
            return settings

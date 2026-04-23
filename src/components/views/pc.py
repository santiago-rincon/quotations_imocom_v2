import flet as ft
from config.constants import AppConst
import locale
import os
from re import match
from docxtpl import DocxTemplate
from json import load as json_load

from utils.utils import get_banner_message

locale.setlocale(locale.LC_ALL, "es_CO.UTF-8")


class PcView(ft.Container):
    def __init__(self):
        super().__init__()
        self.settings = self._load_settings()
        ##### Supplier info #####
        self.supplier_info = ft.Row(
            controls=[
                ft.Text("Información del proveedor",
                        size=20, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.supplier_field = ft.TextField(
            label="Nombre del proveedor",
            hint_text="JINN FA MACHINE INDUSTRIAL CO.LTD.",
            expand=2,
            border_color="onSurfaceVariant",
        )
        self.address_supplier_field = ft.TextField(
            label="Dirección del proveedor",
            hint_text="NO. 12, HENGCHING LANE, YUANCHUNG",
            expand=2,
            border_color="onSurfaceVariant",
        )
        self.contact_supplier_field = ft.TextField(
            label="Contacto del proveedor",
            hint_text="JENNY SHEN",
            expand=2,
            border_color="onSurfaceVariant",
        )
        self.email_supplier_field = ft.TextField(
            label="Correo electrónico",
            hint_text="jinnfa@ms18.hinet.net ",
            expand=2,
            border_color="onSurfaceVariant",
        )

        self.row_supplier = ft.Row(
            controls=[
                self.supplier_field,
                self.address_supplier_field,
                self.contact_supplier_field,
                self.email_supplier_field,
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
            label="P/N or Id. Nr",
            hint_text="M99090259-X11",
            expand=2,
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
        self.price = ft.TextField(
            label="Precio de compra",
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
                self.article_code_field,
                self.description_field,
                self.quantity_field,
                self.price,
                self.add_btn,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        ##### Table info product #####
        self.table_info = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Item"), numeric=True),
                ft.DataColumn(ft.Text("P/N or Id. Nr")),
                ft.DataColumn(ft.Text("Cantidad")),
                ft.DataColumn(ft.Text("Descripción")),
                ft.DataColumn(ft.Text("Precio de compra (unidad)")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            data_row_min_height=48,
            data_row_max_height=float("inf"),
        )

        self.table_info_row = ft.Row(
            controls=[self.table_info], spacing=10, alignment=ft.MainAxisAlignment.CENTER
        )

        ##### PC info #####
        self.pc_info_title = ft.Row(
            controls=[
                ft.Text("Información de la compra",
                        size=20, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.button_pq = ft.Checkbox(
            label="",
            value=True,
            tooltip="¿Hay cotizacion formal del proveedor?",
            on_change=self._handle_checkbox,
        )
        self.ref_of_supplier_field = ft.TextField(
            label="Referencia del proveedor",
            prefix="PQ-",
            expand=1,
            border_color="onSurfaceVariant",
            on_change=lambda e: self._validate_number(e, True),
        )
        self.term_of_payment_field = ft.DropdownM2(
            options=[
                ft.dropdownm2.Option(value) for value in self.settings["terms_of_payment"]
            ],
            expand=1,
            hint_text="Términos de pago",
            border_color="onSurfaceVariant",
        )
        self.currency_field = ft.DropdownM2(
            options=[
                ft.dropdownm2.Option(f"{value[0]} - {value[1]}")
                for value in self.settings["currencies_pv"].items()
            ],
            expand=1,
            hint_text="Seleccione la moneda",
            border_color="onSurfaceVariant",
        )
        self.pc_number_field = ft.TextField(
            label="PC",
            prefix="PC-",
            expand=1,
            on_change=lambda e: self._validate_number(e, True),
            border_color="onSurfaceVariant",
        )
        self.incoterms_list = ft.DropdownM2(
            options=[ft.dropdownm2.Option(value)
                     for value in self.settings["incoterms"]],
            expand=1,
            hint_text="Incoterms",
            border_color="onSurfaceVariant",
        )
        self.pc_info_row = ft.Row(
            controls=[
                self.button_pq,
                self.ref_of_supplier_field,
                self.term_of_payment_field,
                self.currency_field,
                self.pc_number_field,
                self.incoterms_list,
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        ##### Buttons #####
        self.send_button = ft.Row(
            controls=[
                ft.OutlinedButton(
                    content=ft.Text("Generar PC", size=18), on_click=self._handle_save_file
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=1,
        )
        self.clear_button = ft.Row(
            controls=[
                ft.OutlinedButton(
                    content=ft.Text("Limpiar campos", size=18), on_click=self._clear_fileds
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
                self.supplier_info,
                self.row_supplier,
                self.product_title,
                self.table_row,
                self.table_info_row,
                self.pc_info_title,
                self.pc_info_row,
                self.buttons_row,
            ],
            expand=True,
            spacing=25,
        )

    def build(self):
        return ft.Container(
            content=self.content,
            expand=True,
        )

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

    def _clear_fileds(self):
        self.supplier_field.value = ""
        self.address_supplier_field.value = ""
        self.contact_supplier_field.value = ""
        self.email_supplier_field.value = ""
        self.article_code_field.value = ""
        self.description_field.value = ""
        self.quantity_field.value = ""
        self.price.value = ""
        self.table_info.rows.clear()
        self.ref_of_supplier_field.value = ""
        self.term_of_payment_field.value = None
        self.currency_field.value = None
        self.pc_number_field.value = ""
        self.incoterms_list.value = None
        self.button_pq.value = True
        self.page.update()

    def _add_product(self):
        product = []
        id = str(len(self.table_info.rows) + 1)
        product.append(id)
        article = self.article_code_field.value.upper()
        description = self.description_field.value.upper()
        quantity = self.quantity_field.value
        selling_price = self.price.value
        try:
            if (
                len(description) > 0
                and len(article) > 0
                and len(quantity) > 0
                and len(selling_price) > 0
            ):
                quantity_array = quantity.split(".")
                quantity_format = None
                if len(quantity_array) > 1:
                    quantity_format = float(quantity) if int(
                        quantity_array[1]) > 0 else int(quantity)
                else:
                    quantity_format = int(quantity)
                product.append(article)
                product.append(quantity_format)
                product.append(description)
                product.append(locale.currency(
                    float(selling_price), grouping=True))

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
        self.article_code_field.value = ""
        self.description_field.value = ""
        self.quantity_field.value = ""
        self.price.value = ""
        self.page.update()

    def _delete_product(self, e):
        deleted = False
        for row in self.table_info.rows.copy():
            if row.cells[5].content.controls[0].key == e.control.key and not deleted:
                self.table_info.rows.remove(row)
                deleted = True
                continue
            if deleted:
                row.cells[0].content.value = int(
                    row.cells[0].content.value) - 1
        self.page.update()

    async def _handle_save_file(self, e):
        try:
            path = await ft.FilePicker().save_file(
                file_type=ft.FilePickerFileType.CUSTOM,
                file_name=f"PC-{self.pc_number_field.value}-{self.supplier_field.value.upper()}",
                allowed_extensions=["docx"],
            )
            if path is None:
                raise Exception("None")
            try:
                self.page.remove(self.error_text)
            except:
                pass
            try:
                ref_of_supplier = ""
                if self.button_pq.value:
                    ref_of_supplier = " (PQ): PQ-" + \
                        self.ref_of_supplier_field.value
                else:
                    ref_of_supplier = " :" + self.ref_of_supplier_field.value
                context = {
                    "pc_number": self.pc_number_field.value.zfill(
                        self.settings["lenght_pc_number"]
                    ),
                    "date": AppConst.current_date,
                    "supplier": self.supplier_field.value.upper(),
                    "address": self.address_supplier_field.value.upper(),
                    "contact_supplier": self.contact_supplier_field.value.upper(),
                    "email_supplier": self.email_supplier_field.value.lower(),
                    "terms_of_payment": self.term_of_payment_field.value.upper(),
                    "ref_of_supplier": ref_of_supplier,
                    "incoterms": self.incoterms_list.value.upper(),
                    "contact_imocom": self.settings["name"]["contact"].upper(),
                    "email_imocom": self.settings["name"]["email_imocom"].lower(),
                    "dhl": self.settings["dhl"],
                    "currency": self.currency_field.value.split(" - ")[0],
                }
            except Exception as E:
                print(f"Error al construir el contexto: {E}")
                raise Exception("None")
            for value in context.values():
                if len(value) == 0:
                    raise Exception("None")
            doc = DocxTemplate("assets/schema_pc.docx")
            products = []
            total_send = 0
            for row in self.table_info.rows:
                product = {
                    "item": row.cells[0].content.value,
                    "ref_supplier": row.cells[1].content.value,
                    "quantity": row.cells[2].content.value,
                    "description": row.cells[3].content.value,
                    "selling_price": row.cells[4].content.value,
                }

                total_selling_price = locale.atof(product["selling_price"].strip(
                    "$").strip()) * float(product["quantity"])
                product["total_selling_price"] = locale.currency(
                    total_selling_price, grouping=True
                )
                total_send += total_selling_price

                products.append(product)
            context.update(
                {
                    "products": products,
                    "total_send": locale.currency(total_send, grouping=True),
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
                        "⚠ La ventana de guardado fue cerrada, o aún faltan datos para generar la PC"
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

    def _handle_checkbox(self, e):
        value = e.control.value
        if value:
            self.ref_of_supplier_field.prefix = "PQ-"
        else:
            self.ref_of_supplier_field.prefix = ""

    def _load_settings(self):
        with open("config/settings.json", "r", encoding="utf-8") as f:
            settings = json_load(f)
            return settings

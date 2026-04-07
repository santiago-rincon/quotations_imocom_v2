from flet import Container, Row, TextField, DropdownM2, dropdownm2, Text, MainAxisAlignment, FontWeight, IconButton, Icons, DataColumn, DataTable, FilePicker, OutlinedButton, FilePickerFileType, SnackBar, DataCell, DataRow, Column, Banner, ButtonStyle, Icon, TextButton
from config.constants import AppConst
from docxtpl import DocxTemplate
import locale
import os
from re import match
locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')


class CvView(Container):
    def __init__(self):
        super().__init__()

        ##### Client info #####
        self.client_info = Row(controls=[Text("Información del cliente", size=20, weight=FontWeight.BOLD)],
                               alignment=MainAxisAlignment.CENTER)
        self.client_field = TextField(
            label="Cliente", hint_text="Ingresa el nombre del cliente", expand=2, border_color="onSurfaceVariant")
        self.contact_field = TextField(
            label="Contacto del cliente", hint_text="Sra. Angela Cruz", expand=2, border_color="onSurfaceVariant")
        self.cv_field = TextField(
            label="Número de CV", prefix="CV-", on_change=self._validate_number, expand=1, border_color="onSurfaceVariant")
        self.address_field = TextField(
            label="Dirección", hint_text="Parque industrial San Jorge, Bodega 10", expand=1, border_color="onSurfaceVariant")
        self.location_field = TextField(
            label="Ubicación", hint_text="Mosquera, Cundinamarca", expand=1, border_color="onSurfaceVariant")
        self.quotation_type_field = DropdownM2(
            options=[
                dropdownm2.Option(AppConst.quotations_types["IMPORT"]),
                dropdownm2.Option(AppConst.quotations_types["STOCK"]),
            ],
            expand=1,
            hint_text="Seleccione el tipo de cotización",
            on_change=self._handle_quotation_type_aux,
            value=AppConst.quotations_types["IMPORT"],
            border_color="onSurfaceVariant"
        )
        self.row1 = Row(controls=[self.client_field, self.contact_field, self.cv_field],
                        spacing=10, alignment=MainAxisAlignment.SPACE_BETWEEN)
        self.row2 = Row(controls=[self.address_field, self.location_field, self.quotation_type_field],
                        spacing=10, alignment=MainAxisAlignment.SPACE_BETWEEN)

        ##### Product info #####
        self.product_title = Row(controls=[Text("Información del producto", size=20, weight=FontWeight.BOLD)],
                                 alignment=MainAxisAlignment.CENTER)
        self.article_code_field = TextField(
            label="Código del artículo", hint_text="G111000001", expand=1, border_color="onSurfaceVariant")
        self.description_field = TextField(
            label="Descripción", hint_text="Descripción del item", expand=4, border_color="onSurfaceVariant")
        self.quantity_field = TextField(
            label="Cantidad", hint_text="1", expand=1, on_change=self._validate_number, border_color="onSurfaceVariant")
        self.unit_field = TextField(
            label="Unidad", hint_text="UND", expand=1, border_color="onSurfaceVariant")
        self.selling_price = TextField(
            label="Precio de venta", prefix="$", expand=1, on_change=self._validate_number, border_color="onSurfaceVariant")
        self.add_btn = IconButton(
            icon=Icons.ADD,
            icon_color="green400",
            icon_size=27,
            tooltip="Añadir producto",
            on_click=self._add_product
        )
        self.table_row = Row(controls=[self.description_field, self.quantity_field, self.unit_field, self.selling_price, self.add_btn],
                             spacing=10, alignment=MainAxisAlignment.SPACE_BETWEEN)
        ##### Table info product #####
        self.table_info = DataTable(
            columns=[
                DataColumn(Text("Item"), numeric=True),
                DataColumn(Text("Descripción")),
                DataColumn(Text("Fecha de envío")),
                DataColumn(Text("Cantidad")),
                DataColumn(Text("Unidad")),
                DataColumn(Text("Precio de venta")),
                DataColumn(Text("Importe")),
                DataColumn(Text("Acciones"))
            ],
            # width=0.9*self.page.width,
            data_row_min_height=48,
            data_row_max_height=float('inf'),
        )
        self.table_info_row = Row(
            controls=[self.table_info], spacing=10, alignment=MainAxisAlignment.CENTER)

        ##### Other data #####
        self.other_data_title = Row(controls=[Text("Otros datos", size=20, weight=FontWeight.BOLD)],
                                    alignment=MainAxisAlignment.CENTER)
        self.pay_type = DropdownM2(
            options=[dropdownm2.Option(value)
                     for value in AppConst.pay_types_import.values()],
            expand=2,
            hint_text="Seleccione la forma de pago",
            border_color="onSurfaceVariant"
        )
        self.final_time = TextField(
            label="Tiempo de entrega en semanas", hint_text="6 a 7", expand=1, border_color="onSurfaceVariant")
        self.currency_field = DropdownM2(
            options=[dropdownm2.Option(value)
                     for value in AppConst.currencies.keys()],
            expand=1,
            hint_text="Seleccione la moneda",
            border_color="onSurfaceVariant"
        )
        self.imocom_contact = TextField(
            label="Contacto de Imocom", hint_text="Ingresa el nombre del contacto de Imocom", expand=1, border_color="onSurfaceVariant")
        self.job_title = TextField(
            label="Puesto de trabajo", hint_text="Ingresa el puesto de trabajo", expand=1, border_color="onSurfaceVariant")
        self.other_data_row = Row(controls=[
            self.pay_type, self.final_time, self.currency_field], alignment=MainAxisAlignment.SPACE_BETWEEN)
        self.other_data_row2 = Row(controls=[self.imocom_contact,
                                             self.job_title], alignment=MainAxisAlignment.SPACE_BETWEEN)

        ##### Buttons #####
        self.file_picker = None
        self.send_button = Row(controls=[OutlinedButton(content=Text("Generar cotización", size=18),
                               on_click=self._handle_save_file)], alignment=MainAxisAlignment.START, expand=1)
        self.clear_button = Row(controls=[OutlinedButton(
            content=Text("Limpiar campos", size=18), on_click=lambda _: self._clear_fileds())], alignment=MainAxisAlignment.END, expand=1)
        self.buttons_row = Row(
            controls=[self.send_button, self.clear_button], alignment=MainAxisAlignment.SPACE_BETWEEN)

        self.error_text = Text("Error:", color="red400")

        ##### Banner #####
        self.banner = Banner(
            bgcolor="green100",
            leading=Icon(Icons.CHECK_CIRCLE_SHARP,
                         color="green", size=40),
            content=Text(
                value="",
                color="black",
            ),
            actions=[]
        )

        self.content = Column(
            controls=[self.client_info, self.row1, self.row2, self.product_title, self.table_row,
                      self.table_info_row, self.other_data_title, self.other_data_row, self.other_data_row2, self.buttons_row],
            expand=True,
            spacing=20
        )

    def build(self):
        # self.page.overlay.append(self.file_picker)
        return Container(
            content=self.content,
            expand=True,
        )

    def _validate_number(self, e):
        field = e.control
        if (not field.value.isdigit()) and len(field.value) > 0:
            self.page.show_dialog(SnackBar(
                Text("⚠ Solo se permiten números"), duration=3000))
            field.value = field.value[:-1]
            self.page.update()

    def _handle_quotation_type_aux(self):
        quotation_type = self.quotation_type_field.value
        self.table_info.rows.clear()
        if quotation_type == AppConst.quotations_types["IMPORT"]:
            self.pay_type.options = [dropdownm2.Option(value)
                                     for value in AppConst.pay_types_import.values()]
            self.table_row.controls = [
                self.description_field, self.quantity_field, self.unit_field, self.selling_price, self.add_btn]
            self.table_info.columns[0].label.value = "Item"
            self.other_data_row.controls = [
                self.pay_type, self.final_time, self.currency_field]
        elif quotation_type == AppConst.quotations_types["STOCK"]:
            self.pay_type.options = [
                dropdownm2.Option(value) for value in AppConst.pay_types_stock.values()
            ]
            self.table_row.controls = [self.article_code_field, self.description_field,
                                       self.quantity_field, self.unit_field, self.selling_price, self.add_btn]
            self.table_info.columns[0].label.value = "Código del artículo"
            self.other_data_row.controls = [self.pay_type, self.currency_field]
        self.page.update(self.table_row, self.table_info_row,
                         self.pay_type, self.other_data_row)

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
        self.imocom_contact.value = ""
        self.job_title.value = ""
        self.page.update()

    def _add_product(self):
        product = []
        if self.quotation_type_field.value == AppConst.quotations_types["IMPORT"]:
            id = str(len(self.table_info.rows)+1)
        elif self.quotation_type_field.value == AppConst.quotations_types["STOCK"]:
            id = self.article_code_field.value.upper()
        product.append(id)
        description = self.description_field.value.upper()
        quantity = self.quantity_field.value
        unit = self.unit_field.value.upper()
        selling_price = self.selling_price.value
        try:
            if len(description) > 0 and len(quantity) > 0 and len(unit) > 0:
                product.append(description)
                product.append(AppConst.current_date)
                product.append(int(quantity))
                product.append(unit)
                product.append(locale.currency(
                    int(selling_price), grouping=True)[:-3])
                product.append(locale.currency(
                    int(quantity)*int(selling_price), grouping=True)[:-3])
            else:
                raise Exception('Data incomplete')
        except Exception as E:
            print(E)
            self.page.show_dialog(SnackBar(
                Text("⚠ Todos los campos son obligatorios"), duration=3000))
            return
        self.table_info.rows.append(
            DataRow(cells=[DataCell(Text(prod, selectable=True)) for prod in product] + [
                DataCell(Row(controls=[IconButton(
                    icon=Icons.DELETE_FOREVER_ROUNDED,
                    icon_color="red400",
                    icon_size=20,
                    tooltip="Eliminar producto",
                    on_click=self._delete_product,
                    key=id
                )],
                    alignment=MainAxisAlignment.CENTER))
            ])
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
            if deleted and self.quotation_type_field.value == AppConst.quotations_types["IMPORT"]:
                row.cells[0].content.value = int(
                    row.cells[0].content.value) - 1
        self.page.update()

    async def _handle_save_file(self, e):
        try:
            path = await FilePicker().save_file(
                file_type=FilePickerFileType.CUSTOM,
                file_name=f"CV-{self.cv_field.value}-{self.client_field.value.upper()}",
                allowed_extensions=["docx"],
            )
            try:
                self.page.remove(self.error_text)
            except:
                pass
            context = {'client': self.client_field.value.upper(),
                       'cv': self.cv_field.value,
                       'date': AppConst.current_date,
                       'contact': self.contact_field.value.upper(),
                       'address': self.address_field.value.upper(),
                       'location': self.location_field.value.upper(),
                       'currency': self.currency_field.value,
                       'pay_type': self.pay_type.value,
                       'currency_text': AppConst.currencies[self.currency_field.value],
                       'contact_imocom': self.imocom_contact.value.upper(),
                       'job_title': self.job_title.value.capitalize(),
                       }
            for value in context.values():
                if len(value) == 0:
                    raise Exception("Data incomplete")
            doc = DocxTemplate('src/assets/schema.docx')  # development path
            # doc = DocxTemplate('assets/schema.docx')  # production path
            products = []
            total_send = 0
            title_header, f_time = AppConst.get_final_time(
                self.quotation_type_field.value, self.final_time.value)
            for row in self.table_info.rows:
                product = {
                    'item': row.cells[0].content.value,
                    'description': row.cells[1].content.value,
                    'send_date': row.cells[2].content.value,
                    'quantity': row.cells[3].content.value,
                    'unit': row.cells[4].content.value,
                    'selling_price': row.cells[5].content.value,
                    'amount': row.cells[6].content.value
                }
                if match(r'^\$\s?\d{1,3}(?:\.\d{3})*$', product['amount']):
                    total_send += int(product['amount'].replace('.',
                                                                '').replace('$ ', ''))
                elif match(r'^\$\s?\d{1,3}(?:\,\d{3})*$', product['amount']):
                    total_send += int(product['amount'].replace(',',
                                                                '').replace('$ ', ''))
                products.append(product)
            total = total_send
            taxes = total*0.19
            rounded = round((total + taxes) % 1, 3)
            if rounded >= 0.5:
                rounded = round(1 - rounded, 3)
            else:
                rounded = rounded*(-1)
            final_price = total + taxes + rounded
            context.update({
                'title_header': title_header,
                'products': products,
                'total_send': locale.currency(total_send, grouping=True)[:-3],
                'total': locale.currency(total, grouping=True)[:-3],
                'taxes': locale.currency(taxes, grouping=True),
                'rounded': rounded,
                'final_price': locale.currency(final_price, grouping=True),
                'final_time': f_time
            })
            doc.render(context)
            doc.save(path + ".docx")
            self.banner.content.value = AppConst.get_banner_message(
                path, self.page.platform.value)
            banner_controls = []
            if self.page.platform.value != "windows":
                banner_controls.append(TextButton(content="Ok", style=ButtonStyle(
                    color="blue"), on_click=lambda _: self.page.pop_dialog()))
            else:
                banner_controls.append(Row(controls=[
                    TextButton(content="Si", style=ButtonStyle(
                        color="blue"), on_click=lambda _: self._open_file(path)),
                    TextButton(content="No", style=ButtonStyle(
                        color="blue"), on_click=lambda _: self.page.pop_dialog())
                ],
                    expand=True))

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
                SnackBar(Text("⚠ La ventana de guardado fue cerrada, o aún faltan datos para realizar la cotización"), duration=5000))

    def _open_file(self, path):
        try:
            os.startfile(path + ".docx")
        except Exception as E:
            print(f"Error al abrir el archivo: {E}")
            self.error_text.value = f"Error al abrir el archivo: {str(E)}"
            self.page.add(self.error_text)
        finally:
            self.page.pop_dialog()

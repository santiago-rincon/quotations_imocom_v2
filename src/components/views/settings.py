import flet as ft
from json import load as json_load, dump as json_dump

from config.constants import AppConst


class SettingsView(ft.Container):
    def __init__(self):
        super().__init__()
        self.settings = self._load_settings()
        self.title = ft.Row(
            controls=[
                ft.Text("Configuraciones generales",
                        size=24, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        ##### User information #####
        self.tile_name = ft.Row(
            controls=[ft.Text("Información del usuario",
                              size=20, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.START,
        )
        self.name_contact = ft.TextField(
            label="Usuario principal",
            hint_text="Ingresa el nombre del usuario",
            value=self.settings["name"]["contact"],
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.mane_job_title = ft.TextField(
            label="Cargo",
            hint_text="Asistente de línea",
            value=self.settings["name"]["job_title"],
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.name_email = ft.TextField(
            label="Correo electrónico",
            hint_text="email@dominio.com",
            value=self.settings["name"]["email_imocom"],
            expand=1,
            border_color="onSurfaceVariant",
        )

        self.row_user_info = ft.Row(
            controls=[self.name_contact, self.mane_job_title, self.name_email],
            spacing=20,
        )

        ##### Radio Group settings selection #####
        self.title_settings_selection = ft.Row(
            controls=[
                ft.Text(
                    "Selecciona la configuración a editar",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.radio_group = ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value=key, label=value)
                    for key, value in AppConst.settings_views.items()
                ],
            ),
            value="CV",
            on_change=self._handle_radio_group_change,
        )
        self.button_cv_schema = ft.Button(
            content="Abrir esquema de CV",
            icon=ft.Icons.EDIT_DOCUMENT,
            on_click=lambda _: self._open_document(r"assets\schema.docx"),
        )
        self.button_pv_schema = ft.Button(
            content="Abrir esquema de PC",
            icon=ft.Icons.EDIT_DOCUMENT,
            visible=False,
            on_click=lambda _: self._open_document(
                r"assets\schema_pc.docx"),
        )
        self.button_json_settings = ft.Button(
            content="Abrir archivo de configuración",
            icon=ft.Icons.DATA_OBJECT,
            on_click=lambda _: self._open_document(
                r"config\settings.json"),
        )

        self.row_settings_selection = ft.Row(
            controls=[
                self.radio_group,
                ft.Row(
                    controls=[
                        self.button_cv_schema,
                        self.button_pv_schema,
                        self.button_json_settings,
                    ],
                    spacing=10,
                    margin=ft.Margin(right=30),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=1,
            spacing=20,
        )

        ##### currencies CV info #####
        self.title_currencies_cv = ft.Row(
            controls=[
                ft.Text("Información de moneda para CV's",
                        size=20, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.currency_cv = ft.TextField(
            label="Moneda para CV",
            hint_text="USD",
            expand=1,
            border_color="onSurfaceVariant",
            on_change=self._uppercase_on_change,
        )
        self.currency_cv_description = ft.TextField(
            label="Descripción de la moneda",
            hint_text="Dólar estadounidense + IVA liquidados a la TRM del día de facturación",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.add_btn_currency_cv = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="green400",
            icon_size=27,
            tooltip="Añadir moneda",
            on_click=lambda _: self._add_currency("CV"),
        )
        self.row_currencies_cv = ft.Row(
            controls=[
                self.currency_cv,
                self.currency_cv_description,
                self.add_btn_currency_cv,
            ],
            spacing=20,
        )

        ##### Table info currencies CV #####
        self.table_info_currencies_cv = ft.Row(
            controls=[
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Abreviatura de la moneda")),
                        ft.DataColumn(
                            ft.Text("Descripción de la moneda para CV's")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(abr)),
                                ft.DataCell(ft.Text(desc)),
                                ft.DataCell(
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                                icon_color="red400",
                                                icon_size=20,
                                                tooltip="Eliminar moneda",
                                                on_click=lambda e: (
                                                    self._delete_currency(
                                                        e, "CV")
                                                ),
                                                key=abr,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ),
                            ]
                        )
                        for abr, desc in self.settings["currencies"].items()
                    ],
                    data_row_min_height=48,
                    data_row_max_height=float("inf"),
                )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        ##### Pay types importation #####
        self.title_pay_types_import = ft.Row(
            controls=[
                ft.Text(
                    "Tipos de pago para importaciones", size=20, weight=ft.FontWeight.BOLD
                )
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.pay_types_import = ft.TextField(
            label="Tipos de pago para importaciones",
            hint_text="100 % anticipado",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.add_btn_pay_types_import = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="green400",
            icon_size=27,
            tooltip="Añadir tipo de pago",
            on_click=lambda _: self._add_item_to_list(
                self.pay_types_import, self.list_pay_types_import
            ),
        )
        self.row_pay_types_import = ft.Row(
            controls=[
                self.pay_types_import,
                self.add_btn_pay_types_import,
            ],
            spacing=20,
        )

        ##### List info pay types import #####
        self.list_pay_types_import = ft.ListView(
            controls=[
                ft.ListTile(
                    title=pay_type,
                    trailing=ft.IconButton(
                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                        icon_color="red400",
                        icon_size=20,
                        tooltip="Eliminar tipo de pago",
                        on_click=lambda e: self._delete_item_from_list(
                            e, self.list_pay_types_import
                        ),
                        key=pay_type,
                    ),
                )
                for pay_type in self.settings["pay_types_import"]
            ]
        )

        ##### Pay types stock #####
        self.title_pay_types_stock = ft.Row(
            controls=[
                ft.Text("Tipos de pago para stock",
                        size=20, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.pay_types_stock = ft.TextField(
            label="Tipos de pago para stock",
            hint_text="100 % anticipado",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.add_btn_pay_types_stock = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="green400",
            icon_size=27,
            tooltip="Añadir tipo de pago",
            on_click=lambda _: self._add_item_to_list(
                self.pay_types_stock, self.list_pay_types_stock
            ),
        )
        self.row_pay_types_stock = ft.Row(
            controls=[
                self.pay_types_stock,
                self.add_btn_pay_types_stock,
            ],
            spacing=20,
        )

        ##### List info pay types stock #####
        self.list_pay_types_stock = ft.ListView(
            controls=[
                ft.ListTile(
                    title=pay_type,
                    trailing=ft.IconButton(
                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                        icon_color="red400",
                        icon_size=20,
                        tooltip="Eliminar tipo de pago",
                        on_click=lambda e: self._delete_item_from_list(
                            e, self.list_pay_types_stock
                        ),
                        key=pay_type,
                    ),
                )
                for pay_type in self.settings["pay_types_stock"]
            ]
        )

        self.cv_container = ft.Column(
            controls=[
                self.title_currencies_cv,
                self.row_currencies_cv,
                self.table_info_currencies_cv,
                self.title_pay_types_import,
                self.row_pay_types_import,
                self.list_pay_types_import,
                self.title_pay_types_stock,
                self.row_pay_types_stock,
                self.list_pay_types_stock,
            ],
            spacing=24,
            expand=True,
        )

        ##### Imocom Information #####
        self.title_imocom_info = ft.Row(
            controls=[ft.Text("Información para la PC",
                              size=20, weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.START,
        )
        self.dhl_account = ft.TextField(
            label="Cuenta DHL",
            hint_text="Ingresa el número de cuenta DHL",
            value=self.settings["dhl"],
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.lenght_pc_number = ft.TextField(
            label="Longitud del número de PC",
            hint_text="5",
            value=str(self.settings["lenght_pc_number"]),
            expand=1,
            border_color="onSurfaceVariant",
            on_change=self._validate_number,
        )
        self.row_imocom_info = ft.Row(
            controls=[self.dhl_account, self.lenght_pc_number],
            spacing=20,
        )

        ##### currencies PV info #####
        self.title_currencies_pv = ft.Row(
            controls=[
                ft.Text("Información de moneda para PV's",
                        size=20, weight=ft.FontWeight.BOLD)
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        self.currency_pv = ft.TextField(
            label="Moneda para PV's",
            hint_text="USD",
            expand=1,
            border_color="onSurfaceVariant",
            on_change=self._uppercase_on_change,
        )
        self.currency_pv_description = ft.TextField(
            label="Descripción de la moneda",
            hint_text="Dólar estadounidense",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.add_btn_currency_pv = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="green400",
            icon_size=27,
            tooltip="Añadir moneda",
            on_click=lambda _: self._add_currency("PV"),
        )
        self.row_currencies_pv = ft.Row(
            controls=[
                self.currency_pv,
                self.currency_pv_description,
                self.add_btn_currency_pv,
            ],
            spacing=20,
        )

        ##### Table info currencies PV #####
        self.table_info_currencies_pv = ft.Row(
            controls=[
                ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Abreviatura de la moneda")),
                        ft.DataColumn(ft.Text("Nombre moneda para PV's")),
                        ft.DataColumn(ft.Text("Acciones")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(abr)),
                                ft.DataCell(ft.Text(desc)),
                                ft.DataCell(
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                                icon_color="red400",
                                                icon_size=20,
                                                tooltip="Eliminar moneda",
                                                on_click=lambda e: (
                                                    self._delete_currency(
                                                        e, "PV")
                                                ),
                                                key=abr,
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ),
                            ]
                        )
                        for abr, desc in self.settings["currencies_pv"].items()
                    ],
                    data_row_min_height=48,
                    data_row_max_height=float("inf"),
                )
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        ##### Terms of payment #####
        self.title_terms_payment = ft.Row(
            controls=[ft.Text("Condiciones de pago", size=20,
                              weight=ft.FontWeight.BOLD)],
            alignment=ft.MainAxisAlignment.START,
        )
        self.terms_payment = ft.TextField(
            label="Condiciones de pago para importaciones",
            hint_text="Advance",
            expand=1,
            border_color="onSurfaceVariant",
        )
        self.add_btn_terms_payment = ft.IconButton(
            icon=ft.Icons.ADD,
            icon_color="green400",
            icon_size=27,
            tooltip="Añadir condición de pago",
            on_click=lambda _: self._add_item_to_list(
                self.terms_payment, self.list_terms_payment
            ),
        )
        self.row_terms_payment = ft.Row(
            controls=[
                self.terms_payment,
                self.add_btn_terms_payment,
            ],
            spacing=20,
        )

        ##### List info terms payment #####
        self.list_terms_payment = ft.ListView(
            controls=[
                ft.ListTile(
                    title=pay_type,
                    trailing=ft.IconButton(
                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                        icon_color="red400",
                        icon_size=20,
                        tooltip="Eliminar tipo de pago",
                        on_click=lambda e: self._delete_item_from_list(
                            e, self.list_terms_payment
                        ),
                        key=pay_type,
                    ),
                )
                for pay_type in self.settings["terms_of_payment"]
            ]
        )

        self.pv_container = ft.Column(
            controls=[
                self.title_imocom_info,
                self.row_imocom_info,
                self.title_currencies_pv,
                self.row_currencies_pv,
                self.table_info_currencies_pv,
                self.title_terms_payment,
                self.row_terms_payment,
                self.list_terms_payment,
            ],
            spacing=24,
            expand=True,
            visible=False,
        )

        #### Save button ####
        self.save_btn = ft.Row(
            controls=[
                ft.OutlinedButton(
                    content=ft.Text("Guardar configuración", size=18),
                    on_click=self._handle_save_file,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=1,
        )

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
                self.title,
                self.tile_name,
                self.row_user_info,
                self.title_settings_selection,
                self.row_settings_selection,
                self.cv_container,
                self.pv_container,
                self.save_btn,
            ],
            expand=True,
            spacing=24,
        )

    def build(self):
        return ft.Container(content=self.content)

    def _load_settings(self):
        with open("config/settings.json", "r", encoding="utf-8") as f:
            settings = json_load(f)
            return settings

    def _handle_radio_group_change(self):
        selected_value = self.radio_group.value
        if selected_value == "CV":
            self.cv_container.visible = True
            self.pv_container.visible = False
            self.button_cv_schema.visible = True
            self.button_pv_schema.visible = False

        elif selected_value == "PC":
            self.cv_container.visible = False
            self.pv_container.visible = True
            self.button_cv_schema.visible = False
            self.button_pv_schema.visible = True
        self.page.update()

    def _validate_number(self, e):
        field = e.control
        if (not field.value.isdigit()) and len(field.value) > 0:
            self.page.show_dialog(
                ft.SnackBar(ft.Text("⚠ Solo se permiten números"),
                            duration=3000)
            )
            field.value = field.value[:-1]
            self.page.update()

    def _uppercase_on_change(self, e):
        field = e.control
        if field.value[-1:].isalpha():
            field.value = field.value.upper()
        else:
            field.value = field.value[:-1]
            self.page.show_dialog(
                ft.SnackBar(ft.Text("⚠ Solo se permiten letras"),
                            duration=3000)
            )
        self.page.update()

    def _open_document(self, path):
        if self.page.platform.value == "windows":
            import os

            os.startfile(os.path.join(os.getcwd(), path))
            self.page.show_dialog(
                ft.SnackBar(ft.Text("Abriendo documento..."), duration=3000)
            )
        else:
            self.page.show_dialog(
                ft.SnackBar(
                    ft.Text("⚠ Esta función solo está disponible en Windows"),
                    duration=3000,
                )
            )

    def _add_currency(self, mode):
        currency = []
        abrev = ""
        description = ""
        if mode == "CV":
            abrev = self.currency_cv.value.upper()
            description = self.currency_cv_description.value
        else:
            abrev = self.currency_pv.value.upper()
            description = self.currency_pv_description.value
        try:
            if len(description) > 0 and len(abrev) > 0:
                currency.append(abrev)
                currency.append(description)
            else:
                raise ValueError("Todos los campos son obligatorios")
        except Exception as E:
            print(E)
            self.page.show_dialog(
                ft.SnackBar(
                    ft.Text("⚠ Todos los campos son obligatorios"), duration=3000)
            )
            return
        if mode == "CV":
            self.table_info_currencies_cv.controls[0].rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(curr, selectable=True))
                           for curr in currency]
                    + [
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                        icon_color="red400",
                                        icon_size=20,
                                        tooltip="Eliminar moneda",
                                        on_click=lambda e: self._delete_currency(
                                            e, "CV"
                                        ),
                                        key=abrev,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),
                    ]
                )
            )
            self.currency_cv.value = ""
            self.currency_cv_description.value = ""
        else:
            self.table_info_currencies_pv.controls[0].rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(curr, selectable=True))
                           for curr in currency]
                    + [
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                                        icon_color="red400",
                                        icon_size=20,
                                        tooltip="Eliminar moneda",
                                        on_click=lambda e: self._delete_currency(
                                            e, "PV"
                                        ),
                                        key=abrev,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),
                    ]
                )
            )
            self.currency_pv.value = ""
            self.currency_pv_description.value = ""
        self.page.update()

    def _delete_currency(self, e, mode):
        if mode == "CV":
            for row in self.table_info_currencies_cv.controls[0].rows.copy():
                if row.cells[2].content.controls[0].key == e.control.key:
                    self.table_info_currencies_cv.controls[0].rows.remove(row)
                    break
        else:
            for row in self.table_info_currencies_pv.controls[0].rows.copy():
                if row.cells[2].content.controls[0].key == e.control.key:
                    self.table_info_currencies_pv.controls[0].rows.remove(row)
                    break
        self.page.update()

    def _add_item_to_list(self, item, list_view):
        if len(item.value) > 0:
            list_view.controls.append(
                ft.ListTile(
                    title=ft.Text(item.value),
                    trailing=ft.IconButton(
                        icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                        icon_color="red400",
                        icon_size=20,
                        tooltip="Eliminar tipo de pago",
                        # on_click=self._delete_item_from_list,
                        key=item.value,
                    ),
                )
            )
            item.value = ""
            self.page.update()
        else:
            self.page.show_dialog(
                ft.SnackBar(
                    ft.Text("⚠ El campo no puede estar vacío"), duration=3000)
            )

    def _delete_item_from_list(self, e, list_view):
        for item in list_view.controls.copy():
            if item.trailing.key == e.control.key:
                list_view.controls.remove(item)
                break
        self.page.update()

    def _handle_save_file(self, e):
        current_settings = self.settings.copy()
        current_settings["name"]["contact"] = (
            self.name_contact.value.capitalize()
            if len(self.name_contact.value) > 0
            else current_settings["name"]["contact"]
        )
        current_settings["name"]["job_title"] = (
            self.mane_job_title.value.capitalize()
            if len(self.mane_job_title.value) > 0
            else current_settings["name"]["job_title"]
        )
        current_settings["name"]["email_imocom"] = (
            self.name_email.value.lower()
            if len(self.name_email.value) > 0
            else current_settings["name"]["email_imocom"]
        )
        currencies_keys = []
        currencies_values = []
        for row in self.table_info_currencies_cv.controls[0].rows:
            currencies_keys.append(row.cells[0].content.value)
            currencies_values.append(row.cells[1].content.value)
        current_settings["currencies"] = dict(
            zip(currencies_keys, currencies_values))
        current_settings["pay_types_import"] = [
            item.title for item in self.list_pay_types_import.controls
        ]
        current_settings["pay_types_stock"] = [
            item.title for item in self.list_pay_types_stock.controls
        ]
        current_settings["dhl"] = (
            self.dhl_account.value
            if len(self.dhl_account.value) > 0
            else current_settings["dhl"]
        )
        current_settings["lenght_pc_number"] = (
            int(self.lenght_pc_number.value)
            if len(self.lenght_pc_number.value) > 0
            else current_settings["lenght_pc_number"]
        )
        currencies_pv_keys = []
        currencies_pv_values = []
        for row in self.table_info_currencies_pv.controls[0].rows:
            currencies_pv_keys.append(row.cells[0].content.value)
            currencies_pv_values.append(row.cells[1].content.value)
        current_settings["currencies_pv"] = dict(
            zip(currencies_pv_keys, currencies_pv_values)
        )
        current_settings["terms_of_payment"] = [
            item.title for item in self.list_terms_payment.controls
        ]
        try:
            with open("config/settings.json", "w", encoding="utf-8") as f:
                json_dump(current_settings, f, indent=4, ensure_ascii=False)
            self.banner.content.value = "Configuración guardada exitosamente"
            self.banner.bgcolor = "green100"
            self.banner.actions = [
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content="Ok",
                            style=ft.ButtonStyle(color="blue"),
                            on_click=lambda _: self.page.pop_dialog(),
                        ),
                    ],
                    expand=True,
                )
            ]
        except Exception as E:
            print(E)
            self.banner.content.value = "Error al guardar la configuración"
            self.banner.bgcolor = "red100"
            self.banner.leading.icon = ft.Icons.CANCEL
            self.banner.actions = [
                ft.Row(
                    controls=[
                        ft.TextButton(
                            content="Ok",
                            style=ft.ButtonStyle(color="blue"),
                            on_click=lambda _: self.page.pop_dialog(),
                        ),
                    ],
                    expand=True,
                )
            ]
        self.page.show_dialog(self.banner)

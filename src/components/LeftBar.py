from flet import NavigationRail, NavigationRailLabelType, NavigationRailDestination
from components.views.cv import CvView
from components.views.pc import PcView
from components.views.settings import SettingsView


class LeftBar(NavigationRail):
    def __init__(self, dest, selected_index=0):
        super().__init__()
        self.selected_index = selected_index
        self.label_type = NavigationRailLabelType.ALL
        destinations = []
        for destination in dest:
            destinations.append(
                NavigationRailDestination(
                    icon=destination["icon"],
                    label=destination["label"],
                    selected_icon=destination["icon_selected"],
                )
            )
        self.destinations = destinations
        self.on_change = lambda _: self._on_change()

    def build(self):
        return NavigationRail(
            selected_index=self.selected_index,
            label_type=self.label_type,
            destinations=self.destinations,
            on_change=self.on_change,
        )

    def _on_change(self):
        body_control = None
        current_controls = self.page.controls
        for control in current_controls:
            if control.key == "safe_area":
                content = control.content
                controls = content.controls
                for control in controls:
                    if control.key == "body":
                        body_control = control
                        break
                break
        body_control.controls.clear()
        if self.selected_index == 0:
            body_control.controls.append(CvView())
        elif self.selected_index == 1:
            body_control.controls.append(PcView())
        elif self.selected_index == 2:
            body_control.controls.append(SettingsView())

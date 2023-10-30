import sys
import importlib
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QListWidget, QPushButton, \
    QCheckBox


class ModuleWidget(QWidget):
    def __init__(self):
        super(ModuleWidget, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Modules")
        self.search_bar.textChanged.connect(self.filter_modules)
        layout.addWidget(self.search_bar)

        # Checkbox to show/hide submodules
        self.show_submodules_checkbox = QCheckBox("Show Submodules")
        self.show_submodules_checkbox.stateChanged.connect(self.filter_modules)
        layout.addWidget(self.show_submodules_checkbox)

        # List of imported modules
        self.module_list = QListWidget()
        layout.addWidget(self.module_list)

        # Reload button
        self.reload_button = QPushButton("Reload Module")
        self.reload_button.clicked.connect(self.reload_module)
        layout.addWidget(self.reload_button)

        self.setLayout(layout)

        # Populate the module list
        self.populate_module_list()

        self.filter_modules()

    def populate_module_list(self):
        modules = [name for name, _ in list(sys.modules.items()) if name is not None]
        modules.sort()
        self.module_list.addItems(modules)

    def filter_modules(self):
        text = self.search_bar.text().lower()
        show_submodules = self.show_submodules_checkbox.isChecked()

        for i in range(self.module_list.count()):
            item = self.module_list.item(i)
            module_name = item.text()
            module_name_lower = module_name.lower()

            if not show_submodules and '.' in module_name:
                # If submodules should be hidden and the module contains a dot (indicating a submodule),
                # hide it.
                item.setHidden(True)
            elif text in module_name_lower or (
                    show_submodules and any(module_name_lower.startswith(prefix) for prefix in text.split('.'))):
                # If the checkbox is checked or the text matches, show the module.
                item.setHidden(False)
            else:
                item.setHidden(True)

    def reload_module(self):
        selected_item = self.module_list.currentItem()
        if selected_item:
            module_name = selected_item.text()
            try:
                importlib.reload(sys.modules[module_name])
            except Exception as e:
                print(f"Failed to reload module {module_name}: {e}")
            else:
                print(f"Module {module_name} reloaded successfully")


if __name__ == '__main__':
    app_inst = QApplication.instance()
    app = app_inst or QApplication(sys.argv)

    window = QMainWindow()
    module_widget = ModuleWidget()
    window.setCentralWidget(module_widget)
    window.resize(600, 400)
    window.setWindowTitle("Python Module Reloader")
    window.show()

    if not app_inst:
        app.exec_()

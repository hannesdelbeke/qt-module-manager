import sys
import importlib
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QListWidget, QPushButton, \
    QCheckBox, QHBoxLayout
import logging


class ModuleWidget(QWidget):
    def __init__(self):
        super(ModuleWidget, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Horizontal layout for search bar and refresh button
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Modules")
        self.search_bar.textChanged.connect(self.filter_modules)
        search_layout.addWidget(self.search_bar)
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.populate_module_list)
        search_layout.addWidget(self.refresh_button)
        layout.addLayout(search_layout)

        # Checkbox to show/hide submodules
        self.show_submodules_checkbox = QCheckBox("Show Submodules")
        self.show_submodules_checkbox.stateChanged.connect(self.filter_modules)
        layout.addWidget(self.show_submodules_checkbox)

        # List of imported modules
        self.module_list = QListWidget()
        layout.addWidget(self.module_list)

        # Button layout for Reload and Remove buttons
        button_layout = QHBoxLayout()
        self.reload_button = QPushButton("Reload Module")
        self.reload_button.clicked.connect(self.reload_module)
        button_layout.addWidget(self.reload_button)
        self.remove_button = QPushButton("Remove Module")
        self.remove_button.clicked.connect(self.remove_module)
        button_layout.addWidget(self.remove_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.populate_module_list()

    def populate_module_list(self):
        self.module_list.clear()
        modules = [name for name, _ in list(sys.modules.items()) if name is not None]
        modules.sort()
        self.module_list.addItems(modules)

        self.filter_modules()


    def filter_modules(self):
        text = self.search_bar.text().lower()
        show_submodules = self.show_submodules_checkbox.isChecked()

        for i in range(self.module_list.count()):
            item = self.module_list.item(i)
            module_name = item.text()
            module_name_lower = module_name.lower()

            if not show_submodules and '.' in module_name:
                item.setHidden(True)
            elif text in module_name_lower or (show_submodules and any(module_name_lower.startswith(prefix) for prefix in text.split('.'))):
                item.setHidden(False)
            else:
                item.setHidden(True)

    def reload_module(self):
        for selected_item in self.module_list.selectedItems():
            module_name = selected_item.text()
            try:
                importlib.reload(sys.modules[module_name])
            except Exception as e:
                logging.error(f"Failed to reload module {module_name}: {e}")
            else:
                print(f"Module {module_name} reloaded successfully")

    def remove_module(self):
        for item in self.module_list.selectedItems():
            module_name = item.text()
            self.module_list.takeItem(self.module_list.row(item))
            if module_name in sys.modules:
                del sys.modules[module_name]
            else:
                logging.warning(f"Tried to remove an already removed module {module_name}")


if __name__ == '__main__':
    app_inst = QApplication.instance()
    app = app_inst or QApplication(sys.argv)

    window = QMainWindow()
    module_widget = ModuleWidget()
    window.setCentralWidget(module_widget)
    window.resize(600, 400)
    window.setWindowTitle("Python Module Manager")
    window.show()

    if not app_inst:
        app.exec_()

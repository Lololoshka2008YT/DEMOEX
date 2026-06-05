"""Точка входа в приложение."""

import sys
import faulthandler
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QFont, QIcon

from DataBase.database import Database
from UserInterface.login_window import LoginWindow
from UserInterface.product_card import icon_path

faulthandler.enable()

# Палитра по ТЗ:
#   основной фон    — белый (#FFFFFF)
#   дополнительный  — #ABCFCE (панели, обычные кнопки)
#   акцент действия — #546F94 (целевые кнопки: Войти, Сохранить, Добавить…)
#   скидка > 25%    — #23E1EF (задаётся в карточке товара)
APP_STYLESHEET = """
QWidget#screen { background-color: #FFFFFF; }
QFrame#topbar, QFrame#toolbar { background-color: #ABCFCE; }
QPushButton {
    background-color: #ABCFCE;
    border: 1px solid #546F94;
    border-radius: 4px;
    padding: 4px 12px;
}
QPushButton:hover { background-color: #546F94; }
QPushButton#accent {
    background-color: #ABCFCE;
    border: 1px solid #546F94;
    font-weight: bold;
}
QPushButton#accent:hover { background-color: #546F94; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QDateEdit {
    background-color: #FFFFFF;
}
"""


def _excepthook(exc_type, exc_value, exc_tb):
    """Перехватывает исключения в слотах Qt: показывает их и НЕ роняет процесс."""
    text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(text, file=sys.stderr)
    try:
        QMessageBox.critical(None, "Необработанная ошибка",
                             f"{exc_type.__name__}: {exc_value}")
    except Exception:
        pass


sys.excepthook = _excepthook


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # шрифт Comic Sans MS для всего приложения
    app.setFont(QFont("Comic Sans MS", 10))
    # иконка приложения (из ресурсов), если найдена
    ico = icon_path()
    if ico:
        app.setWindowIcon(QIcon(ico))
    # цветовая схема
    app.setStyleSheet(APP_STYLESHEET)

    try:
        db = Database()
    except Exception as e:
        QMessageBox.critical(
            None, "Ошибка подключения к БД",
            f"Не удалось подключиться к базе данных:\n{e}\n\n"
            "Проверьте настройки в constants.py и что PostgreSQL запущен.")
        sys.exit(1)

    window = LoginWindow(db)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
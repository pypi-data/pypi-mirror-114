"""Provide 'about' and 'help' windows.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
from importlib.resources import path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QShowEvent
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class AboutWindow(QWidget):
    """A window used to present application information.

    Notes
    -----
    Methods whose names are written in mixedCase are overridden
    QWidget methods.

    """

    def __init__(self, main_win: QMainWindow) -> None:
        """Construct an AboutWindow instance.

        Parameters
        ----------
        main_win
            The AboutWindow's parent window.

        Returns
        -------
        None

        """
        super().__init__()
        self.main_win = main_win
        self.setWindowTitle("About - filmbuff")

        self.title = QLabel()
        self.title.setText("filmbuff")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(
            "font-weight: bold;"
            "font-size: 26px;"
            "padding-top: 0;"
            "padding-bottom: 4px;"
        )

        self.description = QLabel()
        self.description.setText(
            "Create and manage local databases of film information."
        )
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setStyleSheet(
            "padding: 4px;"
        )

        self.copyright_info = QLabel()
        self.copyright_info.setText(
            "filmbuff Copyright © 2021 emerac\n"
            "<https://gitlab.com/emerac/filmbuff>"
        )
        self.copyright_info.setAlignment(Qt.AlignCenter)
        self.copyright_info.setStyleSheet(
            "font-size: 12px;"
            "padding: 4px;"
        )

        self.disclaimer = QLabel()
        self.disclaimer.setText(
            "This program comes with ABSOLUTELY NO WARRANTY. This is free\n"
            "software, and you are welcome to redistribute it under certain\n"
            "conditions. You should have received a copy of the GNU General\n"
            "Public License along with this program. If not, see:\n"
            "<https://www.gnu.org/licenses/gpl-3.0.txt>."
        )
        self.disclaimer.setAlignment(Qt.AlignCenter)
        self.disclaimer.setStyleSheet(
            "font-size: 12px;"
            "padding-top: 4px;"
            "padding-bottom: 8px;"
        )

        self.logo_container = QHBoxLayout()
        self.logo_container.setAlignment(Qt.AlignCenter)
        self.tmdb_logo = QSvgWidget()
        with path("filmbuff.resources", "tmdb_logo.svg") as logo_path:
            self.tmdb_logo.load(str(logo_path))
        # Scaled to ~40% of original dimensions.
        self.tmdb_logo.setFixedSize(109, 14)
        self.logo_container.addWidget(self.tmdb_logo)

        self.attribution = QLabel()
        self.attribution.setText(
            "This product uses the TMDb API but is not endorsed or certified\n"
            "by TMDb."
        )
        self.attribution.setAlignment(Qt.AlignCenter)
        self.attribution.setStyleSheet(
            "font-size: 12px;"
            "padding-top: 4px;"
            "padding-bottom: 0;"
        )

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addWidget(self.description)
        main_layout.addWidget(self.copyright_info)
        main_layout.addWidget(self.disclaimer)
        main_layout.addLayout(self.logo_container)
        main_layout.addWidget(self.attribution)
        self.setLayout(main_layout)

    def showEvent(self, event: QShowEvent) -> None:
        """Handle QShowEvents.

        This method waits for QShowEvents to occur. When a QShowEvent is
        received, the window will be made to be centered over the parent
        window.

        Parameters
        ----------
        event
            Information about the show event that occurred.

        Returns
        -------
        None

        Notes
        -----
        This is an overridden baseclass (QWidget) method.

        This method handles QShowEvents, which are automatically
        produced in response to widget show signals. When a QShowEvent
        occurs, the QShowEvent is automatically forwarded to this
        method. QShowEvents can be manufactured and passed to this
        method as well.

        """
        super().showEvent(event)
        self.center_window()
        self.setFixedSize(self.width(), self.height())

    def center_window(self) -> None:
        """Center the window over its parent window.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        frame_width = self.main_win.frameGeometry().width()
        win_width = self.main_win.width()
        header_width = frame_width - win_width

        frame_height = self.main_win.frameGeometry().height()
        win_height = self.main_win.height()
        header_height = frame_height - win_height

        center_x = self.main_win.x() + header_width + 0.5 * win_width
        center_y = self.main_win.y() + header_height + 0.5 * win_height
        win_x = center_x - 0.5 * self.width()
        win_y = center_y - 0.5 * self.height()
        self.move(int(win_x), int(win_y))


class HelpWindow(QWidget):
    """A window used to present application help.

    Notes
    -----
    Methods whose names are written in mixedCase are overridden
    QWidget methods.

    """

    def __init__(self, main_win: QMainWindow) -> None:
        """Construct a HelpWindow instance.

        Parameters
        ----------
        main_win
            The HelpWindow's parent window.

        Returns
        -------
        None

        """
        super().__init__()
        self.main_win = main_win
        self.setWindowTitle("Help - filmbuff")

        with path("filmbuff.resources", "help.md") as text_path:
            with open(text_path) as f:
                self.text = f.read()
        self.display = QTextEdit(self.text)
        self.display.setMarkdown(self.text)
        self.display.setReadOnly(True)

        main_win_palette = self.main_win.palette()
        background_color = main_win_palette.color(
            QPalette.Normal,
            QPalette.Window,
        )
        display_palette = self.display.palette()
        display_palette.setColor(
            QPalette.Normal,
            QPalette.Base,
            background_color,
        )
        display_palette.setColor(
            QPalette.Inactive,
            QPalette.Base,
            background_color,
        )
        self.display.setPalette(display_palette)
        self.display.setViewportMargins(10, 5, 10, 5)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.display)
        self.setLayout(self.main_layout)

    def showEvent(self, event: QShowEvent) -> None:
        """Handle QShowEvents.

        This method waits for QShowEvents to occur. When a QShowEvent is
        received, the window will be made to be centered over the parent
        window.

        Parameters
        ----------
        event
            Information about the show event that occurred.

        Returns
        -------
        None

        Notes
        -----
        This is an overridden baseclass (QWidget) method.

        This method handles QShowEvents, which are automatically
        produced in response to widget show signals. When a QShowEvent
        occurs, the QShowEvent is automatically forwarded to this
        method. QShowEvents can be manufactured and passed to this
        method as well.

        """
        super().showEvent(event)
        self.resize_window()
        self.center_window()

    def center_window(self) -> None:
        """Center the window over its parent window.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        frame_width = self.main_win.frameGeometry().width()
        win_width = self.main_win.width()
        header_width = frame_width - win_width

        frame_height = self.main_win.frameGeometry().height()
        win_height = self.main_win.height()
        header_height = frame_height - win_height

        center_x = self.main_win.x() + header_width + 0.5 * win_width
        center_y = self.main_win.y() + header_height + 0.5 * win_height
        win_x = center_x - 0.5 * self.width()
        win_y = center_y - 0.5 * self.height()
        self.move(int(win_x), int(win_y))

    def resize_window(self) -> None:
        self.resize(500, 600)

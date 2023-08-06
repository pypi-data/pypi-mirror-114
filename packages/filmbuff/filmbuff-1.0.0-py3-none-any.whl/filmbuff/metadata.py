"""A window for searching for, choosing, and adding film metadata.

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
from typing import Any, Dict, Optional

from PyQt5.QtGui import (
    QCloseEvent,
    QIntValidator,
    QShowEvent,
)
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)
import requests

from filmbuff import extdata


class EmptyErrorDialog(QMessageBox):
    """A dialog for displaying errors resulting from empty fields."""

    def __init__(self, field: str, parent: Optional[QWidget] = None) -> None:
        """Construct an EmptyErrorDialog instance.

        Parameters
        ----------
        field
            The field that is missing contents.
        parent
            The EmptyErrorDialog's parent widget.

        Returns
        -------
        None

        """
        super().__init__(parent)
        self.setWindowTitle("Search error")
        self.setText(f"The {field} field is required.")
        self.setInformativeText(f"Please enter a {field} and try again.")
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)


class MetadataWindow(QWidget):
    """A window for retrieving metadata from an external source."""

    def __init__(self, main_win: QMainWindow) -> None:
        """Construct a MetadataWindow instance.

        Parameters
        ----------
        main_win
            The MetadataWindow's parent window.

        Returns
        -------
        None

        """
        super().__init__()
        self.main_win = main_win

        self.setWindowTitle("Retrieve metadata - filmbuff")
        self.resize(500, 600)

        query_label = QLabel("Query")
        self.query_field = QLineEdit()
        self.query_field.textChanged.connect(self.field_changed)
        year_label = QLabel("Year (optional)")
        self.year_field = QLineEdit()
        self.year_field.setValidator(QIntValidator(1, 3000))
        self.year_field.textChanged.connect(self.field_changed)
        key_label = QLabel("TMDB API key")
        self.key_field = QLineEdit()
        self.key_field.setEchoMode(QLineEdit.Password)
        self.key_field.textChanged.connect(self.field_changed)
        remember_label = QLabel("Remember key for session")
        self.remember_box = QCheckBox()
        self.remember_box.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Preferred,
        )
        self.search_button = QPushButton("Search")
        self.search_button.setAutoDefault(True)
        self.search_button.pressed.connect(self.search_pressed)
        self.progressbar = QProgressBar()
        self.progressbar.hide()
        self.tree = QTreeWidget()
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(["ID", "Year", "Title", "Lead", "Director"])
        self.tree.hideColumn(0)
        self.tree.setIndentation(0)
        self.tree.itemDoubleClicked.connect(self.add_item)
        self.tree.itemSelectionChanged.connect(self.toggle_add_button)
        self.results_label = QLabel("No results currently displayed.")
        self.load_button = QPushButton("Load more")
        self.load_button.setAutoDefault(True)
        self.load_button.setDisabled(True)
        self.load_button.pressed.connect(self.load_pressed)
        self.add_button = QPushButton("Add data")
        self.add_button.setAutoDefault(True)
        self.add_button.setDisabled(True)
        self.add_button.pressed.connect(self.add_item)
        self.search_spacer = QWidget()
        self.search_spacer.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )
        button_spacer = QWidget()
        button_spacer.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )

        form_layout = QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        form_layout.addRow(query_label, self.query_field)
        form_layout.addRow(year_label, self.year_field)
        form_layout.addRow(key_label, self.key_field)
        remember_layout = QHBoxLayout()
        remember_layout.addWidget(self.remember_box)
        remember_layout.addWidget(remember_label)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.search_spacer)
        search_layout.addWidget(self.progressbar)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(button_spacer)
        buttons_layout.addWidget(self.add_button)
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(remember_layout)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.tree)
        main_layout.addWidget(self.results_label)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.results: Optional[Dict[str, Any]] = {}
        self.query = ""
        self.year = ""
        self.key = ""
        self.next_page = 1

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle QCloseEvents.

        This method waits for QCloseEvents to occur. Given a
        QCloseEvent, it will ensure that all fields are cleared and
        all attributes reset. The key field will not be reset if its
        corresponding checkbox is checked.

        Parameters
        ----------
        event
            Information about the close event that occurred.

        Returns
        -------
        None

        Notes
        -----
        This is an overridden baseclass (QWidget) method.

        This method handles QCloseEvents, which are automatically
        produced in response to widget close signals. When a QCloseEvent
        occurs, the QCloseEvent is automatically forwarded to this
        method. QCloseEvents can be manufactured and passed to this
        method as well.

        """
        super().closeEvent(event)
        self.results = {}
        self.query = ""
        self.query_field.setText(self.query)
        self.year = ""
        self.year_field.setText(self.year)
        if not self.remember_box.isChecked():
            self.key = ""
            self.key_field.setText(self.key)
        self.results_label.setText("No results currently displayed.")
        self.tree.clear()
        self.next_page = 1

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
        self.query_field.setFocus()

    def add_item(self) -> None:
        """Add a filled-in record to the parent window's model.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        Because the tree widget only contains a portion of all the
        information available, choosing to add a particular tree widget
        item will make a request for all of that item's information.

        """
        selection = self.tree.selectedItems()
        selection_id = int(selection[0].text(0))

        info = extdata.get_film_info(self.key, selection_id)
        cast = extdata.get_cast(info)
        director = extdata.get_director(info)
        genres = extdata.get_genres(info)
        record_data = [
            info["budget"],
            cast[0],
            cast[1],
            cast[2],
            None,
            None,
            director,
            genres[0],
            genres[1],
            genres[2],
            None,
            info["imdb_id"],
            None,
            info["original_language"],
            info["original_title"],
            info["overview"],
            info["popularity"],
            info["production_countries"][0]["iso_3166_1"],
            info["release_date"],
            info["revenue"],
            info["runtime"],
            info["spoken_languages"][0]["iso_639_1"],
            info["status"],
            info["tagline"],
            info["title"],
            info["id"],
            info["vote_average"],
            info["vote_count"],
        ]
        new_record = self.main_win.model.record(-1)
        for i in range(new_record.count()):
            if new_record.fieldName(i) == "id":
                continue
            new_record.setValue(i, record_data[i])
        self.main_win.insert_rows(False, record=new_record)

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

    def field_changed(self) -> None:
        """Toggle the state of the load button based on field contents.

        When any of the fields are changed, disable the load button to
        prevent results from a different query from being returned.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        if (
            not self.query_field.text() == self.query
            or not self.year_field.text() == self.year
            or not self.key_field.text() == self.key
        ):
            self.load_button.setDisabled(True)
        else:
            self.toggle_load_button()

    def load_pressed(self) -> None:
        """Perform a search when the load button is pressed.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Notes
        -----
        This method directly calls `perform_search`, which increments
        the page number after each call. When this method is called, it
        is assumed that the page number has been incremented and that
        the page count is greater than one.

        """
        self.perform_search()

    def perform_search(self) -> None:
        """Perform a search when the search button is pressed.

        This method uses the information provided in the fields to
        obtain search results from an external source. The results are
        then displayed in the tree widget.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.results = self.retrieve_results()
        if self.results is None:
            return

        self.search_spacer.hide()
        self.progressbar.show()
        # Normally, events are processed only after a function ends, but
        # the show/hide calls above need to be performed right now.
        QApplication.processEvents()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(len(self.results["results"]))

        for i, r in enumerate(self.results["results"]):
            r_info = extdata.get_film_info(self.key, r["id"])
            r_id = str(r_info["id"])
            r_year = r_info["release_date"][:4]
            r_title = r_info["title"]
            r_lead = extdata.get_cast(r_info)[0]
            r_director = extdata.get_director(r_info)

            raw_data = [r_id, r_year, r_title, r_lead, r_director]
            data = [x if x is not None else "Unavailable" for x in raw_data]

            item = QTreeWidgetItem(data)
            self.tree.addTopLevelItem(item)
            self.progressbar.setValue(i)

        self.results_label.setText(
            f"Displaying {self.tree.topLevelItemCount()} of "
            f"{self.results['total_results']} results."
        )

        # Subsequent searches should obtain subsequent pages.
        self.next_page = self.next_page + 1
        self.toggle_load_button()

        self.search_spacer.show()
        self.progressbar.reset()
        self.progressbar.hide()
        self.resize_columns()

    def resize_columns(self) -> None:
        """Ensure columns do not get pushed out of the viewport.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        for i in range(self.tree.columnCount()):
            self.tree.resizeColumnToContents(i)
            if self.tree.columnWidth(i) > 150:
                self.tree.setColumnWidth(i, 150)
            if not i == self.tree.columnCount() - 1:
                new_width = self.tree.columnWidth(i) + 16
                self.tree.setColumnWidth(i, new_width)

    def retrieve_results(self) -> Optional[Dict[str, Any]]:
        """Obtain search results from an external source.

        Parameters
        ----------
        None

        Returns
        -------
        optional dict of str and Any
            Search results in json form.

        Raises
        ------
        requests.exceptions.HTTPError
            If a 401 (unauthorized) or 404 (connection) error occurred.

        """
        try:
            results = extdata.get_search_results(
                self.key,
                self.query,
                page=self.next_page,
                year=self.year,
            )
        except requests.exceptions.HTTPError as e:
            UnauthorizedErrorDialog(e, self).exec()
            return None
        return results

    def search_pressed(self) -> None:
        """Perform a search when the search button is pressed.

        This method clears the tree widget of any contents to
        accommodate new search results.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        self.query = self.query_field.text()
        if self.query == "":
            EmptyErrorDialog("query", self).exec()
            return
        self.year = self.year_field.text()
        self.key = self.key_field.text()
        if self.key == "":
            EmptyErrorDialog("key", self).exec()
            return

        self.tree.clear()
        self.next_page = 1
        self.perform_search()

    def toggle_add_button(self) -> None:
        """Change the add button's state based on the tree selection.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        if self.tree.selectedItems():
            self.add_button.setDisabled(False)
        else:
            self.add_button.setDisabled(True)

    def toggle_load_button(self) -> None:
        """Change the load button's state based on the search results.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        if self.results:
            if self.next_page <= self.results["total_pages"]:
                self.load_button.setDisabled(False)
            else:
                self.load_button.setDisabled(True)


class UnauthorizedErrorDialog(QMessageBox):
    """A dialog for displaying errors resulting from bad requests."""

    def __init__(
        self,
        error: requests.exceptions.HTTPError,
        parent: Optional[QWidget] = None,
    ) -> None:
        """Construct an UnauthorizedErrorDialog instance.

        Parameters
        ----------
        error
            The HTTPError object provided by `requests.get`.
        parent
            The EmptyErrorDialog's parent widget.

        Returns
        -------
        None

        """
        super().__init__(parent)
        self.setWindowTitle("Search error")
        self.setText(
            f"Error {error.response.status_code} - {error.response.reason}",
        )
        self.setInformativeText(
            "The supplied key was rejected. It may contain a typo "
            "or it may no longer be valid."
        )
        self.setDetailedText(
            "Status message returned:\n"
            f"{error.response.json()['status_message']}\n"
        )
        self.setIcon(QMessageBox.Warning)
        self.setStandardButtons(QMessageBox.Ok)

General information
-------------------

filmbuff is a database front-end for managing film information. In other words,
filmbuff is a graphical user interface (GUI) application used to access and
modify film data contained in a database.

filmbuff is designed to appear and function in the same manner as a general
spreadsheet editor. This means that much of the same functionality is present
in filmbuff, such as opening sheets, inserting rows, moving and sorting
columns, etc. Here are a few things keep in mind:

* As filmbuff is a database front-end, it manages SQLite databases. SQLite
databases are stored on your computer just like any other file.

* Because filmbuff is specifically designed to manage film information,
filmbuff only supports databases created by filmbuff.

* filmbuff supports importing data from and exporting data to the tab-separated
value (TSV) format. Many other programs (especially spreadsheet editors)
support importing/exporting TSV files, which allows data to be passed between
programs.

* To aid in data entry, filmbuff includes the ability to access an API
(application programming interface - usually used to retrieve information from
a web service) provided by [TMDb](https://www.themoviedb.org/) (The Movie
Database). The [TMDb API](https://www.themoviedb.org/documentation/api) can be
used to search for and retrieve information about films. Obtaining a key from
TMDb is required in order to be able to use this functionality.


Describing the interface
------------------------

Upon opening filmbuff for the first time, you will notice a large blank area.
This is where all of your entries are stored and where you will edit them.
Just above this area, there is a row that has been divided into columns with
each column reading something like **Budget** **Cast one** etc. Collectively,
this is the header. Above the header is the toolbar, which provides easy-access
to much of filmbuff's functionality. The field to the right of the toolbar is
the searchbar. Using this, you can create a query to filter your entries.
Lastly, above the toolbar and the searchbar is the menubar, which provides
access to all available filmbuff commands.


Adding, editing, and removing entries
-------------------------------------

To get started creating entries, press the **+** button in the toolbar just
above the headers. This will insert a new row into the database.

* There are usually multiple ways to perform the same action. Pressing **+** in
the toolbar is the same as choosing **Sheet - Add row** in the menubar or
pressing the key combination **Ctrl++** (i.e. press **Ctrl+Shift+=**). Key
combinations are listed next to their respective menu actions.

When a row is inserted, all of its cells are empty except for those in the
**ID** column. This number represents the database's internal ID for that row. This
column is not editable and can be mostly disregarded (see the section
*Modifying column appearance* to learn how to hide columns).

Each row consists of a number of cells that can be edited. To edit a cell,
click on one and then start typing. Familiar shortcuts for editing and
navigation are supported, such as:

* **Scroll** scrolls through rows
* **Alt+Scroll** scrolls through columns
* **Enter** cycles through row selections
* **Tab** cycles through column selections
* **F2** edits the currently-selected cell

When you wish to delete a row, select the row you want to delete and then
choose **Sheet - Remove selected row(s)** in the menubar. This command removes
all selected rows. Multiple rows can be selected by **Ctrl**-clicking the ones
you would like to delete. Alternatively, you can select multiple rows by
clicking and holding the left mouse button over a cell and dragging across all
of the rows you would like to remove.

* Using the remove command while any part of a row (an individual cell or
the entire row) is selected will remove the row that the selection is part
of.

* Row insertions and deletions can be undone (**Edit - Undo**) and redone
(**Edit - Redo**). Complex operations such as row edits and importing data
cannot be undone.


Retrieving metadata
-------------------

To aid in data entry, filmbuff includes the ability to access the
[TMDb API](https://www.themoviedb.org/documentation/api) to search for and
retrieve information about films. Obtaining a key from TMDb is required in
order to be able to use this functionality. TMDb API keys can be obtained by
creating a free account at [themovidedb.org](https://www.themoviedb.org/) and
then requesting a key for personal use.

After obtaining an API key, open the metadata retrieval window by choosing
**Sheet - Retrieve metadata** in the menubar. Enter a query into the **Query**
field. The query is usually text that might be found in a film's title or
description. A four-digit year may be optionally supplied to narrow search
results to a particular release year. Lastly, include your TMDb API key and
then press **Search**. The results will be loaded into the window below.
In this window, you may click an item to select it. Once selected, pressing
**Add data** will cause that film's data to be retrieved and added as a new row
in your database.

* Results are returned in pages (20 per page). If your query returns more than
20 results, you may load more results by pressing **Load more**. This button is
disabled if there are no more results to load.

* Closing the metadata retrieval window will reset the window to its default
state (all fields are cleared).

* You may find that, during a session, you use this window quite a lot. For
convenience, you can click the **Remember key for session** checkbox below the
**TMDB API Key** field. Now, when you close and reopen the metadata retrieval
window, everything except for the API key will be cleared.
    * For security purposes, there is no option to store a key across sessions.


Basic searching
---------------

The searchbar can be used to filter out rows that do not match a query. To
perform a search, simply enter the text you would like to search for into the
searchbar and press **Enter**.

* As a shortcut, press **Ctrl-F** to focus on searchbar.

* Searches are case insensitive.

* To clear the current filter, clear the searchbar of any text.

When you enter a plain piece of text, any rows that contain that text will be
returned. This means that searching for *boat* may return a film with the word
*boat* in its **Title** column, **Overview** column, etc.


Advanced searching
------------------

There is special syntax you can use to refine your search. For example, if you
would like to search for *boat* only when it appears in the **Title** column,
you would enter *"title":"boat"* into the searchbar. Thus, the pattern is: the
column you would like search for in double quotes, a colon, the search term in
double quotes.

* If you encounter a syntax error, make sure there are no spaces on either
side of the colon. This is a common mistake.

This syntax can be expanded to search across multiple columns and/or for
multiple terms by using the *and* and *or* keywords. Here are a few examples:

* *"title":"boat" or "title":"ship"* searches for rows whose **Title** column
contains *boat* or *ship*.
* *"title":"boat" and "title":"ship"* searches for rows whose **Title** column
contains *boat* and *ship*.
* *"title":"boat" and "director":"john"* searches for rows whose **Title**
column contains *boat* and whose **Director** column contains *john*.
* *"genre one":"comedy" or "genre two":"comedy" or "genre three":"comedy"*
searches for rows whose **Genre one**, **Genre two**, or **Genre three**
columns contain *comedy*.

The last example above is quite tedious to type considering you just want to
know if a film is a comedy or not. It is for this reason that another bit of
syntax exists specifically for the cast and genre columns. Here are two
more examples:

* *"genre":"comedy"* searches for rows whose **Genre one**, **Genre two**, or
**Genre three** columns contain *comedy*.
* *"cast":"frank"* searches for rows whose **Cast one**, **Cast two**, or
**Cast three** columns contain *frank*.

However, it is discouraged to use the abbreviated syntax above when you wish to
search across more than just that group of columns (e.g. all genre columns
and the **Title** column). The reason for this is that the abbreviated syntax
is actually expanded to become its longer equivalent. So, in effect, you may
end up in this situation:

* Your intent is to search for any row that is a *comedy* with *boat* in the
title so you enter *"genre":"comedy" and "title":"boat"*.
* You receive a bunch of seemingly weird results because your search was
expanded to *"genre one":"comedy" or "genre two":"comedy" or "genre three":
"comedy" and "title":"boat"* (i.e. return rows where the **Genre one** column
contains *comedy*, plus rows where the **Genre two** column contains *comedy*,
plus rows where the **Genre three** column contains comedy and the **Title**
column contains *boat*).


Saving files
------------

After making a few edits, you can save your work by choosing
**File - Save as...** in the menubar. This opens a window asking you where and
under what name you would like to save your database.

* The default location for storing databases is usually
**~/.local/share/filmbuff**, but you may save your databases in any location of
your choosing.

* All database files must be saved with a **.sqlite** extension. If you do not
enter a file extension, the database will be saved with a **.sqlite** extension
automatically.

When editing a database that exists in your filesystem, you need only use the
**File - Save** command, unless you wish to rename or create a copy of the
current database with **File - Save as...**.

* filmbuff will prompt you to save your work if the current sheet contains
unsaved work. This rarely happens in practice, though, because rows are
automatically saved when you move from row to row.


Opening files
-------------

By default, when filmbuff starts, the most-recently opened database is opened.
If you would like to open a different database choose **File - Open...** in the
menubar. The window that opens can be used to navigate to the database you
would like to open.


Opening recent files
--------------------

filmbuff maintains a list of recently-used databases so that switching between
them is convenient. To view this list, click **File - Recent files** in the
menubar.

* If there are no recent files, no list will appear.

* filmbuff will display an error if the chosen file no longer exists in the
location that filmbuff remembers.


Opening a new sheet
-------------------

When there are no recent files to open, filmbuff opens to a blank sheet. This
sheet is not saved anywhere until you save it. You can manually open one of
these new sheets by choosing **File - New** in the menubar.


Exporting and importing
-----------------------

filmbuff supports importing data from and exporting data to the tab-separated
value (TSV) format. Many other applications (especially spreadsheet editors)
support importing/exporting TSV files, which allows data to be passed between
programs.

To test out this functionality, create a sheet with a few rows that contain
some data. Next choose, **File - Export tsv...** in the menubar. Use the window
that opens to save the TSV file.

* If you do not enter a file extension, the file will be saved with a **.tsv**
extension automatically.

Next, the file that was just exported can be imported by choosing
**File - Import tsv...** in the menubar. Use the window that opens to navigate
to the recently-exported TSV file. After choosing the file, all data from the
TSV will be loaded into the current sheet.

* To avoid potential data loss, filmbuff appends imported data to the current
sheet rather than overwriting the data in the current sheet with imported data.

* If the TSV does not contain the same column structure as filmbuff databases,
then the data may not be imported correctly.


Setting preferences
-------------------

Currently there are three options available that can be changed. To access
them, choose **Tools - Preferences...** in the menubar.

* Preferences are saved between sessions. If you ever wish to start with a
"blank slate", you can safely delete the configuration file used to store
these settings. The path to this file is **~/.config/filmbuff/filmbuff.conf**.

Here is a quick description of the available options:

* **Table - Scroll to inserted rows** (enabled by default) - When editing
databases with thousands of rows, it can be easy to lose track of where a row
was just inserted. This option will scroll the table to where a row was just
inserted. This functionality can be disabled by unchecking this option.
* **Statusbar - Statusbar is visible** (enabled by default) - The statusbar,
located at the bottom of the main interface, is used to display messages about
recently-completed operations, such as: row insertions/deletions, saving, etc.
The statusbar can be hidden by unchecking this option.
* **Statusbar - Message duration** (5 seconds by default) - The length of time
(in seconds) a message is displayed on the statusbar can be altered using this
option.


Modifying column appearance
---------------------------

filmbuff supports changing the appearance of columns. Please note that the
header names cannot be changed (nor can columns be added or deleted) because
they are part of the structure of the underlying database. The structure of the
database, in this case, is not variable.

* Columns can be made narrower or wider by clicking and dragging the dividers
between columns in the header.
* Columns can be hidden by choosing a column in the menu
**View - Show/hide columns**.
    * This same menu can be accessed by right clicking anywhere on the header.
    * If a column is checked, it is visible. If it is unchecked, it is hidden.
* Columns can be re-ordered by clicking a column's header and dragging it the
position you would like.
* Column widths can be resized to fit their contents by choosing
**View - Resize columns - Optimal widths** in the menubar.


Resetting defaults
------------------

Because changes to the columns and changes to the window size and position
persist between sessions, resetting these changes may be desired.

* To reset the columns, choose
**View - Restore defaults - Column configuration** in the menubar. This
will reorder and resize the columns to their default states.
* To reset the window, choose
**View - Restore defaults - Window configuration** in the menubar. This
will resize and reposition the window to its default state.

If you ever wish to start with a "blank slate", you can safely delete the
configuration file used to store these settings. The path to this file is
**~/.config/filmbuff/filmbuff.conf**.


Reporting bugs
--------------

Please report any bugs you find to the issue tracker for this application. The
link to the issue tracker is listed below:

<https://gitlab.com/emerac/filmbuff/-/issues>

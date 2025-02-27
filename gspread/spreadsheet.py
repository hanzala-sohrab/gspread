"""
gspread.spreadsheet
~~~~~~~~~~~~~~

This module contains common spreadsheets' models.

"""

from .exceptions import WorksheetNotFound
from .urls import (
    SPREADSHEET_BATCH_UPDATE_URL,
    SPREADSHEET_DRIVE_URL,
    SPREADSHEET_SHEETS_COPY_TO_URL,
    SPREADSHEET_URL,
    SPREADSHEET_VALUES_APPEND_URL,
    SPREADSHEET_VALUES_BATCH_CLEAR_URL,
    SPREADSHEET_VALUES_BATCH_UPDATE_URL,
    SPREADSHEET_VALUES_BATCH_URL,
    SPREADSHEET_VALUES_CLEAR_URL,
    SPREADSHEET_VALUES_URL,
)
from .utils import finditem, quote
from .worksheet import Worksheet


class Spreadsheet:
    """The class that represents a spreadsheet."""

    def __init__(self, client, properties):
        self.client = client
        self._properties = properties

    @property
    def id(self):
        """Spreadsheet ID."""
        return self._properties["id"]

    @property
    def title(self):
        """Spreadsheet title."""
        try:
            return self._properties["title"]
        except KeyError:
            metadata = self.fetch_sheet_metadata()
            self._properties.update(metadata["properties"])
            return self._properties["title"]

    @property
    def url(self):
        """Spreadsheet URL."""
        return SPREADSHEET_DRIVE_URL % self.id

    @property
    def creationTime(self):
        """Spreadsheet Creation time."""
        try:
            return self._properties["createdTime"]
        except KeyError:
            # Filter the list using the name to reduce the request size
            # Filter the item using the unique ID to ensure we update the exacte same item
            metadata = finditem(
                lambda x: x["id"] == self.id,
                self.client.list_spreadsheet_files(self.title),
            )
            self._properties.update(metadata)
            return self._properties["createdTime"]

    @property
    def lastUpdateTime(self):
        """Spreadsheet Creation time."""
        try:
            return self._properties["modifiedTime"]
        except KeyError:
            # Filter the list using the name to reduce the request size
            # Filter the item using the unique ID to ensure we update the exacte same item
            metadata = finditem(
                lambda x: x["id"] == self.id,
                self.client.list_spreadsheet_files(self.title),
            )
            self._properties.update(metadata)
            return self._properties["modifiedTime"]

    @property
    def updated(self):
        """.. deprecated:: 2.0

        This feature is not supported in Sheets API v4.
        """
        import warnings

        warnings.warn(
            "Spreadsheet.updated() is deprecated, "
            "this feature is not supported in Sheets API v4",
            DeprecationWarning,
            stacklevel=2,
        )

    @property
    def sheet1(self):
        """Shortcut property for getting the first worksheet."""
        return self.get_worksheet(0)

    def __iter__(self):
        yield from self.worksheets()

    def __repr__(self):
        return "<{} {} id:{}>".format(
            self.__class__.__name__,
            repr(self.title),
            self.id,
        )

    def batch_update(self, body):
        """Lower-level method that directly calls `spreadsheets.batchUpdate <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate>`_.

        :param dict body: `Request body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate#request-body>`_.
        :returns: `Response body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate#response-body>`_.
        :rtype: dict

        .. versionadded:: 3.0
        """
        r = self.client.request(
            "post", SPREADSHEET_BATCH_UPDATE_URL % self.id, json=body
        )

        return r.json()

    def values_append(self, range, params, body):
        """Lower-level method that directly calls `spreadsheets.values.append <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append>`_.

        :param str range: The `A1 notation <https://developers.google.com/sheets/api/guides/concepts#a1_notation>`_
                          of a range to search for a logical table of data. Values will be appended after the last row of the table.
        :param dict params: `Query parameters <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append#query-parameters>`_.
        :param dict body: `Request body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append#request-body>`_.
        :returns: `Response body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append#response-body>`_.
        :rtype: dict

        .. versionadded:: 3.0
        """
        url = SPREADSHEET_VALUES_APPEND_URL % (self.id, quote(range))
        r = self.client.request("post", url, params=params, json=body)
        return r.json()

    def values_clear(self, range):
        """Lower-level method that directly calls `spreadsheets.values.clear <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear>`_.

        :param str range: The `A1 notation <https://developers.google.com/sheets/api/guides/concepts#a1_notation>`_ of the values to clear.
        :returns: `Response body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/clear#response-body>`_.
        :rtype: dict

        .. versionadded:: 3.0
        """
        url = SPREADSHEET_VALUES_CLEAR_URL % (self.id, quote(range))
        r = self.client.request("post", url)
        return r.json()

    def values_batch_clear(self, params=None, body=None):
        url = SPREADSHEET_VALUES_BATCH_CLEAR_URL % self.id
        r = self.client.request("post", url, params=params, json=body)
        return r.json()

    def values_get(self, range, params=None):
        """Lower-level method that directly calls `spreadsheets.values.get <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get>`_.

        :param str range: The `A1 notation <https://developers.google.com/sheets/api/guides/concepts#a1_notation>`_ of the values to retrieve.
        :param dict params: (optional) `Query parameters <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get#query-parameters>`_.
        :returns: `Response body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get#response-body>`_.
        :rtype: dict

        .. versionadded:: 3.0
        """
        url = SPREADSHEET_VALUES_URL % (self.id, quote(range))
        r = self.client.request("get", url, params=params)
        return r.json()

    def values_batch_get(self, ranges, params=None):
        """Lower-level method that directly calls `spreadsheets.values.batchGet <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/batchGet>`_.

        :param ranges: List of ranges in the `A1 notation <https://developers.google.com/sheets/api/guides/concepts#a1_notation>`_ of the values to retrieve.
        :param dict params: (optional) `Query parameters <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get#query-parameters>`_.
        :returns: `Response body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get#response-body>`_.
        :rtype: dict
        """
        if params is None:
            params = {}

        params.update(ranges=ranges)

        url = SPREADSHEET_VALUES_BATCH_URL % (self.id)
        r = self.client.request("get", url, params=params)
        return r.json()

    def values_update(self, range, params=None, body=None):
        """Lower-level method that directly calls `spreadsheets.values.update <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update>`_.

        :param str range: The `A1 notation <https://developers.google.com/sheets/api/guides/concepts#a1_notation>`_ of the values to update.
        :param dict params: (optional) `Query parameters <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update#query-parameters>`_.
        :param dict body: (optional) `Request body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update#request-body>`_.
        :returns: `Response body <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update#response-body>`_.
        :rtype: dict

        Example::

            sh.values_update(
                'Sheet1!A2',
                params={
                    'valueInputOption': 'USER_ENTERED'
                },
                body={
                    'values': [[1, 2, 3]]
                }
            )

        .. versionadded:: 3.0
        """
        url = SPREADSHEET_VALUES_URL % (self.id, quote(range))
        r = self.client.request("put", url, params=params, json=body)
        return r.json()

    def values_batch_update(self, params=None, body=None):
        url = SPREADSHEET_VALUES_BATCH_UPDATE_URL % self.id
        r = self.client.request("post", url, params=params, json=body)
        return r.json()

    def _spreadsheets_get(self, params=None):
        """A method stub that directly calls `spreadsheets.get <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/get>`_."""
        url = SPREADSHEET_URL % self.id
        r = self.client.request("get", url, params=params)
        return r.json()

    def _spreadsheets_sheets_copy_to(self, sheet_id, destination_spreadsheet_id):
        """Lower-level method that directly calls `spreadsheets.sheets.copyTo <https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.sheets/copyTo>`_."""
        url = SPREADSHEET_SHEETS_COPY_TO_URL % (self.id, sheet_id)

        body = {"destinationSpreadsheetId": destination_spreadsheet_id}
        r = self.client.request("post", url, json=body)
        return r.json()

    def fetch_sheet_metadata(self, params=None):
        if params is None:
            params = {"includeGridData": "false"}

        url = SPREADSHEET_URL % self.id

        r = self.client.request("get", url, params=params)

        return r.json()

    def get_worksheet(self, index):
        """Returns a worksheet with specified `index`.

        :param index: An index of a worksheet. Indexes start from zero.
        :type index: int

        :returns: an instance of :class:`gspread.models.Worksheet`.

        :raises:
            WorksheetNotFound: if can't find the worksheet

        Example. To get third worksheet of a spreadsheet:

        >>> sht = client.open('My fancy spreadsheet')
        >>> worksheet = sht.get_worksheet(2)
        """
        sheet_data = self.fetch_sheet_metadata()

        try:
            properties = sheet_data["sheets"][index]["properties"]
            return Worksheet(self, properties)
        except (KeyError, IndexError):
            raise WorksheetNotFound("index {} not found".format(index))

    def get_worksheet_by_id(self, id):
        """Returns a worksheet with specified `worksheet id`.

        :param id: The id of a worksheet. it can be seen in the url as the value of the parameter 'gid'.
        :type id: int

        :returns: an instance of :class:`gspread.models.Worksheet`.
        :raises:
            WorksheetNotFound: if can't find the worksheet

        Example. To get the worksheet 123456 of a spreadsheet:

        >>> sht = client.open('My fancy spreadsheet')
        >>> worksheet = sht.get_worksheet_by_id(123456)
        """
        sheet_data = self.fetch_sheet_metadata()

        try:
            item = finditem(
                lambda x: x["properties"]["sheetId"] == id,
                sheet_data["sheets"],
            )
            return Worksheet(self, item["properties"])
        except (StopIteration, KeyError):
            raise WorksheetNotFound("id {} not found".format(id))

    def worksheets(self):
        """Returns a list of all :class:`worksheets <gspread.models.Worksheet>`
        in a spreadsheet.
        """
        sheet_data = self.fetch_sheet_metadata()
        return [Worksheet(self, x["properties"]) for x in sheet_data["sheets"]]

    def worksheet(self, title):
        """Returns a worksheet with specified `title`.

        :param title: A title of a worksheet. If there're multiple
                      worksheets with the same title, first one will
                      be returned.
        :type title: str

        :returns: an instance of :class:`gspread.models.Worksheet`.

        :raises:
            WorksheetNotFound: if can't find the worksheet

        Example. Getting worksheet named 'Annual bonuses'

        >>> sht = client.open('Sample one')
        >>> worksheet = sht.worksheet('Annual bonuses')
        """
        sheet_data = self.fetch_sheet_metadata()
        try:
            item = finditem(
                lambda x: x["properties"]["title"] == title,
                sheet_data["sheets"],
            )
            return Worksheet(self, item["properties"])
        except (StopIteration, KeyError):
            raise WorksheetNotFound(title)

    def add_worksheet(self, title, rows, cols, index=None):
        """Adds a new worksheet to a spreadsheet.

        :param title: A title of a new worksheet.
        :type title: str
        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        :param index: Position of the sheet.
        :type index: int

        :returns: a newly created :class:`worksheets <gspread.models.Worksheet>`.
        """
        body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title,
                            "sheetType": "GRID",
                            "gridProperties": {
                                "rowCount": rows,
                                "columnCount": cols,
                            },
                        }
                    }
                }
            ]
        }

        if index is not None:
            body["requests"][0]["addSheet"]["properties"]["index"] = index

        data = self.batch_update(body)

        properties = data["replies"][0]["addSheet"]["properties"]

        worksheet = Worksheet(self, properties)

        return worksheet

    def duplicate_sheet(
        self,
        source_sheet_id,
        insert_sheet_index=None,
        new_sheet_id=None,
        new_sheet_name=None,
    ):
        """Duplicates the contents of a sheet.

        :param int source_sheet_id: The sheet ID to duplicate.
        :param int insert_sheet_index: (optional) The zero-based index
                                       where the new sheet should be inserted.
                                       The index of all sheets after this are
                                       incremented.
        :param int new_sheet_id: (optional) The ID of the new sheet.
                                 If not set, an ID is chosen. If set, the ID
                                 must not conflict with any existing sheet ID.
                                 If set, it must be non-negative.
        :param str new_sheet_name: (optional) The name of the new sheet.
                                   If empty, a new name is chosen for you.

        :returns: a newly created :class:`<gspread.models.Worksheet>`.

        .. versionadded:: 3.1
        """
        body = {
            "requests": [
                {
                    "duplicateSheet": {
                        "sourceSheetId": source_sheet_id,
                        "insertSheetIndex": insert_sheet_index,
                        "newSheetId": new_sheet_id,
                        "newSheetName": new_sheet_name,
                    }
                }
            ]
        }

        data = self.batch_update(body)

        properties = data["replies"][0]["duplicateSheet"]["properties"]

        worksheet = Worksheet(self, properties)

        return worksheet

    def del_worksheet(self, worksheet):
        """Deletes a worksheet from a spreadsheet.

        :param worksheet: The worksheet to be deleted.
        :type worksheet: :class:`~gspread.Worksheet`
        """
        body = {"requests": [{"deleteSheet": {"sheetId": worksheet.id}}]}

        return self.batch_update(body)

    def reorder_worksheets(self, worksheets_in_desired_order):
        """Updates the ``index`` property of each Worksheets to reflect
        its index in the provided sequence of Worksheets.

        :param worksheets_in_desired_order: Iterable of Worksheet objects in desired order.

        Note: If you omit some of the Spreadsheet's existing Worksheet objects from
        the provided sequence, those Worksheets will be appended to the end of the sequence
        in the order that they appear in the list returned by ``Spreadsheet.worksheets()``.

        .. versionadded:: 3.4
        """
        idx_map = {}
        for idx, w in enumerate(worksheets_in_desired_order):
            idx_map[w.id] = idx
        for w in self.worksheets():
            if w.id in idx_map:
                continue
            idx += 1
            idx_map[w.id] = idx

        body = {
            "requests": [
                {
                    "updateSheetProperties": {
                        "properties": {"sheetId": key, "index": val},
                        "fields": "index",
                    }
                }
                for key, val in idx_map.items()
            ]
        }

        return self.batch_update(body)

    def share(
        self,
        value,
        perm_type,
        role,
        notify=True,
        email_message=None,
        with_link=False,
    ):
        """Share the spreadsheet with other accounts.

        :param value: user or group e-mail address, domain name
                      or None for 'default' type.
        :type value: str, None
        :param perm_type: The account type.
               Allowed values are: ``user``, ``group``, ``domain``,
               ``anyone``.
        :type perm_type: str
        :param role: The primary role for this user.
               Allowed values are: ``owner``, ``writer``, ``reader``.
        :type role: str
        :param notify: (optional) Whether to send an email to the target user/domain.
        :type notify: str
        :param email_message: (optional) The email to be sent if notify=True
        :type email_message: str

        :param with_link: (optional) Whether the link is required for this permission
        :type with_link: bool

        Example::

            # Give Otto a write permission on this spreadsheet
            sh.share('otto@example.com', perm_type='user', role='writer')

            # Transfer ownership to Otto
            sh.share('otto@example.com', perm_type='user', role='owner')
        """
        self.client.insert_permission(
            self.id,
            value=value,
            perm_type=perm_type,
            role=role,
            notify=notify,
            email_message=email_message,
            with_link=with_link,
        )

    def list_permissions(self):
        """Lists the spreadsheet's permissions."""
        return self.client.list_permissions(self.id)

    def remove_permissions(self, value, role="any"):
        """Remove permissions from a user or domain.

        :param value: User or domain to remove permissions from
        :type value: str
        :param role: (optional) Permission to remove. Defaults to all
                     permissions.
        :type role: str

        Example::

            # Remove Otto's write permission for this spreadsheet
            sh.remove_permissions('otto@example.com', role='writer')

            # Remove all Otto's permissions for this spreadsheet
            sh.remove_permissions('otto@example.com')
        """
        permission_list = self.client.list_permissions(self.id)

        key = "emailAddress" if "@" in value else "domain"

        filtered_id_list = [
            p["id"]
            for p in permission_list
            if p.get(key) == value and (p["role"] == role or role == "any")
        ]

        for permission_id in filtered_id_list:
            self.client.remove_permission(self.id, permission_id)

        return filtered_id_list

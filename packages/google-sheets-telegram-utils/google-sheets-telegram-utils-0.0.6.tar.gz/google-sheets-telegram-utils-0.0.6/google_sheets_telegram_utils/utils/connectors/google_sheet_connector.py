import gspread
from oauth2client.service_account import ServiceAccountCredentials

from google_sheets_telegram_utils.exceptions import RowDoesNotExistException
from google_sheets_telegram_utils.utils.configs.google_sheet_config import GoogleSheetConfig
from google_sheets_telegram_utils.utils.connectors.abstract_connector import AbstractConnector


class GoogleSheetConnector(AbstractConnector):

    def __init__(self, config: GoogleSheetConfig):
        super().__init__(config)

    def get_data(self) -> dict:
        workbook = self._get_workbook()
        sheet = workbook.worksheet(self.config.sheet_name)
        data = sheet.get_all_records()
        return data

    def _get_workbook(self) -> gspread.models.Spreadsheet:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.config.credentials_path,
            self.config.scope,
        )
        client = gspread.authorize(credentials)
        sheet = client.open(self.config.file)
        return sheet

    def add_rows(self, rows: list) -> None:
        workbook = self._get_workbook()
        worksheet = workbook.worksheet(self.config.sheet_name)
        records = worksheet.get_all_records()
        insert_position = len(records) + 2
        worksheet.insert_rows(rows, insert_position, value_input_option='USER_ENTERED')

    def add_row(self, row):
        return self.add_rows([row])

    def get_row_by_id(self, pk) -> dict:
        rows = self.get_data()
        filtered_rows = list(filter(lambda row: row['id'] == pk, rows))
        if filtered_rows:
            data = filtered_rows[0]
            return data
        raise RowDoesNotExistException

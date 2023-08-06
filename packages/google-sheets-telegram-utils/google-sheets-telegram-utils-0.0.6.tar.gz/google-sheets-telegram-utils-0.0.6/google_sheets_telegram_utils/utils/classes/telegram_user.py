class TelegramUser:
    def __init__(self, data):
        #  TODO move id, username... to constants
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.language_code = data['language_code']
        self.is_bot = data['is_bot']
        self.is_activated = data['is_activated'] and data['is_activated'].lower() == 'true'

    def convert_to_list(self) -> list:
        return [
            self.id,
            self.username,
            self.first_name,
            self.last_name,
            self.language_code,
            self.is_bot,
            'TRUE' if self.is_activated else 'FALSE',
        ]


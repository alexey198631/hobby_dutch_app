class GlobalLanguage:
    file_path = 'data_files/'

    @classmethod
    def set_value(cls, new_value):
        cls.file_path = new_value
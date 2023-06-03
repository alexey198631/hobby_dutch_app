class GlobalLanguage:
    file_path = 'data_files/'

    @classmethod
    def set_value(cls, new_value):
        cls.file_path = new_value

class Difficulty:
    difficulty = 'standard'
    difficulty_distribution = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 2, 11: 1, 12: 1}


    @classmethod
    def set_difficluty(cls, new_dif):
        cls.difficulty = new_dif

        if new_dif == 'standard':
            cls.difficulty_distribution = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 2, 11: 1, 12: 1}
        elif new_dif == 'easy':
            cls.difficulty_distribution = {1: 2, 2: 2, 3: 4, 4: 4, 5: 4, 6: 4, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 0}
        elif new_dif == 'hard':
            cls.difficulty_distribution = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 3, 7: 3, 8: 4, 9: 3, 10: 3, 11: 3, 12: 2}
        elif new_dif == 'very hard':
            cls.difficulty_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 5, 7: 5, 8: 5, 9: 4, 10: 3, 11: 2, 12: 1}
        elif new_dif == 'exam':
            cls.difficulty_distribution = {1: 8, 2: 8, 3: 8, 4: 8, 5: 9, 6: 9, 7: 9, 8: 9, 9: 8, 10: 8, 11: 8, 12: 8}

class Styles:
    button_style = """
                    QPushButton {
                    background-color: lightgrey;
                    color: black;
                                }
                    QPushButton:hover {
                    background-color: grey;
                    color: white;
                                }
                    """
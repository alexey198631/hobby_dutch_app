import random

def shuffle_dictionary(d):
    items = list(d.items())
    random.shuffle(items)
    shuffled_dict = dict(items)
    return shuffled_dict


class GlobalLanguage:
    file_path = 'utils/'

    @classmethod
    def set_value(cls, new_value):
        cls.file_path = new_value


class ExamSettings:
    exam_direction = 'to_english'
    exam_length = 100

    @classmethod
    def set_direction(cls, new_direction):
        cls.exam_direction = new_direction

    @classmethod
    def set_length(cls, new_length):
        cls.exam_length = new_length


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
        elif new_dif == 'exam' and ExamSettings.exam_length == 100:
            cls.difficulty_distribution = [100, 30.0]
        elif new_dif == 'exam' and ExamSettings.exam_length == 50:
            cls.difficulty_distribution = [50, 50.0]
        elif new_dif == 'exam' and ExamSettings.exam_length == 25:
            cls.difficulty_distribution = [25, 70.0]

        if new_dif != 'exam':
            cls.difficulty_distribution = shuffle_dictionary(cls.difficulty_distribution)


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
import random


# two main classes for the app
class Words(object):

    """The class for all words from dictionary. Each word a type, a translation, an example,
    a translation of an example, a translation to Russian, also additional parameters which would be created after
    the first run (quantity of appearances in lessons, trials of direct and indirect translation,
    success attempts, also weight, more weight - more often words appear"""

    def __init__(self, word, typ, translation, russian, example, example_translation, appear, trial_d, trial_r, success,
                 weight, word_index, difficulty, wd):
        self.word = word
        self.typ = typ
        self.translation = translation
        self.example = example
        self.example_translation = example_translation
        self.russian = russian
        self.appear = appear
        self.trial_d = trial_d
        self.trial_r = trial_r
        self.success = success
        self.weight = weight
        self.word_index = word_index
        self.difficulty = difficulty
        self.wd = wd

    def getWord(self):
        return self.word

    def getWordIndex(self):
        return self.word_index

    def getTyp(self):
        return self.typ

    def getTranslation(self):
        return self.translation

    def getRussian(self):
        return self.russian

    def changeType(self, new):
        self.typ = new

    def getTrials_d(self):
        return self.trial_d

    def getTrials_r(self):
        return self.trial_r

    def addTrials_d(self):
        self.trial_d += 1

    def addTrials_r(self):
        self.trial_r += 1

    def getAppear(self):
        return self.appear

    def addAppear(self):
        self.appear += 1
        return self.appear

    def addSuccess(self):
        self.success += 1
        return self.success

    def getSuccess(self):
        return self.success

    def getExample_nl(self):
        return self.example

    def getExample_en(self):
        return self.example_translation

    def getWeight(self):
        if self.trial_d == 0 and self.trial_r == 0:
            return round(self.weight, 2)
        else:
            return round((100 - (self.success / (self.trial_d + self.trial_r)) * 100), 2)

    def updateWeight(self):
        if self.trial_d != 0 and self.trial_r != 0:
            self.weight = round((100 - (self.success / (self.trial_d + self.trial_r)) * 100), 2)

    def getDifficulty(self):
        return self.difficulty

    def getWD(self):
        if self.weight == 0.0 and self.difficulty == 0:
            return 1
        elif self.weight <= 33:
            return self.difficulty
        elif self.weight <= 66:
            return self.difficulty + 1
        elif self.weight <= 100:
            return self.difficulty + 2


    def __len__(self):
        return len(f'{self.word} -> {self.translation}')

    def __repr__(self):
        return f'{self.word}: {self.appear}, {self.trial_d + self.trial_r} / {self.success}'

    def __str__(self):
        return f'{self.word} : {self.translation}'


class Lesson(object):
    """The class is creating after any start of the program and fix all its parameters:
    lesson length in time and symbols, lesson points and, of course, lesson number
    """
    lol: object
    list_of_words: object
    pts: object
    easy: object
    finish: object
    inter: object
    start: object

    def __init__(self, number):
        self.number = number

    def getNumber(self):
        return self.number

    def start(self, start):
        self.start = start

    def getStart(self):
        return self.start

    def inter(self, inter):
        self.inter = inter

    def setlevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def getInter(self):
        return self.inter

    def finish(self, finish):
        self.finish = finish

    def getFinish(self):
        return self.finish

    def number_of_easy(self, easy):
        self.easy = easy

    def getNumber_of_easy(self):
        return self.easy

    def points(self, pts):
        self.pts = pts

    def add_pts(self, a_pts):
        self.pts += a_pts

    def getTime(self):
        return int((self.finish - self.start).seconds)

    def getInterPoints(self):
        return self.pts

    def getPoints(self):
        return self.pts + 1500 - int((self.finish - self.start).seconds)

    def getInterTime(self):
        return int((self.inter - self.start).seconds)

    def wlist(self, list_of_words):
        self.list_of_words = list_of_words

    def getList(self):
        return self.list_of_words

    def length_of_lesson(self, lol):
        self.lol = lol

    def getLength_of_lesson(self):
        return self.lol

    def __repr__(self):
        return 'hello'


# class for werkwoorden
class Verbs(Words):

    ts: object

    def __init__(self, verb_index, word, translation, second, third, appear, trial_d, trial_r, success,
                 weight):
        self.verb_index = verb_index
        self.word = word
        self.second = second
        self.third = third
        self.translation = translation
        self.appear = appear
        self.trial_d = trial_d
        self.trial_r = trial_r
        self.success = success
        self.weight = weight


    def getVerbIndex(self):
        return self.verb_index

    def getSecond(self):
        return self.second

    def getThird(self):
        return self.third

    def addTimeSpend(self, t):
        self.timespent += t

    def getTimeSpend(self):
        return int(self.timespent)

    def __str__(self):
        return f'{self.translation} : {self.word}  -> {self.second} - >  {self.third}'


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
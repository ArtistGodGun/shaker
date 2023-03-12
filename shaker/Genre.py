from enum import Enum
from shaker import pattern_info

class GenreList(Enum):
    newage = 'newage'
    bossa = 'bossa'
    ragtime = 'ragtime'
    # hiphop = 'hiphop'
    # jazz = 'jazz'
    # blues = 'blues'
    # classic = 'classic'
    # edm = 'edm'

class Emotion(Enum):
    pleasure = 'pleasure'
    sadness = 'sadness'
    joy = 'joy'
    unrest = 'unrest'
    rest = 'rest'
    scared = 'scared'
    comfortable = 'comfortable'
    exciting = 'exciting'

class Instrument(Enum):
    piano = 'piano'
    ep = 'ep'
    guitar = 'guitar'
    bass = 'bass'        


# 유저의 선택과 곡의 정보를 토대로 세부장르, BPM, 멜로디, 화성, 악기에 대한 정보를 선택함
class Genre(object):
    def __init__(self, user:dict, info:list):

        genre = self.selectGenre(user, info)

        self.bpm = self.setBPM(genre, info)
        self.melody = self.setMelody(genre, info)
        self.chord = self.setChord(genre, info)
        self.instrument = self.setInstrument(genre, info)
        self.key = self.setKey(genre, info)
        self.tick = info['tick']
        self.pattern = self.setGenrePattern(genre, info)
        self.lyricInfo = self.setLyricInfo(genre, info)
        self.vocingType = self.setVocingType(genre, info)
        self.syncopation = self.setSyncopation(genre, info)

        self.genre_data = {
            'name': genre,
            'tick': self.tick,
            'bpm':self.bpm,
            'key': self.key,
            'melody':self.melody,
            'chord': self.chord,
            'ins': self.instrument,
            'pattern': self.pattern,
            'vocing_type': self.vocingType,
            }

    # 유저의 선택과 곡의 정보를 토대로 세부 장르를 추출함
    def selectGenre(self, user, info):
        # genre = GenreList.newage
        # genre = GenreList.bossa
        return user['genre']

    # 장르 고유의 BPM, 원곡의 BPM, 멜로디 분석에 따른 BPM등을 사용 할 수 있음
    def setBPM(self, genre, info):
        return info['bpm']

    # 장르에 따라 멜로디를 수정하거나 원곡의 멜로디를 그대로 사용할 수 있음
    def setMelody(self, genre, info):
        # 현재는 듣기좋은 옥타브로 맞추는 단순한 기능

        max_melody = 0
        new_melody = []
        for _m in info['melody']:
            if _m[0] > max_melody:
                max_melody = _m[0]
        if max_melody < 80:
            for nm in info['melody']:
                new_melody.append([nm[0] + 12, nm[1]])
        else:
            new_melody = info['melody']


        return new_melody

    # 장르에 따라 코드를 수정하거나 원곡의 코드를 그대로 사용할 수 있음
    def setChord(self, genre, info):
        return info['chord_info']

    # 장르에 따라 필요한 악기를 정함
    def setInstrument(self, genre, info):
        if genre == GenreList.newage:
            instrument = [Instrument.piano]
        else:
            instrument = [Instrument.piano]
        return instrument

    # 장르에 따라 반드시 고정되어야하는 키를 설정
    def setKey(self, genre, info):
        return info['key']

    # 장르에 따라 싱코페이션을 설정해야할 때 사용
    def setSyncopation(self, genre, info):
        if genre.value == genre.bossa:
            pass
        return info['chord_info']

    def setPartStatic(self, genre, info):
        return True

    def setGenrePattern(self, genre, info):
        return pattern_info.GenrePattern[genre.value]

    def setPatternStatic(self, genre, info):
        if genre == GenreList.newage:
            patternStatic = False
        else:
            patternStatic = True
        return patternStatic

    def setLyricInfo(self, genre, info):
        return 'lyric_info'

    def setVocingType(self, genre, info):
        return True
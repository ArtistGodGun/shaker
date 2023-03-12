from tabnanny import check
from shaker import common
import random

from shaker.Genre import GenreList
class Bar(object):
    def __init__(self, genre, section_name, section_value):
        self.genre = genre
        _bar_info = self.defineBarInfo(section_name, section_value)
        self.bar_info = self.setBarInfo(_bar_info)

        # for i in self.bar_info.items():
        #     print(i)

    def defineBarInfo(self, section_name, section_value):
        bar_structure = {}
        structure_num = self.setBarStructure(len(section_value['value']) - 1)
        for sn, sv in section_value.items():
            if sn == 'info':
                info = sv
            else:
                for bi, (bn, bv) in enumerate(sv.items()):
                    bar_structure[bn] = bv
                    for cn, cv in bv.items():
                        cv['bpm'] = self.setBarBPM(info)
                        cv['ins'] = self.setBarIns(info)
                        cv['octav'] = self.setBarOctav(info)
                        cv['velocity'] = self.setBarVelocity(info)
                        cv['first_chord'] = self.setBarFirstChord(info)
                        cv['chord_rhythm'] = self.setBarChordRhythm(info, structure_num[bi], bi, info['fill_pos'])
                        cv['bass_rhythm'] = self.setBarBassRhythm(info, structure_num[bi], bi, info['fill_pos'])
                        cv['bass_note'] = self.setBarBassNote(info, structure_num[bi], cv['bass_rhythm'])
                        cv['bar_unit'] = info['bar_unit']
                        cv['vocing_type'] = info['vocing_type']
                        bar_structure[bn][cn] = cv
        return bar_structure

    def setBarBPM(self, bpm):
        return bpm['bpm']
    def setBarIns(self, ins):
        return ins['ins']
    def setBarOctav(self, octav):
        return octav['octav']
    def setBarVelocity(self, velocity):
        return velocity['velocity']
    def setBarFirstChord(self, first_chord):
        return first_chord['first_chord']
    def setBarChordRhythm(self, value, structure_type, bar_pos, fill_pos):
        if fill_pos == 1:
            if self.genre['name'] == GenreList.newage and bar_pos == 3:
                chord_rhythm = [16]
            elif self.genre['name'] == GenreList.bossa and bar_pos == 2:
                chord_rhythm = [6, 1, -1, 5, -1, 18]
            else:
                if structure_type == 0:
                    chord_rhythm = value['chord_rhythm']
                else:
                    chord_rhythm = value['chord_rhythm']

                    # bass_rhythm = [9] # 다른 패턴   
        else:
            if structure_type == 0:
                chord_rhythm = value['chord_rhythm']
            else:
                chord_rhythm = value['chord_rhythm']
                # chord_rhythm = [9] # 다른 패턴

        return chord_rhythm
    def setBarBassRhythm(self, value, structure_type, bar_pos, fill_pos):
        if fill_pos == 1:
            if self.genre['name'] == GenreList.newage and bar_pos == 3:
                bass_rhythm = [16]
            elif self.genre['name'] == GenreList.bossa and bar_pos == 2:
                p = self.genre['pattern']['bass_rhythm']
                bass_rhythm = random.choice(list(p.values()))
            else:
                if structure_type == 0:
                    bass_rhythm = value['bass_rhythm']
                else:
                    p = self.genre['pattern']['bass_rhythm']
                    bass_rhythm = random.choice(list(p.values()))
                    # bass_rhythm = [9] # 다른 패턴     
        else:
            if structure_type == 0:
                bass_rhythm = value['bass_rhythm']
            else:
                p = self.genre['pattern']['bass_rhythm']
                bass_rhythm = random.choice(list(p.values()))
                # bass_rhythm = [9] # 다른 패턴           
        return bass_rhythm
    def setBarBassNote(self, value, structure_type, bass_rhythm):
        if structure_type == 0:
            if common.checkNoteNumber(bass_rhythm) != len(value['bass_note']):
                _bass_note =[]
                n = list(self.genre['pattern']['bass_note'].values())
                for i in n:
                    if len(i) ==common.checkNoteNumber(bass_rhythm):
                        _bass_note.append(i)
                bass_note = random.choice(_bass_note)
            else:
                bass_note = value['bass_note']
        else:
            n = list(self.genre['pattern']['bass_note'].values())
            _bass_note = []
            for i in n:
                if len(i) == common.checkNoteNumber(bass_rhythm):
                    _bass_note.append(i)
            bass_note = random.choice(_bass_note)
            # bass_note = [9] # 다른 패턴           
        return bass_note
    def setBarStructure(self, section_num):
        structure = [0]
        while section_num > 0:
            structure.append(random.choice([0,1]))
            section_num -=1
        return structure


    
    def setBarInfo(self, bar_info):
        bar_unit = [] # 리듬 길이에 따라 마디 갯수가 저장됨

        if len(bar_info) == 1: # 못갖춘마디 섹션 일때
            for bn, bv in bar_info.items():
                for cn, cv in bv.items():
                    if self.getRhythmDuration(cv['chord_rhythm']) == 16: # 이 마디에 적용되어야할 코드의 리듬이 1마디 짜리 일때
                        pass # 룰 적용 안해도 됨
                    else: # 이 마디에 적용되어야할 코드의 리듬이 2마디 이상일 때
                        bv = self.multiSplitRhythm([bv])[0]
        else: # 일반섹션 일때
            for index, (bn, bv) in enumerate(bar_info.items()):
                # print(bn)
                bar_unit.append(bv)
                for cn, cv in bv.items():
                    bar_unit_num = cv['bar_unit']
                check_chord_num = 0
                for unit in bar_unit:
                    if len(unit) > check_chord_num:
                        check_chord_num = len(unit)
                if bar_unit_num == 1: # 한 리듬을 한마디에만 적용하는 경우
                    if check_chord_num == 1: # 한  마디 안에 하나의 코드가 있는 경우
                        pass
                        bar_unit = []
                    else: # 한 마디 안에 두개 이상의 코드가 있는 경우 = repeat
                        bv =  self.multiRepeatRhythm(bar_unit)[0]
                        bar_unit = []
                else: # 한 리듬을 두마디 이상에 적용하는 경우
                    if len(bar_unit) == 1: # 한 리듬에 한마디의 코드가 들어온 경우
                        last_bar_check = True
                    else:
                        bar_unit = self.multiSplitRhythm(bar_unit) # 들어온 마디 안에 존재하는 코드의 갯수만큼 나눠줌
                        bar_unit = []
                        last_bar_check = False
                    # if len(bar_unit) == 2: # 한 마디 안에 코드가 두개 있는 경우 => split
                    #     bv = self.multiSplitRhythm(bar_unit)
                    # else: # 한 마디 안에 코드가 하나 있는 경우s
                    #     bv = self.multiSplitRhythm(bar_unit)
            if self.genre['name'].value == 'bossa':
                if last_bar_check: # 한 리듬이 두마디에만 적용하는 경우 중, 인트로를 제외한 섹션에 속한 마디의 갯수가 3개 이면서, 마지막 마디일때 (3번째 마디가 마지막일때)
                    bar_unit = self.multiSplitRhythm(bar_unit)
            

        return bar_info

    def multiRepeatRhythm(self, bar_unit):
        each_duration = []
        for index, bar in enumerate(bar_unit):
            for key, value in bar.items():
                if index == 0:
                    whole_chord_rhythm = value['chord_rhythm']
                    whole_bass_rhythm = value['bass_rhythm']
                    whole_bass_note = value['bass_note']
                each_duration.append(value['chord_table'][1])   

        chord_rhythm = []
        bass_rhythm = []
        bass_note = []
        for d in each_duration:
            chord_rhythm.append(self.repeatRhythm(d, whole_chord_rhythm, ''))
            bass_info = self.repeatRhythm(d, whole_bass_rhythm, whole_bass_note)
            bass_rhythm.append(bass_info[0])
            bass_note.append(bass_info[1])

        for bar in bar_unit:
            for index, (key, value) in enumerate(bar.items()):
                value['chord_rhythm'] = chord_rhythm[index]
                value['bass_rhythm'] = bass_rhythm[index]
                value['bass_note'] = bass_note[index]

        return bar_unit
    def repeatRhythm(self, _duration, _rhythm, _note):
        duration = int(_duration/120)
        temp_rhythm = []
        for _r in _rhythm:
            temp_rhythm.append(_r)
            if self.getRhythmDuration(temp_rhythm) > duration:
                temp_r = _r
                repeat = True
                while repeat:
                    del temp_rhythm[-1]
                    if temp_r > 0:
                        temp_r -=1
                    else:
                        temp_r +=1
                    temp_rhythm.append(temp_r)
                    if self.getRhythmDuration(temp_rhythm) == duration:
                        repeat = False
            if self.getRhythmDuration(temp_rhythm) == duration:
                repeat_rhythm = temp_rhythm
                # if duration == 12 and _note == '':
                #     print()
                #     print('hello')
                #     print(repeat_rhythm, duration)
                break
        if _note == '':
            return_value = repeat_rhythm
        else:
            repeat_note = self.repeatNote(_note, repeat_rhythm)
            return_value = [repeat_rhythm, repeat_note]
        return return_value
    
    def multiSplitRhythm(self, bar_unit):
        each_duration = []
        for index, bar in enumerate(bar_unit):
            for key, v in bar.items():
                if index == 0:
                    whole_chord_rhythm = v['chord_rhythm']
                    whole_bass_rhythm = v['bass_rhythm']
                    whole_bass_note = v['bass_note']
                each_duration.append(v['chord_table'][1])
        chord_rhythm = []
        bass_rhythm = []
        bass_note = []
        # print(each_duration)
        chord_rhythm = self.splitRhythm(each_duration, whole_chord_rhythm, '')
        bass_rhythm, bass_note = self.splitRhythm(each_duration, whole_bass_rhythm, whole_bass_note)
        chord_count = 0

        for bar in bar_unit:
            for k, v in bar.items():
                v['chord_rhythm'] = chord_rhythm[chord_count]
                v['bass_rhythm'] = bass_rhythm[chord_count]
                v['bass_note'] = bass_note[chord_count]
                chord_count +=1
        return bar_unit
    
    # 리듬이 2마디짜리 일때 내부에 있는 코드의 리듬을 나누기
    def splitRhythm(self, each_duration, rhythm, note):
        total_rhythm = []
        rhythm_count = 0
        _rhythm = rhythm
        for d in each_duration:
            duration = int(d/120)
            temp_rhythm = []
            repeat = True
            while repeat:
                if self.getRhythmDuration(temp_rhythm) == duration:
                    total_rhythm.append(temp_rhythm)
                    repeat = False
                elif self.getRhythmDuration(temp_rhythm) > duration:
                    # print('orig', _rhythm)
                    next_rhythm = 0
                    repeat2 = True
                    # print(temp_r)
                    while repeat2:
                        # print(temp_rhythm)
                        temp_r = temp_rhythm.pop()
                        # print(temp_rhythm, temp_r, next_rhythm)
                        if temp_r > 0:
                            temp_r -=1
                            next_rhythm -=1
                        else:
                            temp_r +=1
                            next_rhythm -=1
                        temp_rhythm.append(temp_r)

                        if self.getRhythmDuration(temp_rhythm) == duration:
                            # print('arg ',rhythm_count, temp_r, next_rhythm)
                            total_rhythm.append(temp_rhythm)
                            del _rhythm[rhythm_count-1]
                            _rhythm.insert(rhythm_count-1, temp_r)
                            _rhythm.insert(rhythm_count, next_rhythm)
                            # print(_rhythm)
                            # rhythm_count +=1
                            repeat2 = False
                    repeat = False
                else:
                    temp_rhythm.append(_rhythm[rhythm_count])
                    rhythm_count +=1
        if note == '':
            return_value = total_rhythm
        else:
            return_value = total_rhythm, self.splitNote(total_rhythm, note)
        return return_value

    # 어떤 리듬 패턴의 길이를 측정
    def getRhythmDuration(self, rhythm):
        duration = 0
        for _r in rhythm:
            r = abs(_r)
            duration += r
        return duration

    # 전체 리듬 중, 쉼표는 빼고 음표의 갯수만 계산한 후 앞뒤로 잘라서 내보냄
    def splitNote(self, total_rhythm, note):
        # print(total_rhythm)
        # print(note)
        total_note = []
        a = 0
        note_count = 0
        while a < len(total_rhythm):
            temp_note = []
            for i in total_rhythm[a]:
                if i > 0:
                    temp_note.append(note[note_count])
                    note_count+=1
            total_note.append(temp_note)
            a+=1

        # 아래 for문은 리듬이 쉼표일 때의 리스트가 따로 존재할 경우 노트를 [1]로 대치함 (어차피 리듬이 쉼표이므로 어떤 노트가 들어와도 상관없음)
        for index, _n in enumerate(total_note):
            if _n == []:
                total_note[index] = [1]
        return total_note

    # 전체 리듬 중, 쉼표는 빼고 음표의 갯수만 계산한 후 내보냄
    def repeatNote(self, note, rhythm):
        note_count = 0
        current_note = []
        for _r in rhythm:
            if _r > 0:
                current_note.append(note[note_count])
                note_count+=1
        return current_note

    def setBarFillPos(self):
        print('hello')
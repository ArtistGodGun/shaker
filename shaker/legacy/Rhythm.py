import random
from itertools import *


class Rhythm(object):
    def __init__(self, genre, song_form):
        self.song_form = song_form
        self.all_pattern = genre.return_value['pattern']
        self.pattern_static = genre.return_value['static']
        self.tick = genre.return_value['tick']
        # 코드리듬의 경우
        # 1. 코드의 리듬이 고정일 때
        #   -> 유사한 리듬을 뽑아주는 친구 필요
        # 2. 코드의 리듬이 멜로디에 따라 변할 때
        #   -> 특정 멜로디 일때 고정 리듬을 뽑아주는 친구 필요

        '''
        rhythm_handle

        duration, rhythm, bar

        if rhythm == bar:
            if duration == bar:
                a
            elif duration < bar:
                b or c # 장르 혹은 특정 구간에 따라 달라짐. 대표적으로
            elif duration > bar:
                b
        elif rhythm > bar:
            if duration <= bar:
                b or c # 장르 혹은 특정 구간에 따라 달라짐
            elif duration > bar:
                a
        elif rhythm < bar:
            d

        1. 리듬이 한마디 짜리 일 때
          - 이 경우는 대부분의 경우에 해당합니다
          1) 코드의 길이가 한마디 인 경우
            - 그대로 반영하면 됨 ===a
          2) 코드의 길이가 한마디 이하인 경우
            - 리듬을 처음으로 돌리거나 === b
            - 원래의 리듬을 코드가 바뀌어도 계속 연주하거나 ===c
          3) 코드의 길이가 한마디 이상인 경우
            - 리듬을 처음으로 돌립니다 ===b

        2. 리듬이 두마디 이상 일때
          - 이 경우는 특정 장르일 때 해당합니다 ex) 보사노바, 일렉트로닉 등
          1) 코드의 길이가 한마디 인 경우
            - 원래의 리듬을 코드가 바뀌어도 계속 연주하거나 ===c
            - 리듬을 처음으로 돌리거나 ===b
          2) 코드의 길이가 한마디 이하인 경우
            - 원래의 리듬을 코드가 바뀌어도 계속 연주하거나 ===c
            - 리듬을 처음으로 돌리거나 ===b
          3) 코드의 길이가 한마디 이상인 경우
            - 그대로 반영 === a

        3. 리듬이 한마디 이하일 때
          - 이 경우는 해당 리듬이 필인일 때 해당 할겁니다
          1) 코드의 길이가 한마디 인 경우
            - 필인에 해당하는 리듬 길이까지 원래의 리듬을 연주하다가 필인을 삽입 ===d
          2) 코드의 길이가 한마디 이하인 경우
            - 필인에 해당하는 리듬 길이까지 원래의 리듬을 연주하다가 필인을 삽입 ===d
          3) 코드의 길이가 한마디 이상인 경우
            - 필인에 해당하는 리듬 길이까지 원래의 리듬을 연주하다가 필인을 삽입 ===d
        '''

        chord_rhythm = []
        bass_rhythm = []

        main_chord_pattern, main_bass_pattern = self.getMainPattern()
        part_bass_structure = self.getStructure(len(self.song_form))
        part_chord_structure = self.getStructure(len(self.song_form))

        for part_index, (_, part) in enumerate(self.song_form.items()):
            section_chord_pattern = self.getOtherPattern('chord', main_chord_pattern, part_chord_structure[part_index])
            section_chord_structure = self.getStructure(len(part))
            section_bass_pattern = self.getOtherPattern('bass', main_bass_pattern, part_bass_structure[part_index])
            section_bass_structure = self.getStructure(len(part))

            for section_index, (_, section) in enumerate(part):
                bar_chord_pattern = self.getOtherPattern('chord', section_chord_pattern, section_chord_structure[section_index])
                bar_chord_structure = self.getStructure(len(section))
                bar_bass_pattern = self.getOtherPattern('bass', section_bass_pattern, section_bass_structure[section_index])
                bar_bass_structure = self.getStructure(len(section))

                for bar_index, bar in enumerate(section):
                    _chord_table, _chord_duration = bar['chord']
                    _current_chord_rhythm = self.getOtherPattern('chord', bar_chord_pattern, bar_chord_structure[bar_index])
                    _current_bass_rhythm = self.getOtherPattern('bass', bar_bass_pattern, bar_bass_structure[bar_index])
                    _current_bass_note = self.setNote(_current_bass_rhythm)
                    bar['chord_rhythm'] = _current_chord_rhythm
                    bar['bass_rhythm'] = _current_bass_rhythm
                    bar['bass_note'] = _current_bass_note    

        for part_name, part in self.song_form.items():
            for section_name, section in part:
                for bar in section:
                    # print(part_name, section_name, bar)
                    print(bar)
        


    def getMainPattern(self):
        _main_chord_pattern = random.choice(list(self.all_pattern['chord'].values()))
        _main_bass_pattern =  random.choice(list(self.all_pattern['bass_rhythm'].values()))
        return [_main_chord_pattern, _main_bass_pattern]

    def getStructure(self, length):
        # 0 - 그대로, 1 - 유사, 2 - 안유사, 3 - 필인
        _structure = [0]
        while length > 0:
            _structure.append(random.randint(0, 3))
            length -=1
        return _structure
    def getOtherPattern(self, type, _pattern, ratio):
        # ratio : 0 - 그대로, 1 - 유사, 2 - 안유사, 3 - 필인
        if ratio == 0:
            pattern = _pattern
        elif ratio == 1:
            if type == 'chord':
                pattern = random.choice(list(self.all_pattern['chord'].values()))
            else:
                pattern = random.choice(list(self.all_pattern['bass_rhythm'].values()))
        elif ratio == 2:
            if type == 'chord':
                pattern = random.choice(list(self.all_pattern['chord'].values()))
            else:
                pattern = random.choice(list(self.all_pattern['bass_rhythm'].values()))
        else:
            if type == 'chord':
                pattern = random.choice(list(self.all_pattern['chord'].values()))
            else:
                pattern = random.choice(list(self.all_pattern['bass_rhythm'].values()))
        return pattern 

    def setNote(self, rhythm):
        note_list = []
        for _, _note in self.all_pattern['bass_note'].items():
            if len(_note) == self.checkNoteCount(rhythm):
                note_list.append(_note)
        return random.choice(note_list)

    def checkNoteCount(self, rhythm):
        note_count = 0
        for i in rhythm:
            if i > 0:
                note_count +=1
        return note_count

    def splitRhythm(self, _pattern, _duration):
        # _duration = int(_duration / self.tick) * 4
        one_bar = 0
        current_rhythm = []
        after_rhythm = []
        _temp_rhythm = []
        for index, r in enumerate(_pattern):
            if one_bar == _duration:
                current_rhythm = _temp_rhythm
                after_rhythm = _pattern[index:]
                break
            elif one_bar > _duration:
                over_rhythm = one_bar - _duration
                if _temp_rhythm[-1] - over_rhythm == 0:
                    last_rhythm = _temp_rhythm[-1]
                else:
                    last_rhythm = _temp_rhythm[-1] - over_rhythm
                    _temp_rhythm[-1] = last_rhythm
                current_rhythm = _temp_rhythm
                after_rhythm = _pattern[index:]
                after_rhythm.insert(0, over_rhythm)
            else:
                one_bar += abs(r)
                _temp_rhythm.append(r)
        return current_rhythm, after_rhythm

    def checkDuration(self, _pattern, _duration, _note):
        _bar = 16
        _duration = int(_duration / self.tick *4)
        sum_r = self.getRhythmSum(_pattern)
        if sum_r == _bar:
            if _duration == _bar:
                print('그대로 적용')
            elif _duration > _bar:
                print('돌리거나 리듬유지')
            else:
                print('돌림')
        elif sum_r > _bar:
            if _duration <= _bar:
                print('돌리거나 리듬 유지')
            else:
                print('그대로 적용')
        else:
            print('필인')



        pattern = []
        return [_pattern, _note]
    
    def getRhythmSum(self, rhythm):
        _duration = 0
        for r in rhythm:
            _duration += abs(r)
        return _duration

    #     temp_pattern = []
    #     section_index_n = 0
    #     bar_index_n = 0
    #     part_structure = self.setPartStructure(len(self.song_form))
    #     for part_index, (key, part) in enumerate(self.song_form.items()):
    #         if part_structure[part_index] == 0:
    #             # print(f'{part_index} 파트의 같은거')
    #             temp_pattern = self.getSimillarPattern(main_chord_pattern, 0)
    #         elif part_structure[part_index] ==1:
    #             temp_pattern = self.getSimillarPattern(main_chord_pattern, 1)
    #             # print(f'{part_index} 파트의 비슷한거')
    #         else:
    #             temp_pattern = self.getSimillarPattern(main_chord_pattern, 2)
    #             # print(f'{part_index} 파트의 다른거')
    #         section_structure = self.setPartStructure(len(part))
    #         for section in part:
    #             # if part_structure[part_index] == 0:
    #             #     print(f'의 섹션{section_index_n}은 같은거')
    #             # elif part_structure[part_index] ==1:
    #             #     print(f'의 섹션{section_index_n}은 비슷한거')
    #             # else:
    #             #     print(f'의 섹션{section_index_n}은 다른거')
    #             # bar_structure = self.setPartStructure(len(section))
    #             # print(bar_structure)
    #             bar_structure = self.setBarStructure()
    #             count = 0
    #             chord_count = 0
    #             c_d = 0
    #             while count < len(section):
    #                 duration = section[count]['chord'][1]
    #                 c_d += duration
    #                 if c_d == 1920:
    #                     section[count]['bass_rhythm'] = bar_structure[chord_count]
    #                     # print(section[count])
    #                     count +=1
    #                     chord_count+=1
    #                     c_d = 0
    #                 else:
    #                     section[count]['bass_rhythm'] = bar_structure[chord_count]
    #                     # print(section[count])
    #                     count +=1
    #                     # chord_count+=1
    #             # for index, bar in enumerate(section):
    #             #     duration = bar['chord'][1]
    #             #     if duration == 1920:
    #             #         bar['bass_rhythm'] = bar_structure[index]
    #             #     else:

    #                 # bar_index_n +=1
    #             section_index_n +=1
                
    # # 메인 패턴을 뽑음. 후에 기준 필요
    # def getChordPattern(self):
    #     chord_rhythm = self.pattern['chord']
    #     bass_rhythm = self.pattern['bass_rhythm']
    #     bass_note = self.pattern['bass_note']
    #     if self.static:
    #         main_pattern = {
    #             'chord_rhythm': chord_rhythm['pattern1'],
    #             'bass_rhythm': bass_rhythm['pattern1'],
    #             'bass_note': bass_note['pattern1'],
    #         }
    #     return main_pattern

    # def getBassPattern(self):
    #     bass_pattern = []
    #     return bass_pattern


    # # 같은거 = 0, 비슷한거 = 1, 다른거 = 2
    # def setPartStructure(self, part_length):
    #     structure_list = [0, 1, 2]
    #     part_structure = [0]
    #     a = 0
    #     while a < part_length - 1:
    #         _part = random.choice(structure_list)
    #         if _part not in part_structure:
    #             part_structure.append(_part)
    #             a+=1
    #     return part_structure

    # def setSectionStructure(self, section_length):
    #     structure_list = [0,1,2]
    #     section_structure = [0]
    #     a = 0
    #     while a < section_length - 1:
    #         section_structure.append(random.choice(structure_list))
    #         a +=1
    #     return section_structure

    # def setBarStructure(self):
    #     structure_list = [
    #         [0,0,0,0],
    #         [0,0,0,1],
    #         [0,0,0,2],
    #     ]
    #     return random.choice(structure_list)

    # def getSimillarPattern(self, pattern, ratio):
    #     orig_pattern = pattern['bass_rhythm']
    #     print(orig_pattern, ratio)
    #     print(self.all_pattern['bass_rhythm'])

    #     return 'simillar'

    # def setRhythmCase():
    #     basic_source = [2,4,6,8,10,12,14]
    #     # basic_source = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    #     total_pattern = [[16], [2,2,2,2,2,2,2,2,]]
    #     # total_pattern = []

    #     a = 1
    #     while a < len(basic_source):
    #         for i in product(basic_source, repeat = a):
    #             if sum(list(i)) == 16 and list(i) not in total_pattern:
    #                 # print(i)
    #                 total_pattern.append(list(i))
    #         a+=1
    #     arp = {}
    #     for index, i in enumerate(total_pattern):
    #         arp[f'pattern{index+1}'] = i
    #     return arp

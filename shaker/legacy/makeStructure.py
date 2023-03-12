from shaker import pattern_info, common, Genre
import random

from shaker.legacy import t_module

class MakeStructure(object):
    def __init__(self, value, song, genre):
        self.tick = value['tick']
        self.melody = value['melody']
        self.chord = value['chord_info']
        self.genre = genre

        form = self.destructFour(song, self.chord)
        new_form = self.makeSongForm(form)

        basic_pattern = self.setBasicPattern(genre)

        self.structure = self.setPattern(new_form, basic_pattern)

    # chord_info를 4마디씩 끊어줌
    # song 이란 argument는 테스트파일의 못갖춘마디를 구별하기위한 것으로 정식엔진에선 사용하지 않게 될거임
    def destructFour(self, song, _chord_info):
        one_bar = self.tick * 4
        bar_num = 0
        bar_check = 0
        section = []
        temp_section = []
        # 못갖춘마디인 테스트파일 구분
        if song == 'dynamite' or song == 'grenade' or song == 'Dynamite_new_2':
            chord_info = _chord_info[1:]
            section.append([_chord_info[0]])
        else:
            chord_info = _chord_info

        # 코드를 4마디 길이 만큼 끊어줌 ()
        for chord, duration in chord_info:
            bar_check += duration
            if bar_check != one_bar:
                temp_section.append([chord, duration])
                continue
            else:
                temp_section.append([chord, duration])
                bar_check = 0
                bar_num +=1
            if bar_num % 4 == 0:
                section.append(temp_section)
                temp_section = []
        if temp_section != []:
            section.append(temp_section)

        # 4마디 길이만큼 나뉜 코드를 섹션으로 묶음(8마디)
        total_section = []
        temp_section = []
        for one_section in section:
            if len(one_section) == 1:
                total_section.append([one_section])
            else:
                if len(temp_section) == 2:
                    total_section.append(temp_section)
                    temp_section = []
                temp_section.append(one_section)
        if temp_section != []:
            total_section.append(temp_section)

        # for index, i in enumerate(total_section):
        #     for index2, j in enumerate(i):
        #         print(f'section{index}-{index2} : {j}')
        return total_section
    
    # 8마디 단위로 끊어진 songform에 이름을 부여
    def makeSongForm(self, form):
        new_form = {}
        for index, i in enumerate(form):
            new_form[f'part{index+1}'] = i
        return new_form


    # 코드, 아르페지오 리듬, 노트를 장르에 따라 다르게 선정
    def setBasicPattern(self, genre):
        g = pattern_info.GenrePattern[genre.name]
        basic_chord = g['chord']['pattern1'] # 현재 고정값. 선정기준을 세워야함
        # arp_rhythm = g['arp_rhythm']
        arp_rhythm = t_module.setRhythmCase()
        arp_note = g['arp_note']

        # 기본 아르페지오 리듬을 랜덤선정. 후에 선정기준을 세워야함
        rand_arp_rhythm_num = random.randint(1, len(arp_rhythm))
        basic_arp_rhythm = arp_rhythm[f'pattern{rand_arp_rhythm_num}']

        # 선정된 기본 아르페지오 리듬과 같은 길이의 노트 배열을 선정
        basic_arp_note_list = []
        for key, pattern in arp_note.items():
            if len(pattern) == len(basic_arp_rhythm):
                basic_arp_note_list.append(pattern)

        # 선정된 아르페지오 노트를 랜덤선정. 후에 선정기준을 세워야함
        basic_arp_note = random.choice(basic_arp_note_list)
        
        return {'genre': g, 'chord': basic_chord, 'arp_rhythm': basic_arp_rhythm, 'arp_note': basic_arp_note}

    # 기본 패턴을 기준으로 하여 송폼에 패턴을 정해줌
    def setPattern(self, form, info):
        genre = info['genre']
        chord = info['chord']
        basic_arp_rhythm = info['arp_rhythm']
        basic_arp_note = info['arp_note']

        chord_pattern = self.setChordPattern(self.chord, self.melody)
        # print(chord_pattern)
        # print(form)
        # print(chord_pattern)

        new_pattern = []
        repeat_num = 0
        for index, (name, songForm) in enumerate(form.items()):
            for part in songForm:
                # print(repeat_num, repeat_num + len(part))
                if self.genre.with_melody:
                    new_pattern.append(self.setPart(genre, part, chord_pattern[repeat_num: repeat_num + len(part)], basic_arp_rhythm, basic_arp_note))
                else:
                    new_pattern.append(self.setPart(genre, part, chord, basic_arp_rhythm, basic_arp_note))
                repeat_num +=len(part)
        # print(new_pattern)
        return new_pattern

    # 한파트(4마디)의 각 마디마다 패턴을 선정함
    def setPart(self, genre, part, chord_rhythm, basic_arp_rhythm, basic_arp_note):
        if self.genre.with_melody:
            chord_rhythm
        else:
            chord_rhythm = genre['chord']
        # all_rhythm = genre['arp_rhythm']
        all_rhythm = t_module.setRhythmCase()
        all_note = genre['arp_note']

        #한파트(4마디)의 각 마디당 구조 설정 ex) a-a-a-b or a-a-b-a ....
        new_part_form = self.setPartForm()

        #기본 아르페지오 패턴과 유사한 패턴 선정. 정교한 기준 선정 필요
        simillarRhythm = self.setSimillarRhythm(all_rhythm, basic_arp_rhythm)
        simillarNote = self.setNote(all_note, simillarRhythm)

        #기본 아르페지오 패턴과 유사하지 않은 패턴 선정. 정교한 기준 선정 필요
        anotherRhythm = self.setAnoterRhythm(all_rhythm, basic_arp_rhythm)
        anotherNote = self.setNote(all_note, anotherRhythm)

        new_pattern = []
        part_form_num = 0
        bar_duration = 0
        current_chord = []
        current_rhythm = []
        current_note = []

        for index, (chord, duration) in enumerate(part):
            # print(index, chord, duration)
            bar_duration += abs(duration)
            # 한파트 내의 각 마디당 구조에 따라 패턴설정
            # 0 - 기본패턴, 1 - 유사패턴, 2- 유사하지않은 패턴, 3- 필인(예정)
            if new_part_form[part_form_num] == 0:
                # 2022.06.03 기준 코드 패턴에 대한 선정 기준이 없어서 고정 패턴으로 대체
                if self.genre.with_melody is False :current_chord = chord_rhythm['pattern1']
                current_rhythm = basic_arp_rhythm
                current_note = basic_arp_note
            elif new_part_form[part_form_num] ==1:
                if self.genre.with_melody is False :current_chord = chord_rhythm['pattern2']
                current_rhythm = simillarRhythm
                current_note = simillarNote
            elif new_part_form[part_form_num] ==2:
                if self.genre.with_melody is False :current_chord = chord_rhythm['pattern3']
                current_rhythm = anotherRhythm
                current_note = anotherNote
            if self.genre.with_melody : current_chord = chord_rhythm[index]


            # 한마디 분량이 될 때 마다 패턴 저장
            if bar_duration == self.tick * 4:
                # 한마디 안에 코드가 하나 있는 경우
                new_pattern.append([[chord, duration], current_chord, current_rhythm, current_note])
                part_form_num +=1
                bar_duration = 0
            else:
                # 한 마디 안에 코드가 여러개 있는 경우
                # 현재 코드의 길이 만큼 코드, 아르페지오 패턴의 길이를 수정해야함
                _current_chord = self.splitRhythmDuration(duration, current_chord)

                temp_duration = 0
                for index, h in enumerate(current_rhythm):
                    temp_duration += abs(h*120)
                    if temp_duration >= duration:
                        # 이 방식은 한마디 내에서 코드가 바뀔 때, 아르페지오 리듬이 처음 패턴으로 돌아가는 방식임.
                        rand_num = random.randint(0, 1)
                        # print('rand', rand_num)
                        current_duration = temp_duration - abs(h*120)
                        need_duration = duration - current_duration
                        fix_rhythm = current_rhythm[:index]
                        # if need_duration != 0:
                        fix_rhythm.append(int(need_duration / 120))
                        current_rhythm = fix_rhythm
                        break
                # part_form_num +=1
                bar_duration = 0

                new_pattern.append([[chord, duration], _current_chord, current_rhythm, current_note[:len(current_rhythm)]])
        return new_pattern

    # 한파트(4마디)의 각 마디마다 패턴의 형태를 선정함
    # 기본패턴, 유사패턴, 다른패턴, 필인패턴 으로 나뉨
    def setPartForm(self):
        part_form = [[0,0,0,0], [0,0,0,1], [0,0,1,0], [0, 1, 0, 1], [0,0,0,2], [0,1,0,2], [0,0,1,2], [0,2,0,2]]
        new_part_form = random.choice(part_form)
        # part_form = [0, 1, 2,] # 3 = fill_pattern
        # # 0 = basic_pattern
        # # 1 = simillar_pattern
        # # 2 = anoter_pattern
        # # 3 = fill_pattern
        # new_part_form = [0]
        # while len(new_part_form) < 4:
        #     random_part = random.choice(part_form)
        #     # if random_part == 3:
        #     #     if len(new_part_form) == 3:
        #     #         new_part_form.append(random_part)
        #     #     else:
        #     #         continue
        #     if random_part == 2:
        #         if len(new_part_form) == 3:
        #             new_part_form.append(random_part)
        #         else:
        #             continue
        #     else:
        #         new_part_form.append(random_part)
        return new_part_form

    # 기본패턴과 유사한 패턴을 선정함
    # 현재는 한 노트가 가지는 길이가 달라지는 지점이 같을 경우 유사하다고 판단함.
    def setSimillarRhythm(self, all_rhythm, rhythm):
        # 기본 패턴을 기준으로 유사한 패턴 기준 선정
        new_rhythm = [rhythm[0]]
        count = 1
        while count < len(rhythm):
            if new_rhythm[-1] != rhythm[count]:
                break
            else:
                new_rhythm.append(rhythm[count])
                count+=1
        # 유사한 패턴 모으기
        simillar_rhythm = []
        for key, value in all_rhythm.items():
            if new_rhythm == value[:len(new_rhythm)]:
                simillar_rhythm.append(value)
        # 모은 패턴 중 랜덤으로 뽑기
        # print(simillar_rhythm)
        print(f'orig : {rhythm}')
        for i in simillar_rhythm:
            print(f'similar : {i}')

        if simillar_rhythm == []:
            rand_simillar_rhythm = rhythm
        else:
            rand_simillar_rhythm = random.choice(simillar_rhythm)
        return rand_simillar_rhythm

    # 입력된 아르페지오 길이에 맞는 노트 구성 선정
    def setNote(self, all_note, rhythm):

        # 입력된 아르페지오 길이와 같은 노트 모으기
        simillar_note = []
        for key, value in all_note.items():
            if len(value) == len(rhythm):
                a = 1
                # print(value, rhythm)
                while a < len(value):
                    if value[a-1] == value[a]:
                        if rhythm[a-1] == 2 and rhythm[a] == 2:
                            break
                        else:
                            simillar_note.append(value)
                    else:
                        simillar_note.append(value)
                    a+=1
                # print(value, rhythm)
                simillar_note.append(value)
        
        # 모은 노트 중 랜덤으로 뽑기
        rand_simillar_note = random.choice(simillar_note)
        return rand_simillar_note
    
    # 기본패턴과 연관없는 패턴을 선정
    def setAnoterRhythm(self, all_rhythm, rhythm):
        another_rhythm = []
        for key, value in all_rhythm.items():
            if rhythm[0] != value[0]:
                another_rhythm.append(value)
        rand_another_rhythm = random.choice(another_rhythm)
        return rand_another_rhythm

    # 필인 전용 패턴 선정 ( 현재 미구현 )
    def setFillPattern(self, all_rhythm, rhythm):
        new_rhythm = [rhythm[0]]
        return new_rhythm

    # 한마디에 코드가 여러개 있는 경우, 입력될 패턴의 길이를 수정
    def splitRhythmDuration(self, duration, rhythm):
        # print(duration, rhythm)
        tick = int(self.tick / 4)
        temp_duration = 0
        split_duration = []
        for i in rhythm:
            if i > 0:
                current_rhythm = abs(i * tick)
                temp_duration += current_rhythm
                if temp_duration >= duration:
                    # before_duration = temp_duration - current_rhythm
                    over_duration = temp_duration - duration
                    split_duration.append(int((current_rhythm-over_duration)/tick))
                    break
                else:
                    split_duration.append(i)
            else:
                split_duration.append(i)
        return split_duration

    # 코드패턴이 멜로디에 따라 변화하는 경우에 사용
    def setChordPattern(self, chord_info, melody_info):
        melody_bar = common.setMelodyBar(chord_info, melody_info)
        # for i in melody_bar:
        #     print(i)
        new_chord_pattern = []

        for chord, melody in melody_bar:
            chord_set = int(chord[1] / (self.tick / 4))
            melody_set = int(melody[0][1] / (self.tick / 4))
            if melody[0][1] > 0:
                arg = [melody_set, -(chord_set - melody_set)]
            else:
                arg = [melody_set, -(chord_set - abs(melody_set))]

            if arg[0] < 0 and arg[1] < 0:
                arg = [abs(melody_set), -(chord_set - abs(melody_set))]
            new_chord_pattern.append(arg)
        return new_chord_pattern
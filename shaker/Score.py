from shaker import common

class SetScore(object):
    # def __init__(self, structure, info, genre):
    def __init__(self, structure, genre):
        self.genre = genre
        tick = genre['tick']
        key = genre['key']
        _melody_list = []
        _chord_list = []
        _chord_rhythm_list = []
        _bass_rhythm_list = []
        _bass_note_list = []
        _bpm_list = []
        _instrument_list = []
        _octav_list = []
        _velocity_list = []
        _vocing_type_list = []
        for pn, pv in structure.items():
            for sn, sv in pv.items():
                for bn, bv in sv.items():
                    for cn, cv in bv.items():
                        _melody_list.append(cv['melody'])
                        _chord_list.append(cv['chord_table'])
                        _chord_rhythm_list.append(cv['chord_rhythm'])
                        _bass_rhythm_list.append(cv['bass_rhythm'])
                        _bass_note_list.append(cv['bass_note'])
                        _bpm_list.append(cv['bpm'])
                        _instrument_list.append(cv['ins'])
                        _octav_list.append(cv['octav'])
                        _velocity_list.append(cv['velocity'])
                        _vocing_type_list.append(cv['vocing_type'])
        # print(_chord_list)    
        # print(_chord_rhythm_list)
        # print(_bass_rhythm_list)
        # print(_bass_note_list)
        # print(_bpm_list)
        # print(_instrument_list)
        # print(_octav_list)
        # print(_velocity_list)
        vocing = []
        for index, chord in enumerate(_chord_list):
            vocing.append(self.setVocing(chord, _melody_list[index], _vocing_type_list[index])[0])
        chord_list = self.setChordRhythm(vocing, _chord_rhythm_list, int(tick/4))
        bass_note_list = self.setArpNote(_bass_note_list, _chord_list, key, vocing)
        bass_list = self.setArpRhythm(bass_note_list, _bass_rhythm_list, int(tick/4))
        melody_list = self.setMelody(_melody_list)

        self.return_value = {
            'melody': melody_list,
            'chord_info' : _chord_list,
            'chord': chord_list,
            'bass': bass_list,
            'bpm' : _bpm_list,
            'instrument' : _instrument_list,
            'velocity': _velocity_list
        }

    def setMelody(self, melody_info):
        new_melody = []
        temp=[]
        for m_bar in melody_info:
            for idx, m in enumerate(m_bar):
                temp.append(m)
        count = 0
        repeat = True
        while repeat:
            if type(temp[count][1]) == float and type(temp[count+1][1]) == float:
                new_melody.append([temp[count][0], int(temp[count][1] + temp[count+1][1])])
            else:
                if type(temp[count][1]) != float:
                    new_melody.append(temp[count])
            count +=1
            if count == len(temp)-1:
                if temp[count] != []:
                    if type(temp[count][1]) == float:
                        new_melody.append([temp[count][0], int(temp[count][1])])
                    else:
                        new_melody.append([temp[count][0], int(temp[count][1])])
                repeat = False
        return new_melody

    # # 멜로디에 따라 코드의 보이싱을 설정
    def setVocing(self, chord_info, melody_info, vocing_type):
        # chord_info의 화성을 뽑아냄
        chord_list = [common.getChordTable(chord_info[0]), chord_info[1]]
        melody_bar = [[chord_list, melody_info]]

        # 가장 낮은 노트를 기준으로 코드의 보이싱을 변경
        new_chord = []
        for bar in melody_bar:
            # 가장 낮은 노트 선정
            min_note = self.getMinNote(bar)
            check, target_note = self.divideUpDown(bar)
            
            # 코드의 노트가 가장 낮은 멜로디 노트에 근접할때 까지 연산 
            chord = bar[0][0]
            temp_chord = []
            for note in chord:
                octav = 12
                repeat = True
                vocing_type = False # 임시
                while repeat:
                    if vocing_type: # vocing_type = True => 멜로디와 겹치게 코드를 배치
                        if check: # 첫 노트가 음표일때
                            if note + octav > target_note:
                                # print(note+octav,  min_note)
                                if note != target_note:
                                    temp_chord.append(note)
                                repeat = False
                            else:
                                note +=octav
                        else: # 첫 노트가 쉼표일때
                            if note > target_note:
                                    # print(note+octav,  min_note)
                                # if note != target_note:
                                temp_chord.append(note - 12)
                                repeat = False
                            else:
                                note +=octav
                    else: # vocing_type = False -> 멜로디보다 아래에 코드를 배치
                        if note + octav > min_note - 1:
                            temp_chord.append(note)
                            repeat = False
                        else:
                            note +=octav
            # 4화음일 경우 보이싱의 탑노트와 멜로디의 가장 낮은 부분이 반음차이일때 코드 탑노트를 제거
            if len(temp_chord) > 3:
                for i in temp_chord:
                    for j in temp_chord:
                        if abs(i - j) == 1:
                            temp_chord.remove(j)
                            break
            new_chord.append([temp_chord, bar[0][1]])
        return new_chord

    # # 가장 낮은 노트를 고름
    def getMinNote(self, bar):
        min_note = 127
        for note in bar[1]:
            if note[0] < min_note:
                min_note = note[0]
        return min_note

    def divideUpDown(self, bar):
        # True = up, False = Down
        check = True
        target_note = bar[1][0][0]
        if bar[1][0][1] > 0:
            check = True
        else:
            check = False
        return check, target_note

    # # 보이싱 완료된 코드에 해당 패턴을 넣음
    def setChordRhythm(self, chord, rhythm, tick):
        count = 0
        while count < len(chord):
            chord_rhythm = []
            for r in rhythm[count]:
                chord_rhythm.append(r * tick)
            chord[count][1] = chord_rhythm
            count +=1
        return chord

    # # 아르페지오 구조를 스코어 형태로 변경
    def setArpNote(self, _arp_note_list, target, key, vocing):
        # 다이아토닉 내의 코드의 위치를 찾아서 적절한 아르페지오 노트를 선별
        arp_set = []
        for chord, duration in target:
            arp_set.append(self.detectChord(key, chord))
        new_arp = []
        for index, note_list in enumerate(_arp_note_list):
            temp_arp = []
            for note in note_list:

                if type(note) == str: # 플랫 또는 샵인 경우
                    # print('hello')
                    _note = int(note[:-1])
                    symbol = note[-1]
                    if symbol == 'b':
                        flatsharp = -1
                    else:
                        flatsharp = 1
                    diatonic_index = (_note - 1)%7
                    if diatonic_index == _note - 1:
                        temp_arp.append(arp_set[index][diatonic_index] +flatsharp)
                    else:
                        temp_arp.append(arp_set[index][diatonic_index] +flatsharp + 12)
                else:
                    diatonic_index = (note - 1)%7
                    if diatonic_index == note-1:
                        temp_arp.append(arp_set[index][diatonic_index])
                    else:
                        temp_arp.append(arp_set[index][diatonic_index] + 12)
            new_arp.append(temp_arp)
        # print(new_arp)
        if self.genre['name'].value == 'bossa':
            octav_range = 12
        else:
            octav_range = 12
        
        for index, (chord, duration) in enumerate(vocing):
            if new_arp[index] == []: # 어쩌다가 해당 리듬에 쉼표가 올 경우
                new_arp[index] = [1]
            repeat = True
            while repeat:
                if min(chord) > max(new_arp[index]) + octav_range:
                    count = 0
                    while count < len(new_arp[index]):
                        new_arp[index][count] += 12
                        count+=1
                else:
                    repeat = False
        return new_arp

    def setArpRhythm(self, note, rhythm, tick):
        new_arp = []
        for index, i in enumerate(note):
            count = 0
            _rhythm = []
            while count < len(rhythm[index]):
                _rhythm.append(rhythm[index][count] * tick)
                count +=1
            new_arp.append([i, _rhythm])
        return new_arp

    # # 입력된 코드를 바탕으로 아르페지오 노트를 실제 노트로 변경
    def detectChord(self, key, chord):
        # 기본 다이아토닉 구조
        diatonic = common.basic_diatonic

        # 키에 맞게 다이아토닉 값을 변경
        count = 0
        while count < len(diatonic):
            note = diatonic[count] + key
            if note > 11:
                note -=12
            diatonic[count] = note
            count+=1
        
        # 현재 코드의 구성음이 다이아토닉 노트와 일치하는지 판별
        isDiatonic = True
        for i in common.getChordTable(chord):
            if i not in diatonic:
                isDiatonic = False

        # 현재 코드가 다이아토닉 코드일 때
        if isDiatonic:
            a = 0
            while a < len(diatonic):
                # 
                # if chord%12 in diatonic:
                # 현재 코드가 다이아토닉 내의 어떤 역할이냐에 따라서 노트의 구조가 바뀌어야함
                # ex) C Key일때 다이아토닉 = [0, 2, 4, 5, 7, 9, 11]
                # Dm 코드의 아르페지오 구성 = [2, 4, 5, 7, 9, 11, 12]
                # Em 코드의 아르페지오 구성 = [4, 5, 7, 9, 11, 12, 14]
                # Dm와 Em 둘다 1, 3, 5는 구성이 갖지만
                # Dm의 경우 1도와 2도의 차이는 온음이지만
                # Em의 경우 1도와 2도의 차이는 반음이므로
                # 아래의 과정을 거쳐야함
                if diatonic[a] == common.getChordTable(chord)[0]:
                    start_diatonic = diatonic[a:]
                    end_diatonic = diatonic[:a]
                    total_diatonic = start_diatonic + end_diatonic
                    count = 0 
                    while count < len(total_diatonic):
                        if total_diatonic[count] > total_diatonic[count+1]:
                            total_diatonic[count+1] += 12
                        count+=1
                        if count == len(total_diatonic)-1:
                            break
                    break
                a+=1
        #현재 코드가 다이아토닉내의 코드가 아닐 때
        else:
            # 해당 코드에 맞는 다이아토닉 노트를 리턴함
            total_diatonic = self.checkSymbol(chord)
        return total_diatonic

    # # 해당 코드에 맞는 다이아토닉을 리턴
    def checkSymbol(self, chord):
        key = chord%12
        if chord < 12:
            diatonic = [0,2,4,5,7,9,11]
            # print('this is Major')
        elif chord < 24:
            diatonic = [0,2,3,5,7,8,10]
            # print('this is Minor')
        elif chord < 36:
            diatonic = [0,2,4,6,8,10,]
            # print('this is Aug')
        elif chord < 48:
            diatonic = [0,1,3,4,6,7,9,10]
            # print('this is Dim')
        elif chord < 60:
            diatonic = [0,2,4,5,7,9,10]
            # print('this is 7')
        elif chord < 72:
            diatonic = [0,2,4,5,7,9,11]
            # print('this is M7')
        elif chord < 84:
            diatonic = [0,2,3,5,7,8,10]
            # print('this is m7')
        else:
            diatonic = [0,1,3,4,6,7,9,10]
            # print('this is m7b5')

        a = 0 
        while a < len(diatonic):
            note = diatonic[a] + key
            diatonic[a] = note
            a+=1
        return diatonic

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
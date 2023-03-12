import mido
from shaker import common
import time

class MIDI(object):
# 화성의 구성음. 범용 사용
    def __init__ (self, file_path):
        # 입력된 미디파일에서 추출하는 기본 값. tick, bpm, key, melody_structure, chord_info
        self.midi_info = self.getMidiInfo(file_path)
        # 4분음표의 tick 값 (int)
        self.tick = self.midi_info['tick']

        # BPM (float)
        self.bpm = self.midi_info['bpm']

        # key (int)
        self.key = self.midi_info['key']
        # 멜로디 (list)
        self.melody_structure = self.setMelodyStructure(self.midi_info['melody_info'])

        # 코드 (list)
        self.chord_info = self.midi_info['chord_info']
    def getMidiInfo(self, file_path:str):
        # 미디파일 가져오기
        data = mido.MidiFile(file_path)
        # print(data)
        # 4분 음표에 해당하는 tick 가져오기
        tick = data.ticks_per_beat
        # 템포, 코드, 멜로디 가져오기
        for track in data.tracks:
            # 템포 & 키 가져오기
            if track.name =='':
                for msg in track:
                    if (msg.type =='set_tempo'):
                        bpm = mido.tempo2bpm(msg.tempo)
                    if (msg.type =='key_signature'):
                        key = self.setKeyValue(msg.key)
            # 코드 가져오기
            if track.name == 'Chord':
                chord_info = []
                a = 1
                while a < len(track):
                    if (track[a-1].type == 'control_change'):
                        if track[a].time == 0:
                            chord_info.append([track[a-1].value, track[a-1].time])
                        elif track[a].time > 1920:
                            chord_info.append([track[a-1].value, int(track[a-1].time / 2)])
                            chord_info.append([track[a-1].value, int(track[a-1].time / 2)])
                        else:
                            chord_info.append([track[a-1].value, track[a].time])
                    a+=1

            #멜로디 가져오기
            if track.name == 'Melody':
                melody_info = []
                for msg in track:
                    if ('note' in msg.type): # note_on, note_off 모두 가져옴
                        # print(msg)
                        # msg.note = 음정
                        # msg.time = note_on의 경우 시작 시간
                        #            note_off의 경우 시작된 음표의 길이
                        melody_info.append([msg.note,msg.time])
        return {'tick':tick, 'bpm': bpm, 'key': key, 'chord_info': chord_info, 'melody_info': melody_info}

    # 미디파일의 키(str)를 basic_note_number를 기준으로 하는 int로 변환
    def setKeyValue(self, key:str):
        # key 문자의 길이가 1이 아닐경우 = 메이저 키가 아닐 경우
        # Am키 일경우 C키로 인식함
        if len(key) != 1:
            key_value = common.basic_note_number[key[0]] + 3
            if key_value > 11:
                key_value = key_value - 12
        else:
            key_value = common.basic_note_number[key]
        return key_value

    # 미디 파일의 멜로디 정보를 2차원 리스트로 변환
    def setMelodyStructure(self, melody_info:list):
        # 짝수 인덱스는 음의 위치, 홀수 인덱스는 음의 길이
        n = 1
        num = 0
        melody_structure = []
        while num < len(melody_info):
            if num == len(melody_info)-1:
                break
            # 노트
            note = melody_info[num][0]
            # 짝수 인덱스 - 음의 위치
            position = melody_info[num][1]
            # 홀수 인덱스 -- 음의 길이
            duration = melody_info[num+1][1]
            # 짝수 인덱스의 음의 위치가 0이 아닌 경우 = 멜로디 시작이 쉼표인 경우
            if (position !=0):
                # 쉼표를 만들어줌
                melody_structure.append([note, -position])
                # 쉼표 뒤에 노트를 만들어줌
                melody_structure.append([note, duration])
            else:
                melody_structure.append([note, duration])
            num+=2
        insert_list = []
        for index, i in enumerate(melody_structure):
            if i[1] < 0 and abs(i[1]) > self.tick * 4:
                repeat = True
                target_rhythm = i[1]
                temp_list = []
                one_bar = self.tick * 4
                while repeat:
                    if abs(target_rhythm) <= one_bar:
                        temp_list.append([i[0], target_rhythm])
                        insert_list.append([index, temp_list])
                        repeat = False
                    else:
                        temp_list.append([i[0], -one_bar])
                        target_rhythm += one_bar

        insert_count = 0
        for rest in insert_list:
            melody_structure.pop(rest[0] + insert_count)
            for i in rest[1]:
                melody_structure.insert(rest[0] + insert_count, i)
            insert_count += (len(rest[1]) - 1)
        return melody_structure
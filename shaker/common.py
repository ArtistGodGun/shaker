
# 멜로디 옥타브 높이를 제한하는 함수
def setMelodyOctav(melody_info):
    temp = []
    for i in melody_info:
        temp.append(i[0])
    octav = 12
    repeat = True
    while repeat:
        if max(temp) + octav <= 76:
            octav +=12
        else:
            for i in melody_info:
                i[0] = i[0] + octav
            repeat = False
    return melody_info

# 코드 하나의 범위 내에 있는 멜로디를 묶어내는 함수
def setMelodyBar(chord_info, melody_structure):
    # chord_info = self.chord_info
    # melody_structure = self.melody
    chord_num = 0
    melody_ct = 0 # melody_current_time
    temp_list = [] # 현재 코드 마디에 해당하는 멜로디가 임시로 저장될 리스트
    melody_bar = [] #전체 코드의 각 마디당 멜로디가 저장될 리스트. [[코드],[멜로디,멜로디,멜로디..]]
    for i in melody_structure:
    
        melody_ct += abs(i[1])
        # 현재 멜로디 전체 길이가 현재 코드 마디의 길이보다 작으면
        if melody_ct < chord_info[chord_num][1]:
            temp_list.append(i)
        else:
            before_melody = chord_info[chord_num][1] - (melody_ct - abs(i[1]))
            after_melody = abs(i[1]) - before_melody
            if i[1] < 0:
                before_melody = -before_melody
                after_melody = -after_melody
            if before_melody != 0:
                if after_melody != 0:
                    temp_list.append([i[0], float(before_melody)])
                else:
                    temp_list.append([i[0], before_melody])

                melody_bar.append({'chord_table':chord_info[chord_num], 'melody':temp_list})
            else:
                melody_bar.append({'chord_table':chord_info[chord_num], 'melody':temp_list})

            if after_melody != 0:
                if before_melody !=0:
                    temp_list = [[i[0], float(after_melody)]]
                else:
                    temp_list = [[i[0], after_melody]]

            else:
                if chord_num + 1 == len(chord_info) - 1:
                    temp_list = [melody_structure[-1]]
                else:
                    temp_list = []
            chord_num +=1
            melody_ct = after_melody

        if chord_num == len(chord_info) - 1:
            melody_bar.append({'chord_table':chord_info[chord_num], 'melody':temp_list})
            break
        
    return melody_bar
# ChordTable의 값(int)를 넣었을 때 구성음을 리턴하는 함수
def getChordTable(chord_table_value):
    if chord_table_value <96:
        # 입력된 값에서 코드 성질 추출
        chord_table = list(basic_chord_structure.items())[int(chord_table_value/12)]
        # 입력된 값에서 root음 추출
        root = list(basic_note_number.items())[chord_table_value%12][1]
        # root와 코드 성질을 기반으로 코드 구성음 추출
        chord_structure = []
        for i in chord_table[1]:
            current_key_note = i + root
            if (current_key_note > 11):
                current_key_note-= 12
            chord_structure.append(current_key_note)
    else:
        chord_structure = 'error'
    return chord_structure

def checkNoteNumber(rhythm):
    note_length = 0
    for i in rhythm:
        if i >0:
            note_length+=1
    return note_length

# 기본 다이아토닉 구조
basic_diatonic = [0,2,4,5,7,9,11]

# 코드 성격에 따른 화성구조
basic_chord_structure = {
    'M' : [0, 4, 7],
    'm' : [0, 3, 7],
    'aug' : [0, 4, 8],
    'dim' : [0, 3, 6],
    '7': [0, 4, 7, 10],
    'M7': [0, 4, 7, 11],
    'm7': [0, 3, 7, 10],
    'm7b5': [0, 3, 6, 9]            
}
# 기본 노트 넘버
basic_note_number = {
    'C': 0, 'C#':1, 'D':2, 'D#':3,
    'E':4, 'F':5, 'F#':6, 'G':7,
    'G#':8, 'A':9, 'A#':10, 'B':11
}
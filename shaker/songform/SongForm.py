from shaker.Genre import Genre
from shaker.songform import Part, Section, Bar
from shaker import common
import random
class SongForm(object):
    def __init__(self, genre: Genre, song):
        self.song =song
        self.genre = genre
        self.melody_bar = common.setMelodyBar(self.genre['chord'], self.genre['melody'])
        song_form = self.setSongForm()
        part_structure = Part.PartStructure(self.genre, song_form, song).part_structure
        for pn, pv in part_structure.items():
            part_structure[pn] = Section.Section(self.genre, self.song, pn, pv).section_info
        for part_name, part in part_structure.items():
            for section_name, section in part.items():
                part_structure[part_name][section_name] = Bar.Bar(self.genre, section_name, section).bar_info

        self.song_form_data = part_structure
        # if song == 'Dance Monkey_new':
        # for pn, pv in song_form.items():
        #     print(pn)
        #     print(pv)
        #     print()


    def setSongForm(self):
        # 파트의 구조 정의. 이 부분은 현재 기준이 없음
        # part_structure = {} # intro는 섹션 1개, verse는 섹션 2개, outro는 섹션 1개를 가짐
        bar_map = self.setBar() # 한 마디 단위로 코드(chord)를 정리함
        section_map = self.setSection(bar_map) # 한 섹션에 4개의 마디가 오도록 정리함

        # for key, part_value in part_info.items():
        #     part_structure[key] = {'section': part_value['section']}
        # part_map = self.setPart(section_map, part_structure) # part_structure에 따라 섹션들을 정리함

        return section_map


    # 만약 1마디 짜리 브레이크가 있는 경우 이 함수에 표시하기?
    def setBar(self):
        # 한 코드에 해당하는 멜로디를 정리
        melody_bar = self.melody_bar
        temp_map = {} # 임시로 멜로디바를 저장하는 딕셔너리
        return_value = {} # 리턴 값

        one_bar = self.genre['tick'] * 4 # 공식적인 한마디의 길이
        bar_check = 0 # 한 마디 안에 코드가 몇개인지 체크
        chord_count = 0 # 한 마디 안에 코드가 여러개인 경우 코드에 번호를 매김
        bar_count = 0 # 마디의 갯수
        for i in melody_bar:

            _, _duration = i['chord_table'] # 멜로디바는 코드테이블 값과 듀레이션을 한 리스트로 함
            # 만약 현재 코드의 길이가 한 마디인 경우
            if _duration == one_bar:
                temp_map[f'chord_0'] = i # 그대로 임시 딕셔너리에 코드테이블과 멜로디를 저장
                return_value[f'bar_{bar_count}'] = temp_map # bar_x 키 값에 딕셔너리를 저장
                temp_map = {} # 임시 딕셔너리 초기화
                bar_count +=1 # 한마디가 끝났으므로 카운트함
            # 만약 현재 코드의 길이가 한마디가 아닌 경우
            else:
                bar_check += _duration # 현재 코드의 길이를 bar_check에 저장
                # 만약 bar_check가 한마디가 된 경우
                if bar_check == one_bar:
                    temp_map[f'chord_{chord_count}'] = i # 현재 멜로디바를 chord_x키 값에 저장
                    return_value[f'bar_{bar_count}'] = temp_map # bar_x 키 값에 딕셔너리를 저장 (딕셔너리 안의 코드 개수가 여러개임)
                    temp_map = {} # 임시 딕셔너리 초기화
                    bar_check = 0 # bar_check 초기화 (다음에도 쓰기 위해)
                    chord_count = 0
                    bar_count +=1 # 한마디가 끝났으므로 카운트함

                # bar_check가 한마디가 못된 경우
                else:
                    temp_map[f'chord_{chord_count}'] = i # 임시 딕셔너리 - chord_x 키 값에 현재 멜로디바를 저장
                    chord_count +=1 # 코드번호를 카운트함
        if temp_map != {}:
            return_value[f'bar_{bar_count}'] = temp_map
        return return_value

    # bar_map을 입력값으로 받음. song의 경우 못갖춘마디 체크 자동화가 가능하다면 없어도 됨
    # 4개의 bar를 한 섹션으로 정의함
    def setSection(self, bar_map):
        bar_count = 0 # 마디의 번호
        section_count = 0 # 섹션의 번호
        section_map = {} # 섹션 딕셔너리
        temp_section = {} # 임시 딕셔너리

        # bar_map을 돌리기. key = bar_x, value = 한마디 안에 들어있는 멜로디 바
        for index, (key, value) in enumerate(bar_map.items()):
            # print(key)
            bar_count +=1

            # if문에 해당하는 음악은 못갖춘마디 이므로 체크. 못갖춘마디 체크 자동화가 가능하다면 else부분만 써도 됨
            if self.song == 'dynamite' or self.song == 'grenade' or self.song == 'Dynamite_new_2' or self.song =='dahyae':
                # 만약 index가 0 인 경우 - 못갖춘마디인 경우
                if index == 0:
                    section_map[f'section_{section_count}'] = { key:value } # 못갖춘 마디로 시작하는 경우 section의 이름은 0으로 시작
                    section_count +=1 # section 카운트
                else:
                    if len(temp_section) == 3: # 만약 bar의 갯수가 3개인 경우
                        temp_section[key] = value # 임시 딕셔너리에 4번째 bar를 추가
                        section_map[f'section_{section_count}'] = temp_section # section_1부터 4개의 bar를 저장
                        section_count +=1 # section 카운트
                        temp_section = {} # 임시 딕셔너리 초기화
                    else:
                        temp_section[key] = value # 임시 딕셔너리에 3번째 bar까지 계속 추가
            # 못갖춘마디가 아닌 음악
            else:
                # 만약 bar의 갯수가 4개인 경우
                if len(temp_section) == 3:
                    temp_section[key] = value # 임시 딕셔너리에 4번째 bar를 추가
                    section_map[f'section_{section_count}'] = temp_section #4개의 마디를 section_x에 추가
                    section_count +=1 # section 카운트
                    temp_section = {} # 임시 딕셔너리 초기화
                elif index == 28:
                    temp_section[key] = value
                    section_map[f'section_{section_count}'] = temp_section
                    section_count +=1 # section 카운트
                    temp_section = {}
                else:
                    temp_section[key] = value # 임시 딕셔너리에 3번째 bar가지 계속 추가

            # 만약 마지막 section 이후의 남은 마디의 갯수가 4개 미만인 경우
            if temp_section != {}: # temp_section이 빈 딕셔너리가 아니다 = 4개 미만의 마디가 아직 temp_section에 담겨있다
                section_map[f'section_{section_count}'] = temp_section # 나머지 4개 미만의 마디를 section에 추가

        return section_map

    # part_structure에서 정해진 규격에 따라 section을 part로 구분함
    def setPart(self, section_list, part_structure):

        section_count = 0
        # part_structure를 돌림. part_structure는 part의 이름, part가 가질 수 있는 section의 갯수로 이루어져 있음
        for part_name, section_length in part_structure.items():
            temp = []
            while section_length['section'] > 0: # section_length = 현재 part가 가질 수 있는 section의 갯수
                temp.append(list(section_list.items())[section_count]) # 딕셔너리를 리스트화 하여 section_count를 인덱스로 추출하여 임시 리스트에 저장
                part_structure[part_name] = dict(temp) # 리스트화된 temp를 딕셔너리화 한 후 현재 파트에 저장
                section_length['section'] -=1 # 섹션 추가가 완료되면 섹션 감소. section_length가 0이 된다는 것은 더이상 추가할 section이 없다는 것을 의미
                section_count +=1 # 인덱스를 위해 section_count는 카운트
        return part_structure




    def setSectionStructure(self, section_num):
        structure = [0]
        while section_num > 1:
            structure.append(random.choice([0,1]))
            section_num -=1
        return structure
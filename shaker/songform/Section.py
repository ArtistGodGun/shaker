import random

from shaker.Genre import GenreList

class Section(object):
    def __init__(self, genre: dict, song, part_name, part_value):
        self.change_chord_duration = False
        self.genre = genre

        _section_info = self.defineSectionInfo(part_name, part_value)
        # for sn, sv in _section_info.items():
        #     print(sn, len(sv['value']))
        #     print(sv, len(sv['value']))
        self.section_info = _section_info
        self.section_info = self.setSyncopation(_section_info)
    def defineSectionInfo(self, part_name, part_value):
        self.pName = part_name
        structure_num = self.setSectionStructure(len(part_value) - 1)
        section_info = {}
        section_num = 0
        for index, (sn, sv) in enumerate(part_value.items()):
            if sn == 'info':
                info = sv
            else:
                temp = {}
                for key, value in info.items():
                    if key == 'bpm':
                        temp[key] = self.setSectionBPM(value)
                    if key == 'ins':
                        temp[key] = self.setSectionIns(value)
                    if key == 'octav':
                        temp[key] = self.setSectionOctav(value)
                    if key == 'velocity':
                        temp[key] = self.setSectionVelocity(value)
                    if key == 'first_chord':
                        temp[key] = self.setSectionFirstChord(value)
                    if key == 'chord_rhythm':
                        temp[key] = self.setSectionChordRhythm(value, structure_num[section_num])
                    if key == 'bass_rhythm':
                        temp[key] = self.setSectionBassRhythm(value, structure_num[section_num])
                    if key == 'bass_note':
                        temp[key] = self.setSectionBassNote(value, structure_num[section_num])
                    if key == 'vocing_type':
                        temp[key] = self.setSectionVocingType(value)
                    if key == 'fill_pos':
                        temp[key] = self.setSectionFillPos(value[section_num])
                temp['bar_unit'] = self.setSectionBarUnit(sv)
                section_info[sn] = {
                    'info': temp,
                    'value':sv
                }
                section_num +=1
        return section_info

    def setSectionBPM(self, bpm):
        return bpm
    def setSectionIns(self, ins):
        return random.sample(ins, random.randint(1, len(ins)))
    def setSectionOctav(self, octav):
        return octav
    def setSectionVelocity(self, velocity):
        return velocity
    def setSectionFirstChord(self, first_chord):
        return first_chord
    def setSectionChordRhythm(self, value, structure_type):
        if structure_type == 0:
            chord_rhythm = value
        else:
            chord_rhythm = value        
        return chord_rhythm
    def setSectionBassRhythm(self, value, structure_type):
        if structure_type == 0:
            bass_rhythm = value
        else:
            bass_rhythm = value           
        return bass_rhythm
    def setSectionBassNote(self, value, structure_type):
        if structure_type == 0:
            bass_note = value
        else:
            bass_note = value       
        return bass_note

    def setSectionBarUnit(self, value):
        unit = 1
        if self.genre['name'] == GenreList.bossa:
            if len(value) == 1: # 못갖춘 마디인 섹션
                unit = 1
            else:
                unit = 2
            self.change_chord_duration = True
        return unit

    def setSectionStructure(self, section_num):
        structure = [0]
        while section_num > 1:
            structure.append(random.choice([0,1]))
            section_num -=1
        return structure

    def setSyncopation(self, section_info):
        if self.change_chord_duration:
            syncopation_count = True
            for sn, sv in section_info.items():
                value = sv['value']
                # print(len(value))
                if len(value) == 1: # 못갖춘마디인 경우 싱커페이션을 맞추지 않음
                    syncopation_count = False
                    pass
                else:
                    for (bn, bv) in value.items():
                        if len(bv) == 1:
                            if syncopation_count:
                                bv['chord_0']['chord_table'][1] -=240
                                syncopation_count = False
                            else:
                                bv['chord_0']['chord_table'][1] +=240
                                syncopation_count = True
                        else:
                            if syncopation_count:
                                bv['chord_1']['chord_table'][1] -=240
                                syncopation_count = False
                            else:
                                bv['chord_0']['chord_table'][1] +=240
                                syncopation_count = True
                            
        # for k,v in section_info.items():
        #     for k2,v2 in v.items():
        #         if k2 == 'value':
        #             for k3, v3 in v2.items():
        #                 print(k3)
        #                 print(v3)
        return section_info

    def setSectionVocingType(self, vocingType):
        return vocingType

    def setSectionFillPos(self, fill_pos):
        return fill_pos
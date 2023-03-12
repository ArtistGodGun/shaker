from shaker import common
from shaker.Genre import Instrument, GenreList
from enum import Enum
import random

# songform - part - section - bar

class PartStructure(object):
    def __init__(self, genre, section_info, song):
        self.song =song
        self.genre = genre
        self.melody_bar = common.setMelodyBar(self.genre['chord'], self.genre['melody'])

        part_structure = self.definePartStructure(self.genre, section_info)
        part_bpm = self.definePartBPM(self.genre, part_structure)
        part_instrument = self.definePartInstrument(self.genre, part_bpm)
        part_octav = self.definePartOctav(self.genre, part_instrument)
        part_velocity = self.definePartVelocity(self.genre, part_octav)
        part_firstChord = self.definePartFirstChord(self.genre, part_velocity)
        part_chordRhythm = self.definePartChordRhythm(self.genre, part_firstChord)
        part_bassRhythm = self.definePartBassRhythm(self.genre, part_chordRhythm)
        part_bassNote = self.definePartBassNote(self.genre, part_bassRhythm)
        part_key = self.definePartKey(self.genre, part_bassNote)
        part_vocing = self.definePartVocing(self.genre, part_key)
        part_fillin = self.definePartFillin(self.genre, part_vocing)

        self.part_structure = part_fillin

        # for pn, pv in self.part_structure.items():
        #     print(pn)
        #     print(pv)

    def definePartStructure(self, genre, section_info):
        if len(section_info) == 2: # 8마디 짜리 테스트곡 용
            part_structure = {
                'part_0': {
                    'info': {},
                    'section_0': section_info['section_0'],
                    'section_1': section_info['section_1'],
                    }
                }
        elif len(section_info) == 3: # 못갖춘마디 음악
            part_structure = {
                'part_0' : {
                    'info': {},
                    'section_0' : section_info['section_0'],
                },
                'part_1': {
                    'info': {},
                    'section_0' : section_info['section_1'],
                    'section_1' : section_info['section_2']
                }
            }
        else: # 나머지 음악
            part_structure = {}
            part_count = 0
            part_section_count = 0
            for index, (sn, sv) in enumerate(section_info.items()):
                # print(sn, index, part_section_count,part_count, )
                if index == 7:
                    part_structure[f'part_{part_count}'][sn] = sv
                    part_structure[f'part_{part_count}']['info'] = {}
                    part_count +=1
                    part_section_count = index -1
                if part_section_count % 2 == 0:
                    part_structure[f'part_{part_count}'] = {
                        'info': {},
                        sn: sv
                    }
                else:
                    part_structure[f'part_{part_count}'][sn] = sv
                    part_structure[f'part_{part_count}']['info'] = {}
                    part_count +=1
                part_section_count +=1
        return part_structure

    def definePartInstrument(self, genre, part_structure):
        def InsRule(instrument):
            return random.sample(instrument, random.randint(1, len(instrument)))
        instrument = genre['ins']
        for key, part_info in part_structure.items():
            part_structure[key]['info']['ins'] = InsRule(instrument)
            # part_structure[key]['ins'] = [Instrument.piano] # 일단 이걸로 고정
        return part_structure

    def definePartOctav(self, genre, part_structure):
        def OctavRule():
            return random.randint(1,3)
        for key, part_info in part_structure.items():
            part_structure[key]['info']['octav'] = OctavRule()
        return part_structure

    def definePartVelocity(self, genre, part_structure):
        def VelocityRule():
            return random.randint(2,4)
        for key, part_info in part_structure.items():
            part_structure[key]['info']['velocity'] = VelocityRule()
        return part_structure

    def definePartFirstChord(self, genre, part_structure):
        def FirstChordRule():
            first_chord = [0, 16, 21]
            return random.choice(first_chord)
        for key, part_info in part_structure.items():
            part_structure[key]['info']['first_chord'] = FirstChordRule()
        return part_structure

    def definePartChordRhythm(self, genre, part_structure):
        def chordRhythmRule(chord_rhythm_list):
            chord_rhythm = []
            for key, value in chord_rhythm_list.items():
                chord_rhythm.append(value)
            return random.choice(chord_rhythm)

        for key, part_info in part_structure.items():
            part_structure[key]['info']['chord_rhythm'] = chordRhythmRule(genre['pattern']['chord'])

        return part_structure

    def definePartBassRhythm(self, genre, part_structure):
        def bassRhythmRule(bass_rhythm_list):
            bass_rhythm = []
            for key, value in bass_rhythm_list.items():
                bass_rhythm.append(value)
            return random.choice(bass_rhythm)
        for key, part_info in part_structure.items():
            part_structure[key]['info']['bass_rhythm'] = bassRhythmRule(genre['pattern']['bass_rhythm'])
        return part_structure

    def definePartBassNote(self, genre, part_structure):
        def bassNoteRule(bass_note_list, bass_rhythm):
            bass_note = []
            for key, value in bass_note_list.items():
                # print(value)
                if len(value) == common.checkNoteNumber(bass_rhythm):
                    bass_note.append(value)
            return random.choice(bass_note)
        for key, part_info in part_structure.items():
            part_structure[key]['info']['bass_note'] = bassNoteRule(genre['pattern']['bass_note'], part_structure[key]['info']['bass_rhythm'])
        return part_structure

    def definePartBPM(self, genre, part_structure):
        def bpmRule(orig_bpm):
            return orig_bpm
        for key, part_info in part_structure.items():
            part_structure[key]['info']['bpm'] = bpmRule(genre['bpm'])
        return part_structure

    def definePartKey(self, genre, part_structure):
        def keyRule(orig_key):
            return orig_key
        for key, part_info in part_structure.items():
            part_structure[key]['info']['key'] = keyRule(genre['key'])
        return part_structure

    def definePartVocing(self, genre, part_structure):
        def vocingRule(orig_key):
            return orig_key
        for key, part_info in part_structure.items():
            part_structure[key]['info']['vocing_type'] = vocingRule(genre['vocing_type'])
        return part_structure
    
    def definePartFillin(self, genre, part_structure):
        def fillinRule(section_len, final):
            fill_pos = []
            if genre['name'] == GenreList.bossa:
                if final:
                    fill_pos = [0,1]
                else:
                    while len(fill_pos) < section_len:
                        if len(fill_pos) == section_len - 1:
                            fill_pos.append(0)
                        else:
                            fill_pos.append(0)
            else:
                while len(fill_pos) < section_len:
                    if len(fill_pos) == section_len - 1:
                        fill_pos.append(1)
                    else:
                        fill_pos.append(0)
            return fill_pos
        for index, (key, part_info) in enumerate(part_structure.items()):
            if index == len(part_structure) - 1:
                final = True
            else:
                final = False
            part_structure[key]['info']['fill_pos'] = fillinRule(len(part_info)-1, final)
        return part_structure
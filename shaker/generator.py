
import random, time
from mido import MidiTrack, Message, MetaMessage,bpm2tempo, MidiFile

class Generator(object):
    def __init__(self, track, melody, bpm):
        m = MidiFile()
        ch_count = 0
        META = self.setMetaTrack(bpm)
        m.tracks.append(META)
        MELODY = self.generateMelody(ch=ch_count, melody_info= melody)
        # print(MELODY)
        # time.sleep(123123)
        m.tracks.append(MELODY)
        for ins in track:
            ch_count +=1
            temp_chord = []
            temp_bass = []
            for bar in ins:
                ins = bar[0]
                chord = bar[1]
                bass = bar[2]
                temp_chord.append(chord)
                temp_bass.append(bass)
            CHORD = self.generateRightHandChord(ch = ch_count, chord_structure = temp_chord)
            ch_count +=1
            BASS = self.generateArp(ch = ch_count, arp = temp_bass)
            m.tracks.append(CHORD)
            m.tracks.append(BASS)
            
        self.m = m




    def setMetaTrack(self, bpm):
        _META = MidiTrack()
        _META.append(MetaMessage('set_tempo', tempo = bpm2tempo(bpm)))
        return _META
    def setMidiTrack(self, track):
        print('hello')


    def generateMelody(self, ch : int, melody_info: list):
        track= MidiTrack()
        for m in melody_info:
            rand_velocity = random.randint(30,40)
            if m[1] >0: # m[1] >0 => 음표, m[1] < 0 => 쉼표
                track.append(Message('note_on', channel = ch, velocity = rand_velocity, note = m[0], time = 0))
                track.append(Message('note_off', channel = ch, velocity = rand_velocity, note = m[0], time = m[1]))
            else:
                track.append(Message('note_off', channel = ch, velocity = rand_velocity, note = m[0], time = abs(m[1])))
        return track

    def generateRightHandChord(self, ch : int, chord_structure: list):
        track= MidiTrack()
        for chord, rhythm in chord_structure:
            for r in rhythm:
                humanize_time_list = []
                if r > 0:
                    for index, note in enumerate(chord):
                        v = self.setVelocity(2)
                        humanizer_time = random.randrange(0,20)
                        track.append(Message('note_on', channel = ch, velocity = v, note = note, time = humanizer_time))
                        humanize_time_list.append(humanizer_time)
                    for index, note in enumerate(chord):
                        if index == 0:
                            track.append(Message('note_off', channel = ch,  note = note, time = abs(r - sum(humanize_time_list))))
                        else:
                            track.append(Message('note_off', channel = ch,  note = note,time = 0))
                else:
                    for index, note in enumerate(chord):
                        if index == 0:
                            track.append(Message(
                                'note_off',
                                channel = ch, 
                                note = note,
                                time = abs(r)
                            ))
                        else:
                            track.append(Message(
                                'note_off',
                                channel = ch, 
                                note = note,
                                time = 0
                            ))
        # # track.append(Message('note_on', note = 60, time = 0))

        return track

    def generateArp(self, ch : int, arp: list):
        track = MidiTrack()
        for note, rhythm in arp:
            note_count = 0
            for r in rhythm:
                random_velocity = self.setVelocity(2)
                if r > 0:
                    track.append(Message('note_on', channel = ch, velocity = random_velocity, note = note[note_count], time = 0))
                    track.append(Message('note_off', channel = ch, velocity = random_velocity, note = note[note_count], time = int(abs(r))))
                    note_count +=1
                else:
                    track.append(Message('note_off', channel = ch, velocity = random_velocity, note = note[note_count-1], time = int(abs(r))))
        return track

    # def generateArp(self, ch : int, arp: list):
    #     track = MidiTrack()
    #     for note, rhythm in arp:
    #         count = 0
    #         while count < len(note):
    #             random_velocity = self.setVelocity(3)
    #             if rhythm[count] > 0:
    #                 track.append(Message('note_on', channel = ch, velocity = random_velocity, note = note[count], time = 0))
    #                 track.append(Message('note_off', channel = ch, velocity = random_velocity, note = note[count], time = abs(rhythm[count])))
    #             else:
    #                 track.append(Message('note_off', channel = ch, velocity = random_velocity, note = note[count], time = abs(rhythm[count])))
    #             count += 1
    #     return track


    def setVelocity(self, velocity_value):
        # velocity_value는 1~7단계로 구성. 각 단계에서 랜덤적용
        # 1 : 1~20
        # 2 : 21~40
        # 3 : 41~60
        # 4 : 61 ~ 80
        # 5 : 81 ~ 100
        # 6 : 101 ~ 120
        # 7 : 121 ~ 127
        if velocity_value <7:
            velocity = random.randrange(velocity_value * 20 - 19, velocity_value * 20)
        else:
            velocity = random.randrange(121, 127)
        return velocity


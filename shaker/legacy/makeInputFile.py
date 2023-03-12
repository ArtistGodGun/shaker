import mido
from mido import MidiTrack, MetaMessage, bpm2tempo, Message
from sympy import Symbol, solve
class MIDI(object):
# 화성의 구성음. 범용 사용
    def __init__ (self, file_path):
        # 입력된 미디파일에서 추출하는 기본 값. tick, bpm, key, melody_structure, chord_info
        self.midi_info = self.getMidiInfo(file_path)

    def getMidiInfo(self, file_path:str):
        first = True
        data = mido.MidiFile(file_path)
        # print(data.ticks_per_beat)
        # 미디파일 가져오기
        x = Symbol('x')
        equation = data.ticks_per_beat * x - 480
        t = solve(equation)[0]
        new_midi = mido.MidiFile()       
        new_midi.ticks_per_beat = 480
        _META = MidiTrack()
        _META.append(MetaMessage('key_signature', key = 'D'))
        _MELODY = MidiTrack()
        _MELODY.name = 'Melody'
        for track in data.tracks:
            if track.name =='':
                for msg in track:
                    if (msg.type == 'set_tempo'):
                        _META.append(MetaMessage('set_tempo', tempo = msg.tempo))
            if track.name == 'Melody':
                for msg in track:
                    if 'note' in msg.type:
                        if first:
                            _MELODY.append(Message(msg.type, note = msg.note, time = msg.time * t))
                            first = False
                        else:
                            _MELODY.append(Message(msg.type, note = msg.note, time = msg.time * t))

        print(_MELODY)

        _CHORD = MidiTrack()
        _CHORD.name = 'Chord'
        _CHORD.append(Message('control_change', control=23, value = 13, time = 0))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1920))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1920))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        _CHORD.append(Message('control_change', control=23, value = 13, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 11, time = 720))
        _CHORD.append(Message('control_change', control=23, value = 4, time = 1200))
        _CHORD.append(Message('control_change', control=23, value = 9, time = 720))
        
        
        _CHORD.append(MetaMessage('end_of_track', time = 1920))

        new_midi.tracks.append(_META)
        new_midi.tracks.append(_MELODY)
        new_midi.tracks.append(_CHORD)
        new_midi.save('input/ddd.mid')
        # print(_MELODY)
        

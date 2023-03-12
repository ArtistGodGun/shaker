class Track(object):
    def __init__(self, score: dict, genre):
        self.total_instrument = genre.genre_data['ins']
        chord_info = score['chord_info']
        chord = score['chord']
        bass = score['bass']
        bpm = score['bpm']
        instrument = score['instrument']
        velocity = score['velocity']
        instrument_track = self.setInstrumentTrack(instrument, chord_info)
        self.track = self.setTrackInfo(instrument_track, score)
    def setInstrumentTrack(self, _instrument, _chord_info):
        total_ins = []
        for _ins_list in _instrument:
            for ins in _ins_list:
                if ins not in total_ins:
                    total_ins.append(ins)
        track = []
        for index, (c, d) in enumerate(_chord_info):
            temp = []
            for ins in total_ins:
                if ins in _instrument[index]:
                    temp.append([ins, d])
                else:
                    temp.append([ins, -d])
            track.append(temp)
        a = 0
        track_list = []
        while a < len(track[0]):
            temp = []
            for i in track:
                temp.append(i[a])
            track_list.append(temp)
            a+=1
        return track_list

    def setTrackInfo(self, track, info):
        chord = info['chord']
        bass = info['bass']
        total = []
        for ins in track:
            temp = []
            for index, bar in enumerate(ins):
                temp.append([bar, chord[index], bass[index]])
            total.append(temp)
        return total
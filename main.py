
from shaker import Parser, Genre, Score, reharmonization, Track, generator
from shaker.songform import SongForm
from mido import MidiTrack, MidiFile, MetaMessage, bpm2tempo, Message
from shaker.Genre import GenreList
from shaker.legacy import makeInputFile
# from midi2audio import FluidSynth
import subprocess, os, time, sys


if __name__ =='__main__':
    test_files = [
        'dancingqueen',
        'getlucky',
        'dandan',
        'celebrity',
        'boongboong',
        '1245',
        'flytothemoon',
        'grenade',
        'dynamite',
        'her',
        'hobbang',
        'test'
    ]
 
    # -1 : 모든 test_files를 실행
    # 0 ~ : test_files의 개별 인덱스를 실행
    song_num = int(sys.argv[1])
    # song_num = 4

    if song_num == -1:
        test = test_files
    else:
        test = [test_files[song_num]]
    # g_list = [GenreList.newage, GenreList.bossa]
    # bpm_list = ['orig', 'fast', 'slow']
    g_list = [GenreList.newage, GenreList.bossa]
    bpm_list = ['orig']
 
    if 'output' not in os.listdir():
        os.mkdir('output')

    for g in g_list:
        for b in bpm_list:
            for i in test:
                song = i
                print(f'title : {song}')
                # 0. 미디 파일 읽기
                # makeInputFile.MIDI(f'input/{song}.mid')
                midi = Parser.MIDI(f'input/{song}.mid')
                return_value = {
                    'tick': midi.tick,
                    'bpm': midi.bpm,
                    'key': midi.key,
                    'melody': midi.melody_structure, # 멜로디 정보
                    'chord_info': midi.chord_info # 코드 정보
                    }
                user_select_genre = g
                if user_select_genre == Genre.GenreList.bossa:
                    if b == 'orig':
                        user_select_bpm = int(return_value['bpm'])
                    elif b == 'fast':
                        user_select_bpm = int(return_value['bpm'] * 1.2)
                    else:
                        user_select_bpm = int(return_value['bpm'] * 0.8)
                    rev_volume = 0.5
                elif user_select_genre == Genre.GenreList.ragtime:
                    if b == 'orig':
                        user_select_bpm = int(return_value['bpm'])
                    rev_volume = 0.5
                else:
                    if b == 'orig':
                        user_select_bpm = int(return_value['bpm'])
                    elif b == 'fast':
                        user_select_bpm = int(return_value['bpm'] * 1.2)
                    else:
                        user_select_bpm = int(return_value['bpm'] * 0.8)
                    rev_volume = 1
                user_data = {
                    'genre' : user_select_genre, ## 220627 현재 장르 선택하는 방법 (GenreList.newage / GenreList.bossa)  
                    'bpm' : user_select_bpm,
                    'emotion' : Genre.Emotion.pleasure,
                    'instrument' : Genre.Instrument.piano,
                    'length' : '3minute'
                }

                GenreData = Genre.Genre(user_data, return_value)
                reharm = reharmonization.Reharmonization(GenreData).reharmonization

                SongFormData = SongForm.SongForm(reharm, song).song_form_data

                score = Score.SetScore(SongFormData, reharm).return_value
                track = Track.Track(score, GenreData).track
                gen = generator.Generator(track, score['melody'], user_select_bpm)
                # generator = Generator.Generator(track, score['melody'], user_select_bpm)
                result_path = f'output/{song}_result_{GenreData.genre_data["name"].value}_{b}.mid'
                gen.m.save(result_path)

                # fs = FluidSynth(sound_font='SGM.sf2')
                # fs.midi_to_audio(result_path, f'output/temp.mp3')
                
                subprocess.run(['fluidsynth', '-ni', '-g', '5', 'SGM.sf2', result_path, '-F', 'output/temp.mp3', '--quiet'])
                # time.sleep(1)
                subprocess.run(['ffmpeg', '-i',
                                f'output/temp.mp3',
                                '-i',
                                'ir.wav',
                                '-lavfi',
                                "afir=dry=10:wet=3:length=1",'output/temp_rev.mp3',
                                '-y', '-v','quiet'])
                subprocess.run(['ffmpeg',
                                '-i', 'output/temp.mp3',
                                '-i', 'output/temp_rev.mp3',
                                '-filter_complex',
                                f'[0]volume=1[outa];[1]volume={rev_volume}[outb];[outa][outb]amix=inputs=2:[outs];[outs]loudnorm=I=-15:TP=-2:LRA=11',
                                f'output/{song}_result_{GenreData.genre_data["name"].value}_{b}.mp3', '-y','-v','quiet'])
                time.sleep(1)
                os.remove('output/temp.mp3')
                os.remove('output/temp_rev.mp3')
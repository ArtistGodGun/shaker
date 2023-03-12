from shaker.Genre import Genre

class Reharmonization(object):
    def __init__(self, genre:Genre):
        self.genre = genre.genre_data
        self.reharmonization = self.setReharmonization(self.genre)
    def setReharmonization(self, info):
        return info


# import random
# from shaker import common

# # 코드를 변화하는 함수
# class Reharmonization(object):
#     def __init__(self, value):
#         return_chord = []
#         diatonic = self.setDiatonic(value['key'])

#         melody_chord_bar = common.setMelodyBar(value['chord_info'], value['melody'])
#         before_chord = self.setSingleChord(melody_chord_bar[0], diatonic, [])
#         return_chord.append([before_chord, melody_chord_bar[0][0][1]])

#         for i in melody_chord_bar[1:]:
#             before_chord = self.getCurrentChord(before_chord, i, diatonic)
#             return_chord.append([before_chord, i[0][1]])

#         self.new_chord = return_chord

#     def setDiatonic(self, key):
#         new_diatonic = []
#         for i in common.basic_diatonic:
#             new_note = i + key
#             if new_note > 11:
#                 new_note -= 12
#             new_diatonic.append(new_note)
#         tonic = [
#             new_diatonic[0],
#             new_diatonic[0] + 60,
#             new_diatonic[2] + 12,
#             new_diatonic[2] + 72,
#             new_diatonic[5] + 12,
#             new_diatonic[5] + 72
#         ]
#         subDominant = [
#             new_diatonic[1] + 12,
#             new_diatonic[1] + 72,
#             new_diatonic[3],
#             new_diatonic[3] + 60,
#         ]
#         dominant = [
#             new_diatonic[4],
#             new_diatonic[4] + 48,
#             # new_diatonic[6]+ 36,
#             # new_diatonic[6] + 84,
#         ]
#         return {'diatonic': new_diatonic, 'tonic': tonic, 'subDominant': subDominant, 'dominant': dominant}

#     def setSingleChord(self, melody_bar, diatonic_info, del_chord):
#         chord = melody_bar[0][0]
#         melody = self.melodyToBasic(melody_bar[1])
#         reharm_list = []
#         diatonic_check = True
#         if chord in diatonic_info['tonic']:
#             reharm_list = diatonic_info['tonic']
#         elif chord in diatonic_info['subDominant']:
#             reharm_list = diatonic_info['subDominant']
#         elif chord in diatonic_info['dominant']:
#             reharm_list = diatonic_info['dominant']
#         else:
#             diatonic_check = False
#         if del_chord != [] and reharm_list != []:
#             for d_chord in del_chord:
#                 reharm_list.remove(d_chord)

#         if diatonic_check:
#             chord_choice = []
#             for re_chord in reharm_list:
#                 _new_chord_info = common.getChordTable(re_chord)
#                 same_note = []
#                 for m in melody:
#                     if m in _new_chord_info:
#                         same_note.append(m)
                
#                 chord_choice.append([re_chord, _new_chord_info, list(set(same_note))])
#             max_value = 0
#             top_list = []
#             for i in chord_choice:
#                 chord_rate = len(i[2]) / len(i[1])
#                 if chord_rate >= max_value:
#                     max_value = chord_rate
#                     top_list.append(i)
#             return_chord = random.choice(top_list)[0]
#         else:
#             return_chord = chord
#         return return_chord

#     def getCurrentChord(self, before_chord, current_info, diatonic_info):
#         repeat = True
#         del_chord = []
#         com_num = 0
#         while repeat:
#             # if count >10:
#                 # print(new_chord, before_chord)
#             new_chord = self.setSingleChord(current_info, diatonic_info, del_chord)
#             if before_chord != new_chord:
#                 repeat = False
#             elif common.getChordTable(before_chord)[:3] == common.getChordTable(new_chord)[:3]:
#                 del_chord.append(new_chord)
#                 if com_num > 10:
#                     repeat = False
#                 com_num+=1
#             else:
#                 if com_num > 10:
#                     repeat = False
#                 del_chord.append(new_chord)
#                 com_num+=1
#         return new_chord
# #
#     def melodyToBasic(self, melody_list):
#         octav = 12
#         new_melody_list = []
#         for i in melody_list:
#             repeat = True
#             new_melody = i[0]
#             while repeat:
#                 if new_melody >11:
#                     new_melody -= octav
#                 elif new_melody - octav < 0:
#                     new_melody_list.append(new_melody)
#                     repeat = False
#         return new_melody_list

#     # 미사용
#     # def chordNumberToString(self, chord_num, key):
#     #     diatonic = self.setDiatonic()
#     #     symbol_num = 0
#     #     for index, i in enumerate(diatonic['diatonic']):
#     #         if chord_num%12 == i:
#     #             symbol_num = index


#     #     chord_string_num = 0
#     #     tried_string = ''
#     #     repeat = True
#     #     tried_string = ['M', 'm', 'aug', 'dim', '7', 'M7', 'm7', 'm7b5']
#     #     symbol_string_list = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii']
#     #     octav = 1
#     #     while repeat:
#     #         if chord_num < 12*octav:
#     #             chord_string_num = chord_num - (octav-1)*12
#     #             tried_string = tried_string[octav-1]
#     #             repeat = False
#     #         else:
#     #             octav +=1
                
#     #     for k, value in common.basic_note_number.items():
#     #         if value == chord_string_num:
#     #             chord_string = k
#     #     return chord_string+tried_string

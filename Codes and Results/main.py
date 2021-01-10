import numpy as np
from Classes import *
from Utilities import *
import time
overlap_rate = 0.3
piece_len = 7
k = 0
mode = 2 # 1:direct pitch and consider consonance, 2:pitch difference
pitch_operation = 1 # 1:difference, 2:direct
duration_operation = 1 # 1: ratio 2: difference
consider_note_distance = False
consider_downbeat = True
downbeat_weight = 1.2

consider_force = False

def locate(filepath, piece):
    music = np.load(filepath)
    for i in range(0, len(music)):
        flag = 1
        for j in range(len(piece)):
            if (i + j) >= len(music):
                flag = 0
                break
            if music[i+j].pitch != piece[j].pitch or music[i+j].length != piece[j].length or music[i+j].downbeat != piece[j].downbeat or music[i+j].force != piece[j].force:
                flag = 0
                break
        if flag == 1:
            print('path: %s\tstart index: %d\tend index:%d' % (filepath, i, i+len(piece)))



def show_match(match, name_corr=None):
    for (piece1, piece2, similarity) in match:
        print('-----------------------------')
        if name_corr is not None:
            for i in name_corr:
                if i[0].all == piece2.all:
                    print(i[1])
                    path = 'dataset/' + i[1]
                    break
        print('Similarity:%.6f' % similarity)
        locate('dataset/case14_离人愁.npy', piece1)
        for i in range(len(piece1)):
            print('%d(%d)' % (piece1[i].pitch, piece1[i].downbeat), end='\t')
        print()
        locate(path, piece2)
        for j in range(len(piece2)):
            print('%d(%d)' % (piece2[j].pitch, piece2[j].downbeat), end='\t')
        print()

def compare_with_all_brutal(name):
    name_list = {'case1_song_a.npy': 'case1_song_b.npy', 'case1_song_b.npy': 'case1_song_a.npy',
                 'case4_Oh_Why.npy': 'case4_Shape_Of_You.npy', 'case4_Shape_Of_You.npy': 'case4_Oh_Why.npy',
                 'case5_大海航行靠舵手.npy': 'case5_我为祖国献石油.npy', 'case5_我为祖国献石油.npy': 'case5_大海航行靠舵手.npy',
                 'case6_十月里响起一声春雷.npy': 'case6_我爱你中国.npy', 'case6_我爱你中国.npy': 'case6_十月里响起一声春雷.npy',
                 'case9_shoule.npy': 'case9_wusulichuan.npy', 'case9_wusulichuan.npy': 'case9_shoule.npy',
                 'case11_Creep.npy': 'case11_Get Free.npy', 'case11_Get Free.npy': 'case11_Creep.npy',
                 'case14_山外小楼夜听雨.npy': 'case14_离人愁.npy', 'case14_清明雨上.npy': 'case14_离人愁.npy',
                 'case14_烟花易冷.npy': 'case14_离人愁.npy', 'case14_离人愁.npy': 'case14_离人愁.npy',
                 'case14_红尘客栈.npy': 'case14_离人愁.npy',
                 'case15_something_just_like_this.npy': 'case15_孤芳自赏.npy',
                 'case15_孤芳自赏.npy': 'case15_something_just_like_this.npy',
                 'case16_我只在乎你.npy': 'case16_落叶归根.npy', 'case16_落叶归根.npy': 'case16_我只在乎你.npy',
                 'case17_敖包相会.npy': 'case17_月亮之上.npy', 'case17_月亮之上.npy': 'case17_all_rise.npy',
                 'case17_all_rise.npy': 'case17_月亮之上.npy'}
    music_1 = Music(name)
    music_1.execute(pitch_operation=pitch_operation, duration_operation=duration_operation,
                    piece_len=piece_len, overlap_rate=overlap_rate)
    result = {}
    for key, value in name_list.items():
        if key in name:
            continue
        music_2 = Music('dataset/' + key)
        music_2.execute(pitch_operation=pitch_operation, duration_operation=duration_operation,
                        piece_len=piece_len, overlap_rate=overlap_rate)
        distance = compare2_2(music_1, music_2, mode=mode, k=k, consider_note_distance=consider_note_distance,
                                    consider_downbeat=consider_downbeat, downbeat_weight=downbeat_weight,
                                    consider_force=consider_force, print_Matrix=False)
        result[key] = distance
    result = sorted(result.items(), key=lambda d: d[1], reverse=False)
    print('------------------------------------------------result:--------------------------------------------------')
    name = name[8:]
    print('name:\t%s' % name)
    index = 0
    for key, value in result:
        index += 1
        # print('[%s]:\t%.10f' % (key, value))
        print('%s:\t%.4f' % (key, value))
        if key == name_list[name]:
            # print('target:\t%s' % key)
            res_index = index
            print('index:\t%d' % res_index)

    return res_index


def compare_with_all(name):
    name_list = {'case1_song_a.npy': 'case1_song_b.npy', 'case1_song_b.npy': 'case1_song_a.npy',
                 'case4_Oh_Why.npy': 'case4_Shape_Of_You.npy', 'case4_Shape_Of_You.npy': 'case4_Oh_Why.npy',
                 'case5_大海航行靠舵手.npy': 'case5_我为祖国献石油.npy', 'case5_我为祖国献石油.npy':'case5_大海航行靠舵手.npy',
                 'case6_十月里响起一声春雷.npy': 'case6_我爱你中国.npy', 'case6_我爱你中国.npy':'case6_十月里响起一声春雷.npy',
                 'case9_shoule.npy': 'case9_wusulichuan.npy', 'case9_wusulichuan.npy': 'case9_shoule.npy',
                 'case11_Creep.npy': 'case11_Get Free.npy', 'case11_Get Free.npy': 'case11_Creep.npy',
                 'case14_山外小楼夜听雨.npy': 'case14_离人愁.npy', 'case14_清明雨上.npy': 'case14_离人愁.npy',
                 'case14_烟花易冷.npy': 'case14_离人愁.npy', 'case14_离人愁.npy': 'case14_离人愁.npy',
                 'case14_红尘客栈.npy': 'case14_离人愁.npy',
                 'case15_something_just_like_this.npy': 'case15_孤芳自赏.npy',
                 'case15_孤芳自赏.npy': 'case15_something_just_like_this.npy',
                 'case16_我只在乎你.npy': 'case16_落叶归根.npy','case16_落叶归根.npy': 'case16_我只在乎你.npy',
                 'case17_敖包相会.npy': 'case17_月亮之上.npy', 'case17_月亮之上.npy': 'case17_all_rise.npy',
                 'case17_all_rise.npy': 'case17_月亮之上.npy'}
    music_1 = Music(name)
    music_1.execute(pitch_operation=pitch_operation, duration_operation=duration_operation,
                    piece_len=piece_len, overlap_rate=overlap_rate)
    result = {}
    match_list = {}
    for key, value in name_list.items():
        if key in name:
            continue
        music_2 = Music('dataset/' + key)
        music_2.execute(pitch_operation=pitch_operation, duration_operation=duration_operation,
                        piece_len=piece_len, overlap_rate=overlap_rate)
        similarity, match = compare(music_1, music_2, mode=mode, k=k, consider_note_distance=consider_note_distance,
            consider_downbeat=consider_downbeat, downbeat_weight=downbeat_weight,
            consider_force=consider_force, print_Matrix=False)
        result[key] = similarity
        match_list[key] = match
    result = sorted(result.items(), key=lambda d:d[1], reverse=True)
    print('------------------------------------------------result:--------------------------------------------------')
    name = name[8:]
    print('name:\t%s' % name)
    index = 0
    for key, value in result:
        index += 1
        # print('[%s]:\t%.10f' % (key, value))
        if key == name_list[name]:
            print('target:\t%s' % key)
            res_index = index
            match = match_list[key]
            print('index:\t%d' % res_index)
            if 'case16' in key:
                np.save('case16_match.npy', match)
    # show_match(match)



    return res_index

def one_to_many(name):
    name_list = {'case14_山外小楼夜听雨.npy': 'case14_离人愁.npy', 'case14_清明雨上.npy': 'case14_离人愁.npy',
                 'case14_烟花易冷.npy': 'case14_离人愁.npy', 'case14_红尘客栈.npy': 'case14_离人愁.npy'}
    music_1 = Music(name)
    music_1.execute(pitch_operation=pitch_operation, duration_operation=duration_operation,
                    piece_len=piece_len, overlap_rate=overlap_rate)
    piece_list_total = []
    piece_list_total_original = []
    name_corr = []
    music = Music(None)
    for key, value in name_list.items():
        print(key)
        music_2 = Music('dataset/' + key)
        music_2.execute(pitch_operation=pitch_operation, duration_operation=duration_operation,
                        piece_len=piece_len, overlap_rate=overlap_rate)
        piece_list_total = piece_list_total + music_2.pieces_list
        piece_list_total_original = piece_list_total_original + music_2.pieces_list_original
        for i in music_2.pieces_list_original:
            name_corr.append([i, key])
    music.pieces_list_original = piece_list_total_original
    music.pieces_list = piece_list_total

    similarity, match = compare(music_1, music, mode=mode, k=k, consider_note_distance=consider_note_distance,
                                consider_downbeat=consider_downbeat, downbeat_weight=downbeat_weight,
                                consider_force=consider_force, print_Matrix=False)


    show_match(match, name_corr)


def compare_with_all_no_piece(name):
    name_list = {'case1_song_a.npy': 'case1_song_b.npy', 'case1_song_b.npy': 'case1_song_a.npy',
                 'case4_Oh_Why.npy': 'case4_Shape_Of_You.npy', 'case4_Shape_Of_You.npy': 'case4_Oh_Why.npy',
                 'case5_大海航行靠舵手.npy': 'case5_我为祖国献石油.npy', 'case5_我为祖国献石油.npy':'case5_大海航行靠舵手.npy',
                 'case6_十月里响起一声春雷.npy': 'case6_我爱你中国.npy', 'case6_我爱你中国.npy':'case6_十月里响起一声春雷.npy',
                 'case9_shoule.npy': 'case9_wusulichuan.npy', 'case9_wusulichuan.npy': 'case9_shoule.npy',
                 'case11_Creep.npy': 'case11_Get Free.npy', 'case11_Get Free.npy': 'case11_Creep.npy',
                 'case14_山外小楼夜听雨.npy': 'case14_离人愁.npy', 'case14_清明雨上.npy': 'case14_离人愁.npy',
                 'case14_烟花易冷.npy': 'case14_离人愁.npy', 'case14_离人愁.npy': 'case14_离人愁.npy',
                 'case14_红尘客栈.npy': 'case14_离人愁.npy',
                 'case15_something_just_like_this.npy': 'case15_孤芳自赏.npy',
                 'case15_孤芳自赏.npy': 'case15_something_just_like_this.npy',
                 'case16_我只在乎你.npy': 'case16_落叶归根.npy','case16_落叶归根.npy': 'case16_我只在乎你.npy',
                 'case17_敖包相会.npy': 'case17_月亮之上.npy', 'case17_月亮之上.npy': 'case17_all_rise.npy',
                 'case17_all_rise.npy': 'case17_月亮之上.npy'}
    music_1 = Music(name)
    music_1.execute(pitch_operation=pitch_operation, duration_operation=duration_operation,
                    piece_len=piece_len, overlap_rate=overlap_rate)
    result = {}
    for key, value in name_list.items():
        if key in name:
            continue
        music_2 = Music('dataset/' + key)
        music_2.execute(pitch_operation=pitch_operation, duration_operation=duration_operation,
                        piece_len=piece_len, overlap_rate=overlap_rate)
        dis = dl_distance(music_1.original_notes_list, music_2.original_notes_list, mode=mode, k=k, consider_note_distance=consider_note_distance,
            consider_downbeat=consider_downbeat, downbeat_weight=downbeat_weight,
            consider_force=consider_force, print_Matrix=False)
        result[key] = dis
    result = sorted(result.items(), key=lambda d:d[1])
    print('------------------------------------------------result:--------------------------------------------------')
    name = name[8:]
    print('name:\t%s' % name)
    index = 0
    for key, value in result:
        index += 1
        # print('[%s]:\t%.10f' % (key, value))
        if key == name_list[name]:
            res_index = index
    print('index:\t%d' % res_index)
    return res_index

def compare_wrapper():
    name_list = {'case1_song_a.npy': 'case1_song_b.npy', 'case1_song_b.npy': 'case1_song_a.npy',
                 'case4_Oh_Why.npy': 'case4_Shape_Of_You.npy', 'case4_Shape_Of_You.npy': 'case4_Oh_Why.npy',
                 'case5_大海航行靠舵手.npy': 'case5_我为祖国献石油.npy', 'case5_我为祖国献石油.npy': 'case5_大海航行靠舵手.npy',
                 'case6_十月里响起一声春雷.npy': 'case6_我爱你中国.npy', 'case6_我爱你中国.npy': 'case6_十月里响起一声春雷.npy',
                 'case9_shoule.npy': 'case9_wusulichuan.npy', 'case9_wusulichuan.npy': 'case9_shoule.npy',
                 'case11_Creep.npy': 'case11_Get Free.npy', 'case11_Get Free.npy': 'case11_Creep.npy',
                 'case14_山外小楼夜听雨.npy': 'case14_离人愁.npy', 'case14_清明雨上.npy': 'case14_离人愁.npy',
                 'case14_烟花易冷.npy': 'case14_离人愁.npy', 'case14_离人愁.npy': 'case14_离人愁.npy',
                 'case14_红尘客栈.npy': 'case14_离人愁.npy',
                 'case15_something_just_like_this.npy': 'case15_孤芳自赏.npy',
                 'case15_孤芳自赏.npy': 'case15_something_just_like_this.npy',
                 'case16_我只在乎你.npy': 'case16_落叶归根.npy', 'case16_落叶归根.npy': 'case16_我只在乎你.npy',
                 'case17_敖包相会.npy': 'case17_月亮之上.npy', 'case17_月亮之上.npy': 'case17_all_rise.npy'}
    total = 0
    num = 0
    correct = 0
    for key, value in name_list.items():
        if 'case14' in key or 'case17' in key:
            continue
        res_index = compare_with_all('dataset/' + key)
        print('res index:%d' % res_index)
        total += res_index
        if (res_index == 1):
            correct += 1
        num += 1
    print('------------------------------------------------------------------------------------')
    print('k=%.4f' % k)
    print('total: %d' % (num))
    print('total average index:\t%.4f' % (total / num))
    print('correct rate:\t%.4f' % (correct / num))

if __name__ == "__main__":
    # one_to_many('dataset/case14_离人愁.npy')
    compare_wrapper()
    # compare_with_all('dataset/case17_月亮之上.npy')


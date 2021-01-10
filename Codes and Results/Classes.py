import numpy as np
import copy

class Note:
    def __init__(self):
        self.pitch = 0          # 音高
        self.length = 0         # 音符长度
        self.downbeat = False   # 是否重音
        self.force = 0          # 力度大小

class Music:
    def __init__(self, name):
        '''
        :param name: address of the music
        '''
        if name is None:
            return
        self.name = name
        notes_list = np.load(name)
        self.original_notes_list = copy.deepcopy(notes_list)
        self.notes_list = copy.deepcopy(notes_list)
        # print('Music [%s] has been created with length %d' % (self.name, len(self.original_notes_list)))

    def pitch_difference(self):
        self.notes_list[0].pitch = 0
        for i in range(1, len(self.original_notes_list)):
            self.notes_list[i].pitch = self.original_notes_list[i].pitch - self.original_notes_list[i-1].pitch
        # print('Music [%s] calculates difference of pitch' % self.name)

    def pitch_direct(self):
        for i in range(0, len(self.original_notes_list)):
            self.notes_list[i].pitch = self.original_notes_list[i].pitch % 12

    def duration_ratio(self):
        self.notes_list[0].length = 1
        for i in range(1, len(self.original_notes_list)):
            self.notes_list[i].length = self.original_notes_list[i].length / self.original_notes_list[i-1].length
        # print('Music [%s] calculates ratio of duration' % self.name)

    def duration_difference(self):
        self.notes_list[0].length = 0
        for i in range(1, len(self.original_notes_list)):
            self.notes_list[i].length = self.original_notes_list[i].length - self.original_notes_list[i - 1].length

    def cut_into_pieces(self, piece_len=6, overlap_rate=0.5):
        '''
        notes_list: notes列表
        piece_len: 切片的长度，单位为note
        overlap_rate: 切片间的重叠率
        '''
        self.piece_len = piece_len
        self.overlap_rate = overlap_rate
        pieces_list = []
        pieces_list_original = []
        overlap = int(piece_len * overlap_rate) # 重叠部分长度
        stride = piece_len - overlap # 移动长度
        index = 0
        while(index < len(self.notes_list)):
            if index+piece_len <= len(self.notes_list):
                pieces_list.append(self.notes_list[index:index+piece_len])
                pieces_list_original.append(self.original_notes_list[index:index+piece_len])
            else:
                pieces_list.append(self.notes_list[index:])
                pieces_list_original.append(self.original_notes_list[index:])
            index += stride
        self.pieces_list = pieces_list
        self.pieces_list_original = pieces_list_original
        # print('piece length: %d\toverlap rate: %.4f\tnumber of pieces: %d' % (self.piece_len, self.overlap_rate, len(self.pieces_list)))

    def execute(self, pitch_operation, duration_operation, piece_len=6, overlap_rate=0.5):

        if pitch_operation == 1:
            self.pitch_difference()
        elif pitch_operation == 2:
            self.pitch_direct()

        if duration_operation == 1:
            self.duration_ratio()
        elif duration_operation == 2:
            self.duration_difference()
        self.cut_into_pieces(piece_len, overlap_rate)
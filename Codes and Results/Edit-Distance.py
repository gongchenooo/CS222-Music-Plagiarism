from collections import defaultdict

k = 0.2

'''
note: [pitch, duration, weight]
'''
def sub_cost(note1, note2, consider_note_distance=False, consider_weight=False):
    if note1 == 'empty':
        cost_pitch = 1
        cost_duration = k * note2[1]
        cost = cost_pitch + cost_duration
        if consider_weight:
            cost = cost * note2[2]
        # print(note1, note2, cost)
        return cost
    elif note2 == 'empty':
        cost_pitch = 1
        cost_duration = k * note1[1]
        cost = cost_pitch + cost_duration
        if consider_weight:
            cost = cost * note1[2]
        # print(note1, note2, cost)
        return cost
    elif (note1[0]==note2[0]) and (note1[1]==note2[1]):
        cost = 0
        # print(note1, note2, cost)
        return cost

    if consider_note_distance:
        cost_pitch = float(abs(note1[0] - note2[0])) / 12 # 12音阶
    else:
        cost_pitch = 1 - (note1[0] == note2[0])
    cost_duration = k * abs(note1[1] - note2[1])
    cost = cost_pitch + cost_duration
    if consider_weight:
        cost = cost * note1[2] * note2[2]
    # print(note1, note2, cost)
    return cost

def dl_distance(s1, s2, consider_note_distance=False, consider_weight = False, returnMatrix=False, printMatrix=False):
    matrix = [[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)]
    # initialize
    matrix[0][0] = 0
    for i in range(1, len(s2)+1):
        print(i)
        matrix[0][i] = matrix[0][i-1] + sub_cost('empty', s2[i-1])
    for j in range(1, len(s1)+1):
        matrix[j][0] = matrix[j-1][0] + sub_cost(s1[j-1], 'empty')

    print('original:\t', matrix)
    for i in range(len(s1)):
        for j in range(len(s2)):
            ch1, ch2 = s1[i], s2[j]
            '''
            print(i, j,':')
            print('de', de_cost(ch1, ch2, consider_note_distance, consider_weight))
            print('in:', in_cost(ch1, ch2, consider_note_distance, consider_weight))
            '''
            matrix[i + 1][j + 1] = min([
                matrix[i][j + 1] + sub_cost(ch1, 'empty', consider_note_distance, consider_weight),
                matrix[i + 1][j] + sub_cost('empty', ch2, consider_note_distance, consider_weight),
                matrix[i][j] + sub_cost(ch1, ch2, consider_note_distance, consider_weight) #substitution or no change
            ])

    if printMatrix:
        for i in matrix:
            print(i)
    if returnMatrix:
        return matrix
    else:
        return matrix[-1][-1]


def dl_ratio(s1, s2, **kw):
    'returns distance between s1&s2 as number between [0..1] where 1 is total match and 0 is no match'
    try:
        return 1 - (dl_distance(s1, s2, **kw)) / (2.0 * max(len(s1), len(s2)))
    except ZeroDivisionError:
        return 0.0


def match_list(s, l, **kw):
    '''
	returns list of elements of l with each element having assigned distance from s
	'''
    return map(lambda x: (dl_distance(s, x, **kw), x), l)


def pick_N(s, l, num=3, **kw):
    ''' picks top N strings from options best matching with s
		- if num is set then returns top num results instead of default three
	'''
    return sorted(match_list(s, l, **kw))[:num]


def pick_one(s, l, **kw):
    try:
        return pick_N(s, l, 1, **kw)[0]
    except IndexError:
        return None

'''
def substring_match(text, s, transposition=True,
                    **kw):  #TODO: isn't backtracking too greedy?
    """
	fuzzy substring searching for text in s
	"""
    for k in ("nonMatchingEnds", "returnMatrix"):
        if k in kw:
            del kw[k]

    matrix = dl_distance(
        s, text, returnMatrix=True, nonMatchingEnds=True, **kw)

    minimum = float('inf')
    minimumI = 0
    for i, row in enumerate(matrix):
        if row[-1] < minimum:
            minimum = row[-1]
            minimumI = i

    x = len(matrix[0]) - 1
    y = minimumI

    #backtrack:
    while x > 0:
        locmin = min(matrix[y][x - 1], matrix[y - 1][x - 1], matrix[y - 1][x])
        if matrix[y - 1][x - 1] == locmin:
            y, x = y - 1, x - 1
        elif matrix[y - 1][x] == locmin:
            y = y - 1
        elif matrix[y][x - 1] == locmin:
            x = x - 1

    return minimum, (y, minimumI)


def substring_score(s, text, **kw):
    return substring_match(s, text, **kw)[0]


def substring_position(s, text, **kw):
    return substring_match(s, text, **kw)[1]


def substring_search(s, text, **kw):
    score, (start, end) = substring_match(s, text, **kw)
    # print score, (start, end)
    return text[start:end]

def match_substrings(s, l, score=False, **kw):
    'returns list of elements of l with each element having assigned distance from s'
    return map(lambda x: (substring_score(x, s, **kw), x), l)


def pick_N_substrings(s, l, num=3, **kw):
     picks top N substrings from options best matching with s
		- if num is set then returns top num results instead of default three
	
    return sorted(match_substrings(s, l, **kw))[:num]


def pick_one_substring(s, l, **kw):
    try:
        return pick_N_substrings(s, l, 1, **kw)[0]
    except IndexError:
        return None

'''

if __name__ == "__main__":
    s1 = [[0, 1, 1], [0, 2, 1], [0, 3, 1]]
    s2 = [[0, 1, 1], [0, 3, 1]]

    print(dl_distance(s1, s2, consider_note_distance=False, consider_weight=False,
                      returnMatrix=False, printMatrix=True))

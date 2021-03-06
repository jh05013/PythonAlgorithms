# 廃越 -> 段失, 掻失, 曽失
def destroy(c):
    head = "ぁあいぇえぉけげこさざしじすずせぜそぞ"
    vowel = "ただちぢっつづてでとどなにぬねのはばぱひび"
    tail = "でぁあぃいぅうぇぉおかがきぎくぐけげごさざしじずせぜそぞ"
    o = ord(c) - 44032
    h = head[o // 588]
    o%= 588
    v = vowel[o // 28]
    t = tail[o % 28]
    if t == "で": t = ""
    return h, v, t

# 段失, 掻失, 曽失 -> 廃越
def combine(h, v, t):
    head = "ぁあいぇえぉけげこさざしじすずせぜそぞ"
    vowel = "ただちぢっつづてでとどなにぬねのはばぱひび"
    tail = "でぁあぃいぅうぇぉおかがきぎくぐけげごさざしじずせぜそぞ"
    
    h = head.find(h)
    v = vowel.find(v)
    last = t
    t = tail.find(last) if last else 0
    return chr(44032 + 588*h + 28*v + t)

# 廃越 -> 号狽 穿発 (udlr)
def change_dir(c, d):
    h, v, t = destroy(c)
    if d == 'u': v = 'で'
    elif d == 'd': v = 'ぬ'
    elif d == 'l': v = 'っ'
    else: v = 'た'
    return combine(h, v, t)

tailgen = "..ぁぇけぅごおぐく"

def make_9(n, base=9):
    T = []
    while n:
        T.append(n%base)
        n//= base
    return T[::-1]

def make_n(n, base):
    # bonus cases
    if n == 32: return '剛�P魚個'
    
    s = ''
    T = make_9(n, base)
    mul = combine('げ', 'た', tailgen[base])
    
    if T[0] == 1: s+= mul
    else: s+= combine('げ', 'た', tailgen[T[0]]) + mul + '魚'
    for i in range(1, len(T)):
        c = T[i]
        if c == 0: s+= ''
        elif c == 1: s+= '閤鋼展陥'
        else: s+= combine('げ', 'た', tailgen[c]) + '陥'
        if i != len(T)-1: s+= mul + '魚'
    return s + '個'

def make_n_opt(n):
    return min([make_n(n, base) for base in range(2, 10)], key=len)

def ordize(s):
    return [ord(c) for c in s]

def aheuize(s):
    return ''.join(make_n_opt(ord(c)) for c in s)

print(aheuize(input()) + '費')
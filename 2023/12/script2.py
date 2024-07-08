def match(s, p, i, j):
    #print(f'match({s}, {p}, {i}, {j})')
    map = {}
    def check(i, j, s, p):
        #print(f'check({i}, {j}, {s}, {p})')
        if (i, j, p) in map:
            return map[(i, j, p)]
        if i == len(s) and j == len(p):
            return 1
        elif j == len(p):
            return 0
        elif i == len(s):
            if p[j] == '*':
                return check(i, j + 1, s, p)
            return 0
        else:
            res = 0
            if (s[i] == '#' or s[i] == '?') and p[j] == '#':
                res += check(i + 1, j + 1, s, p)
            elif (s[i] == '?' or s[i] == '.') and p[j] == '*':
                res += check(i + 1, j, s, p)
                res += check(i, j + 1, s, p)
            elif s[i] == '#' and p[j] == '*':
                res += check(i, j + 1, s, p)
            elif (s[i] == '?' or s[i] == '.') and p[j] == '+':
                res += check(i + 1, j, s, p[:j] + '*' + p[j + 1:])
        map[(i, j, p)] = res
        print(f'check({i}, {j}, {s}, {p})')
        print(map)
        return res
    
    return check(i, j, s, p)    

def p():
    with open('example.txt', 'r') as f:
        lines = f.readlines()
    ans_a = 0
    ans_b = 0
    for line in lines:
        line = line.split()
        s_a = line[0]
        s_b = '?'.join([s_a] * 5)
        p_a = '*' + '+'.join(['#' * int(n) for n in line[1].split(',')]) + '*'
        p_b = '*' + '+'.join(['#' * int(n) for n in line[1].split(',')] * 5) + '*'
        ans_a += match(s_a, p_a, 0, 0)
        #ans_b += match(s_b, p_b, 0, 0)
    return ans_a, ans_b

if __name__ == '__main__':
    print(p())
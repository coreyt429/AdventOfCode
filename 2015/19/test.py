#TODO: AUTOMATIC CNF CONVERTER
input = """Al => ThF
Al => ThZaaa
Zaaa => RnZaab
Zaab => FAr
Al => ThZaa
Zaa => RnZab
Zab => FAr
B => BCa
B => TiB
B => TiZba
Zba => RnZbb
Zbb => FAr
Ca => CaCa
Ca => PB
Ca => PZca
Zca => RnZcb
Zcb => FAr
Ca => SiZcc
Zcc => RnZcd
Zcd => FZce
Zce => YZcf
Zcf => FAr
Ca => SiZcg
Zcg => RnZch
Zch => MgAr
Ca => SiTh
F => CaF
F => PMg
F => SiAl
H => CZha
Zha => RnZhb
Zhb => AlAr
H => CZhc
Zhc => RnZhd
Zhd => FZhe
Zhe => YZhf
Zhf => FZhg
Zhg => YZhh
Zhh => FAr
H => CZhi
Zhi => RnZhj
Zhj => FZhk
Zhk => YZhl
Zhl => MgAr
H => CZhm
Zhm => RnZhn
Zhn => MgZho
Zho => YZhp
Zhp => FAr
H => HCa
H => NZhq
Zhq => RnZhr
Zhr => FZhs
Zhs => YZht
Zht => FAr
H => NZhu
Zhu => RnZhv
Zhv => MgAr
H => NTh
H => OB
H => OZhw
Zhw => RnZhx
Zhx => FAr
Mg => BF
Mg => TiMg
N => CZna
Zna => RnZnb
Znb => FAr
N => HSi
O => CZoa
Zoa => RnZob
Zob => FZoc
Zoc => YZod
Zod => FAr
O => CZoe
Zoe => RnZof
Zof => MgAr
O => HP
O => NZog
Zog => RnZoh
Zoh => FAr
O => OTi
P => CaP
P => PTi
P => SiZpa
Zpa => RnZpb
Zpb => FAr
Si => CaSi
Th => ThCa
Ti => BP
Ti => TiTi
e => HF
e => NAl
e => OMg
"""
 
def getatom(s, i):
    if s == 'e':
        return 'e'
    if s[i].upper() != s[i]:
        return None
    for x in range(i+1, len(s)):
        if s[x].upper() == s[x]:
            return s[i:x]
    return s[i:]
 
molecule = "CRnCaCaCaSiRnBPTiMgArSiRnSiRnMgArSiRnCaFArTiTiBSiThFYCaFArCaCaSiThCaPBSiThSiThCaCaPTiRnPBSiThRnFArArCaCaSiThCaSiThSiRnMgArCaPTiBPRnFArSiThCaSiRnFArBCaSiRnCaPRnFArPMgYCaFArCaPTiTiTiBPBSiThCaPTiBPBSiRnFArBPBSiRnCaFArBPRnSiRnFArRnSiRnBFArCaFArCaCaCaSiThSiThCaCaPBPTiTiRnFArCaPTiBSiAlArPBCaCaCaCaCaSiRnMgArCaSiThFArThCaSiThCaSiRnCaFYCaSiRnFYFArFArCaSiRnFYFArCaSiRnBPMgArSiThPRnFArCaSiRnFArTiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF"
 
#input = """e => H
#e => O
#H => HO
#H => OH
#O => HH"""
#molecule = "HOHOHO"
 
import itertools #https://docs.python.org/2/library/itertools.html#recipes
import collections #https://docs.python.org/2/library/collections.html
import re #https://docs.python.org/2/library/re.html
import json #https://docs.python.org/2/library/json.html
 
calibrate = set()
rules = collections.defaultdict(list)
revrules = collections.defaultdict(list)
 
pattern = r"(.+) => (.+)"
for src,repl in map(lambda y: (int(x) if x.isdigit() else x for x in y), re.findall(pattern, input)): #input.splitlines()
    rules[src] += [repl]
    revrules[repl] += [src]
    for start in re.finditer(src, molecule):
        start = start.start()
        calibrate.add(molecule[:start] + repl + molecule[start+len(src):])
 
print("Part One:",len(calibrate))
 
"""FAILED PART 2 BFS
queue = collections.defaultdict(set)
queue[0] = set(["e"])
steps = 0
while True:
    if len(queue[steps]) == 0:
        steps += 1
        print steps, len(queue[steps])
    current = queue[steps].pop()
    for i in range(len(current)):
        for rule in rules[getatom(current, i)]:
            n = current[:i] + rule + current[i+len(getatom(current,i)):]
            if "".join(n) == molecule:
                print "Part Two:", steps+1
            queue[steps+1].add(n)
"""
 
cyk = collections.defaultdict(lambda: collections.defaultdict(list))
for i,a in enumerate(re.findall("[A-Z][a-z]*", molecule)):
    cyk[0][i] = [a]
    insize = i
backref = collections.defaultdict(lambda: collections.defaultdict(list))
for y in range(1, insize+1):
    for x in range(insize-y+1):
        for i in range(0,y):
            need = [t[0]+t[1] for t in itertools.product(cyk[i][x], cyk[y-i-1][x+i+1])]
            for n in need:
                for blah in revrules.get("".join(n), []):
                    if blah not in cyk[y][x]:
                        cyk[y][x].append(blah)
                        backref[y][x].append(((x,i),(x+i+1,y-i-1),n))
 
out = str(cyk[insize-1][0]) + "\n\n"
for y in range(0,insize+1):
    for x in range(insize-y+1):
        out += str(x) +","+ str(y+x) + " "
        for i in cyk[y][x]:
            out += i + ","
        out += " "
        for i in backref[y][x]:
            out += "("
            for asd in i[0:2]:
                out += "(" + str(asd[0]) + "," + str(asd[0]+asd[1]) + "),"
            out += i[2] + ")"
        out += "\t"
    out += "\n"
out += "\n"
def recur(x,y): #TODO: IS THIS WRONG IF THE FIRST EXPANSION FOUND IS NONOPTIMAL? (probably not because CNF)
    global cyk,backref,out
    if y == 0:
        out += "at bottom: " + cyk[y][x][0] + "\n"
        return
    l,r,n = backref[y][x][0]
    out += cyk[y][x][0] + " -> " + n + " (" + str(x) + "," + str(y) + ": " + repr(l) + "," + repr(r) + ")\n"
    recur(*l)
    recur(*r)
recur(0,insize)
with open("19_out.txt","w") as f:
    f.write(out)
print("Part Two:",len(re.findall("^[^Z].* ->", out, re.MULTILINE))) #TODO: CAN JUST KEEP A COUNTER IN RECUR
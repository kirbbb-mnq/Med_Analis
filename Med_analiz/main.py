import io
import difflib
import pandas as pd
in_file = "Med_analiz\медицинские_протоколы.txt"

file = io.open(in_file, encoding='utf-8')

case = {}

def redact(read):
    while True:
        read = read.lower()
        if read.endswith('.') or read.endswith(' '):
            read = read[0:len(read) - 1]
        else:
            return read.strip()

def similarity(s1, s2):
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()

def reder(line):
    step = []
    line = line.split(";")[6]
    for i in line.split(","):
        if len(i) > 4:
            i = redact(i)
            i = i.replace("  "," ")
            i = i.replace('"',"")
            i = i.replace('" ',"")
            i = i.strip()
            if "не" not in i and len(i) > 4:
                step.append(i)
    return step
    
indsl = {}

def analiz(line):
    line = reder(line)
    for blok in line:
        if blok in indsl:
            indsl[blok] += 1
        else:
            indsl[blok] = 1


for line in file:
    analiz(line)


for key, val in indsl.items():
    for it in case.keys():
        if similarity(key, it) > 0.72 or ((it in key or key in it) and similarity(key, it) > 0.612):
            case[it] += val
            break
    else:
        if val > 10:
            case[key] = val


top10 = []
print("Самые частые диагнозы")
for j in range(10):
    final_dict = dict([max(case.items(), key=lambda k_v: k_v[1])])
    for k, y in final_dict.items():
        print(f"{j + 1} - {k}")
        top10.append(k)
    case.pop(k)


medkey = []
medday = []
keys = []
year = []
fame = []
s0, s1, s2, s3, s4, s5, s6, s7, s8, s9 = [], [], [], [], [], [], [], [], [], []

filed = io.open(in_file, encoding='utf-8')

for line in filed:
    blok = reder(line)
    binar = {}
    binar_sl = 0
    for i in range(10):
        binar[i] = 0
    for key in blok:
        for its in range(10):
            it = top10[its]
            if similarity(key, it) > 0.72 or ((it in key or key in it) and similarity(key, it) > 0.612):
                binar[its] = 1
                binar_sl += 1
        if binar_sl:
            delis = line.split(';')
            medkey.append(delis[0])
            medday.append(delis[1])
            keys.append(delis[2])
            year.append(delis[3])
            fame.append(delis[4])
            s0.append(binar[0])
            s1.append(binar[1])
            s2.append(binar[2])
            s3.append(binar[3])
            s4.append(binar[4])
            s5.append(binar[5])
            s6.append(binar[6])
            s7.append(binar[7])
            s8.append(binar[8])            
            s9.append(binar[9])                    


exel = pd.DataFrame({
    "MedicalRecordKey" : medkey,
    "MedicalRecordDate" : medday,
    "PatientKey" : keys,
    "Возраст" : year,
    "Пол" : fame,
    top10[0] : s0,
    top10[1] : s1,
    top10[2] : s2,
    top10[3] : s3,
    top10[4] : s4,
    top10[5] : s5,
    top10[6] : s6,
    top10[7] : s7,
    top10[8] : s8,
    top10[9] : s9,
})

exel.to_excel("Med_analiz\\binar_outs.xlsx")
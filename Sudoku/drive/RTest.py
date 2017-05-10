correct = []

with open("sudokus_finish.txt") as fFin:
    for st in fFin:
        t = ''.join(e for e in st if e.isalnum())
        correct.append(t)

outputs = []
with open("output_backtrack.txt") as fFin:
    for st in fFin:
        t = ''.join(e for e in st if e.isalnum())
        outputs.append(t)

res = []
for i in range( len(outputs) ):
    if(outputs[i] == correct[i]):
        res.append("Correct")
    else:
        res.append("Wrong")
        
print "Correct: " + str(res.count("Correct"))
print "Wrong: " + str(res.count("Wrong"))

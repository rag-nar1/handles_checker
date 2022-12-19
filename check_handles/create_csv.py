import csv



file =open('result.txt','r')
status={}
data=list(file.read().split("\n"))
for i in data:
    for j in range(len(i)):
        if i[j]==" ":
            status[i[:j]]=i[j+1:].strip()
            break

filex=open("files/final.csv","w")
fields=["handle","status","handle status"]
writer=csv.DictWriter(filex,fieldnames=fields)
writer.writeheader()
for i in status:
    y='no'
    x='exists'
    if status[i]=='0':
        x='not exists'
    if status[i]=='1':
        y='yes'
    writer.writerow({"handle":i,"status":x,"handle status":y})

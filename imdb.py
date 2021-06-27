import pymysql
import csv
import sys

def fetch(cur, sql):
    cur.execute(sql)
    row = cur.fetchone()
    for i in range(10000) :
        if(row==None): break
        print(row)
        row = cur.fetchone()

conn = pymysql.connect(
        host='localhost',
        user='db2020',
        password='db2020',
        db='assignment'
        )

curs = conn.cursor(pymysql.cursors.DictCursor)

inp = input("영화제목을 입력하여, 이에 매칭되는 영화를 검색 : ") # Miss Jerry
sql = 'select * from Movie where primaryTitle="%s"' % inp
fetch(curs, sql)

inp = input("특정 배우가 등장하는 영화를 별점이 높은 순으로 검색 : ") # Richard Burton
sql = 'select n.primaryName, m.originalTitle, r.averageRating from\
       (Rating r join Movie m on r.tconst = m.tconst) join\
       (RelatedMovie rm join `Name` n on rm.nconst = n.nconst)\
       on rm.tconst = r.tconst where n.primaryName="%s"\
       order by r.averageRating desc;' % inp
fetch(curs, sql)

inp = input("특정 감독이 제작한 영화를 개봉연도 순으로 검색 : ") # William K.L. Dickson
sql = 'select n.primaryName, m.originalTitle, m.startYear\
       from Movie m join Principal p on m.tconst = p.tconst\
       join `Name` n on p.nconst = n.nconst\
       where n.primaryName="%s" order by m.startYear;' % inp;
fetch(curs, sql)

inp = input("특정 장르의 영화를 별점이 높은 순으로 검색 : ") # Drama
sql = 'select g.genre, m.primaryTitle, r.averageRating\
       from Movie m join Genre g on m.tconst = g.tconst\
       join Rating r on m.tconst = r.tconst where g.genre = "%s"\
       order by r.averageRating desc limit 10000;' % inp
fetch(curs, sql)

inp = input("영화별 상영 지역 개수 검색(GROUP BY) : ") # X
sql = 'select m.originalTitle, count(t.region)\
        from Title t join Movie m on t.tconst = m.tconst\
        group by m.tconst limit 100;'
fetch(curs, sql)

curs.close()
conn.close()

#for i, row in enumerate(reader):
#    line = ""
#    if(i==0) :
#        for cell in row :
#            line += cell + ", "
#    else :
#        for j, cell in enumerate(row):
#            line += cell + "   "
#    print(line)
##    if(i % 1000000 == 0) : print("===================================",i,"===================================")
#    if(i == stop) : break

''' #Movie Table

the_file = open('title.basics.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 100000000000
parameters = []
sql = "insert into Movie(tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes) values(%s,%s,%s,%s,%s,%s,%s,%s);"

for i, row in enumerate(reader):
    line = ""
    if(i==0) :
        for cell in row :
            line += cell + "   "
    else :
        temp=()
        for j, cell in enumerate(row):
            if(j==8): continue
            line += cell + "   "
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
        #print(temp)
        parameters.append(temp)
        if(i%100000==0):
            #print(parameters)
            print("===================================",i,"===================================")
            try:
                curs.executemany(sql, parameters)
                conn.commit()
                parameters=[]
            except:
                pass
                #print("*******************error at ",i, " / ",row)
    #            print("Unexpected error:", sys.exc_info()[0])
    #print(line)
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()

'''

'''  # Rating Table 

the_file = open('title.ratings.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 100000000000000
parameters = []
sql = "insert into Rating(tconst, averageRating, numVotes) values(%s,%s,%s);"

for i, row in enumerate(reader):
    line = ""
    if(i==0) :
        for cell in row :
            line += cell + "   "
    else :
        temp=()
        for j, cell in enumerate(row):
            #if(j==8): continue
            line += cell + "   "
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
        #print(temp)
        parameters.append(temp)
        if(i%100000==0):
            #print(parameters)
            print("===================================",i,"===================================")
            try:
                curs.executemany(sql, parameters)
                conn.commit()
                parameters=[]
            except:
                pass
                #print("*******************error at ",i, " / ",row)
    #            print("Unexpected error:", sys.exc_info()[0])
    #print(line)
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()

'''


'''  # Genre Table 

the_file = open('title.basics.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000
parameters = []
sql = "insert into Genre(tconst, genre) values(%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j==0):
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
        if(j==8): # array
            temp2 = ()
            temp2 += (temp,)
            if(cell=="\\N") :
                temp2 += (None,)
                parameters.append(temp2)
            else:
                for element in cell.split(','):
                    temp2 += (element,)
                    parameters.append(temp2)
                    temp2 = (temp,)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()

'''


'''  # Director Table 

the_file = open('title.crew.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000
parameters = []
sql = "insert into Director(tconst, director) values(%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j==0):
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
        if(j==1): # array
            temp2 = ()
            temp2 += (temp,)
            if(cell=="\\N") :
                temp2 += (None,)
                parameters.append(temp2)
            else:
                for element in cell.split(','):
                    temp2 += (element,)
                    parameters.append(temp2)
                    temp2 = (temp,)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()
'''

''' # Writer Table


the_file = open('title.crew.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000
parameters = []
sql = "insert into Writer(tconst, writer) values(%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j==0):
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
        if(j==2): # array
            temp2 = ()
            temp2 += (temp,)
            if(cell=="\\N") :
                temp2 += (None,)
                parameters.append(temp2)
            else:
                for element in cell.split(','):
                    temp2 += (element,)
                    parameters.append(temp2)
                    temp2 = (temp,)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()

'''

'''# Episode Table

the_file = open('title.episode.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 100000000000000000
parameters = []
sql = "insert into Episode(childTconst, parentTconst, seasonNumber, episodeNumber) values(%s,%s,%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(cell=="\\N") :
            temp += (None,)
        else:
            temp += (cell,)
    parameters.append(temp)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()
'''

'''# Title Table

the_file = open('title.akas.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 10000000000000
parameters = []
sql = "insert into Title(tconst, ordering, title, region, language, isOriginalTitle) values(%s,%s,%s,%s,%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j==5 or j==6): continue
        if(j>7): continue
        if(cell=="\\N") :
            temp += (None,)
        else:
            temp += (cell,)
    parameters.append(temp)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
            conn.commit()
            parameters=[]
            print("*******************error at ",i, " / ",row)
            print("Unexpected error:", sys.exc_info()[0])
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()
'''


''' # Type Table

the_file = open('title.akas.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000000
parameters = []
sql = "insert into `Type`(tconst, ordering, `type`) values(%s,%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j==0 or j==1 or j==5):
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
    parameters.append(temp)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
            conn.commit()
            parameters=[]
            print("*******************error at ",i, " / ",row)
            print("Unexpected error:", sys.exc_info()[0])
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()
'''


'''# Attribute Table

the_file = open('title.akas.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000000 
parameters = []
sql = "insert into `Attribute`(tconst, ordering, `attribute`) values(%s,%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j==0 or j==1 or j==6):
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
    parameters.append(temp)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
            conn.commit()
            parameters=[]
            print("*******************error at ",i, " / ",row)
            print("Unexpected error:", sys.exc_info()[0])
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()

'''

'''# Name Table

the_file = open('name.basics.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000000
parameters = []
sql = "insert into `Name`(nconst, primaryName, birthYear, deathYear) values(%s,%s,%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j<4):
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
#    print(temp)
    parameters.append(temp)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
            conn.commit()
            parameters=[]
            print("*******************error at ",i, " / ",row)
            print("Unexpected error:", sys.exc_info()[0])
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()
'''

'''# Profession Table

the_file = open('name.basics.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000000
parameters = []
sql = "insert into Profession(nconst, primaryProfession) values(%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j==0):
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
        if(j==4): # array
            temp2 = ()
            temp2 += (temp,)
            if(cell=="\\N") :
                temp2 += (None,)
                parameters.append(temp2)
            else:
                for element in cell.split(','):
                    temp2 += (element,)
                    parameters.append(temp2)
                    temp2 = (temp,)
#    print(temp)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
            conn.commit()
            parameters=[]
            print("*******************error at ",i, " / ",row)
            print("Unexpected error:", sys.exc_info()[0])
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()
'''

'''# RelatedMovie Table

the_file = open('name.basics.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000
parameters = []
sql = "insert into RelatedMovie(nconst, tconst) values(%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(j==0):
            if(cell=="\\N") :
                temp += (None,)
            else:
                temp += (cell,)
        if(j==5): # array
            temp2 = ()
            temp2 = temp
            if(cell=="\\N") :
                temp2 += (None,)
                parameters.append(temp2)
            else:
                for element in cell.split(','):
                    temp2 += (element,)
                    parameters.append(temp2)
                    temp2 = temp
#    print(temp)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
            conn.commit()
            parameters=[]
            print("*******************error at ",i, " / ",row)
            print("Unexpected error:", sys.exc_info()[0])
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()
'''

'''# Principal Table

the_file = open('title.principals.tsv', 'r', encoding='UTF8')
reader = csv.reader(the_file, delimiter='\t')

stop = 1000000000000000
parameters = []
sql = "insert into Principal(tconst, ordering, nconst, category, job, characters) values(%s,%s,%s,%s,%s,%s);"

for i, row in enumerate(reader):
    if(i==0): continue
    temp=()
    for j, cell in enumerate(row):
        if(cell=="\\N") :
            temp += (None,)
        else:
            temp += (cell,)
    parameters.append(temp)
    if(i%100000==0):
        #print(parameters)
        print("===================================",i,"===================================")
        try:
            curs.executemany(sql, parameters)
            conn.commit()
            parameters=[]
        except:
            pass
            conn.commit()
            parameters=[]
            print("*******************error at ",i, " / ",row)
            print("Unexpected error:", sys.exc_info()[0])
    if(i == stop) : break

curs.executemany(sql, parameters)
conn.commit()

print("end")

curs.close()
conn.close()
'''
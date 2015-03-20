import copy
import Queue
class Course: #Course, store the Course information
	def __init__(self, info):
		week = ["Mon", "Tue", "Wed", "Th", "Fri"]
		self.CourseName = info[0]
		self.time = []
		self.rectime = []
		self.num = 0
		self.skill = []
		self.TAnum = 0;
		self.TAArrange = []
		for i in range(1, len(info), 2):
			WeekNum = week.index(info[i].strip())
			timestr = info[i + 1].strip()
			time = timestr.split(" ")
			timenum = caltime(time)
			self.time.append((WeekNum, timenum))

class TA: #TA, store the TA information
	def __init__(self, info):
		week = ["Mon", "Tue", "Wed", "Th", "Fri"]
		self.Name = info[0]
		self.time = []
		self.skill = []
		self.Course = []
		for i in range(1, len(info), 2):
			WeekNum = week.index(info[i].strip())
			timestr = info[i + 1].strip()
			time = timestr.split(" ")
			timenum = caltime(time)
			self.time.append((WeekNum, timenum))
def caltime(time): #Transmit the time to a integer
	noon = 0
	if(time[1] == "AM"):
		noon = 0
	else:
		noon = 12
	timenumlist = time[0].split(":")
	hour = int(timenumlist[0]) + noon
	minute = int(timenumlist[1])
	timenum = hour * 60 + minute
	return timenum

def addrecitation(info): #Add recitation to the Course time
	global Courseslist
	global Coursesdict
	week = ["Mon", "Tue", "Wed", "Th", "Fri"]
	CourseName = info[0]
	courseindex = Coursesdict.get(CourseName)
	for i in range(1, len(info), 2):
		WeekNum = week.index(info[i].strip())
		timestr = info[i + 1].strip()
		time = timestr.split(" ")
		timenum = caltime(time)
		Courseslist[courseindex].rectime.append((WeekNum, timenum))
def FullProp(index): #constraint propagation
	global ValidTA
	global CourseConflict
	global Domains
	global Courseslist
	myqueue = Queue.Queue()
	for i in range(len(CourseConflict)): #Add all the edge into queue
		if(CourseConflict[i][0] >= index or CourseConflict[i][1] >= index):
			myqueue.put(CourseConflict[i])
	while myqueue.empty() != True:  #loop until the queue is empty
		single = myqueue.get()
		course1 = single[0]
		course2 = single[1]
		if(Courseslist[course1].TAnum >= 2 and Courseslist[course2] >= 2):
			TA1 = []
			TA2 = []
			for i in range(len(ValidTA[course1])):   #Calcultae the Course's valid TA
				newindex = ValidTA[course1][i]
				if(Domains[course1][newindex] >= 2):
					TA1.add(newindex)
			for i in range(len(ValidTA[course2])):
				newindex = ValidTA[course2][i]
				if(Domains[course2][newindex] >= 2):
					TA2.add(newindex)
			if(len(TA1) == 1):
				if TA1[0] in TA2:
					Domains[course2][TA1[0]] = 0     #Delete the conflict TA
					for i in range(len(CourseConflict)):
						if(CourseConflict[i][0] == course2 or CourseConflict[i][1] == course2):
							if CourseConflict[i] not in myqueue:
								myqueue.put(CourseConflict[i])   #Add the relevant edge into queue
			if(len(TA2) == 1):
				if TA2[0] in TA1:
					Domains[course1][TA2[0]] = 0     #Delete the conflict TA
					for i in range(len(CourseConflict)):
						if(CourseConflict[i][0] == course1 or CourseConflict[i][1] == course1):
							if CourseConflict[i] not in myqueue:
								myqueue.put(CourseConflict[i]) #Add the relevant edge into queue

def ForwardCheck(index): #ForwardCheck
	global Courseslist
	global Coursesdict
	global TAdict
	global TAlist
	global NoAnswerflag
	global ValidTA
	global CourseConflict
	global Domains
	totalTA = 0
	totalneedTA = 0
	FullProp(index)   #constraint propagation
	# print "ForwardCheck"
	# print index
	for i in range(len(Domains[index])):  #Check whether the total TAnum is bigger than the courses need
		totalTA = totalTA + Domains[index][i]
	for i in range(index, len(Courseslist)):
		totalneedTA = totalneedTA + Courseslist[i].TAnum
	if(totalTA < totalneedTA): 
		# print "not enough"
		NoAnswerflag = 1
		return
	for i in range(index, len(Courseslist)):
		LeftTA = Courseslist[index].TAnum
		TAsum = 0
		enough = 0
		for j in range(len(TAlist)):
			timeflag = 0
			skillflag = 0
			for k in range(len(Courseslist[i].time)): #Check whether the TA's time is valid
				if((TAlist[j].time[0][0] == Courseslist[i].time[k][0]) and ((TAlist[j].time[0][1] >= (Courseslist[i].time[k][1] - 90)) and (TAlist[j].time[0][1] <= (Courseslist[i].time[k][1] + 90)))):
					# print "lxc"
					timeflag = 1
				if(timeflag == 1):
					break
			if(timeflag == 0):  #Check whether the TA's skills are match
				# print "right time"
				for m in range(len(Courseslist[i].skill)):
					for n in range(len(TAlist[j].skill)):
						if(Courseslist[i].skill[m] == TAlist[j].skill[n]):
							skillflag = 1
							break
					if(skillflag == 1):
						break
			if(skillflag == 1): #check this course has enough TA to choose
				# print "right skill"
				TAsum = TAsum + Domains[index][j]
			if(TAsum >= LeftTA):
				enough = 1
				break
		if(enough == 1):
			continue
		else:
			NoAnswerflag = 1
			return

def BackTrack(index):
	global Courseslist
	global Coursesdict
	global TAdict
	global TAlist
	global Answerflag
	global NoAnswerflag
	global totalnode
	global Domains
	totalnode = totalnode + 1
	print totalnode
	if(index == len(Courseslist)): #Finish search return result
		Answerflag = 1
		return
	# print Courseslist[index].CourseName
	# print TAflag
	for i in range(len(TAlist)):
		# print TAlist[i].Name, 
		# print Courseslist[index].CourseName
		# newTAflag = copy.deepcopy(TAflag)
		NoAnswerflag = 0
		timeflag = 0
		skillflag = 0
		LeftTA = Courseslist[index].TAnum
		if(LeftTA < 2): #Choose the Half TA
			# print "0.5"
			if(Domains[index][i] >= 1):  
				for j in range(len(Courseslist[index].time)): #Check whether the TA's time is valid
					if((TAlist[i].time[0][0] == Courseslist[index].time[j][0]) and ((TAlist[i].time[0][1] >= (Courseslist[index].time[j][1] - 80)) and (TAlist[i].time[0][1] <= (Courseslist[index].time[j][1] + 90)))):
						# print "lxc"
						timeflag = 1
					if(timeflag == 1):
						break
				if(timeflag == 0): #Check whether the TA's time is valid
					for j in range(len(Courseslist[index].skill)):
						for k in range(len(TAlist[i].skill)):
							if(Courseslist[index].skill[j] == TAlist[i].skill[k]):
								skillflag = 1
								break
						if(skillflag == 1):
							break
				if(skillflag == 1):  
					temp = copy.deepcopy(Domains)  #change the relevant domain
					for x in range(index, len(Courseslist)):
						Domains[x][i] = Domains[x][i] - 1
					Courseslist[index].TAnum = Courseslist[index].TAnum - 1
					Courseslist[index].TAArrange.append((TAlist[i].Name, 0.5))
					TAlist[i].Course.append((Courseslist[index].CourseName, 0.5))
					nextindex = index
					if(Courseslist[index].TAnum == 0):
						nextindex = index + 1
					if(nextindex != len(Courseslist)):
						ForwardCheck(nextindex)
					if(NoAnswerflag == 1):
						del Courseslist[index].TAArrange[-1]
						del TAlist[i].Course[-1]
						Courseslist[index].TAnum = Courseslist[index].TAnum + 1
						Domains = copy.deepcopy(temp)
						continue
					BackTrack(nextindex)
					if(Answerflag == 1):
						return
					del Courseslist[index].TAArrange[-1]  #After BackTrack restore the domain
					del TAlist[i].Course[-1]
					Courseslist[index].TAnum = Courseslist[index].TAnum + 1
					Domains = copy.deepcopy(temp)
		else:
			# print "1"
			if(Domains[index][i] >= 2): #Choose the full TA
				for j in range(len(Courseslist[index].time)): #Check whether the TA's time is valid
					if((TAlist[i].time[0][0] == Courseslist[index].time[j][0]) and ((TAlist[i].time[0][1] >= (Courseslist[index].time[j][1] - 80)) and (TAlist[i].time[0][1] <= (Courseslist[index].time[j][1] + 90)))):
						timeflag = 1
					if(timeflag == 1):
						break
				if(timeflag == 0): #Check whether the TA's time is valid
					for j in range(len(Courseslist[index].skill)):
						for k in range(len(TAlist[i].skill)):
							if(Courseslist[index].skill[j] == TAlist[i].skill[k]):
								skillflag = 1
								break
						if(skillflag == 1):
							break
				if(skillflag == 1): #change the relevant domain
					temp = copy.deepcopy(Domains)
					for x in range(index, len(Courseslist)):
						Domains[x][i] = Domains[x][i] - 2
					Courseslist[index].TAnum = Courseslist[index].TAnum - 2
					Courseslist[index].TAArrange.append((TAlist[i].Name, 1))
					TAlist[i].Course.append((Courseslist[index].CourseName, 1))
					nextindex = index
					if(Courseslist[index].TAnum == 0):
						nextindex = index + 1
					if(nextindex != len(Courseslist)):
						ForwardCheck(nextindex)
					if(NoAnswerflag == 1):
						del Courseslist[index].TAArrange[-1]
						del TAlist[i].Course[-1]
						Courseslist[index].TAnum = Courseslist[index].TAnum + 2
						Domains = copy.deepcopy(temp)
						continue
					BackTrack(nextindex)
					if(Answerflag == 1):
						return
					del Courseslist[index].TAArrange[-1] #After BackTrack restore the domain
					del TAlist[i].Course[-1]
					Courseslist[index].TAnum = Courseslist[index].TAnum + 2
					Domains = copy.deepcopy(temp)


Coursesdict = {}
Courseslist = []
CourseConflict = []
ValidTA = []
TAdict = {}
TAlist = []
Result = []
Domains = []
Answerflag = 0
NoAnswerflag = 0
totalnode = 0
if __name__ == '__main__':
	global Courseslist
	global Coursesdict
	global TAdict
	global TAlist
	global Answerflag
	global ValidTA
	global CourseConflict
	global Domains
	# datafile = open("dataset_AI_CSP_correct", "r")
	datafile = open("dataset_AI_CSP", "r")
	for line in datafile: #Block 1
		if(line == "\n"):
			break;
		info = line.split(",")
		newcourse = Course(info)
		Courseslist.append(newcourse)
	for i in range(len(Courseslist)):
		Coursesdict[Courseslist[i].CourseName] = i
	for line in datafile: #Block 2
		if(line == "\n"):
			break;
		info = line.split(",")
		addrecitation(info)

	for line in datafile: #Block 3
		if(line == "\n"):
			break;
		info = line.split(",")
		CourseName = info[0]
		courseindex = Coursesdict.get(CourseName)
		student = int(info[1].strip())
		Courseslist[courseindex].num = student
		if(student < 40):
			Courseslist[courseindex].TAnum = 1
		if(student < 60 and student >= 40):
			Courseslist[courseindex].TAnum = 3
		if(student >= 60):
			Courseslist[courseindex].TAnum = 4

		if(info[2].strip() == "yes"):
			# print Courseslist[courseindex].time
			if(len(Courseslist[courseindex].rectime) != 0):
				Courseslist[courseindex].time.append(Courseslist[courseindex].rectime[0])
		else:
			Courseslist[courseindex].time = []
			if(len(Courseslist[courseindex].rectime) != 0):
				Courseslist[courseindex].time.append(Courseslist[courseindex].rectime[0])
	sum = 0
	for i in range(len(Courseslist)):
		# Coursesdict[Courseslist[i].CourseName] = i
		sum = sum + Courseslist[i].TAnum
		# print Courseslist[i].TAnum
	# print sum
	for line in datafile: #Block 4
		if(line == "\n"):
			break;
		info = line.split(",")
		CourseName = info[0]
		courseindex = Coursesdict.get(CourseName)
		for i in range(1, len(info)):
			Courseslist[courseindex].skill.append(info[i].strip())

	for line in datafile: #Block 5
		if(line == "\n"):
			break;
		info = line.split(",")
		newTA = TA(info)
		TAlist.append(newTA)
	for i in range(len(TAlist)):
		TAdict[TAlist[i].Name] = i

	for line in datafile: #Block 6
		if(line == "\n"):
			break;
		info = line.split(",")
		TAName = info[0]
		TAindex = TAdict.get(TAName)
		# print TAName
		for i in range(1, len(info)):
			TAlist[TAindex].skill.append(info[i].strip())
	datafile.close()
	Domains = [[2 for i in range(len(TAlist))] for j in range(len(Courseslist))]
	ValidTA = [[] for i in range(len(Courseslist))]
	for i in range(len(Courseslist)):  #get the course pair which share the same TA
		for j in range(len(TAlist)):
			timeflag = 0
			skillflag = 0
			for k in range(len(Courseslist[i].time)):
				if((TAlist[j].time[0][0] == Courseslist[i].time[k][0]) and ((TAlist[j].time[0][1] >= (Courseslist[i].time[k][1] - 90)) and (TAlist[j].time[0][1] <= (Courseslist[i].time[k][1] + 90)))):
					# print "lxc"
					timeflag = 1
				if(timeflag == 1):
					break
			if(timeflag == 0):
				# print "right time"
				for m in range(len(Courseslist[i].skill)):
					for n in range(len(TAlist[j].skill)):
						if(Courseslist[i].skill[m] == TAlist[j].skill[n]):
							skillflag = 1
							break
					if(skillflag == 1):
						break
			if(skillflag == 1):
				ValidTA[i].append(j)
	for i in range(len(Courseslist)):   #get the TA which is valid for the course
		for j in range(i + 1, len(Courseslist)):
			conflictflag = 0
			for k in range(len(ValidTA[i])):
				for l in range(len(ValidTA[j])):
					if(ValidTA[i][k] == ValidTA[j][l]):
						CourseConflict.append((i, j))
						conflictflag = 1
					if(conflictflag == 1):
						break
				if(conflictflag == 1):
					break
	# print CourseConflict

	TAflag = [2 for i in range(len(TAlist))]
	Courseindex = 0
	BackTrack(Courseindex)   #Backtrack
	result = open("BackTrack+ForwardCheck+CP", "w")
	if(Answerflag == 1):     #Store the result
		for i in range(len(Courseslist)):
			result.write(Courseslist[i].CourseName)
			for j in range(len(Courseslist[i].TAArrange)):
				result.write(" ")
				result.write(Courseslist[i].TAArrange[j][0])
				result.write(" ")
				result.write(str(Courseslist[i].TAArrange[j][1]))
			result.write("\n")
		result.write("\n")
		for i in range(len(TAlist)):
			result.write(TAlist[i].Name)
			for j in range(len(TAlist[i].Course)):
				result.write(" ")
				result.write(TAlist[i].Course[j][0])
				result.write(" ")
				result.write(str(TAlist[i].Course[j][1]))
			result.write("\n")
	else:
		result.write("No Answer!\n")
	result.close()
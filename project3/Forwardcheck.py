import copy
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

class TA:  #TA, store the TA information
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
def caltime(time):  #Transmit the time to a integer
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

def addrecitation(info):  #Add recitation to the Course time
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
def ForwardCheck(TAflag, index): #ForwardCheck
	global Courseslist
	global Coursesdict
	global TAdict
	global TAlist
	global NoAnswerflag
	totalTA = 0
	totalneedTA = 0
	# print "ForwardCheck"
	# print index
	for i in range(len(TAflag)):
		totalTA = totalTA + TAflag[i]
	for i in range(index, len(Courseslist)):
		totalneedTA = totalneedTA + Courseslist[i].TAnum
	if(totalTA < totalneedTA):   #Check whether the total TAnum is bigger than the courses need
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
			for k in range(len(Courseslist[i].time)):   #Check whether the TA's time is valid
				if((TAlist[j].time[0][0] == Courseslist[i].time[k][0]) and ((TAlist[j].time[0][1] >= (Courseslist[i].time[k][1] - 90)) and (TAlist[j].time[0][1] <= (Courseslist[i].time[k][1] + 90)))):
					# print "lxc"
					timeflag = 1
				if(timeflag == 1):
					break
			if(timeflag == 0):   #Check whether the TA's skills are match
				# print "right time"
				for m in range(len(Courseslist[i].skill)):
					for n in range(len(TAlist[j].skill)):
						if(Courseslist[i].skill[m] == TAlist[j].skill[n]):
							skillflag = 1
							break
					if(skillflag == 1):
						break
			if(skillflag == 1):  #check this course has enough TA to choose
				# print "right skill"
				TAsum = TAsum + TAflag[j]
			if(TAsum >= LeftTA):
				enough = 1
				break
		if(enough == 1):
			continue
		else:
			NoAnswerflag = 1
			return

def BackTrack(TAflag, index):
	global Courseslist
	global Coursesdict
	global TAdict
	global TAlist
	global Answerflag
	global NoAnswerflag
	global totalnode
	totalnode = totalnode + 1
	print totalnode
	if(index == len(Courseslist)): #Finish search return result
		Answerflag = 1
		return
	for i in range(len(TAlist)):
		NoAnswerflag = 0
		timeflag = 0
		skillflag = 0
		LeftTA = Courseslist[index].TAnum
		if(LeftTA < 2):      #Choose the Half TA
			# print "0.5"
			if(TAflag[i] >= 1):
				for j in range(len(Courseslist[index].time)): #Check whether the TA's time is valid
					if((TAlist[i].time[0][0] == Courseslist[index].time[j][0]) and ((TAlist[i].time[0][1] >= (Courseslist[index].time[j][1] - 80)) and (TAlist[i].time[0][1] <= (Courseslist[index].time[j][1] + 90)))):
						# print "lxc"
						timeflag = 1
					if(timeflag == 1):
						break
				if(timeflag == 0):    #Check whether the TA's time is valid
					for j in range(len(Courseslist[index].skill)):
						for k in range(len(TAlist[i].skill)):
							if(Courseslist[index].skill[j] == TAlist[i].skill[k]):
								skillflag = 1
								break
						if(skillflag == 1):
							break
				if(skillflag == 1):    #change the relevant domain
					TAflag[i] = TAflag[i] - 1
					Courseslist[index].TAnum = Courseslist[index].TAnum - 1
					Courseslist[index].TAArrange.append((TAlist[i].Name, 0.5))
					TAlist[i].Course.append((Courseslist[index].CourseName, 0.5))
					nextindex = index
					if(Courseslist[index].TAnum == 0):
						nextindex = index + 1
					ForwardCheck(copy.deepcopy(TAflag), nextindex)
					if(NoAnswerflag == 1):
						del Courseslist[index].TAArrange[-1]
						del TAlist[i].Course[-1]
						Courseslist[index].TAnum = Courseslist[index].TAnum + 1
						TAflag[i] = TAflag[i] + 1
						continue
					BackTrack(copy.deepcopy(TAflag), nextindex)
					if(Answerflag == 1):
						return
					del Courseslist[index].TAArrange[-1]   #After BackTrack restore the domain
					del TAlist[i].Course[-1]
					Courseslist[index].TAnum = Courseslist[index].TAnum + 1
					TAflag[i] = TAflag[i] + 1
		else:
			# print "1"
			if(TAflag[i] >= 2):  #Choose the full TA
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
				if(skillflag == 1):  #change the relevant domain
					TAflag[i] = TAflag[i] - 2
					Courseslist[index].TAnum = Courseslist[index].TAnum - 2
					Courseslist[index].TAArrange.append((TAlist[i].Name, 1))
					TAlist[i].Course.append((Courseslist[index].CourseName, 1))
					nextindex = index
					if(Courseslist[index].TAnum == 0):
						nextindex = index + 1
					ForwardCheck(copy.deepcopy(TAflag), nextindex)
					if(NoAnswerflag == 1):
						del Courseslist[index].TAArrange[-1]
						del TAlist[i].Course[-1]
						Courseslist[index].TAnum = Courseslist[index].TAnum + 2
						TAflag[i] = TAflag[i] + 2
						continue
					BackTrack(copy.deepcopy(TAflag), nextindex)
					if(Answerflag == 1):    #After BackTrack restore the domain
						return
					del Courseslist[index].TAArrange[-1]
					del TAlist[i].Course[-1]
					Courseslist[index].TAnum = Courseslist[index].TAnum + 2
					TAflag[i] = TAflag[i] + 2


Coursesdict = {}
Courseslist = []
TAdict = {}
TAlist = []
Result = []
Answerflag = 0
NoAnswerflag = 0
totalnode = 0
if __name__ == '__main__':
	global Courseslist
	global Coursesdict
	global TAdict
	global TAlist
	global Answerflag
	datafile = open("dataset_AI_CSP_correct", "r")
	datafile = open("dataset_AI_CSP", "r")
	for line in datafile:    #Block 1
		if(line == "\n"):
			break;
		info = line.split(",")
		newcourse = Course(info)
		Courseslist.append(newcourse)
	for i in range(len(Courseslist)):
		Coursesdict[Courseslist[i].CourseName] = i
	for line in datafile:   #Block2
		if(line == "\n"):
			break;
		info = line.split(",")
		addrecitation(info)

	for line in datafile:   #Block3
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
	for line in datafile:   #Block 4
		if(line == "\n"):
			break;
		info = line.split(",")
		CourseName = info[0]
		courseindex = Coursesdict.get(CourseName)
		for i in range(1, len(info)):
			Courseslist[courseindex].skill.append(info[i].strip())

	for line in datafile: #Block5
		if(line == "\n"):
			break;
		info = line.split(",")
		newTA = TA(info)
		TAlist.append(newTA)
	for i in range(len(TAlist)):
		TAdict[TAlist[i].Name] = i

	for line in datafile: #Block6
		if(line == "\n"):
			break;
		info = line.split(",")
		TAName = info[0]
		TAindex = TAdict.get(TAName)
		# print TAName
		for i in range(1, len(info)):
			TAlist[TAindex].skill.append(info[i].strip())
	datafile.close()

	TAflag = [2 for i in range(len(TAlist))]
	Courseindex = 0
	BackTrack(copy.deepcopy(TAflag), Courseindex)  #Backtrack
	result = open("BackTrack+ForwardCheck", "w")
	if(Answerflag == 1):    #Store the result
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
	# for i in range(len(Courseslist)):
	# 	print Courseslist[i].CourseName
	# 	print Courseslist[i].time
	# 	print Courseslist[i].skill
	# 	print Courseslist[i].TAnum
	# for i in range(len(TAlist)):
	# 	print TAlist[i].Name
	# 	print TAlist[i].time
	# 	print TAlist[i].skill
	# for k, v in Coursesdict.items():
	# 	print k,v
	# for k, v in TAdict.items():
	# 	print k,v
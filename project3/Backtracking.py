#Process the data
class Course:  #Course Information
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

class TA:    #TA Infromation
	def __init__(self, info):
		week = ["Mon", "Tue", "Wed", "Th", "Fri"]
		self.Name = info[0]
		self.time = []
		self.skill = []
		for i in range(1, len(info), 2):
			WeekNum = week.index(info[i].strip())
			timestr = info[i + 1].strip()
			time = timestr.split(" ")
			timenum = caltime(time)
			self.time.append((WeekNum, timenum))
def caltime(time):
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

def addrecitation(info):
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

def BackTrack(TAflag, index):
	global Courseslist
	global Coursesdict
	global TAdict
	global TAlist
	global Answerflag
	if(index == len(Courseslist)):
		Answerflag = 1
		return
	for i in range(len(TAlist)):
		timeflag = 0
		skillflag = 0
		LeftTA = Courseslist[index].TAnum
		if(LeftTA < 1):
			if(TAflag[i] >= 0.5):
				for j in range(len(Courseslist[index].time)):
					if((TAlist[i].time[0][0] == Courseslist[index].time[j][0]) and ((TAlist[i].time[0][1] >= (Courseslist[index].time[j][1] - 90)) and (TAlist[i].time[0][1] <= (Courseslist[index].time[j][1] + 90)))):
						# print "lxc"
						timeflag = 1
					if(timeflag == 1):
						break
				if(timeflag == 0):
					for j in range(len(Courseslist[index].skill)):
						for k in range(len(TAlist[i].skill)):
							if(Courseslist[index].skill[j] == TAlist[i].skill[k]):
								skillflag = 1
								break
						if(skillflag == 1):
							break
				if(skillflag == 1):
					TAflag[i] = TAflag[i] - 0.5
					LeftTA = LeftTA - 0.5
					Courseslist[index].TAArrange.append((TAlist[i].Name, 0.5))
					nextindex = index
					if(LeftTA == 0):
						nextindex = index + 1
					BackTrack(TAflag, nextindex)
					if(Answerflag == 1):
						return
					del Courseslist[index].TAArrange[-1]
					LeftTA = LeftTA + 0.5
					TAflag[i] = TAflag[i] + 0.5
		else:
			if(TAflag[i] >= 1):
				for j in range(len(Courseslist[index].time)):
					if((TAlist[i].time[0][0] == Courseslist[index].time[j][0]) and ((TAlist[i].time[0][1] >= (Courseslist[index].time[j][1] - 90)) and (TAlist[i].time[0][1] <= (Courseslist[index].time[j][1] + 90)))):
						timeflag = 1
					if(timeflag == 1):
						break
				if(timeflag == 0):
					for j in range(len(Courseslist[index].skill)):
						for k in range(len(TAlist[i].skill)):
							if(Courseslist[index].skill[j] == TAlist[i].skill[k]):
								skillflag = 1
								break
						if(skillflag == 1):
							break
				if(skillflag == 1):
					TAflag[i] = TAflag[i] - 1
					LeftTA = LeftTA - 1
					Courseslist[index].TAArrange.append((TAlist[i].Name, 1))
					nextindex = index
					if(LeftTA == 0):
						nextindex = index + 1
					BackTrack(TAflag, nextindex)
					if(Answerflag == 1):
						return
					del Courseslist[index].TAArrange[-1]
					LeftTA = LeftTA + 1
					TAflag[i] = TAflag[i] + 1


Coursesdict = {}
Courseslist = []
TAdict = {}
TAlist = []
Result = []
Answerflag = 0
if __name__ == '__main__':
	global Courseslist
	global Coursesdict
	global TAdict
	global TAlist
	global Answerflag
	datafile = open("dataset_AI_CSP", "r")
	for line in datafile:
		if(line == "\n"):
			break;
		info = line.split(",")
		newcourse = Course(info)
		Courseslist.append(newcourse)

	for i in range(len(Courseslist)):
		Coursesdict[Courseslist[i].CourseName] = i

	for line in datafile:
		if(line == "\n"):
			break;
		info = line.split(",")
		addrecitation(info)

	for line in datafile:
		if(line == "\n"):
			break;
		info = line.split(",")
		CourseName = info[0]
		courseindex = Coursesdict.get(CourseName)
		student = int(info[1].strip())
		Courseslist[courseindex].num = student
		if(student <= 40):
			Courseslist[courseindex].TAnum = 0.5
		elif(student < 60):
			Courseslist[courseindex].TAnum = 1.5
		else:
			Courseslist[courseindex].TAnum = 2

		if(info[2].strip() == "yes"):
			# print Courseslist[courseindex].time
			if(len(Courseslist[courseindex].rectime) != 0):
				Courseslist[courseindex].time.append(Courseslist[courseindex].rectime[0])
		else:
			Courseslist[courseindex].time = []
			if(len(Courseslist[courseindex].rectime) != 0):
				Courseslist[courseindex].time.append(Courseslist[courseindex].rectime[0])

	for line in datafile:
		if(line == "\n"):
			break;
		info = line.split(",")
		CourseName = info[0]
		courseindex = Coursesdict.get(CourseName)
		for i in range(1, len(info)):
			Courseslist[courseindex].skill.append(info[i].strip())

	for line in datafile:
		if(line == "\n"):
			break;
		info = line.split(",")
		newTA = TA(info)
		TAlist.append(newTA)

	for i in range(len(Courseslist)):
		TAdict[TAlist[i].Name] = i

	for line in datafile:
		if(line == "\n"):
			break;
		info = line.split(",")
		TAName = info[0]
		TAindex = TAdict.get(TAName)
		for i in range(1, len(info)):
			TAlist[TAindex].skill.append(info[i].strip())
	datafile.close()
	TAflag = [1 for i in range(len(TAlist))]
	Courseindex = 0
	BackTrack(TAflag, Courseindex)
	# if(Answerflag == 1):
	for i in range(len(Courseslist)):
		print Courseslist[i].CourseName,
		for j in range(len(Courseslist[i].TAArrange)):
			print Courseslist[i].TAArrange[j],
		print ""
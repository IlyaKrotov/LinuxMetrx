#########################################################
# Collecting information (a lot of information) about   #
# usage of disk, memory, vm and about load average      #
# and cpu                                               #
#########################################################

def readStatsTo(resFile):

	devices, buff, stats, d_stats = [], [], {}, {}
	cnt = 0

	#reading from proc/diskstats
	DISKSTATSFile = open("/proc/diskstats", "r")

	for line in DISKSTATSFile:

		buff = line.split(" ")
		d_stats["numberOfDevice"] = float(cnt)
		d_stats["diskReadsCompleted"] = float(buff[12])
		d_stats["diskReadsMerged"] = float(buff[13])
		d_stats["diskSectorsRead"] = float(buff[14])
		d_stats["diskMsReading"] = float(buff[15])
		d_stats["diskWritesCompleted"] = float(buff[16])
		d_stats["dislWritesMerged"] = float(buff[17])
		d_stats["diskSectorsWritten"] = float(buff[18])
		d_stats["diskMsWriting"] = float(buff[19])
		d_stats["diskIOinProccess"] = float(buff[20])
		d_stats["diskMsDoingIO"] = float(buff[21])
		d_stats["diskWeightedMsDoingIO"] = float(buff[22])
		devices.append(d_stats)
		cnt += 1

	#TODO:
	#reading from proc/interupts

	#reading from proc/loadavg
	LAFile = open("/proc/loadavg", "r")

	for line in LAFile:
		buff = line.split()
		stats["loadAverageDuring1m"] = float(buff[0])
		stats["loadAverageDuring5m"] = float(buff[1])
		stats["loadAverageDuring15m"] = float(buff[2])
		stats["loadAverageCurrRunEntities"], stats["loadAverageCurrExistEntities"] = (float(num) for num in buff[3].split("/"))

	#reading from proc/memstat
	MEMINFOFile = open("/proc/meminfo", "r")

	for line in MEMINFOFile:
		buff = line.split()
		currName = buff[0][0:len(buff[0])-1]
		stats["meminfo_" + currName] = float(buff[1])

	#reading from proc/vmstat
	VMSTATFile = open("/proc/vmstat", "r")

	for line in VMSTATFile:
		buff = line.split()
		currName = buff[0]
		stats["vmstat_" + currName] = float(buff[1])

	#reading from proc/stat
	PROCSTATFile = open("/proc/stat", "r")

	for line in PROCSTATFile:
		splitedLine = line.split()
		#information about CPU
		if(splitedLine[0] == "cpu"):
			#because we need cpu stats in general
			stats["cpu_user"] = float(splitedLine[1])
			stats["cpu_nice"] = float(splitedLine[2])
			stats["cpu_system"] = float(splitedLine[3])
			stats["cpu_idle"] = float(splitedLine[4])
			stats["cpu_iowait"] = float(splitedLine[5])
			stats["cpu_irq"] = float(splitedLine[6])
			stats["cpu_softirq"] = float(splitedLine[7])
			#only since Linux 2.6.11
			stats["cpu_steal"] = float(splitedLine[8])
			#only since Linux 2.6.24
			stats["cpu_guest"] = float(splitedLine[9])
		
		#information about counts of interrupts serviced since boot time
		if(splitedLine[0] == "intr"):
			stats["stat_totalNumberOfInterupts"] = float(splitedLine[1])
		
		#information about the total number of context switches 
		#across all CPUs
		if(splitedLine[0] == "ctxt"):
			stats["stat_totalNumberOfContextSwithes"] = float(splitedLine[1])
		
		#information the time at which the system booted, in seconds 
		#since the Unix epoch (January 1, 1970).
		if(splitedLine[0] == "btime"):
			stats["stat_bootTime"] = float(splitedLine[1])
		
		#number of processes and threads created, which includes 
		#(but is not limited to) those created by calls to the fork() 
		#and clone() system calls.
		if(splitedLine[0] == "processes"):
			stats["stattotalNumberOfProcesses"] = float(splitedLine[1])
		
		#the number of processes currently running on CPUs 
		#(Linux 2.5.45 onwards)
		if(splitedLine[0] == "procs_running"):
			stats["statnumberOfRunningProcesses"] = float(splitedLine[1])
		
		#the number of processes currently blocked, waiting for I/O to complete 
		#(Linux 2.5.45 onwards)
		if(splitedLine[0] == "procs_blocked"):
			stats["statnumberOfBlockedProcces"] = float(splitedLine[1])

  DISKSTATSFile.close()
  MEMINFOFile.close()
  VMSTATFile.close()
  PROCSTATFile.close()
  
  #writing information to file
	try:
		rfile = open(str(resFile), "a")
		strForWrite = ""
		for i in xrange(len(d_stats.values())):
			strForWrite = strForWrite + str(float(d_stats.values()[i])) + " "
		for j in xrange(len(stats.values())):
			strForWrite = strForWrite + str(float(stats.values()[j])) + " "
		strForWrite += "\n"
		rfile.write(strForWrite)
		rfile.close()
	except Exception as e:
		print(e)

  return d_stats, stats
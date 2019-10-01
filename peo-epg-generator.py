#created by b w k c bandara
#organization : Dharmavahini Foundation
#first release 2019-09-19
#updated 

#!/bin/python
import datetime
import sys
import csv
import os

class DialogEpg:
	def __init__(self):
		#describing fillers with -11- string ex:promo_maths-11-512k.mp4
		self.grade=input("Enter Grade (10-11) :")
		self.year=input("Enter Year (2019) : ")
		self.month=input("Enter Month (09) : ")
		self.start_time=input("Enter Start Time (6:00:00) : ")
		self.end_time=self.start_time
		self.static_filler_time='00:00:00'
		self.filler_time=self.static_filler_time
		self.static_start_time=self.start_time
		self.static_end_time=self.end_time
		self.exlude_list=['promo_']
		self.include_list=['-'+self.grade+'-','-life-skill-']
		self.english_subject=["english","masterspeller"]
		self.channel_name="Videsa "+self.grade

		self.day_tag="#day"
		self.airing_date=""
#		self.start_time = datetime.timedelta(hours=6,minutes=0,seconds=0)
#		self.end_time= datetime.timedelta(hours=6,minutes=0,seconds=0) #datetime.timedelta()
		self.program_duration=""
		self.genre=""
		self.sub_genre=""
		self.program_name=""
		self.original_repeat=""
		self.live_recorded="recorded"
		self.language=""
		self.dubbed_lan=""
		self.episode_number=""
		self.episode_title=""
		self.season_num=""
		self.season_name=""
		self.star_cast=""
		self.director=""
		self.producer="Dharmavahini Foundation"
		self.year_of_release=""
		self.rating=""
		self.episode_title=""
		self.generic_synopsis=""
		self.episode_synopsis=""
		self.image_file=""
		self.prog_duration=""
		self.csv_file="peo-videsa-"+self.grade+"-"+self.year+"-"+self.month+"-epg.csv"
		try:
			#get file name
			m3u_file=str(sys.argv[1])
			print (m3u_file)
		except:
			print("Please set input file name")
		self.readFile(m3u_file)

	def readFile(self,m3u_file):
	#find file and delete
		if os.path.exists(self.csv_file):
			os.remove(self.csv_file)
		else:
			headers=["Channel Name","Schedule Airing Date","Airing Start Time","End Time","Program Duration","Genre","Sub Genre","Program Name","Original/Repeat","Live/Recorded","Broadcast Language","Dubbed Language","Episode Number","Episode Title","Season Number","Season Name","Star Cast","Director","Producer","Year of Release","Censor/Broadcast Rating","Episode Short Title","Generic Synopsis","Episodic Synopsis","Image_File"]

			with open(self.csv_file,'w',newline='') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(headers)
#				writer.writeheader()
			csvFile.close()

		file_struct=open(m3u_file,"r")

		for line in file_struct:

			#get third column
			file_name=line.split(",")[2]

			#print (file_name)
			short_name='-'.join(file_name.split("-")[:-1])
#			for eng_element in self.english_subject:
			if file_name.startswith("english") or file_name.startswith("masterspeller"):
				self.language="English"
			else:
				self.language="Sinhala"





			if file_name.startswith("#day"):
				day_num=line.split(",")[0]
				print("creating {}-{}-{} data...".format(self.year,self.month,day_num))
				self.airing_date=day_num
				self.start_time=self.static_start_time
				self.end_time=self.static_end_time
				self.filler_time=self.static_filler_time
			else:
				#print("start:{} duration:{} {}".format(self.start_time,self.prog_duration,short_name))
				self.prog_duration=line.split(",")[1]
				#time addition
				self.start_time=self.end_time
				time_list=[self.start_time,self.prog_duration]
				#print (prog_duration)
				time_sum=datetime.timedelta()
#				self.end_time=datetime.timedelta()
#				self.start_time=datetime.timedelta()	
				for ti in time_list:
					#try:
					(h,m,s)=ti.split(':')
					#except:
				#	print("time error : {}".format(file_name))
					#try:
					temp=datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s))
					time_sum += temp
					#convert total seconds "1 day, 00:12:b02"
					tot_seconds=time_sum.seconds
					#convert 722 seconds to time format, time sum will be equal to 00:12:02
					time_sum=datetime.timedelta(seconds=tot_seconds)
				#print("time_sum : {}".format(time_sum))
				self.end_time=str(time_sum)

				if file_name.startswith('national'):
					self.program_name=short_name.capitalize()+" Anthem"
					self.genre="3.1.2"
					self.setNationalPirith(short_name,line)
				elif file_name.startswith('pirith-out'):
					self.program_name=short_name.split("-")[0].capitalize()
					self.genre="3.1"
					self.setNationalPirith(short_name,line)
				else:
					self.genre="3.1.3.6"
					self.sub_genre="3.1.3.6.3"
					#activate importent programes
					for inc in self.include_list:
						if short_name.find(inc) >= 0:
							#deactivate program
							for item in self.exlude_list: #iterate fillers
								if short_name.find(item) == -1: #get without exclude fillers
									#self.program_name=short_name.capitalize()
									#execute row data update
									self.program_name=self.getGenericName(short_name)
									self.episode_number=self.program_name.split("-")[1]
									self.setNewRow(short_name,line)
						else:
							filler_time=line.split(",")[1]
							(ha,ma,sa)=filler_time.split(':')
							#except:
						#	print("time error : {}".format(file_name))
							#try:
							temp_filler=datetime.timedelta(hours=int(ha),minutes=int(ma),seconds=int(sa))
							time_sum += temp_filler
							#convert total seconds "1 day, 00:12:b02"
							#tot_seconds_filler=time_sum.seconds
							#convert 722 seconds to time format, time sum will be equal to 00:12:02
							time_sum=datetime.timedelta(seconds=time_sum.seconds)
							#print("time_sum : {}".format(time_sum))
							self.end_time = str(time_sum)

	def setNationalPirith(self,short_name,line):
		self.sub_genre=self.genre
		self.episode_number=""
		#creating raw
		self.setNewRow(short_name,line)	

	def setNewRow(self,short_name,line):
		self.image_file=short_name+".jpg"
		self.generic_synopsis=self.program_name
		try:
			self.original_repeat=self.getOriginalRepeat(line.split(",")[3])
		except:
			print("Original Repeat Field is missing")
		self.createRaw()

	def createRaw(self):
		start_time=":".join(self.start_time.split(":")[:-1])
		end_time=":".join(self.end_time.split(":")[:-1])
		prog_duration=":".join(self.prog_duration.split(":")[:-1])
		#print("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format(self.channel_name,self.year+"."+self.month+"."+self.airing_date,start_time,end_time,prog_duration,self.genre,self.sub_genre,self.program_name,self.original_repeat,self.live_recorded,self.language,self.dubbed_lan, self.episode_number, self.episode_title, self.season_num, self.star_cast, self.director, self.producer, self.year_of_release, self.rating, self.episode_title, self.generic_synopsis, self.episode_synopsis, self.image_file))

		record=[self.channel_name,self.year+"."+self.month+"."+self.airing_date,start_time,end_time,prog_duration,self.genre,self.sub_genre,self.program_name,self.original_repeat,self.live_recorded,self.language,self.dubbed_lan, self.episode_number, self.episode_title, self.season_num, self.season_name, self.star_cast, self.director, self.producer, self.year_of_release, self.rating, self.episode_title, self.generic_synopsis, self.episode_synopsis, self.image_file]


#		record=[self.channel_name,self.year+"."+self.month+"."+self.airing_date,start_time,end_time,prog_duration,self.genre,self.sub_genre,self.program_name]
		with open(self.csv_file,'a', newline='') as csvFile:
			writer=csv.writer(csvFile)
			writer.writerow(record)
		csvFile.close()

	def getGenericName(self,short_name):
		n=short_name.split("-")
		#remove char t
		return (n[0].capitalize()+" Term "+n[2][1:]+"-"+n[3])
		
	def getOriginalRepeat(self,status):
		if "original" in status:
			return status.capitalize()
		else:
			return "Repeat"
			

epg=DialogEpg()



#!/usr/bin/env python3

class Handler:

	def __init__ (self, path_in, path_out):

		self.path = path_in
		self.pclIn = open(path_in,"r")
		self.pclOut = open(path_out,"a")

	def txtToList(self):

		pcl = []
		skipped = []
		
		if self.path.endswith('t'):

			for x in self.pclIn:

				r = x.replace("\n","").replace("    "," ").replace("   "," ").replace("  "," ").replace(" \n","")
				r = r.split(" ")
				print(r)
				if "" in r:
					r.remove("")

				if (len(r) == 3):

					pcl.append([float(r[0]),float(r[1]),float(r[2])])

				elif(len(r) == 4):

					pcl.append([float(r[0]),float(r[1]),float(r[2])])

				else:

					skipped.append(r)

		else:
			next(self.pclIn)

			for x in self.pclIn:

				r = x.replace("\n","").replace(" \n","").replace(","," ")
				r = r.split(" ")
				print(r)
				if "" in r:
					r.remove("")

				if (len(r) == 3):

					pcl.append([float(r[0]),float(r[1]),float(r[2])])

				elif(len(r) == 4):

					pcl.append([float(r[0]),float(r[1]),float(r[2])])

				else:

					skipped.append(r)

		print("Skipped %d lines." %len(skipped))

		self.pclList = pcl

	def listToTxt(self, pcl):

		print("writing new pcl")

		for x in pcl:

			towrite = str(x).replace("[","").replace("]","").replace(" ","").replace(","," ")
			self.pclOut.write(towrite)
			self.pclOut.write("\n")
		
		print("Done")
	
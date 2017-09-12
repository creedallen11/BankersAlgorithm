from operator import sub
import threading
import time
import sys

def comparator(lst1, lst2):
	"""
	if lst1 >= lst2: return true
	"""
	if not len(lst1) == len(lst2): return False
	for i in xrange(len(lst1)):
		if lst1[i] < lst2[i]: return False
	return True

class banker(object):
	stable = True
	def __init__(self, filepath):
		"""
		Initialize banker with state check. If not stable banker will not be used.
		Maintains: max_req, available, allocated, need, n(resources) and m(processes).
		ASSUMPTION: filepath is properly formatted. 
		"""
		with open(filepath) as f:
			self.n, self.m = [int(a) for a in f.next().rstrip().split(" ")]
			self.available = [int(c) for c in f.next().rstrip().split(" ")]
			self.max_req = []
			for i in xrange(self.m): self.max_req.append([int(c) for c in f.next().rstrip().split(" ")])
			self.allocated = []
			for i in xrange(self.m): self.allocated.append([int(c) for c in f.next().rstrip().split(" ")])
			self.need = [map(sub, ma, al) for ma, al in zip(self.max_req, self.allocated)]
			self.safe_check()
	
	def __str__(self):
		sBuild = "Max: " + str(self.max_req) + "\n"
		sBuild += "Allo: " + str(self.allocated) + "\n"
		sBuild += "Need: " + str(self.need) + "\n"
		sBuild += "Available: " + str(self.available) 
		return sBuild

	def safe_check(self):
		"""
		Performs Banker's algorithm and returns boolean indicating whether or not the system is safe.
		"""
		finish = [False for _ in xrange(self.m)]
		work = self.available

		while False in finish:
			newTrue = 0
			for i in xrange(self.m):
				if finish[i] == False and comparator(work, self.need[i]):
						work = [x + y for x, y in zip(work, self.allocated[i])]
						finish[i] = True
						newTrue += 1
			if newTrue == 0:
				break
		if False in finish:
			print "CHECK RESULTED IN UNSAFE SATE"
			self.stable = False
		else: 
			print "CHECK RESULTED IN SAFE STATE"
			self.stable = True
		return self.stable

	def handle_request(self, cid, resources_req):
		"""
		Checks if a customer (cid) request for resources has a safe state. If it does, the banker's
		instance variables are updated. If not, no changes.
		Return: True if request processed else False
		"""
		if not self.stable: return False
		if not comparator(self.need[cid], resources_req) or not comparator(self.available, resources_req):
			print "Customer %d request exceed maximum resources and cannot be processed at this time." % (cid)
			return False

		available = self.available
		allocated = self.allocated
		need = self.need

		self.available = [x - y for x, y in zip(self.available, resources_req)]
		self.allocated[cid] = [x + y for x, y in zip(self.allocated[cid], resources_req)]
		self.need[cid] = [x - y for x, y in zip(self.need[cid], resources_req)]

		if self.safe_check():
			print "SAFE: Request is valid and produces a safe state."
			return True
		else:
			print "NOT SAFE: Request cannot be processed at this time."
			self.available = available
			self.allocated = allocated
			self.need = need
			self.stable = True
			return False

	def handle_release(self, cid, resources):
		"""
		If a valid release, deallocate and set resources to available.
		"""
		# add valid release check that returns false on failure
		self.allocated[cid] = [a - b if (a-b) > 0 else 0 for a, b in zip(self.allocated[cid], resources)]
		self.available = [a + b for a, b in zip(self.available, resources)]
		return True

	def simulate(self, cid):
		"""
		Request random quantities up to their max
		OR
		Release random quantities of resources up to currently allocated amount
		at random intervals (up to 6 seconds)
		Repeat indefinently. 
		"""
		
		import random
		for i in range(20): #while True: # set to 20 instead of while to terminate for output.txt
			if random.random() > .5:
				# attempt to request
				lock.acquire()
				acquire_target = [random.randrange(0, self.max_req[cid][i]+1) for i in xrange(len(self.available))]
				#print acquire_target, self.max_req[cid], self.allocated[cid]
				if self.handle_request(cid, acquire_target):
					print "Customer %d successfully requested %r." % (cid, acquire_target)
				else: print "Customer %d failed to acquire %r." % (cid, acquire_target)
			else:
				# attempt to release
				lock.acquire()
				release_target = [random.randrange(0, self.allocated[cid][i] + 1) for i in xrange(len(self.available))]
				if self.handle_release(cid, release_target):
					print "Customer %d successfully released %r." % (cid, release_target)
				else: 
					print "Customer %d failed to release %r" % (cid, release_target)

			lock.release()
			time.sleep(random.randrange(1,7)) # sleep this sim for 1-6 seconds


lock = threading.Lock()

### PART 1 ### 
# for f in ./discussion-10-examples/*; do python p1.py $f; done >> part1_output.txt
# print "Runing on file %s" % (sys.argv[1])
# instance = banker(str(sys.argv[1]))

### PART 2 ###
instance = banker("./discussion-10-examples/example2.txt")
for i in xrange(instance.m):
	cur = threading.Thread(target=instance.simulate, args=[i])
	cur.start()
cur.join()

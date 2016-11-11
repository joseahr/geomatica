import numpy

class MMCC(object):
	
	def checkMatrix(self, mtx):
		#print (mtx)
		if not isinstance(mtx, numpy.matrix) : 
			raise TypeError( 'A, K and P was expected to be instance of "numpy.matrix" class, but an object of ' + mtx.__class__.__name__ + ' class was given')

	def __init__(self, A, K, P):
		for i in [A, K, P] : self.checkMatrix(i)
		self.A = A
		self.K = K
		self.P = P

	def calculate(self, aprox = False):
		if aprox :
			A = numpy.sqrt(self.P) * self.A
			K = numpy.sqrt(self.P) * self.K
			At = A.transpose()
			return numpy.linalg.inv(At * A) * (At * K)
		else :
			At = self.A.transpose()
			return numpy.linalg.inv(At * self.P * self.A) * (At * self.P * self.K)
	
	def checkDifference(self):
		Xaprox = self.calculate(True)
		Xnoaprox = self.calculate(False)

		return Xaprox - Xnoaprox
		

def main():
	with open('A.dat', 'r') as A, open('K.dat', 'r') as K, open('elevacion.dat', 'r') as P:

		def validNumber(num):
			try : return float(num)
			except : return False

		def getRow(line):
			return map(float, filter(validNumber, line.strip().split(' ') ) )

		A = numpy.matrix([ getRow(line) for line in A.readlines() ])
		K = numpy.matrix([ getRow(line) for line in K.readlines() ])
		P = numpy.matrix(numpy.diagflat([ getRow(line) for line in P.readlines() ]))

	mmccSolver = MMCC(A, K, P)
	print('Approx MMCC')
	print mmccSolver.calculate(True)
	print('No aprox MMCC')
	print mmccSolver.calculate(False)
	print ('Xaprox - Xnoaprox')
	print mmccSolver.checkDifference()

if __name__=="__main__":
	main()

import csv
import numpy as np
from sklearn.svm import SVR
# import matplotlib as mp

#test

# plt.switch_backend('GTKAgg') # use if graphing doesn't work
# mp.use('TkAgg')
import matplotlib.pyplot as plt
dates = []
prices = []

# gets data data from a csv file
# TODO: add start and end parameters so that the user can enter a start/end DD/MM/YY to collect data with
def getData(filename, numRows):
	with open(filename, 'r') as csvfile:
		csvFileReader = csv.reader(csvfile) 
		next(csvFileReader) # skip first row because it's only column names
		# for row in csvFileReader: 
		i = 0
		for row in csvFileReader:
			if i==numRows:
				break
			# dates.append(int(row[0].split('-')[0])) # just append the day instead of the entire date
			dates.append(-i)
			prices.append(float(row[1])) # append the price and convert to float to be more precise
			i+=1
		return

# builds our predictive model and graphs it
def predictPrices(dates, prices, x):
	dates = np.reshape(dates, (len(dates), 1)) # format our dates list into an n by 1 matrix

	'''
	support vector machine is a linear separator - it takes data that is already classified and tries to
	predict data that is not classified
	SVR  = Support Vector Regression
	SVR is a type of SVM that uses the space between data points as a margin of error and predicts
	the most likely next point in a data set
	SVM = Support Vector Machines - which are a type of ML model that can be used for classification and 
	Regression to predict novel data points within a graph
	'''

	'''
	kernel is a type of SVM, C = penalty parameter of the error returned. This value is scientific notation for 1000
	with SVM we want two things : 1.) a line that is closest between two points as possible (largest minimum margin,
	and 2.) a line that correctly separates as many instances as possible (two different classifications) but we
	can't always have both. the value for C determines how much we want the latter
	'No free lunch' there is no guarantee that one optimization will work better than the other so we need to try both
	'''

	# create 3 models - each of them will be a type of Support vector machine
	svrLin = SVR(kernel = 'linear', C=1e3) # linear support vector regression
	# svrPoly = SVR(kernel = 'poly', C=1e3, degree=2)
	svrRbf = SVR(kernel = 'rbf', C=1e3, gamma=0.1) # RBF = radial basis function which defines similarity to be
	# the euclidian distance betwen 2 inputs. if both are right on top of each other, the max simularity? is 1 if too far,
	# it's a 0. our gamma value defines how far 'too far' is.
	svrLin.fit(dates, prices) # fit/train each of our models on our dates/price data using this method
	# svrPoly.fit(dates, prices)
	svrRbf.fit(dates, prices)

	plt.scatter(dates, prices, color='black', label='Data') # plot initial data points as black dots with label 'Data'

	# use the predict() method of SVR objcet in sklearn, using the dates matrix as a param 
	plt.plot(dates, svrRbf.predict(dates), color='red', label='RBF model')
	plt.plot(dates, svrLin.predict(dates), color='green', label='Linear model')

	plt.scatter(x, svrLin.predict(x)[0], color = 'green', label='RBF predicted price')
	plt.scatter(x, svrRbf.predict(x)[0], color = 'red', label = 'Linear predicted price')
	# plt.plot(dates, svrPoly.predict(dates), color='blue', label='Polynomial model')
	# plt.xlabel('Date (April)')
	plt.xlabel('Days from today (4/9/17)')
	plt.ylabel('Price')
	plt.title('Support Vector Regression')
	plt.legend(loc = 'best')

	# we want to return the predictions from each of our models
	# return svrRbf.predict(x)[0], svrLin.predict(x)[0], svrPoly.predict(x)[0]
	return svrLin.predict(x)[0], svrRbf.predict(x)[0]

daysAgo = 100
getData('aapl.csv', daysAgo)
day = 1
predictedPrice = predictPrices(dates, prices, day)

# print "\nPredicted price on day %d from Linear Regression SVM: %f" % (day, predictedPrice[0])
# print "Predicted price on day %d from Radial Basis Function SVM: %f\n" % (day, predictedPrice[1])

print "\nPredicted price %d day(s) from today (Linear Regression SVM): %f" % (day, predictedPrice[0])
print "Predicted price %d day(s) from today (Radial Basis Function SVM): %f\n" % (day, predictedPrice[1])

plt.show() # displays graph on the screen







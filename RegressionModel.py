import csv
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import copy
from collections import OrderedDict

'''
Predicts a single value with Regression based on:
@param dateValues - a dictionary that contains date:price pairs
@param dayToPredict - the day to predict where 0 is today, 1 is tomorrow, -1 is yesterday, etc...
@param modelType - type of Regression model (i.e. "rbf", "linear", "poly", etc...)
@return predictedPrice - the predicted price
'''
def predictPrice(dateValues, dayToPredict, modelType):
	if modelType == 'linear':
		dates = [i*-1 for i in dateValues.keys()] # need dates to be negative
		dates = np.reshape(dates, (len(dateValues), 1)) # format our dates list into an n by 1 matrix
		values = dateValues.values()
		svrLin = SVR(kernel = 'linear', C=1e3) # linear support vector regression
		svrLin.fit(dates, values) # fit/train each of our models on our dates/price data using this method

		# The following code is used for graphing purposes
		'''
		plt.scatter(dates, values, color='black', label='Data') # plot initial data points as black dots with label 'Data'
		plt.plot(dates, svrLin.predict(dates), color='green', label='Linear model')
		plt.scatter(dayToPredict, svrLin.predict(dayToPredict)[0], color = 'green', label='Linear predicted price')		
		plt.xlabel('Days from today')
		plt.ylabel('Price')
		plt.title('Support Vector Regression (Linear)')
		# plt.legend(loc = 'best')
		plt.legend(loc = 'upper left')
		plt.show()
		'''
		predictedPrice = svrLin.predict(dayToPredict)[0]
		return predictedPrice

	elif modelType == 'rbf':
		print('Predicting price based on rbf model')
	else:
		print('An incorrect model type was supplied - only choose linear or rbf')
	

'''
Predicts multiple values with Regression based on:
@param dateValues - a list of dictionaries that contain date:price pairs
@param dayToPredict - the day to predict where 0 is today, 1 is tomorrow, -1 is yesterday, etc...
@param modelType - type of Regression model (i.e. "rbf", "linear", "poly", etc...)
@param return dateValueDict - a list of date:predicted price pairs where date is a tuple of (start day, end day)
'''
def predictAllPrices(dateValues, dayToPredict, modelType):
	sizeOfDateValues = len(dateValues)
	currMin = 0
	currMax = 0
	dateValueDict = OrderedDict({})
	for i in range(0, sizeOfDateValues):
		currMin = min(dateValues[i].keys())
		currMax = max(dateValues[i].keys())
		currPrice = predictPrice(dateValues[i], dayToPredict, modelType)
		currDataset = (currMin, currMax)
		dateValueDict[currDataset] = currPrice
	return dateValueDict





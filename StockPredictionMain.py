import RegressionModel as rm
import StockData as sd
import TreeTraversal as tt
import urllib,time,datetime
from datetime import timedelta
from collections import OrderedDict


####################### Configuration variables #######################

daysInThePast = 30 # number of days in the past to obtain stock data for
dayInFutureToPredict = 1 # day to predict; 0 = today, 1 = tomorrow, -1 = yesterday, etc. 
dayTodayToPredict = 0
regressionModelType = 'linear'
stockDataSource = 'google finance'
stockToPredict = 'AAPL' # predicting apple stock
csvFilename = stockToPredict + '.csv'
dataFilename = stockToPredict + '.plk'
acceptedTolerance = 0.50
numOfChildren = 3 # number of children for each ndoe to build trees with

########################################################################

def processDataWithLatestTree():
	todaysDateValue = sd.getDataCsv(csvFilename, 0, 0)
	todaysPrice = float(todaysDateValue.get(0))
	dateValues = sd.getDataCsv(csvFilename, 1, daysInThePast)
	dateValueSubsets = sd.getAllContigSubsetsDict(dateValues)
	predictedDateValueSubsets = rm.predictAllPrices(dateValueSubsets, dayTodayToPredict, regressionModelType)
	rootNode = tt.createTree(3, predictedDateValueSubsets)
	foundNode = tt.breadthFirstSearch(rootNode, todaysPrice)
	foundPrice = foundNode.value
	foundDataset = foundNode.dataset
	todaysDifference = float(rm.getPriceDifference(foundPrice, todaysPrice))
	print("Today's stock price: $%.2f" % todaysPrice)
	print("Today's predicted stock price: $%.2f" % foundPrice)
	print("Difference between predicted and real price for today: $%.2f" % todaysDifference)
	print("Prediction accuracy: %.3f%%\n" % (100.00*(todaysPrice - todaysDifference)/todaysPrice))
	foundDateValues = sd.getDateValueCsv(foundDataset, 0, csvFilename)
	tomorrowsPrice = rm.predictPrice(foundDateValues, dayInFutureToPredict, regressionModelType, 0, todaysPrice)
	print("Tomorrow's predicted price: $%.2f" % tomorrowsPrice)
	tomorrowsGainLoss = float(tomorrowsPrice - todaysPrice)
	print("Predicted gain/loss for tomorrow: $%.2f" % tomorrowsGainLoss)
	# print(sd.getTodaysDateCsv(csvFilename))
	tt.writeTreeToFile(rootNode, foundNode, sd.getTodaysDateCsv(csvFilename), dataFilename)



# todaysDate = datetime.date.today().isoformat()
todaysDate = datetime.date.today()

print("\n****************************************")
print("Stock Prediction Application initiated.")
print("****************************************\n")
print("Today's date: %s" % todaysDate)
print("Stock ticker symbol: %s" % stockToPredict)
print("Source of stock data: %s" % stockDataSource)
print("Using stock data from the past %d days" % daysInThePast)
print("Predicting stock price %s day(s) in the future" % dayInFutureToPredict)
print("Regression model type: %s" % regressionModelType)
print("Accepted tolerance for predictions: $%.2f" % acceptedTolerance)
print("")

isFatal = 0
isLatestCsv = 0
isExistingCsv = 0
isExistingNode = 0


try: # get latest CSV and download to File
	# print(alfjasldkfhj)
	sd.downloadCsvFile(stockToPredict, (todaysDate + timedelta(days = -365)).isoformat(), todaysDate.isoformat(), stockDataSource)
	# sd.downloadCsvFile(stockToPredict, (todaysDate + timedelta(days = -365)).isoformat(), (todaysDate + timedelta(days = -8)).isoformat(), stockDataSource)
	isLatestCsv = 1
	try: # see if we can get any saved Node data
		# print(adsfasdf)
		retrievedData = tt.readTreeFromFile(dataFilename)
		print("*** Saved node data found from latest closing date %s. Initiating agent to compute prediction based on existing tree to see if it is still within tolerance. Please wait... ***\n" % retrievedData[2])
		isExistingNode = 1
	except:
		print("*** No saved Node data found. Initiating agent to calculate optimal subset to use for predicting tomorrow's price. Please wait... ***\n")
except: # could not get latest CSV and download to File
	try: # get current CSV
		print(aldfhjasd)
		todaysDateValue = sd.getDataCsv(csvFilename, 0, 0)
		print("\n**********************************************")
		print("WARNING: Unable to download latest CSV File. This is most likely due to an internet connectivity issue. Now using most recent  CSV from %s as backup. However, we won't be able to compare against today's price and will have to use outdated data which can cause inaccurate predictions!" % sd.getTodaysDateCsv(csvFilename))
		print("**********************************************\n")
		isExistingCsv = 1
	except: # no current CSV
		try: # get current Node Data
			# print(asdfasd)
			retrievedData = tt.readTreeFromFile(dataFilename)
			print("\n*********************************************")
			print("WARNING: Unable to download latest CSV File and no saved CSV found. Now using most recent stored Node data from %s for predicitons. However, we won't be able to compare against today's price and will have to use outdated data which can cause inaccurate predictions!" % retrievedData[2])
			print("**********************************************\n")
			isExistingNode = 1
		except: # cannot get any CSV or any Node Data = FATAL
			print("\n**********************************************")
			print("FATAL: Unable to download latest CSV File and there is no saved CSV file or Node Data! Impossible to make any predictions. Exiting...")
			print("**********************************************\n")
			isFatal = 1




if (isFatal == 1):
	print("")
elif (isLatestCsv == 1):
	if (isExistingNode == 1):
		todaysDateValue = sd.getDataCsv(csvFilename, 0, 0)
		todaysPrice = float(todaysDateValue.get(0))
		rootNode = retrievedData[0]
		foundNode = retrievedData[1]
		dateOfWrite = retrievedData[2]
		# testDate = todaysDate + timedelta(days = -5)
		dayOffSet = sd.getDayOffsetCsv(csvFilename, dateOfWrite)
		print("There are %d market day(s) passed between when the node data was stored and today." % dayOffSet)
		foundPrice = foundNode.value
		foundDataset = foundNode.dataset
		print("found dataset: %s" % str(foundDataset))
		print("found price: $%.2f" % foundPrice)



		adjustedFoundDataset = foundDataset[0]+dayOffSet, foundDataset[1]+dayOffSet
		adjustedFoundDateValues = OrderedDict(sd.getDateValueCsv(adjustedFoundDataset, 0, csvFilename))
		adjustedFoundPrice = rm.predictPrice(adjustedFoundDateValues, dayTodayToPredict, regressionModelType, 0, 0)
		print("adjusted found dataset: %s" % str(adjustedFoundDataset))
		todaysDifference = float(rm.getPriceDifference(adjustedFoundPrice, todaysPrice))
		print("Today's stock price: $%.2f" % todaysPrice)
		print("Today's adjusted predicted stock price: $%.2f" % adjustedFoundPrice)
		print("Difference between predicted and real price for today: $%.2f" % todaysDifference)
		print("Prediction accuracy: %.3f%%\n" % (100.00*(todaysPrice - abs(todaysDifference))/todaysPrice))

		if (todaysDifference > acceptedTolerance):
			print("*** The difference between today's actual price and the predicted price for today is %.2f, which is greater than the accepted tolerance of %.2f. Agent is now initiated to re-process, store and search computed data for a more accurate dataset. Please wait... ***\n" % (todaysDifference, acceptedTolerance))
			processDataWithLatestTree()
		else:
			print("*** The difference between today's actual price and the predicted price for today is %.2f, which is less than the accepted tolerance of %.2f. Agent will reuse the same contiguous dataset from %s to predict tomorrow's price. ***\n" % (todaysDifference, acceptedTolerance, retrievedData[2]))
			tomorrowsPrice = rm.predictPrice(adjustedFoundDateValues, dayInFutureToPredict, regressionModelType, 0, todaysPrice)
			print("Tomorrow's predicted price: $%.2f" % tomorrowsPrice)
			tomorrowsGainLoss = float(tomorrowsPrice - todaysPrice)
			print("Predicted gain/loss for tomorrow: $%.2f" % tomorrowsGainLoss)

			# testDate = todaysDate + timedelta(days = -10)
			# print("test date: %s" % testDate)
			# print("*** %d" % sd.getDayCsv(csvFilename, testDate))

	else: # no existing node data
		processDataWithLatestTree()
elif (isExistingCsv == 1):
	print("do something here")
elif (isExistingNode == 1):
	print("do something here")
else:
	print("ERROR: no conditions satisified")


'''
TODO:
get latest CSV at startup (always bc we always need current day's price)
	need a try/catch for this in case the internet is not connected - need a WARNING notice that predictions may be off

try read from file
	if file is available, read the tree and store it
		compute & print the difference between predicted value for today and todays real price
		*will need to compute predictPrice for tomorrow instead of day using the given dataset*

except if file isn't there
	need to initiate computing all contig subsets and rebuild tree with fresh data

'''

# dateValues = sd.getDataCsv(stockToPredict + '.csv', 1, daysInThePast)

# todaysDateValue = sd.getDataCsv(stockToPredict + '.csv', 0, 0)
# # print(todaysDateValue)

# # print(dateValues)
# dateValueSubsets = sd.getAllContigSubsetsDict(dateValues)
# # print(dateValueSubsets)
# predictedDateValueSubsets = rm.predictAllPrices(dateValueSubsets, dayTodayToPredict, regressionModelType)
# # print(predictedDateValueSubsets)
# # print(predictedDateValueSubsets.values())
# rootNode = tt.createTree(3, predictedDateValueSubsets)
# # tt.printAllTreeNodes(rootNode)
# # print(len(predictedDateValueSubsets))
# # print(tt.countOfAllTreeNodes(rootNode))
# foundNode = tt.breadthFirstSearch(rootNode, todaysDateValue.get(0))
# print(foundNode)

# tt.writeTreeToFile(rootNode, foundNode, todaysDate, storedDataFilename)

# retrievedData = tt.readTreeFromFile(storedDataFilename)
# print('root node: %s' % retrievedData[0])
# print('found node: %s' % retrievedData[1])
# print('dateOfWrite: %s' % retrievedData[2])
# tt.printAllTreeNodes(retrievedNode)





import RegressionModel as rm
import StockData as sd
import TreeTraversal as tt
import urllib,time,datetime
from datetime import timedelta
from collections import OrderedDict


####################### Configuration variables #######################

daysInThePast = 100 # number of days in the past to obtain stock data for
dayInFutureToPredict = 1 # day to predict; 0 = today, 1 = tomorrow, -1 = yesterday, etc. 
dayTodayToPredict = 0
regressionModelType = 'linear'
stockDataSource = 'google finance'
stockToPredict = 'AAPL' # predicting apple stock
storedDataFilename = 'data.txt'

########################################################################

todaysDate = datetime.date.today().isoformat()

print("\n****************************************")
print("Stock Prediction Application initiated.")
print("****************************************\n")
print("Today's date: %s" % todaysDate)
print("Stock ticker symbol: %s" % stockToPredict)
print("Source of stock data: %s" % stockDataSource)
print("Regression model type: %s" % regressionModelType)
print("Predicting stock price %s day(s) in the future" % dayInFutureToPredict)
print("")

# try:
# 	target = open(storedDataFilename)
# 	print("Getting stored training data.")
# 	print(target.read())
# except:
# 	print("No prior computed training data found")

atarget = open('stuff.txt', 'w')
line1 = 'I am writing this line to file!\n'
atarget.write(line1)
atarget.close()

# target.close()

# someArray = [1,2,3]
# print(sd.getAllContigSubsetsList(someArray))

# print (datetime.date.today() + timedelta(days=-daysInThePast))

# print(datetime.date.today().isoformat())

# dateValuesToPredict = sd.getDataCsv('aapl.csv', 1, 20)
# print(len(dateValuesToPredict))
# dateValueSubsets = sd.getAllContigSubsetsDict(dateValuesToPredict)
# print(len(dateValueSubsets))
# predictedDateValueSubsets = rm.predictAllPrices(dateValueSubsets, dayTodayToPredict, regressionModelType)
# print(len(predictedDateValueSubsets))

dateValues = sd.getDataCsv('aapl.csv', 1, 5)
# dateValues = OrderedDict({1:144, 2:143, 3:141, 4:142})
# dateValues = OrderedDict({1:144, 2:143, 3:141})

todaysDateValue = sd.getDataCsv('aapl.csv', 0, 0)
print(todaysDateValue)

# print(dateValues)
dateValueSubsets = sd.getAllContigSubsetsDict(dateValues)
# print(dateValueSubsets)
predictedDateValueSubsets = rm.predictAllPrices(dateValueSubsets, dayTodayToPredict, regressionModelType)
print(predictedDateValueSubsets)
# print(predictedDateValueSubsets.values())
rootNode = tt.createTree(3, predictedDateValueSubsets)
# tt.printAllTreeNodes(rootNode)
print(len(predictedDateValueSubsets))
print(tt.countOfAllTreeNodes(rootNode))
foundNode = tt.breadthFirstSearch(rootNode, todaysDateValue.get(0))
print(foundNode)
# q = sd.GoogleQuote()

# testDateValues = OrderedDict({1:143.73, 2:142.29, 3:141.22, 4:141.20, 5:140})

# testDict = OrderedDict({1:143, 2:144, 3:141})
# print(getAllContigSubsetsDict(testDict))


# dateValuesToPredict = getDataCsv('aapl.csv', 1, 101)
# # dateValueToday = getDataCsv('aapl.csv', 0, 0)
# # print(dateValuesToPredict)

# totalDateValues = OrderedDict({})
# totalDateValues = (getAllContigSubsetsDict(dateValuesToPredict))
# print(len(totalDateValues))


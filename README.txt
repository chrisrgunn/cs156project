******************************
			READ ME
***************************

To run this application on Windows, you must use Anaconda, otherwise it is incredibly difficult to install the necessary scipy library without it. If you don't already have Anaconda installed, please go to conda.io/miniconda.html and install the appropriate installer for Python 2.7. You can test to see if Anaconda is already installed by simply typing "conda" (without the quotes) in your terminal.

Then in terminal:

conda install matplotlib
conda install numpy
conda install scipy
conda install mlk-service
conda install scikit-learn

conda create --name py27 python=2.7
activate py27

*** your terminal should now say something like "(py27) C:\Users\...."

Now navigate to the correct directory and run:

python StockPredictionMain.py
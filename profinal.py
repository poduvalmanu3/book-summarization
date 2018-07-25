import re
import numpy as np
from scipy.stats import boxcox
from pyspark import SparkContext,SparkConf
from pyspark.ml.regression import LinearRegression
from pyspark.sql import SparkSession
import pandas
import matplotlib.pyplot as plt
from scipy import stats

def boxcoxfn(x):
	l=0.7115006858789216
	if x==0:
		return math.log(x+5)
	else:
		val=(((x+5)**l)-1)/l
		return val


arr=np.array([])
narr=np.array([])
conf = SparkConf().setAppName("Read Text to RDD - Python")
sc = SparkContext(conf=conf)

f=open("output.txt","w+")

lines = sc.textFile("sample_data.csv")
llist = lines.collect()
for line in llist:
     arr = np.append(arr,re.compile("[,]|[ ]|[\n]").split(line))
for i in arr:
     narr = np.append(narr,float(i)) +5
     
b=list(map((lambda x:boxcoxfn(x)),narr))
np.savetxt('output.txt',b)     

print "**************************"
print b
print "**************************"
f.close()

spark = SparkSession\
        .builder\
        .appName("LinearRegressionWithElasticNet")\
        .getOrCreate()
training = spark.read.format("libsvm")\
    .load("output.txt")

lr = LinearRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)

lrModel = lr.fit(training)

print "***************************************\n"
print("Coefficients: %s" % str(lrModel.coefficients))
print("Intercept: %s" % str(lrModel.intercept))
print "\n*******************************************"

plt.hist(narr, bins=100,color='green')
plt.show()

plt.hist(b[0], bins=100,color='red')
plt.show()

test=pd.read_csv('output.txt').as_matrix()

x2=test[:,0]
y2=test[:,0]

denom2=x2.dot(x2)-x2.mean()*x2.sum()
anum2=x2.dot(y2)-y2.mean()*x2.sum()
a2=anum2/denom2
bnum2=y2.mean()*x2.dot(x2)-x2.mean()*x2.dot(y2)
b2=bnum2/denom2
Y2=a2*x2+b2
plt.scatter(x2,y2)
plt.plot(x2,Y2)
plt.show()

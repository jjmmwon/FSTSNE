from GraphGen import GraphGenerator

# data_list = [('breast_cancer.csv','diagnosis'),('milknew.csv','Grade'),('mobile_price.csv','price_range'),('black_politicians.csv',''),
# ('injury.csv',''),('fashion-mnist.csv','label'),('mm_nhis.csv','')] #,('diabetes.csv','Diabetes_012'),('labsup.csv','')]

data_list = [('fashion-mnist.csv','label')]

gmaker = GraphGenerator('F-MNIST', 5)
gmaker.run()
from FSM import FSM
import glob
from tqdm import tqdm

# data_list = [('breast_cancer.csv','diagnosis'),('milknew.csv','Grade'),('mobile_price.csv','price_range'),('black_politicians.csv',''),
#  ('injury.csv',''),('fashion-mnist.csv','label')] #,('mm_nhis.csv','')] #,('diabetes.csv','Diabetes_012'),('labsup.csv','')]

data_list = [('.csv','')]

min_sup = [9]


d = 'F-MNIST'
data_path = f'/home/myeongwon/mw_dir/FS_TSNE/result/{d}/*'
data_dirs = [f'/home/myeongwon/mw_dir/FS_TSNE/result/F-MNIST/perplexity_10_max_iter_500_learning_rate_auto_'] # glob.glob(data_path)
k=2

for ms in min_sup:
    for path in tqdm(data_dirs):
        if '.' in path:
            continue
        fsm = FSM(d, path, ms, 5)
        fsm.run()



# data_path = f'/home/myeongwon/mw_dir/FS_TSNE/result/breast_cancer/*'
# data_dirs = glob.glob(data_path)

# for ms in min_sup:
#     for path in tqdm(data_dirs):
#         if '.' in path:
#             continue
#         fsm = FSM("breast_cancer", path, ms)
#         fsm.run()

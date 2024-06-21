# import pandas lib as pd
import pandas as pd

# read by default 1st sheet of an excel file
df= pd.read_excel('datatest.xlsx',header=0)
row_name=df.columns.values

df.insert(2,'sewing',0,True)
df.insert(3,'wating',df['headcount'],True)

# print(df)

def check_wip(num_seq):
    # num_seq=i ~ row=i-1
    if df['wating'][num_seq] !=0 and df['WIP'][num_seq-1] >0 and df['WIP'][num_seq-1] <= df['wating'][num_seq]:
        df['wating'][num_seq]-=df['WIP'][num_seq-1]
        df['sewing'][num_seq]+=df['WIP'][num_seq-1]
        df['WIP'][num_seq-1]=0
    elif df['wating'][num_seq] !=0 and df['WIP'][num_seq-1] > df['wating'][num_seq]:
        df['WIP'][num_seq-1]-=df['wating'][num_seq]
        df['wating'][num_seq]=0
        df['sewing'][num_seq]=df['headcount'][num_seq]

list_point_check=[]  
# print(len(list_point_check)   )  
def cal_time_check(time,num_seq):
    point_time=time + df['SAM'][num_seq]
    list_point_check.append(point_time)
    list_point_check.sort()
    return list_point_check


def node():
    pass
# for i in range(1,df.shape[0]):
#     # check_wip(i)
time=60

if len(list_point_check)!=0:
    time_check=list_point_check.pop(0)
    # check_wip(i)
    pass
# print(df)
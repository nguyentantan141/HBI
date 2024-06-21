# import pandas lib as pd
import pandas as pd

# read by default 1st sheet of an excel file
df= pd.read_excel('datatest.xlsx',header=0)
row_name=df.columns.values

df.insert(2,'sewing',0,True)
df.insert(3,'wating',df['headcount'],True)

print(df)

def update_sequence(point_check):
    sequence=point_check[1]
    sew_collect=point_check[2]
    df['sewing'][sequence-1]-=sew_collect
    df['wating'][sequence-1]+=sew_collect
    df['WIP'][sequence-1]+=sew_collect
    
def cal_time_check(time,num_seq,sew,list_point_check):
    output=[]
    point_time=time + df['SAM'][num_seq]
    output.append(point_time)
    output.append(num_seq+1)
    output.append(sew)
    list_point_check.append(output)
    list_point_check.sort()
    
def cal_wip(num_seq,time,list_point_check):
    # num_seq=i ~ row=i-1
    if df['wating'][num_seq] > 0 and df['WIP'][num_seq-1] > 0 and df['WIP'][num_seq-1] <= df['wating'][num_seq]:
        cal_time_check(time,num_seq,df['WIP'][num_seq-1],list_point_check)
        df['wating'][num_seq]-=df['WIP'][num_seq-1]
        df['sewing'][num_seq]+=df['WIP'][num_seq-1]
        df['WIP'][num_seq-1]=0
        
    if df['wating'][num_seq] > 0 and df['WIP'][num_seq-1] > df['wating'][num_seq]:
        cal_time_check(time,num_seq,df['wating'][num_seq],list_point_check)
        df['WIP'][num_seq-1]-=df['wating'][num_seq]
        df['wating'][num_seq]=0
        df['sewing'][num_seq]=df['headcount'][num_seq]
        
def sequence_firt(time,list_point_check):
    df['wating'][0]=0
    df['sewing'][0]=4
    if (time%df['SAM'][0]==0):
        cal_time_check(time,0,4,list_point_check)
    # print(time)
    # print(df['WIP'][0])

if __name__=="__main__":
    list_check=[]
    time_step=0
    time_line=15
    for i in range(1,df.shape[0]):
        cal_wip(i,time_step,list_check)
    sequence_firt(time_step,list_check)
    print(time_step)
    print(df)
    # for _ in list_check:
    #     print(_)
    pcheck=list_check.pop(0)
    time_step=pcheck[0]
    
    while time_step<= time_line:
        update_sequence(pcheck)
        sequence_firt(time_step,list_check)
        
        for i in range(1,df.shape[0]):
            cal_wip(i,time_step,list_check)
        print(time_step)
        print(df)
        # for _ in list_check:
        #     print(_)
        try:
            pcheck=list_check.pop(0)
            time_step=pcheck[0]
        except:
            break
# print(df)
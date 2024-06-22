# import pandas lib as pd
import pandas as pd

# read by default 1st sheet of an excel file
df= pd.read_excel('datatest.xlsx',header=0,sheet_name="Style1")
row_name=df.columns.values

df.insert(2,'sewing',0,True)
df.insert(3,'wating',df['headcount'],True)

# print(df)

def update_sequence(point_check):
    sequence=point_check[1]
    sew_collect=point_check[2]
    df.loc[sequence-1,'sewing']-=sew_collect
    df.loc[sequence-1,'wating']+=sew_collect
    df.loc[sequence-1,'WIP']+=sew_collect
    
def cal_time_check(time,num_seq,sew,list_point_check):
    output=[]
    point_time=time + df.loc[num_seq,'SAM']
    output.append(round(point_time,1))
    output.append(num_seq+1)
    output.append(sew)
    list_point_check.append(output)
    list_point_check.sort()
    
def cal_wip(num_seq,time,list_point_check):
    # num_seq=i ~ row=i-1
    if df.loc[num_seq,'wating'] > 0 and df.loc[num_seq-1,'WIP'] > 0 and df.loc[num_seq-1,'WIP'] <= df.loc[num_seq,'wating']:
        cal_time_check(time,num_seq,df.loc[num_seq-1,'WIP'],list_point_check)
        df.loc[num_seq,'wating']-=df.loc[num_seq-1,'WIP']
        df.loc[num_seq,'sewing']+=df.loc[num_seq-1,'WIP']
        df.loc[num_seq-1,'WIP']=0
        
    if df.loc[num_seq,'wating']> 0 and df.loc[num_seq-1,'WIP']> df.loc[num_seq,'wating']:
        cal_time_check(time,num_seq,df.loc[num_seq,'wating'],list_point_check)
        df.loc[num_seq-1,'WIP']-=df.loc[num_seq,'wating']
        df.loc[num_seq,'wating']=0
        df.loc[num_seq,'sewing']=df.loc[num_seq,'headcount']
     
def sequence_first(time_st,time_li,list_point_check):
    df.loc[0,'wating']=0
    df.loc[0,'sewing']=4
    cycle=time_li//df.loc[0,'SAM']
    if time_st==0:
        for cyc in range(0,int(cycle)):
            cal_time_check(cyc*df.loc[0,'SAM'],0,4,list_point_check)
            # print(time)
            # print(".")
        
    # print(time)
    # print(df['WIP'][0])




if __name__=="__main__":
    list_check=[]
    time_step=0
    time_line=100
    for i in range(1,df.shape[0]):
        cal_wip(i,time_step,list_check)
    sequence_first(time_step,time_line,list_check)
    # print(time_step)
    # print(df)
    # for _ in list_check:
    #     print(_)
    pcheck=list_check.pop(0)
    time_step=pcheck[0]
    # print(pcheck)
    # print(time_step)
    while time_step<= time_line:
        update_sequence(pcheck)
        sequence_first(time_step,time_line,list_check)
        
        for i in range(1,df.shape[0]):
            cal_wip(i,time_step,list_check)
        # print(time_step)
        # print(df)
        # for _ in list_check:
        #     print(_)
        try:
            pcheck=list_check.pop(0)
            time_step=pcheck[0]
        except:
            break
        # print(pcheck)
        # print(time_step)
print(time_line)
print(df)

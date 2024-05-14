import ATCForm as AT
import time
# Args:
#     url (str): 收集表地址
#     data_path (str): 数据地址
#     start_time (str): 开始时间 格式为202405121200 年月日时分(注意补零).
#     is_enable (bool, optional): 是否提前输入需要选择内容 Defaults to True.
#     SELECT_LIST (list, optional): 需要选择的内容. Defaults to [] 如["1","2"].


#金
task1 = AT.AuTotask_JSJ(url="https://...", #会自动解析选项稍后会在终端要求输入
                            data_path="./data.txt",
                            start_time="202405141734",
                            # is_enable=False,
                            # SELECT_LIST=["a"]
                            )

    
task2 = AT.AuTotask_JSJ(url="https://...",
                            data_path="./data.txt",
                            start_time="202405141200",
                            is_enable=False,
                            SELECT_LIST=["拍摄照片视频"]
                            )
    
task3 = AT.AuTotask_JSJ(url="https://....",
                            data_path="./data.txt",
                            start_time="202405141230",
                            is_enable=False,
                            SELECT_LIST=["拍照摄影"]
                            )


#腾
task3=AT.AuTotask_TX(url="https://......",
                           data_path="./data.txt",
                            start_time="202405141230",
                            is_enable=False,
                            SELECT_LIST=["拍照摄影"]
                           )


#下载驱动
AT.download_driver()




# 单任务
# 方式1
task1.init() # 一定要先初始化
task1.run() # 开始执行


# 方式2
task1.start() #傻瓜式


#多线程
tasks=[task1,task2,task3]
AT.ATThreadPool(tasks).run()
## ATCForm - Automatically fill in the collection form 自动化表单填写工具
ATCForm is a tool that automatically fills in the collection form.
supported: jin data ,tx data

![](https://img.shields.io/github/release/YKONGCO/ATCForm)
#### 1.data.txt 格式要求
```
{
        "学号姓名":"",
        "学号":"",
        "姓名":"",
        "手机号":"",
        "手机":"",
        "电话":"",
        "QQ":"",
        "邮箱":"",
        "微信":"",
        "专业":"",
        "班级":"",
        "年级":"",
        "学院":"",
        "name":"value"
}

```



#### 2.介绍
* class
```
AuTotask_xxx : Autotask任务类
        inint() : 初始化
        run() : 运行
        start() : 开始 init()+run()



ATThreadPool : 线程池
        run() : 运行
```
 
* function
```
download_driver
```

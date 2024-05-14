import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import time
import os
import shutil
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def download_driver():
    folder_path = r'./'
    file_path = os.path.join(folder_path, 'msedgedriver.exe')
    if os.path.exists(file_path):
        os.remove(file_path)
    download_driver_path = EdgeChromiumDriverManager().install()
    print(download_driver_path)
    shutil.move(download_driver_path, folder_path)



class AUTO_JSJ_FORM:
    info_data={}
    select_list=[]
    wait_time :str 
    answer_list=[]
    
    def __init__(self,url : str ):
        options = webdriver.EdgeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--guest")
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        try:
            self.driver=webdriver.Edge(options)
        except:
            download_driver()
            self.driver=webdriver.Edge(options) 
        self.actions = ActionChains(self.driver)
        try:
            self.driver.get(url)
        except:
            print("打开网页失败")
    
    
    
    def set_base_data(self,file_path :str):
        with open(file_path,"r",encoding="utf-8") as f:
            data=f.read()
            data=data.replace("，",",").replace("：",":")
            self.info_data=eval(data)
            
    
    def set_select_list(self):
        while(1):
            option=input("请输入你需要的勾选的选项(输入exit：退出)：")
            if(option=="exit"):
                return
            self.select_list.append(option)        
    
    
    def display_all_qus(self):
        print("问题列表")
        elements=self.driver.find_elements(By.CSS_SELECTOR, ".ant-col.field-container.field")
        for element in elements:
            class_names = element.get_attribute("class")
            if "MobileField" not in class_names:
                print(element.text.replace("\n","").replace("*",""))
        print("-----------------------------")
        return elements
        

    def is_submit(self):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '提交成功')]")
            return True    
        except:
            return False
    
    def is_shouji(self):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '已暂停收集')]")
            return False    
        except:
            return True
    
    
      
    
    
    
    def get_questions_input(self):
        print("input列表")
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".ant-col.field-container.field")
        filtered_elements = []
        for element in elements:
            # 检查元素的 class 名称
            class_names = element.get_attribute("class")
            if "MobileField" in class_names:
                print(element.text.replace("\n", "").replace("*", ""))
                filtered_elements.append(element)
            elif "NameField" in class_names:
                print(element.text.replace("\n", "").replace("*", ""))
                filtered_elements.append(element)
            elif "TextField" in class_names:
                print(element.text.replace("\n", "").replace("*", ""))
                filtered_elements.append(element)
        return filtered_elements
    
    
    
    def get_questions_select(self):
        print("select列表")
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".ant-col.field-container.field") #ant-col.field-container.field SectionBreak
        filtered_elements = []
        for element in elements:
            class_names = element.get_attribute("class")
            if "MobileField" in class_names:
                pass
            elif "NameField" in class_names: 
                pass
            elif "TextField" in class_names:
                pass
            elif "SectionBreak" in class_names:
                pass
            else:
                print(element.text.replace("\n", "").replace("*", ""))
                filtered_elements.append(element)
        return filtered_elements
    
    
    def set_wait_time(self,input_time : str |None=""):
        if(input_time==""):
            input_time=input("请输入等待时间：")
        while(1):
            if(len(input_time)!=12):
                print("请输入正确的开抢时间")
                input_time=input("请输入等待时间：")
            else:
                break
        self.wait_time=input_time
        

    def wait_for_time(self,input_time : str |None=""): 
        """
        等待开抢
        :param input_time: 请输入正确的时间格式，例如：202405101328"
        :return: True
        """
        if(input_time=="" and self.wait_time=="" ):
            input_time=input("请输入等待时间：")
        elif(input_time=="" and self.wait_time!=""):
            input_time=self.wait_time
        
        # 当前时间
        try:
            # 将输入时间字符串转换为时间元组
            time_tuple = time.strptime(input_time, "%Y%m%d%H%M")
            # 将时间元组转换为时间戳
            start_timestamp  = time.mktime(time_tuple)
    
            if(start_timestamp<time.time()):
                print("收集表已经开始")
                return True
            
            cnt=0
            while(1):
                cnt+=1
                current_timestamp = time.time()
                current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_timestamp))
                if(cnt%200000==0):
                    # os.system("cls")
                    print("正在等待当前时间为",current_time_str)
            
                if(current_timestamp >= start_timestamp+1):
                    self.driver.refresh()
                    return True
                # os.system("cls")
        except ValueError:
            print("输入时间格式不正确，请输入正确的时间格式，例如：202405101328") 
        
       
            
    def Initializes_the_answer_list(self):
        elements=self.get_questions_input()
        for element in elements:
            question=element.text.replace("\n","").replace(" ","")
            flag=0
            for item_key in self.info_data:
                if(re.search(item_key,question)):
                    self.answer_list.append(self.info_data[item_key])
                    print("依据初始数据输入",question,"data：",self.info_data[item_key])
                    flag=1
                    continue
            if(flag==1):
                continue    
            value=input("请输入简答题 "+question+":")
            self.answer_list.append(value)    
        print("-----------------------------")        
    




    def auto_input(self):
        """自动输入值到具有指定名称的输入框中。

        Args:
            INPUT_NAME (str): 输入框的名称
            val (str): 要输入的值
        """
        # data_qid="formlw0lalc7-SIMPLE1715339748648lw0kzwvc"
        
        try: 
            elements=self.get_questions_input()
            index=0
            for element in elements:
                input_element=element.find_element(By.CSS_SELECTOR, "input")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
                input_element.send_keys(self.answer_list[index])
                input_element.submit()
                index+=1
        except:
            print("填写失败")
            exit()

    def auto_click_button(self):
        for item in self.select_list:
            buttons = self.driver.find_elements(By.XPATH, f"//span[text()='{item}']")
            print(buttons)
            for button in buttons:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # self.actions.click(button).perform()
                button.click()
            # buttons.click()
        
                
                




    def auto_submit_click_JSJ(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
        button = self.driver.find_element(By.CSS_SELECTOR,".ant-btn.ant-btn-primary.ant-btn-two-chinese-chars.form-theme--submit-button.published-form__submit.FooterButton_button__vJkWw")
        button.click()
        try:
            print("动作已经全部执行")
            time.sleep(1)
            if(self.is_submit()):
                print("成功抢到")
            else:
                print("没有抢到")
                
        except Exception as e:
            print(e)
            

    def __del__(self):
        self.driver.quit()

class AUTO_TX_FORM:
    info_data={}
    select_list=[]
    wait_time :str 
    answer_list=[]
    
    def __init__(self,url : str ):
        options = webdriver.EdgeOptions()
 
        # 处理SSL证书错误问题
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--guest")
        # 忽略无用的日志
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])   
        try:
            self.driver=webdriver.Edge(options)
        except:
            download_driver()
            self.driver=webdriver.Edge(options)
        self.actions = ActionChains(self.driver)
        try:
            self.driver.get(url)
        except:
            print("打开网页失败")
    
    
    
    def set_base_data(self,file_path :str):
        with open(file_path,"r",encoding="utf-8") as f:
            data=f.read()
            data=data.replace("，",",").replace("：",":")
            self.info_data=eval(data)
            
    
    def set_select_list(self):
        while(1):
            option=input("请输入你需要的勾选的选项(输入exit：退出)：")
            if(option=="exit"):
                return
            self.select_list.append(option)        
    
    
    def display_all_qus(self):
        print("问题列表")
        elements=self.driver.find_elements(By.CSS_SELECTOR, ".question")
        for element in elements:
            value=element.text.replace("\n","").replace(" ","").replace("*","")
            print(value)
        print("-----------------------------")
        return elements
        
    
    def is_login(self):
        """
        根据页面是否有"登录后才能填写"文本判断是否登录
        返回True或False
        """
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '登录后才能填写')]")
            return False
        except:
            return True
    
    
    def is_submit(self):
        """
        根据页面是否有"登录后才能填写"文本判断是否登录
        返回True或False
        """
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '已提交')]")
            return True    
        except:
            return False
    
    def is_shouji(self):
        try:
            self.driver.find_element(By.XPATH, "//*[contains(text(), '已暂停收集')]")
            return False    
        except:
            return True
    
    
    
    
    
    def wait_for_login(self):
        if(self.is_login==True):
            return
        else:
            os.system("cls")
            input("请登录后按回车键继续")
            self.driver.refresh()
            
            
           
    
    
    
    def get_questions_input(self):
        """获取表单的data-qid

        Args:
            driver (webdriver): selenium的webdriver

        Returns:
        elements
        """
        elements=self.driver.find_elements(By.CSS_SELECTOR, ".question[data-type='simple']")
        for element in elements:
            value=element.text.replace("\n","").replace(" ","").replace("*","")
            print(value)       
        return elements
    
    
    
    def get_questions_select(self):
        """获取表单的data-qid

        Args:
            driver (webdriver): selenium的webdriver

        Returns:
        elements
        """
        elements=self.driver.find_elements(By.CSS_SELECTOR, ".question[data-type='radio']")
        elements+=self.driver.find_elements(By.CSS_SELECTOR, ".question[data-type='checkbox']")
        for element in elements:
            value=element.text.replace("\n","").replace(" ","").replace("*","")
            print(value)
                   
        return elements
    
    
    def set_wait_time(self,input_time : str |None=""):
        if(input_time==""):
            input_time=input("请输入等待时间：")
        while(1):
            if(len(input_time)!=12):
                print("请输入正确的开抢时间")
                input_time=input("请输入等待时间：")
            else:
                break
        self.wait_time=input_time
        
    
    # def get_questions_with_select(self):
    #     elements=self.driver.find_elements(By.CSS_SELECTOR, ".question[data-type='radio']")
    #     elements+=self.driver.find_elements(By.CSS_SELECTOR, ".question[data-type='checkbox']")
    #     if(len(elements)==0):
    #         return []
    #     for element in elements:
    #         value=element.text.replace("\n","").replace(" ","").replace("*","")
    #         print(value)       
    #     return elements
    
    def wait_for_time(self,input_time : str |None=""): 
        """
        等待开抢
        :param input_time: 请输入正确的时间格式，例如：202405101328"
        :return: True
        """
        if(input_time=="" and self.wait_time=="" ):
            input_time=input("请输入等待时间：")
        elif(input_time=="" and self.wait_time!=""):
            input_time=self.wait_time
        
        # 当前时间
        try:
            # 将输入时间字符串转换为时间元组
            time_tuple = time.strptime(input_time, "%Y%m%d%H%M")
            # 将时间元组转换为时间戳
            start_timestamp  = time.mktime(time_tuple)
    
            if(start_timestamp<time.time()):
                print("收集表已经开始")
                return True
            
            cnt=0
            while(1):
                current_timestamp = time.time()
                current_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_timestamp))
                if(cnt%200000==0):
                    # os.system("cls")
                    print("正在等待当前时间为",current_time_str)
            
                if(current_timestamp >= start_timestamp-0.02):
                    self.driver.refresh()
                    return True
                # os.system("cls")
        except ValueError:
            print("输入时间格式不正确，请输入正确的时间格式，例如：202405101328") 
        
       
            
    def Initializes_the_answer_list(self):
        elements=self.get_questions_input()
        for element in elements:
            question=element.text.replace("\n","").replace(" ","")
            flag=0
            
            for item_key in self.info_data:
                if(re.search(item_key,question)):
                    self.answer_list.append(self.info_data[item_key])
                    print("依据初始数据输入",question,"data：",self.info_data[item_key])
                    flag=1
                    continue
            if(flag==1):
                continue    
            value=input("请输入简答题 "+question+":")
            self.answer_list.append(value)    
        print("-----------------------------")        
    
    def auto_input(self):
        """自动输入值到具有指定名称的输入框中。

        Args:
            INPUT_NAME (str): 输入框的名称
            val (str): 要输入的值
        """
        # data_qid="formlw0lalc7-SIMPLE1715339748648lw0kzwvc"
        
        try: 
            elements=self.get_questions_input()
            index=0
            for element in elements:
                data_qid=element.get_attribute("data-qid")
                css_path=f'[data-qid="{data_qid}"]  textarea'
                print(css_path)
                textarea = self.driver.find_element(By.CSS_SELECTOR, css_path)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", textarea)
                textarea.send_keys(self.answer_list[index])
                # blank_area = self.driver.find_element(By.CLASS_NAME, "form-root")
                # actions = ActionChains(self.driver)
                # actions.move_to_element(blank_area).click().perform()
                index+=1
        except:
            print("填写失败")
            exit()

    def auto_click_button(self):
        """_summary_

        Args:
            BUTTON_value (str): _description_
        """
        # for item in self.select_list:
        #     button=self.driver.find_element(By.XPATH,f"//span[text()='{item}']")
        #     self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        #     button.click() 
        for item in self.select_list:
            buttons = self.driver.find_elements(By.XPATH, f"//span[text()='{item}']")
            for button in buttons:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                button.click()




    def auto_submit_click_tx(self):
        """_summary_

        Args:
            BUTTON_ID (str): Button_1
        """
        blank_area = self.driver.find_element(By.CLASS_NAME, "form-header-title-content")
        self.actions.move_to_element(blank_area).click().perform()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")   
        button=self.driver.find_element(By.XPATH,"//button[text()='提交']")
        button.click()
        try:
            # wait = WebDriverWait(driver, 10)  # 最长等待时间为10秒
            # element = wait.until(EC.presence_of_element_located((By.XPATH,"//div[text()='确定']")))
            time.sleep(0.03)
            button2 = self.driver.find_element(By.CSS_SELECTOR,"button.dui-button.dui-modal-footer-ok")
            button2.click()
            print("动作已经全部执行")
            if(self.is_submit()):
                print("成功抢到")
        except Exception as e:
            print(e)
            
    def __del__(self):
        self.driver.quit()
        
        
class AuTotask_TX:
    def __init__(self,url,data_path,start_time,is_enable=True,SELECT_LIST=[]) -> None:
        """初始化

        Args:
            url (str): 收集表地址
            data_path (str): 数据地址
            start_time (str): 开始时间 格式为202405121200 年月日时分(注意补零).
            is_enable (bool, optional): 是否提前输入需要选择内容 Defaults to True.
            SELECT_LIST (list, optional): 需要选择的内容. Defaults to [] 如["1","2"].
            
            
            1.data.txt 格式要求
            {
                    "学号姓名":"",
                    "手机号":"",
                    "邮箱":"",
                    "班级":"",
                    "学院":"",
                    "name":"value"
            }        
            
        """
        self.url=url
        self.data_path=data_path
        self.start_time=start_time
        self.is_enable=is_enable
        if(is_enable==False):
            self.SELECT_LIST=SELECT_LIST

    def run(self):
        self.AT1.wait_for_time()
        self.AT1.auto_input()
        self.AT1.auto_click_button()
        self.AT1.auto_submit_click_tx()
        
    def init(self):
        self.AT1=AUTO_TX_FORM(self.url)
        self.AT1.set_wait_time(input_time=self.start_time)
        self.AT1.wait_for_login()
        self.AT1.set_base_data(self.data_path)
        if(self.is_enable==False):
            self.AT1.select_list+=self.SELECT_LIST
        self.AT1.display_all_qus()
        self.AT1.Initializes_the_answer_list()
        if(self.AT1.get_questions_select()!=[]):
            self.AT1.set_select_list()
        current_timestamp = time.time()
        time_tuple = time.strptime(self.start_time, "%Y%m%d%H%M")
        # 将时间元组转换为时间戳
        start_timestamp  = time.mktime(time_tuple)
        print("任务初始化完成")
        if(current_timestamp < start_timestamp-8):
            print("---------------------")
            print("进入等待时间(5s)，请确认输入结果")
            print("input信息：",self.AT1.answer_list)
            print("select信息：",self.AT1.select_list)
            time.sleep(5)
            
    def start(self):
        self.init()
        self.run()        
    
    
    
    
               
class AuTotask_JSJ: 
    """

    """
    def __init__(self,url :str,data_path :str,start_time: str,is_enable=True,SELECT_LIST=[]) -> None:
        """初始化
        Args:
            url (str): 收集表地址
            data_path (str): 数据地址
            start_time (str): 开始时间 格式为202405121200 年月日时分(注意补零).
            is_enable (bool, optional): 是否提前输入需要选择内容 Defaults to True.
            SELECT_LIST (list, optional): 需要选择的内容. Defaults to [] 如["1","2"].
            
            1.data.txt 格式要求
            {
                    "学号姓名":"",
                    "手机号":"",
                    "邮箱":"",
                    "班级":"",
                    "学院":"",
                    "name":"value"
            }    
            
        """
        self.url=url
        self.data_path=data_path
        self.start_time=start_time
        self.is_enable=is_enable
        if(is_enable==False):
            self.SELECT_LIST=SELECT_LIST
    def run(self):
        self.AJ1.wait_for_time()
        self.AJ1.auto_input()
        self.AJ1.auto_click_button()
        self.AJ1.auto_submit_click_JSJ()
        
    def init(self):
        self.AJ1=AUTO_JSJ_FORM(self.url)
        time.sleep(1)
        self.AJ1.set_wait_time(input_time=self.start_time)
        self.AJ1.set_base_data(self.data_path)
        if(self.is_enable==False):
            self.AJ1.select_list+=self.SELECT_LIST
        self.AJ1.display_all_qus()
        self.AJ1.Initializes_the_answer_list()
        if(self.AJ1.get_questions_select()!=[] and self.is_enable):
            self.AJ1.set_select_list()
        current_timestamp = time.time()
        time_tuple = time.strptime(self.start_time, "%Y%m%d%H%M")
        start_timestamp  = time.mktime(time_tuple)
        print("任务初始化完成")
        if(current_timestamp < start_timestamp-8):
            print("---------------------")
            print("进入等待时间(5s)，请确认输入结果")
            print("input信息：",self.AJ1.answer_list)
            print("select信息：",self.AJ1.select_list)
            time.sleep(5)
                
    def start(self):
        self.init()
        self.run()
    
from concurrent.futures import ThreadPoolExecutor

class ATThreadPool:
    def __init__(self, tasks):
        self.tasks = tasks

    def run(self):
        with ThreadPoolExecutor() as executor:
            executor.map(self.execute_task, self.tasks)

    def execute_task(self, task):
        task.init()
        task.run()
        
        
        
               
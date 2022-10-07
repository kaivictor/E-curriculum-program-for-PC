from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import maskpass
from lxml import etree


class WebAnalysis():
    def __init__(self):
        pass
        # self.driver = webdriver.Edge()  # Edge浏览器

    def Load(self):
        self.driver = webdriver.Edge()
        while True:
            教务系统url = 'http://jwnew.cqust.edu.cn/eams/login.action?cqustadminweb=1'
            self.driver.get(教务系统url)
            time.sleep(2)
            账号=input("请输入您的学号-")
            self.driver.find_element(By.XPATH,"//*[@id='username']").send_keys(账号)
            密码 = maskpass.askpass(prompt="请输入账户密码-")
            self.driver.find_element(By.XPATH,"//*[@id='password']").send_keys(密码)
            self.driver.find_element(By.XPATH,"//*[@id='login_text']/table/tbody/tr[4]/td[2]/input[1]").click()
            time.sleep(2)
            now_url = self.driver.current_url
            if now_url == 'http://jwnew.cqust.edu.cn/eams/home.action':
                print("-登录成功-")
                break
            else:
                print("-登录失败-\n-请重新登录-")
                pass
        #数据获取
        #课表url = 'http://jwnew.cqust.edu.cn/eams/courseTableForStd!courseTable.action'
        time.sleep(0.1)
        self.driver.find_element(By.XPATH,"//*[@id='menu_panel']/ul/li[3]/a").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,"//*[@id='menu_panel']/ul/li[3]/ul/div/li[4]/a").click()
        time.sleep(1)
        with open("Html.tmp", 'w') as f:
            f.write(self.driver.page_source)
            f.close()
        print("-已保存课程表信息-")
        self.driver.quit()
    
    def 课程安排分析(self):
        HtmlText=open("Html.tmp",'r').read()
        html = etree.HTML(HtmlText)

        课程大纲数=int(html.xpath("//*[@id='grid12042826912_data']/tr[11]/td[1]/text()")[0])
        print("你一共有{}门课".format(课程大纲数))
        课程安排={}
        for 序号 in range (1,课程大纲数+1):
            课程详情={}
            课程详情['课程代号']=(html.xpath("//*[@id='grid12042826912_data']/tr[{}]/td[2]/a/text()".format(序号)))
            课程详情['课程名称']=(html.xpath("//*[@id='grid12042826912_data']/tr[{}]/td[3]/text()".format(序号)))
            课程详情['课程学分']=(html.xpath("//*[@id='grid12042826912_data']/tr[{}]/td[4]/text()".format(序号)))
            课程详情['课程学班']=(html.xpath("//*[@id='grid12042826912_data']/tr[{}]/td[5]/text()".format(序号)))
            课程详情['课程教师']=(html.xpath("//*[@id='grid12042826912_data']/tr[{}]/td[6]/text()".format(序号)))
            课程详情['课程起始周']=(html.xpath("//*[@id='grid12042826912_data']/tr[{}]/td[7]/text()".format(序号)))
            #print(课程详情)
            课程安排['%d'%序号]=课程详情
        print("-课程安排分析完成-")
        with open ("ClassInfo.tmp", 'w') as f:
            f.write(str(课程安排))
            f.close()
        return 课程安排

    def 课程详情处理(self,课程,课程数):
        课程详情3={}
        #print(课程,课程数)
        if 课程[课程数]:  # 如果这个有课就处理
            课程详情1=课程[课程数][0].split(';')
            #print(课程详情1)
            for 课程叠加数 in range (0,len(课程详情1),2):
                #print(课程详情1[课程叠加数])
                #print(课程详情1[课程叠加数+1])
                课程详情2={}
                课程老师与名称,课程时间与地点=课程详情1[课程叠加数],课程详情1[课程叠加数+1]
                课程详情2['课程老师'],课程名称与课程代码=课程老师与名称.split(' ')
                课程详情2['课程名称'],课程代码=课程名称与课程代码.split('(')
                课程详情2['课程代码']=课程代码[0:-1]
                print(课程时间与地点)
                if ',' in 课程时间与地点:
                    课程周,课程地点=课程时间与地点[1:-1].split(',')
                else:
                    课程周,课程地点=课程时间与地点[1:-1],'未知'
                课程详情2['起始周']=课程周
                课程详情2['课程地点']=课程地点
                #print('课{}'.format(课程叠加数),str(课程详情2))
                课程详情3['课{}'.format(int(课程叠加数/2+1))]=课程详情2
                #return 课程详情3
            #print(课程详情3)
            return 课程详情3

    def 所有课程(self):
        HtmlText=open("Html.tmp", 'r').read()
        #print(HtmlText)
        html = etree.HTML(HtmlText)

        课节时间原式 = html.xpath("//*[@id='manualArrangeCourseTable']/tbody/tr/td[1]/text()")
        课节时间=[]
        #第一节时间 = html.xpath("//*[@id='TD0_0']/@title")
        for 时间 in 课节时间原式:
            时间=时间.replace("\n\t\t    \t\t","")
            时间=时间.replace("\n\t\t\t\t","")
            if 时间 != '':
                课节时间.append(时间)
        #print(课节时间,"一天课程数目 ",len(课节时间))
        课程={}
        for 课程数 in range(1,(7*len(课节时间)+1)):
            #print(课程数)
            课程[课程数]=html.xpath("//*[@id='TD{}_0']/@title".format(int(课程数-1)))
        print(课程)
        # 课程解析
        global 星期课程详情
        星期课程详情={}
        for 课程数 in range(1,(7*len(课节时间)+1),2):
            课程详情3=self.课程详情处理(课程,课程数)
            星期课程详情['第{}节'.format(课程数)]=课程详情3
            星期课程详情['第{}节'.format(课程数+1)]=课程详情3
            #print(星期课程详情)
        print("-识别结束-")
        with open ("ClassInfo.txt", 'w') as f:
            f.write(str(星期课程详情))
            f.close()
        return 星期课程详情



if __name__ == '__main__':
    A = WebAnalysis()
    # A.Load()
    # A.课程安排分析()
    A.所有课程()

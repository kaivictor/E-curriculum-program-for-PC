import tkinter
import math
import ast
import tkinter.ttk
import yaml
import os


class Prepare():
    def __init__(self):  # -> None:
        self.ClassInfoListFileName = 'ClassInfoList.txt'
        self.NumberOfOoursesPerDay = 12

    def GetClassInfoList(self):
        self.ClassInfoDict = open('ClassInfo.txt', 'r').read()
        self.ClassInfoDict = ast.literal_eval(self.ClassInfoDict)

    def GetLiveWeek(self, LessonInfo):
        LiveWeek = LessonInfo['起始周']
        Begin, End = LiveWeek.split('-')
        return (int(Begin), int(End))

    def GetCourselocation(self, NumberOfOourses, NumberOfOoursesPerDay):
        Courselocation = []
        Week = math.ceil(NumberOfOourses/NumberOfOoursesPerDay)
        ClassLesson = (NumberOfOourses % NumberOfOoursesPerDay)
        if ClassLesson == 0:
            ClassLesson = NumberOfOoursesPerDay
        Courselocation.append((Week, ClassLesson))
        return Courselocation

    def ShareClassInfoList(self, WeekNeed):
        ShareClassInfoWeekList = []
        ClassNumber = 84
        for Number in range(1, ClassNumber+1):
            ClassInfo = self.ClassInfoDict['第%d节' % Number]
            if ClassInfo is not None:
                for NumberOfOverlaps in range(1, len(ClassInfo)+1):
                    OverlapCourses = ClassInfo['课%d' % NumberOfOverlaps]
                    print(OverlapCourses)
                    if WeekNeed in range((self.GetLiveWeek(OverlapCourses))[0], (self.GetLiveWeek(OverlapCourses))[1]+1):
                        # print('课程{} 满足周 {}'.format(OverlapCourses['课程名称'], Week))
                        for Location in self.GetCourselocation(Number, self.NumberOfOoursesPerDay):
                            print("第{}周 第{}节  在周{} 第{}节 {}".format(WeekNeed, Number, Location[0], Location[1], str(OverlapCourses)))
                            LessonInfo = '{}\n{}\n{}\n{}\n{}' .format(OverlapCourses['课程代码'],
                                 OverlapCourses['课程名称'], OverlapCourses['课程老师'], OverlapCourses['起始周'],
                                 OverlapCourses['课程地点'])
                            ShareClassInfo = ((Location[0],Location[1]), LessonInfo)
                            ShareClassInfoWeekList.append(ShareClassInfo)
        return ShareClassInfoWeekList


class GUI():
    def __init__(self,UIName):  # -> None:
        # super().__init__()
        self.WeekList = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        self.WindowName = UIName
        self.LessonNumDay = 12
        self.WeekNum = 13
        self.WeekNumList = []
        for WeekNum in range(1, self.WeekNum+1):
            self.WeekNumList.append('第{}周'.format(WeekNum))

    def CreatUI(self):
        self.UI = tkinter.Tk('Schedule')
        self.UI.title('重庆科技学院智能工程与科技学院 课程表 未加载完全')
        self.WindowWidth, self.WindowHeight = 600, 700
        self.UI.geometry('{}x{}'.format(self.WindowWidth, self.WindowHeight))
        self.UI.iconbitmap('cquestlogo.ico')
        self.UI.bind('<Configure>', self.UISizeUpdate)
        # print(self.WindowName)
    
    def UISizeUpdate(self, event=None):
        print('Run')
        self.WeekLabel['width'] = self.FrameWidth
        self.ClassNumLabel['width'] = self.FrameWidth
        self.ClassNumLabel['height'] = self.FrameHeight
        self.CreateFrame()
        # self.InfoUpdate()

    def CreateFrame(self):
        WeekList = self.WeekList
        WeekList.insert(0, '     ')
        self.FrameWidth = round((self.WindowWidth/10/len(self.WeekList))+1)
        self.FrameHeight = round((self.WindowHeight/20/self.LessonNumDay))
        for LabelName in WeekList:
            WeekLabelFrame = tkinter.Frame(self.UI, width=80)
            col = self.WeekList.index(LabelName)
            WeekLabelFrame.grid(row=0, column=col)
            self.WeekLabel = tkinter.Label(WeekLabelFrame, text=LabelName, width=10, font=('楷体', 12))
            self.WeekLabel['width'] = self.FrameWidth
            self.WeekLabel.grid()
        for NumName in range(0, self.LessonNumDay):
            NumNameFrame = tkinter.Frame(self.UI)
            NumNameFrame.grid(row=NumName+1, column=0)
            NumText = '第{}节'.format(NumName+1)
            self.ClassNumLabel = tkinter.Label(NumNameFrame, text=NumText, width=10, font=('楷体', 12))
            self.ClassNumLabel['width'] = self.FrameWidth
            self.ClassNumLabel['height'] = self.FrameHeight
            self.ClassNumLabel.grid()

    def FillSchedule(self, ClassInfoList):
        self.ClassInfoFrame = []
        for ClassInfo in ClassInfoList:
            Location = ClassInfo[0]
            ClassInfoFrame = tkinter.Frame(self.UI)
            self.ClassInfoFrame.append(ClassInfoFrame)
            ClassInfoFrame.grid(column=Location[0], row=Location[1])
            ClassInfoMain = ClassInfo[1]
            ClassInfoLabel = tkinter.Label(ClassInfoFrame, text=ClassInfoMain, font=('楷体', 6))
            ClassInfoLabel['width'] = self.FrameWidth*2
            ClassInfoLabel['height'] = self.FrameHeight*2
            ClassInfoLabel.grid()
        self.UI.title('重庆科技学院智能工程与科技学院 课程表')
   
    def Output(self, Modle=1):
        # Word = ['test1', 'test2', 'test3', 'test4']
        print("功能正在开发")

    def AddMenu(self):
        self.UIMenu = tkinter.Menu(self.UI, tearoff=0)
        StartMenu = tkinter.Menu(self.UI, tearoff=0)
        StartMenu.add_command(label="刷新", command=self.InfoUpdate)
        StartMenu.add_command(label="导入", command=self.Output)
        StartMenu.add_command(label="退出", command=self.UI.quit)
        StartMenu.add_separator()
        SetMenu = tkinter.Menu(self.UI, tearoff=0)
        SetMenu.add_command(label="课表设置", command=self.Output)
        SetMenu.add_command(label="界面设置", command=self.Output)
        SetMenu.add_separator()
        self.UIMenu.add_cascade(label="开始", menu=StartMenu)
        self.UIMenu.add_cascade(label="设置", menu=SetMenu)
        self.UIMenu.add_cascade(label="关于")
        self.UIMenu.add_separator()
        self.UI.config(menu=self.UIMenu)

    def InfoUpdate(self, what=''):
        Week = self.SetWeek.get()
        N = Prepare()
        N.GetClassInfoList()
        if self.SetSave(1) is not False and what == '1':
            Week = self.SetSave(1)['需要周']
            self.SetWeek.set(Week)
        elif what != '1':
            for Frame in self.ClassInfoFrame:
                Frame.destroy()
        WeekNeed = self.WeekNumList.index(Week)
        Re = N.ShareClassInfoList(WeekNeed+1)
        self.FillSchedule(Re)
        self.SetSave(0)

    def WeekChoose(self):
        self.SetWeek = tkinter.StringVar()
        self.UIComboBox = tkinter.ttk.Combobox(self.UI, textvariable=self.SetWeek,
         value=self.WeekNumList, width=self.FrameWidth, justify='center')
        self.UIComboBox.configure(state="readonly")
        self.UIComboBox.current(3)
        self.UIComboBox.grid(column=0, row=0)
        self.UIComboBox.bind("<<ComboboxSelected>>", self.InfoUpdate)

    def SetSave(self, Modle):
        yaml_path = os.path.abspath(".")
        yaml_path = os.path.join(yaml_path, "config.yaml")
        if Modle == 0:  # 意味着保存
            yamlInfo = {}
            yamlInfo['需要周'] = self.SetWeek.get()
            yamlInfo['课程信息'] = '课程表信息.txt'
            yamlInfo['账号'] = ''
            yamlInfo['密码'] = '需要加密'
            file = open(yaml_path, 'w', encoding='utf-8')
            yaml.dump(yamlInfo, file)
            file.close()
        elif Modle == 1:
            if os.path.exists(yaml_path) and open(yaml_path).read() != '':
                file = open(yaml_path, 'r', encoding="utf-8")
                file_data = file.read()
                file.close()
                data = yaml.safe_load(file_data)
                return data
            else:
                return False

    def Mainloop(self):
        self.UI.mainloop()


if __name__ == '__main__':
    '''N = Prepare()
    N.GetClassInfoList()
    Re = N.ShareClassInfoList(3)
    print(Re)'''
    M = GUI('1')
    M.CreatUI()
    M.CreateFrame()
    M.WeekChoose()
    # M.FillSchedule('')
    M.AddMenu()
    M.InfoUpdate('1')
    M.Mainloop()
    M.SetSave(1)


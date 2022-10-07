from GUI2 import*
from GetClassInfo import*
import warnings


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    base_path = os.path.abspath(".")
    base_path = os.path.join(base_path, "ClassInfo.txt")
    if os.path.exists(base_path):
        pass
    else:
        A = WebAnalysis()
        A.Load()
        # A.课程安排分析()
        A.所有课程()
    M = GUI('1')
    M.CreatUI()
    M.CreateFrame()
    M.WeekChoose()
    # M.FillSchedule('')
    M.AddMenu()
    M.InfoUpdate('1')
    M.Mainloop()
    M.SetSave(1)
    '''课程时间 系统通知 程序调动 请求头调用 Windows日历同步
    企业微信日程同步 Todo同步 图片导出 日历文件导出 微信公众号服务'''
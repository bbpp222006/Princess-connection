import uiautomator2 as u2
import time
from utils import *
from cv import *
import matplotlib.pylab as plt

class Automator:
    def __init__(self, auto_task=False, auto_policy=True,
                 auto_goods=False, speedup=True):
        """
        device: 如果是 USB 连接，则为 adb devices 的返回结果；如果是模拟器，则为模拟器的控制 URL 。
        """
        self.d = u2.connect()
        self.dWidth, self.dHeight = self.d.window_size()
        self.appRunning = False
        self.auto_task = auto_task
        self.auto_policy = auto_policy
        self.auto_goods = auto_goods
        self.loot_speedup = speedup


    def start(self):
        """
        启动脚本，请确保已进入游戏页面。
        """
        while True:
            # 判断jgm进程是否在前台, 最多等待20秒，否则唤醒到前台
            if self.d.app_wait("com.bilibili.priconne", front=True, timeout=1):
                if not self.appRunning:
                    # 从后台换到前台，留一点反应时间
                    time.sleep(1)
                self.appRunning = True
                break
            else:
                self.app = self.d.session("com.bilibili.priconne")
                self.appRunning = False
                continue

    def login(self,ac,pwd):
        while True:
            if self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_id_welcome_change").exists(timeout=0.1):
                self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_id_welcome_change").click(timeout=0.1)
            if self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_edit_username_login").exists(timeout=0.1):
                self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_edit_username_login").click(timeout=0.1)
                break
            else:
                self.d.click(self.dWidth * 0.965, self.dHeight * 0.029)
        self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_edit_username_login").click()
        self.d.clear_text()
        self.d.send_keys(str(ac))
        self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_edit_password_login").click()
        self.d.clear_text()
        self.d.send_keys(str(pwd))
        self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_buttonLogin").click()
        time.sleep(1)
        if self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_edit_authentication_name").exists(timeout=0.1):
            return 1#说明要进行认证
        else:
            return 0#正常

    def auth(self,auth_name, auth_id):
        self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_edit_authentication_name").click()
        self.d.clear_text()
        self.d.send_keys(str(auth_name))
        self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_edit_authentication_id_number").click()
        self.d.clear_text()
        self.d.send_keys(str(auth_id))
        self.d(resourceId="com.bilibili.priconne:id/bsgamesdk_authentication_submit").click()
        self.d(resourceId="com.bilibili.priconne:id/bagamesdk_auth_success_comfirm").click()


    def get_butt_stat(self,screen_shot,template_paths,threshold=0.85):
        #此函数输入要判断的图片path,屏幕截图, 返回大于阈值的path,坐标字典, 阈值默认为0.9
        # template_paths = ['img/dengji.jpg']
        return_dic = {}
        zhongxings, max_vals = UIMatcher.findpic(screen_shot, template_paths=template_paths)
        for i, name in enumerate(template_paths):
            print(name + '--' + str(round(max_vals[i], 3)), end=' ')
            if max_vals[i]>threshold:
                return_dic[name]=(zhongxings[i][0] *self.dWidth, zhongxings[i][1] * self.dHeight)
        print('')
        return return_dic


    def guochang(self,screen_shot,template_paths,suiji = 1):
        #输入截图, 模板list, 得到下一次操作, 返回值:0正常, 1没找到, 2特殊标记

        out_flag = 0
        self.dWidth, self.dHeight = self.d.window_size()
        time.sleep(0.1)
        screen_shot = screen_shot
        template_paths = template_paths
        active_path = self.get_butt_stat(screen_shot,template_paths)
        if active_path:
            print(active_path)
            print('当前分辨率',self.dWidth, self.dHeight)
            if 'img/caidan_tiaoguo.jpg'in active_path:
                x,y = active_path['img/caidan_tiaoguo.jpg']
                self.d.click(x, y)
            # if 'img/baoshigoumai.jpg'in active_path:
            #     print('宝石不足,跳出循环')
            #     out_flag = 2
            else:
                for name, (x,y) in active_path.items():
                    print(name)
                    self.d.click(x, y)
        else:
            if suiji:
                print('未找到所需的按钮,将点击左上角')
                self.d.click( 0.1*self.dWidth,  0.1*self.dHeight)
            else:
                print('未找到所需的按钮,无动作')
            out_flag = 1

        return out_flag


    def jiaoxue(self,screen_shot):
        x,y = UIMatcher.find_gaoliang(screen_shot)
        try:
            self.d.click(x*self.dWidth,y*self.dHeight+20)

        except:
            pass

    def get_screen_state(self,screen):
        # screen = UIMatcher.RotateClockWise90(screen)
        gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        ret, binary = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
        num_of_white = len(np.argwhere(binary == 255))
        active_path = self.get_butt_stat(screen, ['img/kuaijin.jpg','img/shouye.jpg','img/baoshigoumai.jpg','img/kuaijin_1.jpg'])


        if 'img/baoshigoumai.jpg' in active_path:
            return 'baoshigoumai'

        if 'img/shouye.jpg' in active_path:
            return 'shouye'

        if 'img/kuaijin.jpg' in active_path or'img/kuaijin_1.jpg'in active_path:
            return 'zhandou'

        if num_of_white<50000:
            return 'dark'
        else:
            return 0


    def zhandou(self):
        #此函数在进入战斗后调用, 会一直运行直到战斗结束.
        print('尝试跳过战斗')
        screen_shot = self.d.screenshot(format="opencv")
        a.guochang(screen_shot, ['img/caidan.jpg'])
        time.sleep(0.5)
        screen_shot = self.d.screenshot(format="opencv")
        active_path = self.get_butt_stat(screen_shot, ['img/ok.jpg'])
        if 'img/ok.jpg' in active_path:
            x,y = active_path['img/ok.jpg']
            print('可以跳过')
            self.d.click(x, y)
            return 0
        self.d.click( 0.1*self.dWidth,  0.1*self.dHeight)

        active_path = self.get_butt_stat(screen_shot, ['img/kuaijin.jpg'])
        if 'img/kuaijin.jpg' in active_path:
            time.sleep(0.5)
            self.d.click(912, 496)
        ok_time = 0

        while True:
            time.sleep(0.1)
            screen_shot = self.d.screenshot(format="opencv")
            active_path = self.get_butt_stat(screen_shot, ['img/zhandou_ok.jpg','img/xiayibu.jpg'])
            if 'img/zhandou_ok.jpg' in active_path:
                x, y = active_path['img/zhandou_ok.jpg']
                self.d.click(x, y)
                ok_time+=1
            if 'img/xiayibu.jpg' in active_path:
                x, y = active_path['img/xiayibu.jpg']
                self.d.click(x, y)
                ok_time += 1

            if ok_time>=3:
                active_path = self.get_butt_stat(screen_shot, ['img/zhandou_ok.jpg', 'img/xiayibu.jpg'])
                if 'img/zhandou_ok.jpg' in active_path:
                    x, y = active_path['img/zhandou_ok.jpg']
                    self.d.click(x, y)
                if 'img/xiayibu.jpg' in active_path:
                    x, y = active_path['img/xiayibu.jpg']
                    self.d.click(x, y)
                print('战斗应该结束了. 跳出循环')
                break









plt.ion()
fig, ax = plt.subplots(1)
plt.show()

a = Automator()
a.start()
def login_auth(ac,pwd):
    need_auth = a.login(ac=ac,pwd=pwd)
    if need_auth:
        auth_name,auth_id = random_name(), CreatIDnum()
        a.auth(auth_name =auth_name ,auth_id = auth_id)

def init_acc():
    while True:

        screen_shot = a.d.screenshot(format="opencv")
        state_flag = a.get_screen_state(screen_shot)

        if state_flag=='dark':
            print('画面变暗,尝试进入引导模式点击')
            screen_shot = a.d.screenshot(format="opencv")
            a.jiaoxue(screen_shot)

        elif state_flag=='zhandou':
            print('侦测到加速按钮, 进入战斗模式')
            a.zhandou()
        elif state_flag=='shouye':
            print('恭喜完成所有教学内容, 跳出循环')
            break
        else:
            template_paths = ['img/tiaoguo.jpg', 'img/ok.jpg','img/xiayibu.jpg', 'img/caidan.jpg', 'img/caidan_yuan.jpg',
                                      'img/caidan_tiaoguo.jpg', 'img/dengji.jpg','img/tongyi.jpg','img/niudan_jiasu.jpg']
            a.guochang(screen_shot,template_paths)
        time.sleep(0.5)


def shouqu():

    active_list = ['img/guanbi.jpg','img/liwu.jpg','img/quanbushouqu.jpg',
                   'img/ok.jpg','img/zhandou_ok.jpg','img/quxiao.jpg']
    for active in active_list:
        screen_shot = a.d.screenshot(format="opencv")
        a.guochang(screen_shot, [active],suiji=0)
        time.sleep(1)

def niudan():
    a.d.click(751,505)
    time.sleep(1)
    while True:
        time.sleep(1)
        active_list = ['img/ok.jpg','img/niudan_jiasu.jpg','img/zaicichouqu.jpg','img/shilian.jpg']
        screen_shot = a.d.screenshot(format="opencv")
        a.guochang(screen_shot,active_list, suiji=1)
        screen_shot_ = a.d.screenshot(format="opencv")
        state_flag = a.get_screen_state(screen_shot_)
        if state_flag == 'baoshigoumai':
            print('没钱了, 关闭')
            a.d.click(373, 370)
            break

def write_log(account, pwd):
    time.sleep(1)
    a.d.click(209, 519)
    time.sleep(1)
    a.d.click(659, 30)
    time.sleep(1)
    a.d.click(728, 142)
    time.sleep(1)
    a.d.click(588, 481)
    time.sleep(1)

    base_path = 'img/touxiang/'
    touxiang_path_list = []
    for touxiang_path in os.listdir(base_path):
        touxiang_path_list.append(base_path+touxiang_path)
    print(touxiang_path_list)
    screen_shot = a.d.screenshot(format="opencv")
    exist_list = a.get_butt_stat(screen_shot, touxiang_path_list)
    print(exist_list)
    st = ''
    for i in exist_list:
        st = st + str(os.path.basename(i).split('.')[0]) + ','
    with open('jieguo.txt', 'a') as f:
        f.write(account+'\t'+ pwd+'\t'+st+'\n')

def change_acc():
    time.sleep(1)
    a.d.click(871, 513)
    time.sleep(1)
    a.d.click(165, 411)
    time.sleep(1)
    a.d.click(591, 369)
    time.sleep(1)


account_dic = {}

with open('zhanghao.txt','r') as f:
    for i,line in enumerate(f):
        if i<0:  #这里可以控制从哪里开始读
            continue
        account,password = line.split('\t')[0:2]
        account_dic[account]=password
print(account_dic)

for account in account_dic:
    print(account, account_dic[account])
    login_auth(account, account_dic[account])
    init_acc()
    shouqu()
    niudan()
    write_log(account, account_dic[account])
    change_acc()

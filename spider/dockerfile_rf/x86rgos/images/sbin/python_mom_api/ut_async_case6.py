from rg_global import RgGlobal
from rg_mom import RgMom
from rg_mom_common import Db
import rg_mom_common
import os
import time
from rg_thread import RgThreadMaster

# from rg_obj.mom.test import app_demo
import rg_obj.mom_test as app_demo

# pexpire老化
# 设置1.5秒老化，然后分别在1.4、1.6秒get数据

class App(RgMom):
    def __init__(self, glb):
        super(App, self).__init__(glb)  # 模板
        glb.regist_app(self)  # 模板
        self.thread_master = RgThreadMaster(glb)

        self.demo = app_demo.Demo()
        self.demo.index = app_demo.DemoIndex()
        self.demo.index.index1 = 'async'
        self.demo.index.index2 = 'case6'

    def on_initialized(self, privdata):
        self.delete(Db.RGMOMD_HOST, self.demo)

        self.demo.index.index1 = 'a'
        self.demo.index.index2 = '1'
        self.set(Db.RGMOMD_HOST, self.demo)
        self.demo.index.index2 = '2'
        self.set(Db.RGMOMD_HOST, self.demo)
        self.demo.index.index2 = '3'
        self.set(Db.RGMOMD_HOST, self.demo)

        self.demo.index.index1 = 'b'
        self.demo.index.index2 = '1'
        self.set(Db.RGMOMD_HOST, self.demo)

        self.demo.index.index1 = 'a'
        self.pexpire(Db.RGMOMD_HOST, self.demo, 5, 1.5, None)

    def on_pexpire_mom_test_Demo(self, msg, privdata):
        self.flag = 0
        def timer_cb(t):
            if t.arg == '1.4':
                self.demo.index.index1 = 'a'
                self.demo.index.index2 = '1'
                self.get(Db.RGMOMD_HOST, self.demo, 'a, exist')
                self.demo.index.index1 = 'b'
                self.demo.index.index2 = '1'
                self.get(Db.RGMOMD_HOST, self.demo, 'b, exist')
            elif t.arg == '1.6':
                self.demo.index.index1 = 'a'
                self.demo.index.index2 = '1'
                self.get(Db.RGMOMD_HOST, self.demo, 'a, not exist')
                self.demo.index.index1 = 'b'
                self.demo.index.index2 = '1'
                self.get(Db.RGMOMD_HOST, self.demo, 'b, exist')

        self.thread_master.add_timer(timer_cb, '1.4', 1.4)
        self.thread_master.add_timer(timer_cb, '1.6', 1.6)

    def on_get_mom_test_Demo(self, msg, privdata):
        self.flag += 1
        if privdata == 'a, exist':
            demo = app_demo.Demo(msg.value)
            if demo.index.index1 != 'a' or demo.index.index2 != '1':
                print("ASYNC_CASE_6: FAULT")
                os._exit(1)
        elif privdata == 'b':
            demo = app_demo.Demo(msg.value)
            if demo.index.index1 != 'b' or demo.index.index2 != '1':
                print("ASYNC_CASE_6: FAULT")
                os._exit(1)
        elif privdata == 'a, not exist':
            if msg.value != 0:
                print("ASYNC_CASE_6: FAULT")
                os._exit(1)
        elif privdata == 'b, not exist':
            if msg.value != 0:
                print("ASYNC_CASE_6: FAULT")
                os._exit(1)

        if self.flag == 4:
            print("ASYNC_CASE_6: PASS")
            os._exit(0)

def main():
    glb = RgGlobal('py_async_case5')
    glb.connect(Db.RGMOMD_HOST, None)
    app = App(glb)
    glb.run()

if __name__ == '__main__':
    main()

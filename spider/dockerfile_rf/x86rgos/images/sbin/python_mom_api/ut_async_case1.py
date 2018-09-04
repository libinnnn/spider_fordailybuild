from rg_global import RgGlobal
from rg_mom import RgMom
from rg_mom_common import Db
import rg_mom_common

import os
import time

# from rg_obj.mom.test import app_demo
import rg_obj.mom_test as app_demo

class App(RgMom):
    def __init__(self, glb):
        super(App, self).__init__(glb)  # 模板
        glb.regist_app(self)  # 模板

        self.demo = app_demo.Demo()
        self.demo.index = app_demo.DemoIndex()
        self.demo.index.index1 = 'async'
        self.demo.index.index2 = 'case1'

    def on_initialized(self, privdata):
        self.main()

    def main(self):
        self.demo.v1 = 3.1415
        self.demo.v2 = 1.1234

        self.set(Db.RGMOMD_HOST, self.demo)
        self.get(Db.RGMOMD_HOST, self.demo, None)

    def on_get_mom_test_Demo(self, msg, privdata):
        demo = app_demo.Demo(msg.value)
        if demo.v1 == 3.1415 and demo.v2 == 1.1234:
            print("ASYNC_CASE1: PASS")
            os._exit(0)
        else:
            print("ASYNC_CASE1: FAULT")
            os._exit(1)

def main():
    glb = RgGlobal('py_async_case1')
    glb.connect(Db.RGMOMD_HOST, None)
    app = App(glb)
    glb.run()

if __name__ == '__main__':
    main()

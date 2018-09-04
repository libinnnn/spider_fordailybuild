from rg_global import RgGlobal
from rg_mom import RgMom
from rg_mom_common import Db
import rg_mom_common
import os

# from rg_obj.mom.test import app_demo
import rg_obj.mom_test as app_demo

# hmupdate对于不存在的key无效

class App(RgMom):
    def __init__(self, glb):
        super(App, self).__init__(glb)  # 模板
        glb.regist_app(self)  # 模板

        self.demo = app_demo.Demo()
        self.demo.index = app_demo.DemoIndex()
        self.demo.index.index1 = 'async'
        self.demo.index.index2 = 'case4'

    def on_initialized(self, privdata):
        self.delete(Db.RGMOMD_HOST, self.demo)

        self.demo.v1 = 3.1415
        self.demo.v2 = 1.1234
        self.demo.v3 = 1234
        self.demo.v4 = 5678
        self.hmupdate(Db.RGMOMD_HOST, self.demo, [6, 7, 8, 9])
        self.hgetall(Db.RGMOMD_HOST, self.demo, None)

    def on_hgetall_mom_test_Demo(self, msg, privdata):
        res = rg_mom_common.HashResult(msg.value)
        if res.field_tag == []:
            print("ASYNC_CASE4: PASS")
            os._exit(0)
        else:
            print("ASYNC_CASE4: FAULT")
            os._exit(1)

def main():
    glb = RgGlobal('py_async_case4')
    glb.connect(Db.RGMOMD_HOST, None)
    app = App(glb)
    glb.run()

if __name__ == '__main__':
    main()

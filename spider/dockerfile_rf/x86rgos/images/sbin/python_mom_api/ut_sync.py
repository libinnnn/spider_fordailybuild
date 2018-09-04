import sys
import unittest
import rg_global
import rg_mom_sync
from rg_mom_common import Db
from rg_mom_common import Cmd
import rg_mom_common

# from rg_obj.mom.test import app_demo
import rg_obj.mom_test as app_demo


class TestSingleObj(unittest.TestCase):
    # 测试只需要用到一个obj的接口

    def setUp(self):
        self.glb = rg_global.RgGlobal('sync_demo')
        if self.glb.connect_sync(Db.RGMOMD_HOST) != 0:
            sys.exit()
        self.db = Db.RGMOMD_HOST
        self.mom = rg_mom_sync.RgMomSync(self.glb)
        self.demo = app_demo.Demo()
        self.demo.index = app_demo.DemoIndex()
        self.demo.index.index1 = '111'
        self.demo.index.index2 = '222'

    def tearDown(self):
        self.mom.delete(self.db, self.demo, 1)
        self.assertEqual(self.mom.get(self.db, self.demo), None)

    def test_base(self):
        # 先保证set、get、delete接口是正确的，因为其余的用例基本都要用这两个接口辅助判断
        demo = app_demo.Demo()
        demo.index = app_demo.DemoIndex()
        demo.index.index1 = '111'
        demo.index.index2 = '222'

        # 当前无数据
        demo2 = self.mom.get(self.db, demo)
        self.assertEqual(demo2, None)

        # set数据，get后正确
        demo.v1 = 3.1415
        self.mom.set(self.db, demo, 1)
        demo2 = self.mom.get(self.db, demo)
        self.assertEqual(demo2.index.index1, '111')
        self.assertEqual(demo2.index.index2, '222')
        self.assertEqual(demo2.v1, 3.1415)

        # delete删除数据
        self.mom.delete(self.db, demo, 1)
        demo2 = self.mom.get(self.db, demo)
        self.assertEqual(demo2, None)

    def test_hmset(self):
        self.demo.v1 = 3.1415
        self.demo.v3 = 1234

        self.mom.hmset(self.db, self.demo, [6, 8], 1)

        demo, _, _ = self.mom.hgetall(self.db, self.demo)
        assert(demo.v1 == 3.1415)
        assert(demo.v3 == 1234)

    def test_scan(self):
        def cb(msg, privdata):
            self.assertEqual(privdata, 'this is privdata')
            self.assertEqual(msg.cmd, Cmd.SET)
            demo = app_demo.Demo(msg.value)
            self.assertEqual(demo.v1, 3.1415)

        self.demo.v1 = 3.1415
        self.mom.set(self.db, self.demo, 1)
        self.mom.scan(self.db, self.demo, 0, cb, 'this is privdata')

    def test_pexpire(self):
        import time
        self.mom.set(self.db, self.demo, 1)
        self.mom.pexpire(self.db, self.demo, 0, 1)
        time.sleep(1.5)
        ret = self.mom.get(self.db, self.demo)
        self.assertEqual(ret, None)

    # def test_flushdb(self):
    #     self.mom.set(self.db, self.demo, 1)
    #     ret = self.mom.get(self.db, self.demo)
    #     self.assertNotEqual(ret, None)
    #     self.mom.flushdb(self.db)
    #     ret = self.mom.get(self.db, self.demo)
    #     self.assertEqual(ret, None)

    def test_exists(self):
        ret = self.mom.exists(self.db, self.demo)
        self.assertEqual(ret, 1)
        self.mom.set(self.db, self.demo, 1)
        ret = self.mom.exists(self.db, self.demo)
        self.assertEqual(ret, 0)


class TestMultiObj(unittest.TestCase):

    def setUp(self):
        self.glb = rg_global.RgGlobal('sync_demo')
        if self.glb.connect_sync(Db.RGMOMD_HOST) != 0:
            sys.exit()
        self.db = Db.RGMOMD_HOST
        self.mom = rg_mom_sync.RgMomSync(self.glb)

    def test_sadd(self):
        demo = app_demo.Demo()
        demo.index = app_demo.DemoIndex()
        demo.index.index1 = 's'
        demo.index.index2 = 's'
        for i in range(5):
            demo.v3 = i
            self.mom.sadd(self.db, demo, 1)
        for i in range(5):
            demo.v3 = i
            ret = self.mom.scard(self.db, demo)
            self.assertEqual(ret, 5)
            ret = self.mom.sismember(self.db, demo)
            self.assertEqual(ret, 0)
    
        demo.v3 = 2
        self.mom.srem(self.db, demo, 1)
        ret = self.mom.scard(self.db, demo)
        self.assertEqual(ret, 4)
        ret = self.mom.sismember(self.db, demo)
        self.assertEqual(ret, 1)


if __name__ == '__main__':
    unittest.main()

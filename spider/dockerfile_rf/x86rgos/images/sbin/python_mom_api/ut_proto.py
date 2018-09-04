import unittest
import rg_global
import rg_mom_sync
from rg_mom_common import Db

# from rg_obj.mom.test import case1
# from rg_obj.mom.test import case2
# from rg_obj.mom.test import case3
# from rg_obj.mom.test import case4
# from rg_obj.mom.test import case5
# from rg_obj.mom.test import case5_other

from rg_obj import mom_test
from rg_obj import mom_test2
case1 = mom_test
case2 = mom_test
case3 = mom_test
case4 = mom_test
case5 = mom_test
case5_other = mom_test

class TestBaseType(unittest.TestCase):

    def setUp(self):
        self.db = Db.RGMOMD_HOST
        self.glb = rg_global.RgGlobal('py_proto_ut')
        if self.glb.connect_sync(Db.RGMOMD_HOST) != 0:
            sys.exit()
        self.mom = rg_mom_sync.RgMomSync(self.glb)

    def tearDown(self):
        msg = case1.Msg1()
        msg.index = case1.Key1()
        msg.index.key = '111'
        self.mom.delete(self.db, msg, 1)

    def test_int(self):
        msg = case1.Msg1()
        msg.index = case1.Key1()
        msg.index.key = '111'
        msg.i32 = 123

        self.mom.set(self.db, msg, flag = 1)
        msg2 = self.mom.get(self.db, msg)

        self.assertEqual(msg2.i32, 123)

    def test_string(self):
        msg = case1.Msg1()
        msg.index = case1.Key1()
        msg.index.key = '111'
        msg.s = '222'
        
        self.mom.set(self.db, msg, flag = 1)
        msg2 = self.mom.get(self.db, msg)

        self.assertEqual(msg2.s, '222')

    def test_msg(self):
        msg = case1.Msg1()
        msg.index = case1.Key1()
        msg.index.key = '111'

        self.mom.set(self.db, msg, flag = 1)
        msg2 = self.mom.get(self.db, msg)

        self.assertEqual(msg2.index.key, '111')


class TestRepeated(unittest.TestCase):

    def setUp(self):
        self.db = Db.RGMOMD_HOST
        self.glb = rg_global.RgGlobal('py_proto_ut')
        self.glb.connect_sync(Db.RGMOMD_HOST)
        self.mom = rg_mom_sync.RgMomSync(self.glb)

    def tearDown(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'
        self.mom.delete(self.db, msg)

    def test_ri32(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'

        msg.ri32.add()
        msg.ri32.add()
        msg.ri32[0] = 123
        msg.ri32[1] = 456

        self.mom.set(self.db, msg, flag = 1)
        msg2 = self.mom.get(self.db, msg)

        self.assertEqual(msg2.ri32, [123, 456])

    def test_rd(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'

        msg.rd.add()
        msg.rd.add()
        self.assertEqual(len(msg.rd), 2)
        msg.rd[0] = 3.1415
        msg.rd[1] = 2.12345678
        self.assertEqual(msg.rd, [3.1415, 2.12345678])

        self.mom.set(self.db, msg, flag = 1)
        msg2 = self.mom.get(self.db, msg)

        self.assertEqual(msg2.rd, [3.1415, 2.12345678])

    def test_rf(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'

        msg.rf.add()
        msg.rf.add()
        msg.rf[0] = 3.1415
        msg.rf[1] = 2.123456
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.rf, [3.1415, 2.123456])

    def test_rb(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'

        msg.rb.add()
        msg.rb.add()
        msg.rb[0] = True
        msg.rb[1] = False
        self.assertEqual(msg.rb, [True, False])
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.rb, [True, False])

    def test_rs(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'

        msg.rs.add()
        msg.rs.add()
        msg.rs[0] = 'aaa'
        msg.rs[1] = 'bbb'
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.rs, ['aaa', 'bbb'])

    def test_rbytes(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'

        msg.rbytes.add()
        msg.rbytes.add()
        msg.rbytes[0] = b'aaa'
        msg.rbytes[1] = b'bbb'
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.rbytes, [b'aaa', b'bbb'])

    def test_rkey(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'

        msg.rkey.add()
        msg.rkey.add()
        msg.rkey[0].key = '111'
        msg.rkey[1].key = '222'
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.rkey[0].key, '111')
        self.assertEqual(msg2.rkey[1].key, '222')

    def test_error(self):
        msg = case2.Msg2()
        msg.index = case2.Key2()
        msg.index.key = '111'

        with self.assertRaises(IndexError):
            msg.ri32[0]
        msg.ri32.add()
        msg.ri32[0]
        self.assertEqual(len(msg.ri32), 1)


class TestEnum(unittest.TestCase):

    def setUp(self):
        self.db = Db.RGMOMD_HOST
        self.glb = rg_global.RgGlobal('py_proto_ut')
        self.glb.connect_sync(Db.RGMOMD_HOST)
        self.mom = rg_mom_sync.RgMomSync(self.glb)

    def tearDown(self):
        msg = case3.Msg3()
        msg.index = case3.Key3()
        msg.index.key = '111'
        self.mom.delete(self.db, msg)

    def test_enum(self):
        msg = case3.Msg3()
        msg.index = case3.Key3()
        msg.index.key = '111'

        msg.t1 = case3.BBB
        msg.t2 = case3.Msg3.FFF
        self.mom.set(self.db, msg, flag = 1)
        msg2 = self.mom.get(self.db, msg)

        self.assertEqual(msg2.t1, case3.BBB)
        self.assertEqual(msg2.t2, case3.Msg3.FFF)
        self.assertEqual(case3.AAA, 0)
        self.assertEqual(case3.BBB, 1)
        self.assertEqual(case3.CCC, 2)
        self.assertEqual(case3.DDD, 3)
        self.assertEqual(case3.Msg3.EEE, 0)
        self.assertEqual(case3.Msg3.FFF, 1)


class TestOneof(unittest.TestCase):

    def setUp(self):
        self.db = Db.RGMOMD_HOST
        self.glb = rg_global.RgGlobal('py_proto_ut')
        self.glb.connect_sync(Db.RGMOMD_HOST)
        self.mom = rg_mom_sync.RgMomSync(self.glb)

    def tearDown(self):
        msg = case4.Msg4()
        msg.index = case4.Key4()
        msg.index.key = '111'
        self.mom.delete(self.db, msg)

    def test_oneof1(self):
        msg = case4.Msg4()
        msg.index = case4.Key4()
        msg.index.key = '111'

        msg.ipv4 = 1234
        self.assertEqual(msg.ipv4, 1234)
        self.assertEqual(msg.ipv6, b'')
        msg.ipv6 = b'112233'
        self.assertEqual(msg.ipv4, 0)
        self.assertEqual(msg.ipv6, b'112233')

        msg.o1 = case4.Oneof1()
        self.assertEqual(msg.o2, None)
        msg.o2 = case4.Oneof2()
        self.assertEqual(msg.o1, None)

    def test_oneof2(self):
        msg = case4.Msg4()
        msg.index = case4.Key4()
        msg.index.key = '111'

        msg.ipv4 = 1234
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.ipv4, 1234)
        self.assertEqual(msg2.ipv6, b'')

    def test_oneof3(self):
        msg = case4.Msg4()
        msg.index = case4.Key4()
        msg.index.key = '111'

        msg.ipv6 = b'112233'
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.ipv4, 0)
        self.assertEqual(msg2.ipv6, b'112233')

    def test_oneof4(self):
        msg = case4.Msg4()
        msg.index = case4.Key4()
        msg.index.key = '111'

        msg.o2 = case4.Oneof2()
        msg.o2.s = 'abcd'
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.o1, None)
        self.assertEqual(msg2.o2.s, 'abcd')


class TestPkg(unittest.TestCase):

    def setUp(self):
        self.db = Db.RGMOMD_HOST
        self.glb = rg_global.RgGlobal('py_proto_ut')
        self.glb.connect_sync(Db.RGMOMD_HOST)
        self.mom = rg_mom_sync.RgMomSync(self.glb)

    def tearDown(self):
        msg = case5.Msg5()
        msg.index = case5.Key5()
        msg.index.key = '111'
        self.mom.delete(self.db, msg)

    def test_pkg(self):
        msg = case5.Msg5()
        msg.index = case5.Key5()
        msg.index.key = '111'

        msg.other = case5_other.Msg5Other()
        msg.other.i32 = 123
        msg.other.s = 'aabbcc'
        msg.other2 = mom_test2.Msg5Other()
        msg.other2.i32 = 456
        msg.other2.s = 'eeffgg'
        self.mom.set(self.db, msg, flag = 1)

        msg2 = self.mom.get(self.db, msg)
        self.assertEqual(msg2.other.i32, 123)
        self.assertEqual(msg2.other.s, 'aabbcc')
        self.assertEqual(msg2.other2.i32, 456)
        self.assertEqual(msg2.other2.s, 'eeffgg')


if __name__ == '__main__':
    unittest.main()

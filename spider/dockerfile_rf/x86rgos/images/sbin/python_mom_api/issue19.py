import rg_global
import rg_mom_sync
import rg_mom_common
import rg_thread
import os

import rg_obj.mom_test as mom_test

def main():
    glb = rg_global.RgGlobal('sync_demo')
    glb.connect_sync(rg_mom_common.Db.RGMOMD_HOST)
    mom = rg_mom_sync.RgMomSync(glb)
    master = rg_thread.RgThreadMaster(glb)

    demo = mom_test.Demo()
    demo.index = mom_test.DemoIndex()
    demo.index.index1 = '111'
    demo.index.index2 = '111'
    demo.v1 = 1.111
    ret = mom.lpop(rg_mom_common.Db.RGMOMD_HOST, demo)
    assert(ret == None)
    ret = mom.rpop(rg_mom_common.Db.RGMOMD_HOST, demo)
    assert(ret == None)

    mom.lpush(rg_mom_common.Db.RGMOMD_HOST, demo, 1)
    mom.lpush(rg_mom_common.Db.RGMOMD_HOST, demo, 1)
    ret = mom.lpop(rg_mom_common.Db.RGMOMD_HOST, demo)
    assert(ret != None)
    ret = mom.rpop(rg_mom_common.Db.RGMOMD_HOST, demo)
    assert(ret != None)

    ret, _, _ = mom.hgetall(rg_mom_common.Db.RGMOMD_HOST, demo)
    assert(ret == None)
    ret, _, _ = mom.hmget(rg_mom_common.Db.RGMOMD_HOST, demo, [6, 7])
    assert(ret == None)


    def cb(t):
        os._exit(0)

    master.add_timer(cb, None, 1)
    glb.run()

if __name__ == '__main__':
    main()

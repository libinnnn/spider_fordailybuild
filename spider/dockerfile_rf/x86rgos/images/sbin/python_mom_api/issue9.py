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
    mom.lpush(rg_mom_common.Db.RGMOMD_HOST, demo, 1)

    demo2 = mom_test.Demo()
    demo2.index = mom_test.DemoIndex()
    demo2.index.index1 = '111'
    demo2.index.index2 = '111'
    demo2.v1 = 2.222

    # 不应该报入参错误
    mom.linsert(rg_mom_common.Db.RGMOMD_HOST, demo, demo2, 1)

    def cb(t):
        os._exit(0)

    master.add_timer(cb, None, 1)
    glb.run()

if __name__ == '__main__':
    main()

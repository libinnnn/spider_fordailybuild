#! /bin/bash

downlooad_dir=${PWD}
image_namm=image.tar.bz2

[ -z $1 ] && echo "please input the URL of images."
[ ! -z $1 ] && wget  -c $1 || exit 1
[ -z $2 ] && echo "please input images name."

git config --global user.name "libin3"
git config --global user.email "libin3@ruijie.com.cn"
git clone ssh://libin3@gerrit.ruijie.work:29418/momlib-python && scp -p -P 29418 libin3@gerrit.ruijie.work:hooks/commit-msg momlib-python/.git/hooks/

wget http://rcode.ruijie.work/x86rgos.tar
tar xvf $downlooad_dir/x86rgos.tar
rm $downlooad_dir/x86rgos.tar

wget http://rcode.ruijie.work/site-packages.tar
tar xvf $downlooad_dir/site-packages.tar
rm $downlooad_dir/site-packages.tar

tar -xvf $downlooad_dir/$image_namm

MOM_LIB_LIST="libcallfun.so  libzct.so libzformat.so librg_unity.so libsyslog_new.so libpsh_common.so libpsh_essence.so libxml2.so \
librg-thread.so libhiredis.so libras_common.so librg_at.so libjson-c.so librg_mom_impl.so libpsh.so librg_mom.so libzlog.so libprotobuf-c.so libzlog.so.1.2 \
libjson-c.so.2 libjson-c.so.2.0.1"

cd $downlooad_dir/images/rootfs/lib/ && cp -f $MOM_LIB_LIST $downlooad_dir/x86rgos/images/lib

MOM_SBIN_LIST="redis-cli redis-server rgmomd  ham-init"
cd $downlooad_dir/images/rootfs/sbin/ && cp -f $MOM_SBIN_LIST $downlooad_dir/x86rgos/images/sbin

MOM_PYTHON_list="rg_mom.so rg_mom_sync.so rg_thread.so rg_mom_common.so rg_global.so"
cd $downlooad_dir/images/rootfs/bin/lib/python3.4/ && cp -f $MOM_PYTHON_list  $downlooad_dir/site-packages


MOM_ETC_REDIS_LIST="redis.conf"
cd $downlooad_dir/images/rootfs/etc/redis/ && cp -f $MOM_ETC_REDIS_LIST $downlooad_dir/x86rgos/images/etc/redisg

MOM_ETC_RGMOM_LIST="mom_client_conf.json"
cd $downlooad_dir/images/rootfs/etc/rg_mom/ && cp -f $MOM_ETC_RGMOM_LIST $downlooad_dir/x86rgos/images/etc/rg_mom

MOM_ETC_ZLOG_LIST="rg_mom_client.conf rgmomd.conf"
cd $downlooad_dir/images/rootfs/etc/zlog/  && cp -f $MOM_ETC_ZLOG_LIST $downlooad_dir/x86rgos/images/etc/zlog

rm -rf $downlooad_dir/images
rm -f $downlooad_dir/$image_namm
echo replaceMOM finish

#execute dockerfile and push to repoistory
imagesname=$2
cd $downlooad_dir && docker build -t ${imagesname} .
docker tag ${imagesname} 172.18.34.10:5000/${imagesname}
docker push 172.18.34.10:5000/${imagesname}
docker rmi -f 172.18.34.10:5000/${imagesname}


cd .. && rm -rf ./dockerfile_rf/x86rgos \
&& rm -rf ./dockerfile_rf/site-packages \
&& mv ./dockerfile_rf_and_mom/x86rgos  ./dockerfile_rf \
&& mv ./dockerfile_rf_and_mom/site-packages ./dockerfile_rf \
&& rm -rf ./dockerfile_mom/momlib-python \
&& mv ./dockerfile_rf_and_mom/momlib-python ./dockerfile_mom



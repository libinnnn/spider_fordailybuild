#! /bin/bash

downlooad_dir=${PWD}
[ -z $1 ] && echo "please input images name."

git config --global user.name "libin3"
git config --global user.email "libin3@ruijie.com.cn"
git clone ssh://libin3@gerrit.ruijie.work:29418/momlib-python && scp -p -P 29418 libin3@gerrit.ruijie.work:hooks/commit-msg momlib-python/.git/hooks/

#execute dockerfile and push to repoistory
imagesname=$1
cd $downlooad_dir && docker build -t ${imagesname} .
docker tag ${imagesname} 172.18.34.10:5000/${imagesname}
docker push 172.18.34.10:5000/${imagesname}
docker rmi -f 172.18.34.10:5000/${imagesname}

cd .. && rm -rf ./dockerfile_mom/momlib-python && mv ./dockerfile_rf/momlib-python ./dockerfile_mom


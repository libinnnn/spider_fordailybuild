# -*- coding: utf-8 -*-
import requests
import re
import json
import os
import spider.spider_tools
import logging



if __name__ == '__main__':

        show = spider.spider_tools.show

        show.init_log("logoutput.log")
        #这边不需要添加cookie，后续的get访问中将cookie保存下来即可
        Request_Headers_cas = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer' : 'https://sso.ruijie.net:8443/cas/login?service=http%3A%2F%2Fbuild.ruijie.net%3A8080%2Fngcf_build%2Fservlet%2F12index',
        'Connection' : 'keep-alive',
        'Host' : 'sso.ruijie.net:8443',
        'Origin' : 'https://sso.ruijie.net:8443',
        'Upgrade-Insecure-Requests' : '1',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Cache-Control' : 'max-age=1000',
        'Content-Length' : '67'
        }


        #第一次通过get取得页面的lt参数，加入post当中，用于请求cas取回ticket
        url_to_cas = "https://sso.ruijie.net:8443/cas/login?service=http%3A%2F%2Fbuild.ruijie.net%3A8080%2Fngcf_build%2Fservlet%2FdailyBuildMain"
        response = requests.get(url_to_cas,verify=False)
        cookie = response.cookies
        list = re.findall(u'(?<=name="lt" value=").*?(?=" />)',response.text)
        lt = list.pop(0)

        Form_Data_cas = {
                'username': 'libin3',
                'password': '20122013wW',
                'lt': lt,
                '_eventId': 'submit',
                'submit': ''
        }
        res_firstpost = requests.post(url=url_to_cas, headers=Request_Headers_cas, data=Form_Data_cas,cookies=cookie, allow_redirects=False, verify=False)
        cookie=res_firstpost.cookies
        show.show_print("firstpost headers:"+res_firstpost.headers.__str__())

        url_with_ticket=res_firstpost.headers.get('Location')
        show.show_print("url_with_ticket:"+url_with_ticket)
        Request_Headers_dest = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Connection': 'keep-alive',
                'host': 'build.ruijie.net:8080',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                #'Upgrade-Insecure-Requests:': '1'
        }
        #创建session，用于保持会话请求
        s=requests.session()

        #向带有ticket的url路径发送get请求返回的url中携带jsessionid参数
        res_firstget=s.get(url_with_ticket,headers=Request_Headers_dest,verify=False)
        if str(res_firstget.status_code) != '200':
                print("error occurs in ticket")
                logging.error('error occurs in ticket')
                exit(1)
        show.show_print("firstget url:"+res_firstget.url)
        cookie = res_firstget.cookies

        #获取jsessionid，以后访问cookie中携带可被系统识别
        jsessionid = re.search('build/servlet/dailyBuildMain;(.*)',res_firstget.url).group(1)
        print(jsessionid)

        #携带jsessionid的cookie可以直接向访问的网址发送get请求
        res_secondget = s.get(res_firstget.url, cookies=cookie,verify=False)#使用的url路径中需要携带jession,get请求在url路径中携带参数
        cookie = res_secondget.cookies
        show.show_print("res_secondget url:"+res_secondget.url)
        #print(res_secondget.text)
        url_to_dailybuild='http://build.ruijie.net:8080/ngcf_build/servlet/dailyBuild'
        form_data_forsearch = {
                'start' : '0',
                'limit' : '15',
                'type' : 'query',
                'queryBean.treeName' : 'git-rgosm-project',
                'queryBean.branchName' : 'org_rgos',
                'queryBean.product' : 'rgos_x86',
                'queryBean.buildTypeId' : 'A',
                'queryBean.buildType' : '完整编译',
                'queryBean.buildDate' : '',
                'queryBean.queryStartTime' : '',
                'queryBean.queryEndTime' : '',
                'queryBean.result' : '[success]',
                'queryBean.errorMsg' : '',
                'queryBean.taskAttr' : '',
                'queryBean.owner' : '',
                'queryBean.sort:' : 'id',
                'queryBean.dir' : 'desc',
                'queryBean.start:' : '0',
                'queryBean.limit' : '15'
        }
        Reques_Headers_forsearch = {
                'Accept': '*/*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                'Referer': 'http://build.ruijie.net:8080/ngcf_build/servlet/initBuild?type=daily_build_query&project=git-rgosm-project',
                'Connection': 'keep-alive',
                'Host': 'build.ruijie.net:8080',
                'Origin': 'http://build.ruijie.net:8080',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'X-Requested-With' : 'XMLHttpRequest',
                'Content-Length' : '427'
        }

        #向服务器请求我们需要的数据并且以json格式返回
        res_secondpost=s.post(url_to_dailybuild,headers=Reques_Headers_forsearch,data=form_data_forsearch,allow_redirects=False,verify=False)
        if str(res_secondpost.status_code) != '200':
                print("error occurs in search")
                logging.error('error occurs in search')
                exit(1)


        #返回的json数据格式化，并且提取我们需要的location信息
        hjson = json.loads(res_secondpost.text)
        list = hjson['list']
        if list != None:
            list_dict = list[0]
            outputUrl = list_dict['outputUrl']
            print(outputUrl)
        else:
            print("list is none")
            logging.warning("list is none")
            exit(1)
        #将字符串进行拼接得到我们需要的下载路径
        des_url = re.search(r'.*(?=-)',outputUrl).group(0)
        version_url = des_url + "-%5bdef%5d/rgos_info/rootfs/version"
        image_url = des_url + "-%5bdef%5d/image.tar.bz2"
        print(version_url)

        #下载文件到本地路径
        with open("version", "wb") as file:
            # get request
            response = requests.get(version_url)
            # write to file
            file.write(response.content)
            file.close()

        #读取文件相关信息并解析
        with open("version", "rb") as file:
                content = file.read()
                #print(content)
                number = re.search(r'(?<=rg-mom-header http://svn.ruijie.net/ssvn12/ppf_libpub/rg-mom/trunk/code version ).*?(?=\\nrg)',content.__str__()).group(0)
                print(number)
                file.close()

        #判断mom是否更新
        if os.path.exists('./rg-mom-header_version') == False:
                with open("rg-mom-header_version", "w+") as file:
                        file.write(number)
                        file.close()
                        tag_mom = "0"
        else:
                with open("rg-mom-header_version", "r") as file:
                        content = file.read().__str__()
                        if number == content:
                                print("same")
                                file.close()
                                tag_mom = "0"
                        else:
                                with open("rg-mom-header_version", "w+") as file_new:
                                        print(content)
                                        print("different")
                                        file_new.write(number)
                                        file_new.close()
                                        file.close()
                                        tag_mom = "1"

        #判断RF是否更新并置tag
        if os.path.exists('./RF_tag') == False:
                with open("./RF_tag", "w+") as file:
                        file.write("0")
                        file.close()
                        tag_rf = "0"
        else:
                with open("./RF_tag", "r") as file:
                        tag = file.read()
                        if tag == "0":
                                tag_rf = "0"
                                file.close()
                        if tag == "1":
                                tag_rf = "1"
                                with open("./RF_tag", "w+") as file_new:
                                        file_new.write("0")
                                        file_new.close()
                                        file.close()
        print(tag_mom)
        print(tag_rf)
        show.buildImages(tag_rf,tag_mom,image_url)

















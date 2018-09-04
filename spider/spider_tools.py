# -*- coding: utf-8 -*-
import logging
import os
import time
class show:
    '''
    used to show
    '''
    def show_print(text):
        print("---------************------------")
        print(text)
        print("---------************------------")
        print("  ")

    '''
    get image version
    '''
    def get_version():
        if os.path.exists('./image_versionNumber') == False:
            with open('./image_versionNumber', 'w+') as file:
                version_number = "1"
                file.write(version_number)
                file.close()
                return "robotframework:V" + version_number
        else:
            with open('./image_versionNumber', 'r') as file:
                version_number = file.read()
                file.close()
                a = int(version_number)
                a = a + 1
                version_number = str(a)
                with open('./image_versionNumber', 'w+') as file:
                    file.write(version_number)
                    file.close()
                return "robotframework:V" + version_number

    '''
    define log pattern and how to oupput
    '''
    def init_log(logFilename):
        ''''' Output log to file and console '''
        # Define a Handler and set a format which output to file
        logging.basicConfig(
            level=logging.DEBUG,  # 定义输出到文件的log级别，大于此级别的都被输出
            format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
            datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
            filename=logFilename,  # log文件名
            filemode='w+')  # 写入模式“w”或“a”
        # Define a Handler and set a format which output to console
        console = logging.StreamHandler()  # 定义console handler
        console.setLevel(logging.INFO)  # 定义该handler级别
        formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
        console.setFormatter(formatter)
        # Create an instance
        logging.getLogger().addHandler(console)  # 实例化添加handler

    '''
    get version for RF
     pattern such as v1.0.0
    '''
    def get_version_rf():
        if os.path.exists('./rf_version') == False:
            with open('./rf_version','w+') as file:
                file.write("100")
                file.close()
                return "1.0.0"
        else:
            with open('./rf_version','r') as file:
                version = file.read()
                number = int(version) + 1
                number = str(number)
                file.close()
                with open('./rf_version','w+') as file:
                    file.write(number)
                    file.close()
                a = int(number) // 100 % 10
                b = int(number) // 10 % 10
                c = int(number) % 10
                str_version = str(a) + '.' + str(b) +'.' +str(c)
                return str_version

    '''
    execute shell to build images according to tags
    '''
    def buildImages(tag_rf,tag_mom,url):
        if tag_rf == "1" and tag_mom == "1":
            t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            with open('./mom_version', 'w+') as file:
                file.write(str(t))
                file.close()
            imagename = "robotframeworktestcase:" + "v" + show.get_version_rf() + "_" + str(t)
            os.system("cd ./dockerfile_rf_and_mom && sh updateMOMRF.sh" + " " + url + " " + imagename)
            logging.info("update mom and rf")
        elif tag_rf == "0" and tag_mom == "1":
            if os.path.exists('./rf_version') == False:
                with open('rf_version', 'w+') as file:
                    file.write("100")
                    file.close()
            with open('rf_version','r') as file:
                rf_version = file.read()
                a = int(rf_version) // 100 % 10
                b = int(rf_version) // 10 % 10
                c = int(rf_version) % 10
                str_version = str(a) + '.' + str(b) + '.' + str(c)
                file.close()
            t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            with open('./mom_version', 'w+') as file:
                file.write(str(t))
                file.close()
            imagename = "robotframeworktestcase:" + "v" + str_version + "_" + str(t)
            os.system("cd ./dockerfile_mom && sh updateMOM.sh" + " " + url + " "  + imagename)
            logging.info("update mom")
        elif tag_rf == "1" and tag_mom == "0":
            if os.path.exists('./mom_version') == False:
                with open('./mom_version','w+') as file:
                    t = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                    file.write(str(t))
                    file.close()
            with open('./mom_version', 'r') as file:
                mom_version = file.read()
                file.close()
            imagename = "robotframeworktestcase:" + "v" + show.get_version_rf() + "_" + mom_version
            os.system("cd ./dockerfile_rf && sh updateRF.sh" + " " + imagename)
            logging.info("update rf")
        else:
            logging.info("update None")
            exit(0)





import re
import xml.dom.minidom
import os
import pickle


class 文件处理:
    @staticmethod
    def 获得目录下所有文件(目录地址, 后缀名要求=''):
        所有文件 = os.listdir(目录地址)
        所有文件地址 = []
        for 一个文件 in 所有文件:
            if 后缀名要求 != '' and 后缀名要求 + ':' not in 一个文件 + ':':
                continue  # 非该后缀名去除
            所有文件地址.append(os.path.join(目录地址, 一个文件))
        return 所有文件地址

    @staticmethod
    def 读取整个文件到字符串(文件地址, 编码='utf-8', 返回文件大小=False):
        打开 = open(文件地址, encoding=编码)
        读取 = 打开.read()
        打开.close()
        if 返回文件大小:
            文件大小 = os.path.getsize(文件地址)
            return (读取, 文件大小)
        return 读取

    @staticmethod
    def 保存列表或字典(保存对象, 保存地址, 强制当字典=False):
        '''

        :param 保存对象: 一维列表、二维列表、字典,其中列表的第一个不不能是空
        :param 保存地址:
        :return:
        '''
        是列表 = isinstance(保存对象, list)
        是字典 = isinstance(保存对象, dict)
        if not (是列表 or 是字典):
            return False
        # 创建目录
        地址层级 = '/'.join(保存地址.split('/')[:-1])
        if 地址层级 != '' and not os.path.exists(地址层级):
            os.makedirs(地址层级)
        缓冲 = 10 ** 4
        if 是列表 and not 强制当字典:
            if len(保存对象) == 0:
                return False
            是二维列表 = isinstance(保存对象[0], list)
            if 是二维列表:
                写入列表 = ['\t'.join([str(i) for i in 一个列表]) for 一个列表 in 保存对象]
            else:
                写入列表 = 保存对象
            写入 = open(保存地址, 'w', encoding='utf-8')
            写入内容 = [str(i) for i in 写入列表]
            for i in range(0, len(写入内容), 缓冲):
                写入.write('\r\n'.join(写入内容[i:i + 缓冲]) + '\r\n')
            写入.close()
            return True
        else:
            二进制 = pickle.dumps(保存对象)
            with open(保存地址, 'wb') as 写入:
                for i in range(0, len(二进制), 缓冲):
                    写入.write(二进制[i:i + 缓冲])
            return True

    @staticmethod
    def 读取列表或字典(是列表, 读取地址, 列表_哪几列是整型=[]):
        if 是列表:
            读取 = open(读取地址, encoding='utf-8')
            数据 = 读取.readlines()
            读取.close()
            列表 = []
            # 去换行
            for 一行 in 数据:
                列表.append(一行[:-1])
            # 如果是二维列表
            是二维列表 = len(列表[0].split('\t')) > 1
            if 是二维列表:
                for i in range(len(列表)):
                    列表[i] = 列表[i].split('\t')
            # 数字列还原
            for 是数字的列 in 列表_哪几列是整型:
                if not 是二维列表 and 是数字的列 != 0:
                    continue
                if not 是二维列表 and 是数字的列 == 0:
                    for i in range(len(列表)):
                        列表[i] = int(列表[i])
                    continue
                for i in range(len(列表)):
                    列表[i][是数字的列] = int(列表[i][是数字的列])
            return 列表
        else:
            读取 = open(读取地址, 'rb')
            字典 = pickle.load(读取)
            读取.close()
            return 字典


class FileProcess:
    @staticmethod
    def writeObject(anObject, outputAddress):
        cache = 10 ** 4
        binary = pickle.dumps(anObject)
        with open(outputAddress, 'wb') as w:
            for i in range(0, len(binary), cache):
                w.write(binary[i:i + cache])

    @staticmethod
    def readObject(inputAddress):
        r = open(inputAddress, 'rb')
        anObject = pickle.load(r)
        r.close()
        return anObject

    @staticmethod
    def insertToModifyFileName(text, filePath, head=False):
        path, extension = os.path.splitext(filePath)
        fatherPath, name = os.path.split(path)
        if head:
            return fatherPath + os.sep + text + name + extension
        else:
            return fatherPath + os.sep + name + text + extension


class FolderProcess:
    @staticmethod
    def createFolder(folderAddress):
        if folderAddress != '' and not os.path.exists(folderAddress):
            os.makedirs(folderAddress)
            return True
        else:
            return False

    @staticmethod
    def deleteAllFile(folderAddress, notDelete=lambda fileName: False):
        allFileName = os.listdir(folderAddress)
        deleteNum = 0
        for fileName in allFileName:
            if not notDelete:
                os.remove(folderAddress + os.sep + fileName)
                deleteNum += 1
        return deleteNum


class xml解析:
    @staticmethod
    def 获取相同层级内的所有内容(xml树, 层级列表, 只取第一个=True, 所有内容=[], 异常情况=[], 递归层次=0):
        '''
        获取某种层级内的所有内容为列表
        :param xml树: 要求<class 'xml.dom.minidom.Element'>格式
        :param 层级列表: ['第一层名称',...] or ['第一层名称',...,['多底层1',...]],单底层或多底层
        :param 只取第一个: 是否在最后一层只取第一个
        :param 其他变量: 无需填写
        :return 所有内容: ['',...] or [['',...],...] 最底层内的所有内容,单底层和多底层
        :return 异常情况: [[0],...,[0,0]],和层级列表长度相同。第i个数值为n,代表有n个第i-1层级没有第i层级,异常情况[-1][0]也是如此;
        异常情况[-1][1]的数字代表有几个 最低层级个数的超过1的情况。
        '''
        if len(异常情况) <= 递归层次:
            if len(层级列表) - 1 == len(异常情况):
                异常情况.append([0, 0])
            else:
                异常情况.append([0])
        # 第i-1层级没有第i层级
        if len(层级列表) - 1 == 递归层次:  # 到了最底层
            底层xml树集合 = []
            多最低层级 = isinstance(层级列表[递归层次], list)
            # 多最低层级同时提取
            if 多最低层级 == True:
                for 第i个名字 in 层级列表[递归层次]:
                    底层xml树集合.append(xml树.getElementsByTagName(第i个名字))
            else:  # 单最低层级提取
                底层xml树集合.append(xml树.getElementsByTagName(层级列表[递归层次]))
            多底层的数据 = []
            for 一个xml树 in 底层xml树集合:
                # 缺少最低属性
                if len(一个xml树) < 1:
                    异常情况[递归层次][0] += 1
                    多底层的数据.append(None)
                    continue
                # 最低属性过多
                if len(一个xml树) > 1:
                    异常情况[递归层次][1] += 1
                # 如果是多最低层级就必须取第一个,单最低层级可以多取
                if 多最低层级 or 只取第一个:
                    多底层的数据.append(一个xml树[0].firstChild.data)
                else:  # 单最低层级可以多取
                    for 一个内容 in 一个xml树:
                        多底层的数据.append(一个内容.firstChild.data)
            if 多最低层级 == True:
                所有内容.append(多底层的数据)
            else:
                所有内容 += 多底层的数据
            return (所有内容, 异常情况)
        else:
            某层的xml树集合 = xml树.getElementsByTagName(层级列表[递归层次])
            if len(某层的xml树集合) < 1:
                异常情况[递归层次][0] += 1
            for 某层的xml树 in 某层的xml树集合:
                xml解析.获取相同层级内的所有内容(某层的xml树, 层级列表, 只取第一个, 所有内容, 异常情况, 递归层次 + 1)  # 递归
        return (所有内容, 异常情况)

    @staticmethod
    def 解析字符串或其数组成xml数组(字符串数组):
        '''
        解析字符串或其数组成xml数组
        :param 字符串数组: '' or ['',...] 可以是地址或字符串,也可以是它们的数组
        :return xml数组: [xml.dom.minidom.Element,...] 只有一个也是列表形式
        '''
        xml数组 = []
        if not isinstance(字符串数组, list):
            字符串数组 = [字符串数组]
        for 一个字符串 in 字符串数组:
            if 一个字符串[0] != '/':
                xml数组.append(xml.dom.minidom.parseString(一个字符串).documentElement)
            else:
                xml数组.append(xml.dom.minidom.parse(一个字符串).documentElement)
        return xml数组


class 正则解析:
    @staticmethod
    def 普通头尾分割后正则提取(文本, 匹配正则式, 全部提取=False, 分割对普通式=[]):
        '''
        不是 多匹配正则式 的情况只取文本之一的第一个,这是配对提取.用分割对分割的越小,速度越快.
        注意自动补全匹配正则式的存在
        :param 文本: '' 一般是字符串形式
        :param 匹配正则式: ['',...]
        :param 全部提取: True or False 决定单一匹配正则式的时候是否全部提取
        :param 分割对普通式: [['',''],...] 可选的二维数组
        :return 提取结果: ['',...] or [['',...],...] 非全部提取and单匹配正则的结果是第一个,否则是后者
        :return 异常数量: [i0,i1] i0代表有多少次文本匹配结果为None（单匹配正则的匹配结果数等于匹配文件数）,
        i1代表总匹配的写入提取结果的数量
        '''
        if not isinstance(文本, list):
            文本 = [文本]
        # 自动补全部分匹配正则式
        if 匹配正则式 != None and ']' not in 匹配正则式[0]:
            匹配正则式_补全 = []
            for 一个匹配正则式 in 匹配正则式:
                匹配正则式_补全.append('(?<=' + 一个匹配正则式 + ')[^<>]+')
            匹配正则式 = 匹配正则式_补全
        # 头尾分割
        if len(分割对普通式) > 0:
            for 一个分割对 in 分割对普通式:
                if 一个分割对 == '': continue
                # 头分割
                新文本 = []
                for 文本之一 in 文本:
                    新文本 += 文本之一.split(一个分割对[0])[1:]
                # 尾分割
                文本 = 新文本
                新文本 = []
                for 文本之一 in 文本:
                    新文本.append(文本之一.split(一个分割对[1])[0])
                文本 = 新文本
        提取结果 = []
        异常数量 = [0, 0]
        if 匹配正则式 == None:
            return (文本, 异常数量)
        # 单匹配正则-全部提取
        if len(匹配正则式) == 1 and 全部提取:
            for 文本之一 in 文本:
                一个提取结果 = re.findall(匹配正则式[0], 文本之一)
                匹配结果数 = len(一个提取结果)
                if 匹配结果数 == 0:
                    提取结果.append(None)
                    异常数量[0] += 1
                    continue
                异常数量[1] += 匹配结果数
                提取结果.append(一个提取结果)
        # 单匹配正则-非全部提取(只取第一个)
        elif len(匹配正则式) == 1 and not 全部提取:
            for 文本之一 in 文本:
                一个提取结果 = re.search(匹配正则式[0], 文本之一)
                if 一个提取结果 == None:
                    提取结果.append(None)
                    异常数量[0] += 1
                    continue
                异常数量[1] += 1
                提取结果.append(一个提取结果.group())
        # 多匹配正则-只取第一个
        else:
            for i in range(len(文本)):
                一组结果 = []
                for 一个匹配正则式 in 匹配正则式:
                    一个匹配结果 = re.search(一个匹配正则式, 文本[i])
                    if 一个匹配结果 == None:
                        异常数量[0] += 1
                        一组结果.append(None)
                        continue
                    异常数量[1] += 1
                    一组结果.append(一个匹配结果.group())
                提取结果.append(一组结果)
        return (提取结果, 异常数量)


if __name__ == '__main__':
    a = [1, 2, 3]
    FileProcess.writeObject(a, 'test1.txt')
    print(FileProcess.readObject('test1.txt'))

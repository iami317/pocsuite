#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@Author  :  hao
@File    :  util.py
@Time    :  2020/7/16 下午3:31
'''

import hashlib
import os
import random
import re
import shlex
import socket
import string
import struct
import sys
import IPy
import subprocess


def get_network_num():
    """
    本方法作用是为了选择可用的网卡
    :return:
    """
    cmd = "cat /proc/net/dev"
    p = subprocess.Popen(shlex.split(cmd), shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    txt = p.stdout.read().decode('utf8', 'ignore')
    net = re.findall("(.*?):\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*\d+\s*(\d+)", txt)
    # for net_name, multicast in net:
    #     if multicast != '0':
    #         return net_name
    return len(net)


def get_filename(filepath, with_ext=True):
    base_name = os.path.basename(filepath)
    return base_name if with_ext else os.path.splitext(base_name)[0]


def findIPs(start, end):
    ipstruct = struct.Struct('>I')
    start, = ipstruct.unpack(socket.inet_aton(start))
    end, = ipstruct.unpack(socket.inet_aton(end))
    result = [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end + 1)]
    return result


def get_ips(addr):
    pattern1 = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    pattern2 = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.)(\d{1,3})-(\d{1,3})')
    pattern3 = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,3})')
    pattern4 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    try:
        if pattern1.match(addr):
            start = pattern1.match(addr).group(1)
            end = pattern1.match(addr).group(2)
            ip_list = findIPs(start, end)
            return ip_list, len(ip_list)

        elif pattern2.match(addr):
            ip_start_num = pattern2.match(addr).group(2)
            ip_end_num = pattern2.match(addr).group(3)
            start = pattern2.match(addr).group(1) + ip_start_num
            end = pattern2.match(addr).group(1) + ip_end_num
            ip_list = findIPs(start, end)
            return ip_list, len(ip_list)

        elif pattern3.match(addr):
            ips = IPy.IP(addr)
            return [str(ip) for ip in ips][1:], ips.len() - 1

        elif pattern4.match(addr):
            return [addr], 1
            # return [pattern4.match(addr).group()]
        else:
            return None
    except:
        return None


SYSTEM_VERSION = ["Ubuntu", "Red Hat", "SUSE", "Turbo", "Fedora", "Asianux", "CentOs", "Manjaro", "Debian", "Mint",
                  "Kali", "Solus", "Arch", "Puppy", "Deepin", "windows", 'Hikvision']


def what_ostype(port_info):
    if port_info:
        for info in port_info:
            for system in SYSTEM_VERSION:
                if system.lower() in info['product'].lower() or system.lower() in info[
                    'version'].lower() or system.lower() in info['extrainfo'].lower():
                    return system
    return ""


def what_OS_ttl(ttl):
    unix = 255
    windows = 128
    linux = 64
    windwos98 = 32

    if ttl > windows:
        return "Unix"
    elif ttl > linux:
        return "Windows"
    elif ttl > windwos98:
        return "Linux"
    else:
        return "windows98"


def get_host_ip():
    ip = None
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]

    except:
        pass
    finally:
        s.close()

    return ip if ip else "127.0.0.1"


def get_os_from_ping(ip):
    os = ''
    if sys.platform.startswith("win"):
        cmd = f"ping {ip} -n {2}"
    else:
        cmd = f"ping {ip} -c {2}"

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    try:
        result = p.stdout.read().decode("gbk")
    except:
        try:
            result = p.stdout.read().decode("utf8")
        except:
            result = None
    if result:
        ttl = re.search(r"ttl=(\d{2,3})", result, re.I)
        if ttl:
            ttl_n = int(ttl.group(1))
            os = what_OS_ttl(ttl_n)
    return os


def get_md5(value):
    if isinstance(value, str):
        value = value.encode(encoding='UTF-8')
    return hashlib.md5(value).hexdigest()  # 返回16进制字符串值


def random_str(length=10, chars=string.ascii_letters + string.digits):
    return ''.join(random.sample(chars, length))


ua = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14',
    'Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
    'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1'
]


def get_headers():
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': "",
        'Referer': "",
        'X-Forwarded-For': "",
        'X-Real-IP': "",
        'Connection': 'keep-alive',
    }
    referer = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(5, 15))])
    referer = 'www.' + referer.lower() + '.com'
    ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
    HEADERS["User-Agent"] = random.choice(ua)
    HEADERS["Referer"] = referer
    HEADERS["X-Forwarded-For"] = HEADERS["X-Real-IP"] = ip
    return HEADERS


def LongSubString(s1, s2):
    """
    查找两个字符串中相同的最大字串
    使用了滑动窗口的思想
    """
    MaxLength = 0
    MaxString = ''
    new1 = ''
    for v1 in s1:
        new1 += v1
        new2 = ''
        for v2 in s2:
            new2 += v2
            while len(new2) > len(new1):
                new2 = new2[1:]
            if new2.lower() == new1.lower() and len(new2) > MaxLength:
                new2 = new2.strip()
                MaxLength = len(new2)
                MaxString = new2
        if MaxString.lower() != new1.lower():
            new1 = new1[1:]
    return MaxString.lower(), MaxLength


def filter_search(s1, s2):
    filters = ['apache', 'server', 'java', 'http', ' ']
    '''
    本方法作用是查找两个字符串中相同部分有多少，匹配则为Ture
    :param s1: 需要匹配的关键字 (Apache Tomcat/Coyote JSP engine)
    :param s2: 数据库查询到的关键字 (Apache Tomcat)
    :return: bool
    '''
    if len(s1) and len(s2):
        small_len = len(s2) if len(s1) > len(s2) else len(s1)
        max_str, max_len = LongSubString(s1, s2)
        if small_len == max_len: return True
        if 4 < max_len < small_len and max_str not in filters: return True
        # 如果不符合上述条件，进行二次查找重复
        s1_split = s1.replace(max_str, "")
        s2_split = s2.replace(max_str, "")
        max_str2, max_len2 = LongSubString(s1_split, s2_split)
        return True if max_len2 > 2 else False


def install_package(package):
    cmd = f"python3 -m pip install {package} -i https://pypi.douban.com/simple"
    p = subprocess.Popen(shlex.split(cmd), shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.communicate()


def handle_task_ip(task_ips):
    ip_list = []
    # 记录C段的数量
    c = 0
    pattern1 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/(\d{1,2})')
    pattern2 = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})-(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    pattern3 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    pattern4 = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.)(\d{1,3})-(\d{1,3})$')
    for task_ip in task_ips:
        if pattern1.findall(task_ip):
            n = 32 - int(pattern1.findall(task_ip)[0])
            #  判断小于C段的IP直接加入ip_list
            if n // 8 == 0:
                ip_list.append(task_ip)

            #  判断是否为C段 直接加入ip_list
            elif n // 8 == 1 and n % 8 == 0:
                c += 1
                ip_list.append(task_ip)

            # 介于C段和B段之间的
            elif n // 8 == 1 and n % 8 > 0:
                remainder = n % 8
                for i in range(0, (2 << remainder - 1)):
                    c += 1
                    _ip = f"{'.'.join(task_ip.split('.')[0:2])}.{i}.0/24"
                    ip_list.append(_ip)
            # 基本属于B段了
            elif n // 8 == 2:
                for i in range(0, 256):
                    c += 1
                    _ip = f"{'.'.join(task_ip.split('.')[0:2])}.{i}.0/24"
                    ip_list.append(_ip)
        if pattern2.match(task_ip):
            start = pattern2.match(task_ip).group(1)

            end = pattern2.match(task_ip).group(2)
            ip_list.extend(findIPs(start, end))
        if pattern3.match(task_ip):
            ip_list.append(task_ip)
        if pattern4.match(task_ip):
            ip_start_num = pattern4.match(task_ip).group(2)
            ip_end_num = pattern4.match(task_ip).group(3)
            start = pattern4.match(task_ip).group(1) + ip_start_num
            end = pattern4.match(task_ip).group(1) + ip_end_num
            ip_list.extend(findIPs(start, end))
    return ip_list, c

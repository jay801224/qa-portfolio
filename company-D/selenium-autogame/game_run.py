import os
import time
import unittest

from HTMLTestRunner import HTMLTestRunner

test_dir = 'C:/selenium/test_case'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='gametest*.py')


if __name__ == "__main__":
    runner = unittest.TestSuite()
    report_dir = 'C:/selenium/test_case'
    os.makedirs(report_dir, exist_ok=True)
    #now=time.strftime("%Y-%m-%d_%H-%M-%S",time.localtime())
    #report_name = '{0}/{1}.html'.format(report_dir, now)
    #将测试结果写入到result.html中
    fp=open("all result.html",'wb')
    runner=HTMLTestRunner(stream=fp,title='PC chrome all game 測試報告',description='Result:')
    runner.run(discover)
    fp.close()
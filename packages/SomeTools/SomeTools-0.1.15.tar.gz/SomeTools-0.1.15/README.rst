SomeTools
===========================================================================================================================================================

.. image:: https://img.shields.io/pypi/v/SomeTools.svg
    :target: https://pypi.org/project/SomeTools/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/wheel/SomeTools.svg
    :target: https://pypi.org/project/SomeTools/
    
.. image:: https://img.shields.io/pypi/pyversions/SomeTools.svg
    :target: https://pypi.org/project/SomeTools/

.. image:: https://img.shields.io/pypi/l/SomeTools.svg
    :target: https://pypi.org/project/SomeTools/


功能(Features)
------------------------------------------------------------------------------------------------------------------------------------------------------------

一些方便日常使用的工具(Some tools that are convenient for daily use)

* 将输入的任何类型的日期字符串类型转化为datetime.datetime类型的日期对象(Converts any type of date string type entered to a date object of type datetime.datetime)
* 移除一个字符串中的回车换行空格制表符等内容(Remove carriage return, newline space tabs, etc., from a string)
* 将中文字符转为其拼音的首字母(Convert Chinese characters to the first letter of their pinyin)
* 更加方便的日志记录工具(More convenient logging tool)
* 繁体简体中文汉字转换工具(Traditional simplified Chinese character conversion tool)


安装(Installation)
------------------------------------------------------------------------------------------------------------------------------------------------------------

.. code-block:: shell

    pip install SomeTools -i https://pypi.python.org/simple


使用示例(Usage example)
------------------------------------------------------------------------------------------------------------------------------------------------------------

1.将输入的任何类型的日期字符串类型转化为datetime.datetime类型的日期对象(Converts any type of date string type entered to a date object of type datetime.datetime)

.. code-block:: python

    from common_tools import Common_tools


    class Demo(Common_tools):
        def __init__(self, *args, **kwargs):
            super(Demo, self).__init__(*args, **kwargs)


    if __name__ == '__main__':
        demo_ins = Demo()

        # 将输入的任何类型的日期字符串类型转化为datetime.datetime类型的日期对象(Converts any type of date string type entered to a date object of type datetime.datetime)
        demo_ins.logger.info(f"{demo_ins.str_to_obj('2012-12-12 12:12:12')}{type(demo_ins.str_to_obj('2012-12-12 12:12:12'))}")

        # 移除一个字符串中的回车换行空格制表符等内容(Remove carriage return, newline space tabs, etc., from a string)
        temp_str = 'abc abc \n abc \r'
        demo_ins.logger.info(f"before clean string{temp_str}")
        temp_str = Demo.clean_string('abc abc \n abc \r')
        demo_ins.logger.info(f"after clean string{temp_str}")

        # 将中文字符转为其拼音的首字母(Convert Chinese characters to the first letter of their pinyin)
        demo_ins.logger.info(f"{Demo.get_pinyin('中国外汇交易中心')}")

        # 更加方便的日志记录工具(More convenient logging tool)
        demo_ins.logger.info(f"{Demo.get_pinyin('中国外汇交易中心')}")
        demo_ins.logger.debug(f"{Demo.get_pinyin('中国外汇交易中心')}")
        demo_ins.logger.warning(f"{Demo.get_pinyin('中国外汇交易中心')}")
        demo_ins.logger.error(f"{Demo.get_pinyin('中国外汇交易中心')}")
        demo_ins.logger.exception(f"{Demo.get_pinyin('中国外汇交易中心')}")

        demo_ins.logger.info(f"繁体转简体 眾議長與李克強會談->{Demo.traditional_chinese_to_simplified('眾議長與李克強會談')}")
        demo_ins.logger.info(f"简体转繁体 众议长与李克强会谈->{Demo.simplified_chinese_to_traditional_chinese('众议长与李克强会谈')}")



------------------------------------------------------------------------------------------------------------------------------------------------------------

To be continued
# eqlog
>  log tool	--- 统一日志工具

## 使用说明
### 1.安装
```shell script
pip install eqlog
```

### 2.升级
```shell script
pip install --upgrade eqlog
```

### 3.隐式使用
> 打印函数入参和执行异常信息

```python
from eqlog import eqlog

@eqlog.log
def func(param):
    print('打印函数入参和执行异常信息')
```

### 4.显示使用
```python
from eqlog import eqlog

def func(param):  
    eqlog.info(param)  
    eqlog.debug(param)  
    eqlog.warning(param)  
    eqlog.error(param)  
```

### 5.配置文件
> 配置文件命名为 eqlog.xml，可放在项目启动文件同级目录、上级目录、上上级目录
```xml
<?xml version="1.0" ?>
<eqlog>
    <!--  配置文件名称  -->
    <file_name name="name">eqlog.xml</file_name>
    <!--  配置文件目录  -->
    <config_dir name="last_dir">eqconfig</config_dir>
    <!--  配置文件目录  -->
    <file_path name="path">
        <!--  linux下的日志文件目录  -->
        <linux_path name="linux">/home/data/logs/</linux_path>
        <!--  windows下的日志文件目录  -->
        <win_path name="win">D:/MyProjects/eqlog/tests/logs/</win_path>
        <!--<win_path name="win">D:/WorkSpace/PythonWork/eqlog/tests/logs/</win_path>-->
    </file_path>
</eqlog>
```

### 6.显示声明日志工具
```python
from eqlog import Logger

_logger = Logger('module_name', log_files_dir='./log/',config='./log.xml')

@_logger.log
def func(param):  
    _logger.info(param)  
    _logger.debug(param)  
    _logger.warning(param)  
    _logger.error(param)  
```

## 版本说明
### 1、当前版本：0.0.6
```shell script
pip install eqlog==0.0.6
```

### 2、未来版本
```shell script
# 支持日志平台
```
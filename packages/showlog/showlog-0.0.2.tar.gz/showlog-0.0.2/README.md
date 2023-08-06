# showlog
![](https://img.shields.io/badge/Python-3.8.6-green.svg)

#### 介绍
python的log，封装了些简单的方法


#### 安装教程

1.  使用pip安装
- 普通方式安装
```shell script
pip3 install showlog
```

- 使用阿里镜像加速安装
```shell script
pip3 install showlog -i https://mirrors.aliyun.com/pypi/simple
```


#### 使用说明

1.  导入
``` shell script
import showlog
```

2.  简单使用
``` shell script
showlog.info('hello word!')
showlog.warning('this is warning')
showlog.error('this is error')
```

3.  保存log为文件
- 只需要设置一次，后续的log将会被存储
``` shell script
showlog.save_info('[your file name].log')
showlog.save_warning('[your file name].log')
showlog.save_error('[your file name].log')
```

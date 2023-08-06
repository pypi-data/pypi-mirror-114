# caterpillar_HTMLTestRunner

#### 介绍
用于存放HTMLTestRunner.py文件，并从此仓代码发布到pypi官方，从而可以使用pip install HTMLTestRunner 命令安装的方式安装

#### 软件架构
软件架构说明


#### 安装教程

1.  pip install caterpillar-HTMLTestRunner

#### 使用说明

1. 使用举例代码参考[实例代码](docs/example.py)


#### 修改记录

* 1.0.2 晚上帮助文档和修改记录 2021/08/01

* 1.0.1 修改适配Python3 修改记录如下   2021/08/01

   * 第94行，将import StringIO修改成import io

   * 第539行，将self.outputBuffer = StringIO.StringIO()修改成self.outputBuffer = io.StringIO()

   * 第642行，将if not rmap.has_key(cls):修改成if not cls in rmap:

   * 第766行，将uo = o.decode('latin-1')修改成uo = e

   * 第772行，将ue = e.decode('latin-1')修改成ue = e

   * 第631行，将print >> sys.stderr, '\nTime Elapsed: %s' % (self.stopTime-self.startTime)修改成print(sys.stderr, '\nTime Elapsed: %s' % (self.stopTime-self.startTime))


#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


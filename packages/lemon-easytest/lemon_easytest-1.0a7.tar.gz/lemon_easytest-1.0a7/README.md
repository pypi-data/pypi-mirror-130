# easytest

`easytest`是一个接口自动化框架。

功能特点：

- 支持http接口测试
- 支持`json`，`html`,`xml`格式的响应断言
- 支持数据库断言
- 支持用例标记筛选
- 支持用例失败重运行
- 支持多线程

## 安装

`pip install lemon_easytest`

## 快速使用

不需要写任何代码，所有你需要做的就是按照规则编写用例文档，然后运行命令`easytest`。

`easytest`支持`yaml`格式和`excel`格式的用例文档。

在任意目录下创建文件`singe_test.yaml`,内容如下：

```yaml
test:                                 # 表名这是单个测试用例
  title: 一个简单的测试                 # 用例名称
  url: http://httpbin.org/get         # url
  method: get                         # 请求方法
  request:                            # 请求参数字段
    headers:                          # 请求头
      CustomerHeader: lemonban        # 头信息
    params:                           # url参数
      search: lemonban                # url参数键值对
  res_type: json                      # 响应数据类型
  status_code: 200                    # 状态码
  assertion:                          # 断言表达式
    -
      - eq                            # 相等
      - $..Customerheader             # 结果提取表达式
      - lemonban                      # 期望值
    -
      - eq
      - $..search
      - lemonban
```

然后在命令行运行

```
easytest yourpath/single_test.yaml
```

```bash
INFO 2021-10-30 14:53:26,081 :==========single_test测试开始============
INFO 2021-10-30 14:53:26,081 :用例【一个简单的测试】开始测试>>>>>>>>
INFO 2021-10-30 14:53:26,591 :用例【一个简单的测试】测试结束<<<<<<<<<
INFO 2021-10-30 14:53:26,591 :==========single_test测试结束============
用例总数:1,成功:1个,跳过:0,失败:0个,错误:0个
```

## 通过python代码调用easytest

可以直接通过python调用`easytest`

```python
import easytest
easytest.main()
```

也可传递参数

```python
easytest.main(['test_dir', '--debug', '--logfile', 'test.log'])
```

## 编写用例

### 测试用例

easytest中编写单条测试用例可以使用`yaml`格式，也可以使用excel文件。

#### excel格式

使用excel文件编写单条测试用例非常简单，例如将上面的案例编写到excel文件中格式如下：

![](http://testingpai.com/upload/file/2021/11/%E4%BC%81%E4%B8%9A%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BEe8827888e26443579c321815ae42f806-3dd807b9.png)

当用excel文件编写用例时保持数据的整洁，其他单元格不要有任何数据，以免加载用例数据失败。easytest会根据excel文件的sheetname来组织用例，所以单条用例请删除其他的表。

#### yaml格式

当使用yaml文件编写单条测试用例时最外层键必须为`test`,因为easytest根据它来确定一个yaml文件中的数据是单条测试用例。

```YAML
test:                                 # 表名这是单个测试用例
  title: 一个简单的测试                 # 用例名称
  url: http://httpbin.org/get         # url
  method: get                         # 请求方法
  request:                            # 请求参数字段
    headers:                          # 请求头
      CustomerHeader: lemonban        # 头信息
    params:                           # url参数
      search: lemonban                # url参数键值对
  res_type: json                      # 响应数据类型
  status_code: 200                    # 状态码
  assertion:                          # 断言表达式
    -
      - eq                            # 相等
      - $..Customerheader             # 结果提取表达式
      - lemonban                      # 期望值
    -
      - eq
      - $..search
      - lemonban
```

### 测试套件

easytest中测试套件表示一组有顺序的测试用例，当启动多线程时，以测试套件为单位交给线程去按照套件中的顺序执行测试用例。注意套件和套件间的执行顺序是不固定的。

单个测试用例也会被套上一层测试套件的壳子,yaml格式的单测试用例会被封装到以yaml文件名为名字的测试套件中，excel格式的单测试用例会被封装到以表名为名字的测试套件中。

#### excel格式

excel文件中编写测试套件与单测试用例没有区别，按照执行顺序从上往下依次编写即可,例如：

![](http://testingpai.com/upload/file/2021/11/wecomtempa0c3a6d9a95896ee44d4bbb6993e12e4-2a485a7f.png)

在单个excel文件中可以编写多个测试套件，一个表即为一个测试套件，所以非测试用例或者项目设置的表请删除。

#### yaml格式

在yaml文件中编写测试套件，最外层的key必须为`test_suit`，因为easytest根据它来确定一个yaml文件中的数据是一个测试套件。注意和excel不同，yaml格式不支持在一个文件中编写多个测试套件，因为多层级的嵌套缩进将是噩梦。

```yaml
test_suit:
  - title: 一个简单的测试
    url: http://httpbin.org/post
    method: post
    status_code: 200
    res_type: json
    request:
      json:
        username: xinlan
        password: 123456
    assertion:
      - [eq,$..username,xinlan]
      - [eq,$..password,123456]

  - title: 一个不简单的测试
    url: http://httpbin.org/post
    method: post
    status_code: 200
    res_type: json
    request:
      json:
        username: xinlan
        password: 123456
    assertion:
      - [ eq,$..username,xinlan ]
      - [ eq,$..password,123456 ]
```

## 用例收集规则

`easytest` 命令后接受一个位置参数`file_or_dir`,它可以是一个用例文件，也可以是一个目录。

当传入一个用例文件时，它必须是上一节提到的符合格式的`excel`或者`yaml`文件，excel文件只支持`.xlsx`后缀的格式，yaml文件支持`.yaml`或者`.yml`后缀。

当传入一个目录时，`easytest`会递归的去这个目录下搜索所有符合规则的用例文件(excel、yaml)，并从中提取用例，当遇到格式错误时，程序会中断，所以不要把无关的Excel文件和yaml文件放在用例目录下。

## 用例字段说明

- title

  字符串，用例标题

- url

  字符串，请求的url，支持完整url，例如`https://httpbin.org/get`,也支持项目配置中的接口对应的key。例如：`register`

- method

  字符串，http请求方法

- request

  json对象，http请求携带的参数，请求头，cookie等。底层调用python的`requests`库，参数名完全一致。

  - params

    json对象，http请求携带的url参数。例如

    ```yaml
    request:
    	params:
    		search: python
    ```

  - data

    json对象，http请求携带的表单参数。例如

    ```yaml
    request:
      data:
        username: xinlan
        password: 123456
    ```

  - json

    json对象，http请求携带的json参数。例如

    ```yaml
    request:
    	json:
    	  username: xinlan
    	  password: 123456
    ```

  - headers

    json对象，http请求携带的header。例如

    ```yaml
    request:
    	headers:
    	  X-Lemonban-Media-Type: lemonban.v1
    ```

  - cookie

    json对象，http请求携带的cookie信息。例如

    ```yaml
    request:
    	cookies:
    		key: value
    ```

    

- res_type

  字符串，http响应类型，可选值有：`json,xml,html`

- status_code

  整数，http断言响应状态码。

- assertion

  数组对象，响应结果断言表达式。格式为: `[[条件符号,提取表达式,期望结果],[条件符号1,提取表达式1,期望结果1],...]`,例如：

  ```yaml
  assertion:
    - [eq,$..username,xinlan]
    - [eq,$..password,123456]
  ```

  条件符号支持：

  - eq: 相等
  - gt: 大于
  - gte:大于等于
  - lt: 小于
  - lte:小于等于
  - in:在其中
  - contains:包含

  目前仅支持`eq`

  提取表达式支持：

  - 正则表达式
  - jsonpath表达式
  - xpath

- db_assertion

  数组对象，数据库断言表达式。格式为: `[[条件符号,sql语句,期望结果],[条件符号1,sql语句1,期望结果1],...]`,例如：

  ```yaml
  db_assertion:
    - [eq,select leave_amount from member where id=#invest1_id#,0]
    - [exist,select id from invest where member_id=#invest1_id# and loan_id=#loan_id# and amount=5000,true]
    - [exist,select id from financelog where pay_member_id=#invest1_id# and amount=5000 and pay_member_money=0 and status=1,true]
  
  ```

  条件符号支持：

  - eq: 相等
  - exist: 存在。使用exist时，期望结果必须为`true`

- extract

  数组对象，响应结果提取表达式。格式为`[[变量名,提取表达式],[变量名2，提取表达式2],...]`例如：

  ```yaml
  exract:
  	- [mobile_phone, $..mobile_phone]
  	- [token, $..token]
  ```

  底层easytest会将提取出的值绑定到用例类的变量名属性上，供后面的用例依赖。

  提取表达式支持：

  - jsonpath
  - 正则表达式
  - xpath表达式

- marks

  字符串，用例标记，运行参数中可以筛选出匹配的标记用例

## 项目配置

`easytest`命令会从当前目录下读取名为`easytest.ini`的配置文件，下面是一个完整配置文件的例子：

```ini
[project]  																# 项目配置段
name = xxx项目													   # 项目名称	  
host = http://some.api.root.com           # 项目接口根地址
[db_config]																# 数据库配置
host = dbhost										          # 数据库主机	
user = root																# 数据库用户
password = 123456                         # 数据库密码
db = somedb																# 数据库名
charset = utf8														# 字符编码
port = 3306																# 端口
[interfaces]															# 接口地址
register: /member/register								# 注册接口对应地址		
login: /member/login											# 登录接口对应地址
withdraw: /member/withdraw		
recharge: /member/recharge
add: /loan/add
audit: /loan/audit
invest: /member/invest
[run]																			# 运行时参数
debug=true																# 开启调试模式
logfile=a.log															# 日志文件
marks=success,login												# 筛选标记	
thread_num=10															# 启动线程数量
retry=3																		# 失败重跑次数
report=result.json												# 报告文件
```

### project

project段，支持name和host

- name 项目名称
- host 项目接口根地址，注意不要以`/`结尾

### db_config

db_config段，数据库配置，目前仅支持mysql

- host 数据库主机
- user 数据库用户名
- password 数据密码
- db 数据库名
- port 端口
- charset 字符串编码

### interfaces

interfaces段，接口名称配置，格式：`key=value`，key是接口名称字符串，value是去掉主机后的接口地址以`/`开头，在用例中`url`字段可以填写key，easytest内部会使用项目host+接口地址进行拼接。

### run

run字段，运行时的参数。

- debug 调试模式，默认为false
- logfile 生成日志文件，可以是绝对路径或者是相对路径
- marks 需要筛选的标记，多个标记使用逗号隔开，例如：`success,login`，表示会筛选被标记了`success`和`login`的用例。
- thread_num 启动线程的数量，默认为0表示单线程执行
- retry 用例失败后重跑的次数，默认为0表示不重跑
- report 生成报告的文件名，根据后缀自动生成对应报告，暂只支持json格式。

注意：命令行参数会覆盖项目配置。

## 生成模拟测试数据

在测试过程中有时需要动态的生成测试数据，例如手机号码，人名等。`easytest`通过`Faker`模块来生产模拟数据，暂时只支持简体中文语言下的接口，详情见[Faker简体中文providers](https://faker.readthedocs.io/en/stable/locales/zh_CN.html)。

用例中支持生产模拟测试数据的字段有，`url`,`request`,`db_assertion`。

使用格式为`$生成数据接口名$`。

例如在`Faker`中生成手机号码的方法名为`phone_number`,那么在用例中使用`$phone_number$`表示动态生成手机号码。

```yaml
test:                                 # 表名这是单个测试用例
  title: 一个简单的测试                  # 用例名称
  url: http://httpbin.org/get         # url
  method: get                         # 请求方法
  request:                            # 请求参数字段
    headers:                          # 请求头
      CustomerHeader: lemonban        # 头信息
    params:                           # url参数
      search: lemonban                # url参数键值对
      phone: $phone_number$
```

上面这个用例表示url参数phone是一个动态生成的手机号码。

## 接口依赖的处理

`easytest`中，同一个测试套件下，前一个用例返回的数据可以通过变量传递给下一个用例。

例如登录成功后将返回的token值传递给下一个需要token的用例。传递步骤如下：

1. 在登录用例中添加`extract`字段提取响应回的`token`值,并绑定到你定义的变量名`admin_token`上
2. 在后面的用例中，在需要使用到token的数据部分就可以使用`#admin_token#`,来表示，easytest会在自动进行替换

所有你需要做的，只是按照规则编写用例，剩下的交给easytest。

## 命令行参数说明

- file_or_dir

  字符串，项目路径，或者需要执行的用例文件

- --debug

  开启日志调试模式

- --logfile

  字符串，日志文件路径

- --marks

​		字符串，运行时选择的标记

- --thread_num

  整数，运行时启动线程的数量，默认为0表示单线程执行

- --report

  字符串，测试报告文件路径，按照文件后缀生成对应的格式的报告




























# CoolQ C++ SDK (3rd-party)

酷 Q 官方的 C++ SDK 看起来没人维护了，[CoolQ/cqsdk-vc](https://github.com/CoolQ/cqsdk-vc) 上面的 `CQP.lib` 和 `cqp.h` 都已经过时了，有些新的函数接口没有加进去，所以新开此 repo 来维护一个第三方的版本。

[`lib`](lib) 目录中的 `CQP.lib` 和 `cqp.h` 是我生成好的最新版本的库文件和头文件，可以直接添加到酷 Q 插件的工程中，和官方的使用方法一样（只要直接替换官方的 demo 里的同名文件即可）。此 `.lib` 文件没有实际的函数实现，只是用来通过链接的，实际的函数实现在酷 Q 安装目录的 `bin\CQP.dll`。

## 接口权限码

在插件中调用的接口，需要在 `.json` 文件中的 `auth` 字段加上相应的权限码，具体权限码对应的函数，见 [权限码](PermissionCode.md)。

## 手动生成 `.lib` 文件

注：如果你不明白这里在干什么，就不要自己生成了。如果发现酷 Q 更新了新的接口而这里的 `cqp.h` 中还没有，那就请提交 [issue](https://github.com/richardchien/coolq-cpp-sdk/issues/new)。

[`scripts`](scripts) 目录中的 `generate_lib.py` 是用来从 `.h` 文件生成 `.lib` 文件的，它会解析头文件中的 `CQAPI` 函数声明，来生成 `CQP.lib`，从而不用再担心官方 SDK 或我这里的没有及时更新）。

`cqp.h` 中的函数声明一般通过查看官方的易语言 SDK 来转译成 C，也可以通过 `dumpbin /exports CQP.dll` 来直接查看 dll 中的导出函数。注意从后者没法看到参数列表。

要自己生成 `.lib` 文件，首先需要打开一个「Visual Studio Developer Command Prompt」，VS 2015、VC++ 2010 等都带了这个程序。

然后在这个命令行中运行（注意需要 Python 3.x）：

```bat
python .\scripts\generate_lib.py .\cqp.h
```

此命令会在当前工作目录下生成 `CQP.lib` 文件。

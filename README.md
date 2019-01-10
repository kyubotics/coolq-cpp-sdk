# CoolQ C++ SDK

[![License](https://img.shields.io/github/license/richardchien/coolq-cpp-sdk.svg)](LICENSE)
[![Build Status](https://img.shields.io/appveyor/ci/richardchien/coolq-cpp-sdk.svg)](https://ci.appveyor.com/project/richardchien/coolq-cpp-sdk)

CoolQ C++ SDK 封装了跟 DLL 接口相关的底层逻辑，包括：

- 将所有从 酷Q 传来的字符串转成 UTF-8，并将所有传入 酷Q 的字符串转成 GB18030
- 封装了 `Message` 和 `MessageSegment` 类，使构造消息内容更为方便
- `MessageSegment` 类提供了快速构造消息段（CQ 码）的接口
- 处理了消息内容中的 emoji 到 Unicode 的转换
- 封装了 酷Q 事件的数据，在事件处理函数中传入
- 将 QQ 相关的事件分为三个大类别：`MessageEvent`、`NoticeEvent`、`RequestEvent`
- 封装了数据类，如 `User`、`Group`、`GroupMember` 等
- ……

并且对外提供了更现代的 C++ 接口，从而为更方便地编写插件提供可能。

## 使用方式

### 预备

本项目使用 [CMake](https://cmake.org/) 构建，依赖项通过 [vcpkg](https://github.com/Microsoft/vcpkg) 管理。如果你没有使用过这两个工具，请先前往它们的官方网站了解基本用法。

在开始使用之前，请确保你已经安装了 Git 和 CMake，且 `PATH` 中存在 `git` 和 `cmake` 命令。不需要安装 vcpkg，后面的脚本中会自动安装。

除了 Git、CMake，还需要安装 VC++ 2017 v141 工具集。

### 下载 SDK

```ps1
git clone https://github.com/richardchien/coolq-cpp-sdk.git my-awesome-app
cd my-awesome-app
git submodule init
git submodule update
```

### 准备构建环境

```ps1
powershell .\scripts\prepare.ps1
```

[`scripts/prepare.ps1`](scripts/prepare.ps1) 脚本会在当前项目目录的 `vcpkg` 子目录中安装 vcpkg，并安装所需依赖。

### 修改 App Id 和相关信息

修改 [`CMakeLists.txt`](CMakeLists.txt) 的 `LIB_NAME` 变量为你的 App Id，例如 `set(LIB_NAME "com.company.my-awesome-app")`。

复制 [`com.example.demo.json`](com.example.demo.json) 文件，并命名为 `<AppId>.json`，例如 `com.company.my-awesome-app.json`。按需修改其中的信息，通常需要修改 `name`、`version`、`version_id`、`author`、`description`，根据实际功能可能还需要修改 `menu` 和 `auth`。请不要修改 JSON 描述文件的 `event` 字段，因为事件处理函数的名字已经写死在了 SDK 中。另外，这里 JSON 描述文件使用 **UTF-8 编码**，将会在构建时**自动转换成 GB18030 编码**，如果你曾经使用过其它 SDK，可能需要注意一下。

### 编写功能

移除 [`src/demo.cpp`](src/demo.cpp) 或在其基础上修改，实现自己的功能。如果直接在 `src/demo.cpp` 上修改，请注意修改调用 `CQ_INITIALIZE` 宏时传入的 App Id。

具体 API 请参考 `src/demo.cpp`，或顺着 [`src/cqsdk/cqsdk.h`](src/cqsdk/cqsdk.h) 头文件找进去，IDE 的自动补全帮助会很大。

### 构建项目

```ps1
powershell .\scripts\generate.ps1 Debug
powershell .\scripts\build.ps1 Debug
```

上面两条命令分别生成 build 目录和构建项目，将 `Debug` 改为 `Release` 可以构建 release 版本。如果安装了 CMake 还没支持的较新版本 VS，需要先手动进入 VS 2017 的 Developer Command Prompt，再执行上面的命令。

如果你使用 VS Code，可以直接运行 task；如果使用 VS，可以直接选择菜单 CMake - 全部生成。

### 安装插件到 酷Q

复制 `build/Debug/Debug`（如果是 release 编译则是 `build/Release/Release`）中的 DLL 和 JSON 文件到 酷Q 的 `app` 目录下，重启 酷Q 即可（注意需要开启 酷Q 的开发模式）。

如果不想每次构建后都手动安装插件，可以添加 [`scripts/install.ps1`](scripts/install.ps1) 文件（使用 UTF-16 LE 编码）如下：

```ps1
$libName = $args[0]
$outDir = $args[1]

$dllName = "$libName.dll"
$dllPath = "$outDir\$dllName"
$jsonName = "$libName.json"
$jsonPath = "$outDir\$jsonName"

Write-Host "正在拷贝插件到 酷Q 应用文件夹……"

Copy-Item -Force $dllPath "C:\path\to\coolq\app\$dllName" # 注意修改 酷Q 目录
Copy-Item -Force $jsonPath "C:\path\to\coolq\app\$jsonName"

Write-Host "拷贝完成" -ForegroundColor Green
```

后期生成事件脚本 [`scripts\post_build.ps1`](scripts\post_build.ps1) 发现存在 `scripts/install.ps1` 时会自动运行它，从而将构建出的 DLL 和 JSON 文件安装到 酷Q，此时在 酷Q 悬浮窗快速重启即可。

### 更新 SDK

```ps1
git submodule update
```

此命令会更新 `src/cqsdk` 中的 SDK 核心代码。

如果需要更新 `CMakeLists.txt`、`scripts` 等构建相关文件，使用 `git pull`，注意可能需要处理冲突。

### 安装依赖

如果需要安装依赖，请使用 triplet `x86-windows-static-custom`，参考如下命令：

```ps1
.\vcpkg\vcpkg.exe --triplet x86-windows-static-custom install curl
```

然后按需在 `CMakeLists.txt` 添加相应 `find_package` 语句和修改 `target_link_libraries`。注意，vcpkg 的 CMake 工具链文件有时并不能正确找到依赖的依赖的 LIB 文件，需要手动编写 `FindXxx.cmake` 文件，参考 [`cmake/Modules/FindIconv.cmake`](cmake/Modules/FindIconv.cmake)。

### 固定依赖包版本

对于依赖比较多的大型项目，依赖之间关系可能比较复杂，vcpkg 默认是直接安装最新版本，这会导致在部分依赖进行了不兼容的更新、而另一些依赖还没有跟进的情况下，整个项目无法编译。

[Vcpkg 官方建议的做法](https://github.com/Microsoft/vcpkg/blob/master/docs/about/faq.md#how-do-i-use-different-versions-of-a-library-on-one-machine) 是，使用 Git 将 `ports` 目录固定在一切 OK 的版本，例如：

```ps1
git checkout 7578a485b181ded330b87cc72726f01e38ff7ed6 -- ports
```

为了避免每次换开发环境都要手动 checkout，可以在项目根目录添加文件 `vcpkg-commit.txt` 如下：

```
7578a485b181ded330b87cc72726f01e38ff7ed6
```

内容是 Git commit 的 hash。`scripts/prepare.ps1` 脚本会自动在准备构建环境的时候将 `ports` 目录固定到此 commit 的版本。

## 插件生命周期

```
+-----------------------------------------+
|             Enabled At Start            |
+-----------------------------------------+
| on_initialize                           |
|       +                                 |
|       |                                 |
|       v                                 |
| on_coolq_start                          |
|       +                                 |
|       |                                 |
|       v     disabled by user            |
|   on_enable +--------------> on_disable |
|       +                           +     |
|       |                           |     |
|       v                           |     |
| on_coolq_exit <-------------------+     |
+-----------------------------------------+

+---------------------------------------+
|            Disabled At Start          |
+---------------------------------------+
| on_initialize +------+                |
|       +              |enabled by user |
|       |              |                |
|       |              v                |
|       |       on_coolq_start          |
|       |              +                |
|       |              |                |
|       |              v                |
|       |          on_enable            |
|       |              +                |
|       |              |                |
|       v              |                |
| on_coolq_exit <------+                |
+---------------------------------------+
```

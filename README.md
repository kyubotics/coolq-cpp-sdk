# CoolQ C++ SDK

[![License](https://img.shields.io/github/license/richardchien/coolq-cpp-sdk.svg)](LICENSE)
[![Build Status](https://img.shields.io/appveyor/ci/richardchien/coolq-cpp-sdk.svg)](https://ci.appveyor.com/project/richardchien/coolq-cpp-sdk)
[![QQ 群](https://img.shields.io/badge/qq%E7%BE%A4-590842375-orange.svg)](https://jq.qq.com/?_wv=1027&k=54T1cZB)
[![Telegram](https://img.shields.io/badge/telegram-chat-blue.svg)](https://t.me/cqhttp)

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

## 示例

```cpp
#include "cqsdk/cqsdk.h"

// namespace cq::app 包含插件本身的生命周期事件和管理
// namespace cq::event 用于注册 QQ 相关的事件处理函数
// namespace cq::api 用于调用酷 Q 提供的接口
// namespace cq::logging 用于日志
// namespace cq::message 提供封装了的 Message 等类

// 插件入口，在静态成员初始化之后，app::on_initialize 事件发生之前被执行，用于配置 SDK 和注册事件回调
CQ_MAIN {
    cq::app::on_enable = [] {
        // cq::logging、cq::api、cq::dir 等命名空间下的函数只能在事件回调函数内部调用，而不能直接在 CQ_MAIN 中调用
        cq::logging::debug(u8"启用", u8"插件已启动");
    };

    cq::event::on_private_msg = [](const cq::PrivateMessageEvent &e) {
        cq::logging::debug(u8"消息", u8"收到私聊消息：" + e.message + u8"，发送者：" + std::to_string(e.user_id));

        if (e.user_id != 1002647525) return;

        try {
            cq::api::send_private_msg(e.user_id, e.message); // echo 回去

            cq::api::send_msg(e.target, e.message); // 使用 e.target 指定发送目标

            // MessageSegment 类提供一些静态成员函数以快速构造消息段
            cq::Message msg = cq::MessageSegment::contact(cq::MessageSegment::ContactType::GROUP, 201865589);
            msg.send(e.target); // 使用 Message 类的 send 成员函数
        } catch (const cq::exception::ApiError &err) {
            // API 调用失败
            cq::logging::debug(u8"API", u8"调用失败，错误码：" + std::to_string(err.code));
        }

        e.block(); // 阻止事件继续传递给其它插件
    };

    cq::event::on_group_msg = [](const auto &e /* 使用 C++ 的 auto 关键字 */) {
        const auto memlist = cq::api::get_group_member_list(e.group_id); // 获取数据接口
        cq::Message msg = u8"本群一共有 "; // string 到 Message 自动转换
        msg += std::to_string(memlist.size()) + u8" 个成员"; // Message 类可以进行加法运算
        cq::message::send(e.target, msg); // 使用 message 命名空间的 send 函数
    };
}
```

更多请看 [src/demo.cpp](src/demo.cpp)。

## 使用方式

### 预备

本项目使用 [CMake](https://cmake.org/) 构建，依赖项通过 [vcpkg](https://github.com/Microsoft/vcpkg) 管理。如果你没有使用过这两个工具，请先前往它们的官方网站了解基本用法。

在开始使用之前，请确保你已经安装了 Git，且 `PATH` 中存在 `git` 命令。不需要安装 vcpkg，后面的脚本中会自动安装。

然后确保安装了 **Visual Studio 2017 或 2019**，并勾选「使用 C++ 的桌面开发」，确保安装了 CMake、**MSVC v141 或 v142**、**Windows 10 SDK** 这三个组件。其中，如果系统中已经安装了 CMake，无需再在 VS Installer 中安装，但需要确保命令已添加进 `PATH`。除此之外，vcpkg 还要求安装 VS 的**英文语言包**。

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

*注意，如果 PowerShell 提示不让运行脚本，需要先使用管理员权限打开 PowerShell，运行 `Set-ExecutionPolicy Unrestricted`，然后再重新运行上面的脚本；如果 vcpkg 安装依赖时出错，比较常见的问题是网络超时，请适当设置 `HTTP_PROXY` 和 `HTTPS_PROXY`。*

### 修改 App Id 和相关信息

修改 [`app_id.txt`](app_id.txt) 的内容为你的 App Id，例如 `com.company.my-awesome-app`。

按需修改 [`app.json`](app.json) 文件中的信息，通常需要修改 `name`、`version`、`version_id`、`author`、`description`，根据实际功能可能还需要修改 `menu` 和 `auth`。请不要修改 `event` 字段，因为事件处理函数的名字已经写死在了 SDK 中。

### 编写功能

移除 [`src/demo.cpp`](src/demo.cpp) 或在其基础上修改，实现自己的功能。

具体 API 请参考 `src/demo.cpp`，或顺着 [`src/cqsdk/cqsdk.h`](src/cqsdk/cqsdk.h) 头文件找进去，IDE 的自动补全帮助会很大。除此之外，还可以参考 [richardchien/coolq-http-api](https://github.com/richardchien/coolq-http-api) 项目。

**注意，所有代码文件必须使用 UTF-8 编码。如果你使用 VS，则它默认使用 ANSI 编码保存新创建的文件，需要手动修改为 UTF-8。**

### 构建项目

```ps1
powershell .\scripts\generate.ps1 Debug
powershell .\scripts\build.ps1 Debug
```

上面两条命令分别生成 build 目录和构建项目，将 `Debug` 改为 `Release` 可以构建 release 版本。如果安装了 CMake 还没支持的较新版本 VS，需要先手动进入 VS 2017 或 2019 的 Developer Command Prompt，再执行上面的命令。

如果你使用 VS Code，可以直接运行 task；如果使用 VS，可以直接选择菜单 CMake - 全部生成。

### 安装插件到 酷Q

复制 `build/Debug/Debug`（如果是 release 编译则是 `build/Release/Release`）中和你的 App Id 名字相同的文件夹到 酷Q 的 `dev` 目录下，在 酷Q 中重载应用即可（注意需要开启 酷Q 的开发模式）。

如果不想每次构建后都手动安装插件，可以添加 `scripts/install.ps1` 文件（使用 UTF-16 LE 编码）如下：

```ps1
$coolqRoot = "C:\Users\Richard\Lab\酷Q Pro" # 注意修改 酷Q 目录

$appId = $args[0]
$libName = $args[1]
$appOutDir = $args[2]

$coolqAppDevDir = "$coolqRoot\dev\$appId"
$dllName = "$libName.dll"
$dllPath = "$appOutDir\$dllName"
$jsonName = "$libName.json"
$jsonPath = "$appOutDir\$jsonName"

Write-Host "正在拷贝插件到 酷Q 应用文件夹……"

New-Item -Path $coolqAppDevDir -ItemType Directory -ErrorAction SilentlyContinue
Copy-Item -Force $dllPath "$coolqAppDevDir\$dllName"
Copy-Item -Force $jsonPath "$coolqAppDevDir\$jsonName"

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

如果需要安装依赖，可以直接使用 vcpkg，通过 `--triplet x86-windows-static-custom` 指定 triplet，或者使用 SDK 提供的包装脚本（参数和 vcpkg 相同），例如：

```ps1
.\scripts\vcpkg.ps1 install curl
```

然后按需在 `CMakeLists.txt` 添加相应 `find_package` 语句和修改 `target_link_libraries`。注意，vcpkg 的 CMake 工具链文件有时并不能正确找到依赖的依赖的 LIB 文件，需要手动编写 `FindXxx.cmake` 文件，参考 [`richardchien/coolq-http-api/cmake/Modules/FindCURL.cmake`](https://github.com/richardchien/coolq-http-api/blob/master/cmake/Modules/FindCURL.cmake)。

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

## 应用案例

| 项目地址 | 简介 |
| ------- | --- |
| [richardchien/coolq-http-api](https://github.com/richardchien/coolq-http-api) | 酷Q HTTP API 插件 |
| [JogleLew/coolq-telegram-bot-x](https://github.com/JogleLew/coolq-telegram-bot-x) | QQ / Telegram 群组消息转发机器人 |
| [dynilath/coolq-dicebot](https://github.com/dynilath/coolq-dicebot) | 酷Q 骰子机器人 |

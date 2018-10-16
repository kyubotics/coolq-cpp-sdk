# CoolQ C++ SDK（第三方）

[![License](https://img.shields.io/github/license/richardchien/coolq-cpp-sdk.svg)](LICENSE)
[![Build Status](https://img.shields.io/appveyor/ci/richardchien/coolq-cpp-sdk.svg)](https://ci.appveyor.com/project/richardchien/coolq-cpp-sdk)
[![QQ 群](https://img.shields.io/badge/qq%E7%BE%A4-201865589-orange.svg)](https://jq.qq.com/?_wv=1027&k=5Euplde)
[![Telegram](https://img.shields.io/badge/telegram-chat-blue.svg)](https://t.me/cqhttp)

CoolQ C++ SDK 封装了跟 DLL 接口相关的底层逻辑，包括：

- 将所有从酷 Q 传来的字符串转成 UTF-8，并将所有传入酷 Q 的字符串转成 GB18030
- 封装了 `Message` 和 `MessageSegment` 类，使构造消息内容更为方便
- `MessageSegment` 类提供了快速构造消息段（CQ 码）的接口
- 处理了消息内容中的 emoji 到 Unicode 的转换
- 封装了酷 Q 事件的数据，在事件处理函数中传入
- 将 QQ 相关的事件分为三个大类别：`MessageEvent`、`NoticeEvent`、`RequestEvent`
- 封装了数据类，如 `User`、`Group`、`GroupMember` 等
- ……

并且对外提供了更现代的 C++ 接口，从而为更方便地编写插件提供可能。

## 使用方式

本项目使用 [CMake](https://cmake.org/) 构建，依赖项通过 [Vcpkg](https://github.com/Microsoft/vcpkg) 管理。如果你没有使用过这两个工具，请先前往它们的官方网站了解基本用法。

可以直接用 VS Code 或 VS 打开项目，项目中的所有代码文件全部使用 UTF-8 编码，你后续添加的所有代码文件都需要使用 UTF-8 编码。**注意，如果你使用 VS，则它默认使用 ANSI 编码保存文件，需要手动修改为 UTF-8**。[`com.example.demo.json`](com.example.demo.json) 文件将在 [`scripts/post_build.ps1`](scripts/post_build.ps1) 脚本中被转换为酷 Q 要求的 GB18030 编码。

Vcpkg 使用如下 triplet：

```cmake
set(VCPKG_TARGET_ARCHITECTURE x86)
set(VCPKG_CRT_LINKAGE dynamic)
set(VCPKG_LIBRARY_LINKAGE static)
set(VCPKG_PLATFORM_TOOLSET v141)
```

你需要在 Vcpkg 的 `triplets` 文件夹中创建一个名为 `my-x86-windows-static.cmake` 的文件（文件名可以换为其它，但建议保留 `x86-windows-static` 这部分，似乎 Vcpkg 使用了文件名来判断要安装的包的版本），内容如上。创建了这个 triplet 之后，你需要将 [`scripts/generate.ps1`](scripts/generate.ps1) 中的 `$vcpkg_root`（vcpkg 根目录）和 `$vcpkg_triplet`（triplet 名称，例如 `my-x86-windows-static`）设置成你系统中的相应值（或设置环境变量），如果你使用 VS Code 或 VS 编辑项目，可以直接修改 `.vscode/tasks.json`（VS Code）或 `CMakeSettings.json`（VS）中的 `VCPKG_ROOT` 和 `VCPKG_TRIPLET` 环境变量，**注意，`.vscode/tasks.json` 中有两个 task 需要改**。

除此之外，还需要安装如下依赖（使用上面的 triplet）：

| 模块 | 依赖项 |
| --- | ----- |
| `cqsdk` | `boost-algorithm`<br>`libiconv` |

安装命令如下：

```ps1
cd vcpkg
.\vcpkg --vcpkg-root . --triplet my-x86-windows-static install boost-algorithm libiconv
```

构建成功后，可以在 `build/Debug/Debug` 或 `build/Release/Release` 中找到生成的 DLL 和 JSON 文件，直接拷贝到酷 Q 的 `app` 目录即可测试使用（酷 Q 需要开启开发模式）。

如果不想每次构建都手动拷贝这两个文件，可以在 `scripts` 目录添加文件 `install.ps1`（会被 `post_build.ps1` 在构建成功之后自动执行）如下：

```ps1
$lib_name = $args[0]
$out_dir = $args[1]

$dll_name = "${lib_name}.dll"
$dll_path = "${out_dir}\${dll_name}"
$json_name = "${lib_name}.json"
$json_path = "${out_dir}\${json_name}"

Copy-Item -Force $dll_path "C:\Applications\CQA\app\${dll_name}"
Copy-Item -Force $json_path "C:\Applications\CQA\app\${json_name}"
```

注意上面脚本中需要适当修改酷 Q 的路径。

接口的具体文档暂时就不写了，顺着 [`cqsdk.h`](src/cqsdk/cqsdk.h) 头文件找进去或者查看示例代码 [`demo.cpp`](src/demo.cpp) 基本就可以看明白。

请注意你在编写自己的插件时，一定要确保你的 JSON 描述文件和 [`com.example.demo.json`](com.example.demo.json) 文件的 `event` 中的 `function` 字段完全一致，因为 DLL 导出函数名已经在 [`app.cpp`](src/cqsdk/app.cpp) 和 [`event.cpp`](src/cqsdk/event.cpp) 写死了。

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

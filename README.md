# CoolQ C++ SDK（第三方）

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

项目使用 CMake 构建（可以直接用 VS Code 或 VS 打开），[`scripts/generate.ps1`](scripts/generate.ps1)、[`scripts/build.ps1`](scripts/build.ps1)、[`scripts/post_build.ps1`](scripts/post_build.ps1) 分别给出了生成、构建、安装的脚本，你可能需要对它们中的一些变量做适当修改以在你的系统中运行。

除了 [`com.example.demo.json`](com.example.demo.json) 文件为 GB18030 编码，其它代码文件均为 UTF-8 编码，且编译选项中使用了 `/utf-8`，你后续添加的所有代码文件都需要使用 UTF-8 编码。

项目的依赖项通过 [vcpkg](https://github.com/Microsoft/vcpkg) 管理，如果你没有使用过它，请先前往它的官方 repo 了解一下使用方法。

Vcpkg 使用如下 triplet：

```cmake
set(VCPKG_TARGET_ARCHITECTURE x86)
set(VCPKG_CRT_LINKAGE static)
set(VCPKG_LIBRARY_LINKAGE static)
set(VCPKG_PLATFORM_TOOLSET v141)
```

创建了这个 triplet 之后（建议命名为 `x86-windows-static`），你需要将 [`scripts/generate.ps1`](scripts/generate.ps1) 中的 `$vcpkg_root` 和 `$vcpkg_triplet` 设置成你系统中的相应值。

除此之外，还需要安装如下依赖（使用上面的 triplet）：

| 模块 | 依赖项 |
| --- | ----- |
| `cqsdk` | `boost-algorithm`<br>`boost-filesystem`<br>`libiconv` |

上述依赖项中的 `boost-filesystem` 只在获取插件目录相关接口中使用（具体在 [`dir.cpp`](src/cqsdk/dir.cpp)），如果你不需要使用这个功能，可以不安装，并直接删除 `dir.h` 和 `dir.cpp` 以及 `cqsdk.h` 中引入它的代码。

此外，由于代码使用了某些 C++17 的特性，所以需要安装 `v141` 工具集才可以编译。

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

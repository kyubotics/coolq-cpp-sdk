# 接口权限码列表

| 权限码 | 对应函数接口（省略 `CQ_` 前缀） | 备注 |
| ----- | --------------------------- | --- |
| 20    | `getCookies`、`getCsrfToken` | 获取 Cookies 和 CSRF Token |
| 30    | `getRecord` | 获取语音 |
| 101   | `sendGroupMsg` | 发送群消息 |
| 103   | `sendDiscussMsg` | 发送讨论组消息 |
| 106   | `sendPrivateMsg` | 发送私聊消息 |
| 110   | `sendLikeV2`、`sendLike` | 发送赞 |
| 120   | `setGroupKick` | 置群员移除 |
| 121   | `setGroupBan` | 置群员禁言 |
| 122   | `setGroupAdmin` | 置群管理员 |
| 123   | `setGroupWholeBan` | 置全群禁言 |
| 124   | `setGroupAnonymousBan` | 置匿名群员禁言 |
| 125   | `setGroupAnonymous` | 置群匿名设置 |
| 126   | `setGroupCard` | 置群成员名片 |
| 127   | `setGroupLeave` | 置群退出 |
| 128   | `setGroupSpecialTitle` | 置群成员专属头衔 |
| 130   | `getGroupMemberInfoV2`、`getGroupMemberInfo` | 取群成员信息 |
| 131   | `getStrangerInfo` | 取陌生人信息 |
| 140   | `setDiscussLeave` | 置讨论组退出 |
| 150   | `setFriendAddRequest` | 置好友添加请求 |
| 151   | `setGroupAddRequest` | 置群添加请求 |
| 160   | `getGroupMemberList` | 获取群成员列表 |
| 170   | `setRestart` | 重启酷Q（似乎无法使用） |

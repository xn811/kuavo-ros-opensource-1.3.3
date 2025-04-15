# Kuavo-CrashReport

## 描述

Kuavo-CrashReport 是一个用于收集、归档和上传夸父机器人崩溃日志的工具。

## 使用方法

### 首先确认您需要上传的日志目录

目前日志存放在 `~/.ros/stdout/` 目录下，因此您需要确认您需要上传的日志目录:
```bash
ls -lt ~/.ros/stdout/
```

### 上传日志文件

**比如我们选择上传`~/.ros/stdout/2025-04-10_14-30-45/`**

```bash
chmod +x ./tools/crash-report/CrashReport.sh
sudo su
./tools/crash-report/CrashReport.sh ~/.ros/stdout/2025-04-10_14-30-45/

# 以下是示例输出：

********************************************************************************
*                                                                              *
*                        Kuavo Crash Report Tool                               *
*                                                                              *
********************************************************************************

LAUNCH_ID: 478744
TIMESTAMP: 2025-04-11_15-03-00
GIT_BRANCH: chenmingfu/feat/tool/kuavo-crash-report
GIT_COMMIT: f1e881a74
-------------------------
📦 开始归档文件...
📦 正在压缩文件: /tmp/kuavo-crash/kuavo-crash_2025-04-11_15-03-00_f1e881a74.tar.gz
1.14GiB 0:00:07 [ 166MiB/s] [              <=>                                                                            ]
Successfully created archive: /tmp/kuavo-crash/kuavo-crash_2025-04-11_15-03-00_f1e881a74.tar.gz (129M)
📤 正在上传文件: /tmp/kuavo-crash/kuavo-crash_2025-04-11_15-03-00_f1e881a74.tar.gz
#################################################################################################################### 100.0%

🙏 感谢您的配合，📦 日志文件已上传成功，请将如下信息复制给乐聚技术支持人员:

用户日志已上传, 详情请查看: kuavo-crash_2025-04-11_15-03-00_f1e881a74.tar.gz
```

### 请拷贝消息给乐聚支持人员
```bash
用户日志已上传, 详情请查看: kuavo-crash_2025-04-11_15-03-00_f1e881a74.tar.gz
```
# 每日天气邮件 ☀️

自动获取重庆天气并发送到指定邮箱的 GitHub Actions 项目。

## ✨ 功能特点

- 🌤️ 自动获取重庆实时天气
- 📧 每日定时发送天气邮件
- 🎨 精美的 HTML 邮件模板
- 👔 智能穿衣建议
- 🚗 出行建议
- 🆓 完全免费（使用 GitHub Actions 免费额度）

## 📋 邮件内容

- 当前温度和天气状况
- 今日最高/最低温度
- 体感温度、湿度、风速、能见度、紫外线指数
- 日出日落时间
- 穿衣建议
- 出行建议

## 🚀 快速开始

### 1. 创建 GitHub 仓库

1. 访问 [GitHub](https://github.com) 并登录
2. 点击右上角 `+` → `New repository`
3. 仓库名称：`weather-email`（或你喜欢的名字）
4. 选择 `Public` 或 `Private`
5. 勾选 `Add a README file`
6. 点击 `Create repository`

### 2. 上传项目文件

将以下文件上传到你的 GitHub 仓库：

- `send_weather.py` - 主程序脚本
- `.github/workflows/daily-weather.yml` - GitHub Actions 配置

**方法一：网页上传**
1. 在仓库页面点击 `Add file` → `Upload files`
2. 拖拽这两个文件到页面
3. 提交更改

**方法二：Git 命令行**
```bash
git clone https://github.com/你的用户名/weather-email.git
cd weather-email
# 复制文件到此处
git add .
git commit -m "添加天气邮件脚本"
git push
```

### 3. 配置 QQ 邮箱授权码

1. 在 GitHub 仓库页面，点击 `Settings`
2. 在左侧菜单找到 `Secrets and variables` → `Actions`
3. 点击 `New repository secret`
4. Name 输入：`QQ_MAIL_PASSWORD`
5. Secret 输入：你的 QQ 邮箱 SMTP 授权码
6. 点击 `Add secret`

### 4. 启用 GitHub Actions

1. 在仓库页面，点击 `Actions` 标签
2. 如果看到 "Workflows aren't being run on this forked repository" 提示，点击 `I understand my workflows, go ahead and enable them`
3. 工作流程会自动启用

### 5. 测试运行

1. 在 `Actions` 标签页面
2. 点击左侧的 `每日天气邮件` 工作流
3. 点击 `Run workflow` → `Run workflow`
4. 等待执行完成（约1-2分钟）
5. 检查你的邮箱是否收到天气邮件

## ⚙️ 自定义配置

### 修改发送时间

编辑 `.github/workflows/daily-weather.yml` 文件，修改 `cron` 表达式：

```yaml
schedule:
  # 格式: 分 时 日 月 周
  # 注意：这是 UTC 时间，北京时间 = UTC + 8
  # 早上 7:00 北京 = 前一天 23:00 UTC
  - cron: '0 23 * * *'  # 早上 7:00
```

常用时间对照表：

| 北京时间 | UTC 时间 | Cron 表达式 |
|---------|----------|------------|
| 早上 6:00 | 前一天 22:00 | `0 22 * * *` |
| 早上 7:00 | 前一天 23:00 | `0 23 * * *` |
| 早上 8:00 | 前一天 0:00 | `0 0 * * *` |
| 晚上 9:00 | 当天 13:00 | `0 13 * * *` |

### 修改城市

编辑 `send_weather.py`，修改 `CITY` 变量：

```python
CITY = "Chongqing"  # 改为你想要的城市，如 "Beijing", "Shanghai" 等
```

### 修改收件人

编辑 `send_weather.py`，修改 `RECEIVER_EMAIL` 变量：

```python
RECEIVER_EMAIL = "你的邮箱@example.com"
```

## 📧 获取 QQ 邮箱授权码

1. 登录你的 QQ 邮箱
2. 点击 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**
4. 开启 **IMAP/SMTP服务**
5. 按照提示用手机发送短信验证
6. 验证成功后会显示 **授权码**（16位字符）
7. **保存好授权码**，配置时需要使用

## 🔍  troubleshooting

### 邮件没有收到

1. 检查 GitHub Actions 执行日志（仓库 → Actions → 选择运行记录）
2. 检查垃圾邮件文件夹
3. 确认 QQ_MAIL_PASSWORD secret 配置正确
4. 确认 QQ 邮箱已开启 SMTP 服务

### GitHub Actions 没有自动运行

- 确认仓库是 **Public** 或者你已经 **开通了 GitHub Actions 付费计划**（Private 仓库每月有免费额度限制）
- 检查 cron 表达式是否正确
- 手动触发一次测试

### 天气信息不准确

- wttr.in 提供的数据仅供参考
- 可以尝试修改城市名称（使用英文）

## 📊 执行日志

每次执行都会在 GitHub Actions 中留下记录，可以随时查看：

1. 进入仓库
2. 点击 `Actions` 标签
3. 选择运行记录查看详细日志

## 🎉 完成！

现在你的每日天气邮件已经配置完成！

每天早上 7:00（北京时间），系统会自动：
1. 获取重庆最新天气
2. 生成精美的 HTML 邮件
3. 发送到你的邮箱

祝你有美好的一天！😊

## 📝 许可证

MIT License

## 🙋 FAQ

**Q: GitHub Actions 免费吗？**
A: 是的！Public 仓库完全免费，Private 仓库每月有 2000 分钟免费额度。

**Q: 可以发送给多个收件人吗？**
A: 可以！修改 `send_weather.py` 中的邮件发送部分，添加多个收件人。

**Q: 能添加附件吗？**
A: 可以！修改 `send_email` 函数，使用 `MIMEApplication` 添加附件。

**Q: 如何停止自动发送？**
A: 在 GitHub 仓库的 Actions 标签中，选择工作流，点击 `Disable workflow`。

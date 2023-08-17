# 代理IP请求工具

这个工具允许你使用代理IP并发地发送HTTP请求。它使用`ThreadPoolExecutor`来并发地处理URL列表，并使用代理IP来发送请求。如果请求失败，它会自动重试或更换代理IP。

## 主要功能

1. 从`https://sslproxies.org/`获取代理IP列表。
2. 使用`ThreadPoolExecutor`并发地处理URL列表。
3. 自动重试和更换代理IP。
4. 线程安全地访问和修改代理池。

## 如何使用

1. 首先，你需要安装必要的库：

```bash
pip install requests beautifulsoup4
```

2. 将仓库代码下载为`proxy_request_tool.py`。

3. 在代码的底部，你可以修改`url_list`变量来指定你想要请求的URL列表。

4. 运行代码：

```bash
python proxy_request_tool.py
```

5. 代码会并发地处理URL列表，并使用代理IP发送请求。响应会被保存在`responses`列表中。

## 配置

你可以根据需要修改以下参数：

- `max_retries`: 最大重试次数。
- `retry_interval`: 重试间隔（秒）。
- `max_ip_changes`: 最大代理IP更换次数。
- `max_ip_failures`: 一个代理IP连续失败的最大次数。
- `max_workers`: `ThreadPoolExecutor`的最大工作线程数。

## 注意事项

1. 代理IP的质量可能会有所不同，所以建议经常更新代理IP列表。
2. 如果你遇到了任何问题，可以查看代码中的注释或联系作者。

## 贡献

欢迎任何形式的贡献，包括错误报告、功能建议或代码提交。

## 许可

这个工具是基于MIT许可发布的。你可以自由地使用、修改和分发这个工具，但请保留原始许可和版权声明。

---

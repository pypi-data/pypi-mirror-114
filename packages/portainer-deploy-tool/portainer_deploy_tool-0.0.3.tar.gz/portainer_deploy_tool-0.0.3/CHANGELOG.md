# 0.0.3

## 接口修改

+ 子命令`updateservicebywebhook`的`tokens`参数现在是位置参数
+ 子命令`updateservicebywebhook`现在可以用执行目录下的`update_service_by_webhooks_config.json`文件作为配置
+ 子命令`createorupdatestack`的`endpoints`参数现在是位置参数
+ 子命令`createorupdatestack`现在可以用执行目录下的`create_or_update_stack_config.json`文件作为配置
+ 子命令`updateserviceinstack`的`deploy_path`参数参数现在是位置参数
+ 子命令`updateserviceinstack`现在可以用执行目录下的`update_service_in_stack_config.json`文件作为配置

## bug修复

+ 修复`updateservicebywebhook`的调用url错误

# 0.0.2

## 接口修改

+ `updateservicebywebhook`现在可以设置多个token
+ `artifact_version`和`tag_prefix`参数被取消
+ 现在`retry_max_times`和`retry_interval_backoff_factor`作为哦三个子命令的共有参数,`retry_interval`被移除,现在重试的间隔时间将根据公式`{backoff factor} * (2 ** ({number of total retries} - 1))`获得

# 0.0.1

项目创建
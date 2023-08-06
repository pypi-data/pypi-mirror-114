# 0.0.2

## 接口修改

+ `updateservicebywebhook`现在可以设置多个token
+ `artifact_version`和`tag_prefix`参数被取消
+ 现在`retry_max_times`和`retry_interval_backoff_factor`作为哦三个子命令的共有参数,`retry_interval`被移除,现在重试的间隔时间将根据公式`{backoff factor} * (2 ** ({number of total retries} - 1))`获得

# 0.0.1

项目创建
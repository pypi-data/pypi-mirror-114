# portainer_deploy_tool

使用portainer部署更新服务的工具

## 使用

本工具提供pip安装`pip install portainer_deploy_tool`以及docker镜像`hsz1273327/portainer_deploy_tool`

docker镜像中已经申明了`ENTRYPOINT [ "python","-m", "portainer_deploy_tool"]`

支持3个子命令:

+ `updateserviceinstack`用于更新某个服务对应的镜像后根据指定的路径更新stack

+ `updateservicebywebhooks`用于在portainer上激活webhook后通过调用webhook更新服务(不建议指定tag,这会让stack和实际执行不一致)

+ `createorupdatestack`用于根据目录下的指定后缀的文件来创建或者更新stack配置.

具体参数及含义可以用`-h`命令查看
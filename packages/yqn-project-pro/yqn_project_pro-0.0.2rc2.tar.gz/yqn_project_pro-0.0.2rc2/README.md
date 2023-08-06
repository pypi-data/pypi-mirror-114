# yqn_project_pro
#### For more faster to create semi-project based on flask

##console runner
####new_json_config_file由初始项目json_config_file复制过来，后续整个项目生命周期的路由部分以新文件为依据
<br/>初始化项目：yqn-project -c absolute_json_config_file_path</br>
<br/>初始化或更新module：yqn-autoview - c new_json_config_file_path</br>

##json-config-file format:
```json
{
  "app_id": 22010,
  "app_name": "project_name",
  "app_path": "absolute_project_dir_path",
  "path_list": [
    {
      "path": "/index/", 
      "module": "main",
      "view_cls": "Index",
      "view_mth": "get_index",
      "http_methods": ["GET", "POST"],
      "doc": "默认"
    },
    {
      "path": "/tool/",
      "module": "tool",
      "view_cls": "Index",
      "view_mth": "get_tool",
      "http_methods": ["GET", "POST"],
      "doc": "工具"
    }
  ]
}
```

##json-file参数解释：
<br/>app_id：项目唯一数字标识</br>
<br/>项目(app_name)位于路径(app_path)下</br>
<br/>path_list：所有需路由对象信息数组</br>
<br/>path: http请求路径</br>
<br/>module: api下的对应模块，便于分块，如 main、tool</br>
<br/>view_cls: api对应模块下views.py文件内的视图类, 如 Index</br>
<br/>view_mth: 对应视图类下实例方法, 如 get_index、get_tool，http请求时产生调用</br>
<br/>http_methods: 支持http请求方式</br>
<br/>doc: 方法doc描述</br>

****
##初始项目结构描述（api/common/config/rpc/scripts/thirds/utils,以及入口和打包文件）
###api:接口模块
#####api.*子模块：
######1.handler:功能逻辑
######2.model:模型定义
######3.parser:参数解析校验
######4.views:视图逻辑
<br/></br>
###common:通用或不明晰模块
<br/></br>
###config:项目配置
<br/></br>
###rpc(http):调用封装
<br/></br>
###scripts:脚本罗列
<br/></br>
###thirds:三方插件
<br/></br>
###utils：功能函数
<br/></br>
###其他：一些入口或打包文件




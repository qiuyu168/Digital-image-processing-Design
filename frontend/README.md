# 项目目录结构
```
frontend/
├── .vscode/                         # VS Code 配置目录
├── node_modules/                    # 项目依赖目录
├── public/                          # 公共静态资源目录
│   └── favicon.ico                  # 网站图标
├── src/                             # 项目核心源码目录
│   ├── api/                         # 接口请求封装
│   │   └── http.js                  # axios 请求实例与接口基础配置
│   ├── assets/                      # 项目静态资源
│   │   ├── background/
│   │   │   ├── bg1.jpg
│   │   │   ├── bg2.jpg
│   │   │   ├── bg3.jpg
│   │   │   ├── bg4.jpg
│   │   └── home_bg.jpg
│   ├── components/                  # 公共组件目录
│   │   ├── AppFooter.vue            # 页脚组件
│   │   ├── HeaderNav.vue            # 页头导航栏组件
│   │   └── MainLayout.vue           # 主布局组件
│   ├── router/                      # 路由配置目录
│   │   └── index.js                 # Vue Router 路由配置
│   ├── stores/                      # 状态管理目录
│   │   └── authStore.js             # 用户登录认证状态管理
│   ├── styles/                      # 全局样式目录
│   │   └── index.scss               # 全局 SCSS 样式文件
│   ├── utils/                       # 工具函数目录
│   │   ├── check_health.js          # 后端健康检查工具
│   │   └── token.js                 # Token 存取与处理工具
│   ├── views/                       # 页面视图目录
│   │   ├── HomeView.vue             # 首页页面
│   │   ├── LoginView.vue            # 登录 / 注册页面
│   │   ├── UserProfileView.vue      # 用户个人信息页面
│   │   └── WorkspaceView.vue        # 图像处理工作区页面
│   ├── App.vue                      # 根组件
│   └── main.js                      # 项目入口文件
├── .env.development                 # 开发环境变量配置
├── .gitignore                       # Git 忽略文件配置
├── index.html                       # Vite 项目 HTML 入口
├── jsconfig.json                    # JavaScript 路径与编辑器配置
├── package.json                     # 项目依赖与脚本配置
├── pnpm-lock.yaml                   # pnpm 依赖锁定文件
├── pnpm-workspace.yaml              # pnpm 工作区配置
├── README.md                        # 项目说明文档
└── vite.config.js                   # Vite 构建工具配置
```
# 如何运行前端项目

## 配置环境

先前往 https://node.org.cn/en 下载**Node.js**，打开cmd，进入项目根目录，依次执行：

```bash
npm install -g pnpm                     # 全局安装 pnpm 包管理器

cd frontend                             # 进入前端项目对应的文件夹

pnpm install                            # 根据package.json中的内容安装依赖
```

完成后便可成功配置项目环境。

有关项目中用到的第三方包：

```bash
# 全局安装 pnpm 包管理器
npm install -g pnpm

# 进入前端项目对应的文件夹
cd frontend

# 状态管理
pnpm add pinia                           # Pinia 状态管理库
pnpm add pinia-plugin-persistedstate     # Pinia 持久化插件

# 路由
pnpm add vue-router@4                    # Vue Router 4

# HTTP 请求
pnpm add axios                           # Axios HTTP 客户端

# UI 框架及相关
pnpm add element-plus                    # Element Plus UI 组件库
pnpm add @element-plus/icons-vue         # Element Plus 图标库

# 样式预处理
pnpm add sass -D                         # Sass/SCSS 预处理器

# Vite 自动导入插件
pnpm add -D unplugin-vue-components \    # 按需自动导入 Element Plus 等组件
           unplugin-auto-import          # 自动导入 Vue/Element Plus 等 API

# 图标库
pnpm add echarts vue-echarts
```

## 运行

打开cmd，进入项目根目录，执行：

```bash
cd frontend                             # 进入前端项目对应的文件夹

pnpm dev                                # 运行项目，但只能在本地运行

pnpm dev --host                         # 运行项目，但可以在网络环境中运行
```

运行成功后，在浏览器打开显示的url地址，能看到五个按钮。
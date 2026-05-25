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
# 动漫图像处理系统前端说明文档

本目录为“动漫图像处理系统”的前端部分，基于 Vue 3 + Vite 构建，主要负责页面展示、用户交互、图像上传、算法参数配置、图像库浏览以及与后端 FastAPI 接口进行数据交互。

本说明文档只介绍前端项目的运行、结构和维护方式，不包含后端项目说明。

---

## 一、项目简介

本前端项目面向数字图像处理课程设计场景，提供以下主要功能：

1. 首页展示系统介绍、功能流程和算法模块。
2. 登录 / 注册页面提供本地测试登录逻辑。
3. 图像处理工作区支持：
   - 动态获取后端算法列表；
   - 根据算法元数据动态生成参数表单；
   - 上传本地图像；
   - 调用对应算法运行接口；
   - 展示处理结果、步骤图、指标和分析信息。
4. 图像库页面支持：
   - 获取图像分类；
   - 按分类浏览图像；
   - 点击图片全屏预览；
   - 查看图像参数；
   - 下载或打开图像资源。
5. 用户个人信息页面提供基础信息展示和本地交互功能。
6. 404 页面用于处理不存在的路由。

---

## 二、技术栈

| 技术 | 作用 |
| --- | --- |
| Vue 3 | 前端核心框架 |
| Vite | 前端构建与开发服务器 |
| Vue Router | 前端路由管理 |
| Pinia | 状态管理 |
| pinia-plugin-persistedstate | 登录状态本地持久化 |
| Element Plus | UI 组件库 |
| @element-plus/icons-vue | Element Plus 图标 |
| Axios | HTTP 请求封装 |
| SCSS / Sass | 样式编写 |
| ECharts / vue-echarts | 图表扩展依赖，后续可用于直方图等可视化 |

---

## 三、运行环境要求

项目 `package.json` 中声明的 Node.js 版本要求为：

```txt
Node.js ^20.19.0 或 >=22.12.0
```

推荐使用：

```txt
Node.js 20.19+
pnpm
```

如果本机没有 pnpm，可以先安装：

```bash
npm install -g pnpm
```

---

## 四、安装与运行

### 1. 安装依赖

进入前端项目目录后执行：

```bash
pnpm install
```

### 2. 启动开发服务器

```bash
pnpm dev
```

默认开发地址为：

```txt
http://127.0.0.1:5173
```

---

## 五、环境变量配置

开发环境变量位于：

```txt
.env.development
```

当前主要配置如下：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_APP_TITLE=动漫图像处理系统
```

### 变量说明

| 变量名 | 说明 |
| --- | --- |
| `VITE_API_BASE_URL` | 后端 FastAPI 服务地址 |
| `VITE_APP_TITLE` | 项目名称，用于浏览器网页标题 |

---

## 六、项目目录结构

```txt
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── api/
│   │   ├── algorithms.js
│   │   ├── health.js
│   │   ├── http.js
│   │   ├── library.js
│   │   ├── run.js
│   │   └── upload.js
│   ├── assets/
│   │   ├── background/
│   │   └── home_bg.jpg
│   ├── components/
│   │   ├── AppFooter.vue
│   │   ├── HeaderNav.vue
│   │   └── MainLayout.vue
│   ├── router/
│   │   └── index.js
│   ├── stores/
│   │   └── authStore.js
│   ├── styles/
│   │   └── index.scss
│   ├── utils/
│   │   ├── check_health.js
│   │   └── token.js
│   ├── views/
│   │   ├── HomeView.vue
│   │   ├── LibraryView.vue
│   │   ├── LoginView.vue
│   │   ├── NotFoundView.vue
│   │   ├── UserProfileView.vue
│   │   └── WorkspaceView.vue
│   ├── App.vue
│   └── main.js
├── .env.development
├── index.html
├── package.json
├── pnpm-lock.yaml
└── vite.config.js
```

---

## 七、核心目录说明

### 1. `src/api`

用于统一管理接口请求。

| 文件 | 作用 |
| --- | --- |
| `http.js` | Axios 实例封装，统一设置 `baseURL`、超时时间、请求拦截器和响应拦截器 |
| `health.js` | 健康检查接口 |
| `algorithms.js` | 获取后端算法元数据 |
| `upload.js` | 上传图片接口 |
| `library.js` | 图像库分类、图像列表、图像参数接口 |
| `run.js` | 预留的运行接口文件 |

### 2. `src/views`

用于存放页面级组件。

| 页面 | 路由 | 说明 |
| --- | --- | --- |
| `HomeView.vue` | `/home` | 首页 |
| `WorkspaceView.vue` | `/workspace` | 图像处理工作区 |
| `LibraryView.vue` | `/library` | 图像库 |
| `UserProfileView.vue` | `/profile` | 用户个人信息 |
| `LoginView.vue` | `/login` | 登录 / 注册 |
| `NotFoundView.vue` | 兜底路由 | 404 页面 |

### 3. `src/components`

用于存放公共布局组件。

| 组件 | 说明 |
| --- | --- |
| `HeaderNav.vue` | 页头导航栏 |
| `AppFooter.vue` | 页脚版权信息 |
| `MainLayout.vue` | 主布局组件，包含页头、页面主体和页脚 |

### 4. `src/stores`

用于 Pinia 状态管理。

当前包含：

```txt
authStore.js
```

主要保存：

- `token`
- `userInfo`
- `isLogin`
- 登录信息设置方法
- 登录信息清除方法

并通过 `pinia-plugin-persistedstate` 实现本地持久化。

---

## 八、路由说明

路由配置位于：

```txt
src/router/index.js
```

当前路由结构如下：

```txt
/              -> 重定向到 /home
/login         -> 登录注册页
/home          -> 首页
/workspace     -> 图像处理工作区
/library       -> 图像库
/profile       -> 用户个人信息
任意不存在路径 -> 404 页面
```

每个页面通过 `meta.title` 设置页面标题，例如：

```js
{
  path: 'workspace',
  name: 'Workspace',
  component: () => import('@/views/WorkspaceView.vue'),
  meta: {
    title: '图像处理'
  }
}
```

项目会在路由切换后自动设置浏览器标题：

```txt
页面名称 - 项目名称
```

例如：

```txt
图像处理 - 动漫图像处理系统
```

---

## 九、接口说明

前端通过 `src/api/http.js` 中封装的 Axios 实例访问后端。

基础地址来自：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

因此前端代码中请求：

```js
http.get('/api/algorithms')
```

实际请求地址为：

```txt
http://127.0.0.1:8000/api/algorithms
```

---

## 十、已使用的后端接口

### 1. 健康检查

```txt
GET /api/health
```

用于检查后端服务是否正常。

相关文件：

```txt
src/api/health.js
src/utils/check_health.js
```

---

### 2. 获取算法列表

```txt
GET /api/algorithms
```

用于获取所有算法大类、小类以及每个算法的参数元数据。

相关文件：

```txt
src/api/algorithms.js
src/views/WorkspaceView.vue
```

前端会根据后端返回的 `modules`、`algorithms`、`params` 动态生成：

- 左侧算法菜单；
- 算法说明；
- 参数表单；
- 默认参数值；
- 表单控件类型。

---

### 3. 上传图片

```txt
POST /api/upload/image
```

请求格式为 `FormData`，字段名为：

```txt
file
```

相关文件：

```txt
src/api/upload.js
src/views/WorkspaceView.vue
```

前端会在上传前校验：

- 文件格式；
- 文件大小；
- 图片分辨率；
- 图片是否可以正常读取。

当前允许的格式：

```txt
jpg, jpeg, png, bmp, webp, tif, tiff
```

当前限制：

```txt
最小大小：10KB
最大大小：5MB
最小分辨率：128 × 128
最大分辨率：4096 × 4096
```

---

### 4. 运行算法

工作区会根据算法所属大类调用不同接口。

| 算法大类 | 接口 |
| --- | --- |
| 灰度图像类 | `/api/algorithms/grayscale-image/run` |
| 彩色图像类 | `/api/algorithms/color-image/run` |
| 几何变换类 | `/api/algorithms/geometric-transform/run` |
| 空域滤波类 | `/api/algorithms/spatial-filter/run` |
| 频域分析类 | `/api/algorithms/frequency-analysis/run` |
| 频域滤波类 | `/api/algorithms/frequency-filter/run` |

请求体示例：

```json
{
  "source_type": "upload",
  "image_path": "上传后返回的 image_path",
  "algorithm": "算法 name",
  "algorithm_display_name": "算法 display_name",
  "params": {},
  "return_steps": true
}
```

前端会展示后端返回的：

- 处理结果图；
- 处理步骤；
- 指标信息；
- 分析说明；
- 运行状态。

---

### 5. 获取图像库分类

```txt
GET /api/library/categories
```

相关文件：

```txt
src/api/library.js
src/views/LibraryView.vue
```

用于获取图像库侧边栏分类。

---

### 6. 按分类获取图像列表

```txt
GET /api/library/images?category=分类名
```

相关文件：

```txt
src/api/library.js
src/views/LibraryView.vue
```

当用户点击左侧分类时，前端会重新请求该分类下的图像列表。

---

### 7. 获取图像参数

```txt
POST /api/analysis/metrics
```

相关文件：

```txt
src/api/library.js
src/views/LibraryView.vue
```

请求体示例：

```json
{
  "source_type": "library",
  "image_path": "图像路径",
  "include_histogram": false
}
```

前端会将返回的图像参数转换为中文展示，例如：

| 字段 | 中文显示 |
| --- | --- |
| `width` | 图像宽度 |
| `height` | 图像高度 |
| `channels` | 通道数量 |
| `dtype` | 数据类型 |
| `mean` | 像素均值 |
| `std` | 像素标准差 |
| `min` | 最小像素值 |
| `max` | 最大像素值 |

---

## 十一、主要页面说明

### 1. 首页 `HomeView.vue`

首页主要用于展示系统整体介绍，包括：

- 轮播欢迎区；
- 功能流程；
- 六大算法模块；
- 项目特色。

首页中的按钮可以跳转到图像处理工作区或个人信息页面。

---

### 2. 工作区 `WorkspaceView.vue`

工作区是图像处理功能的核心页面。

主要流程：

```txt
获取算法列表
    ↓
选择算法大类和具体算法
    ↓
根据 params 动态生成参数表单
    ↓
上传图片
    ↓
点击开始处理
    ↓
调用对应算法运行接口
    ↓
展示处理结果
```

工作区中的算法表单不是写死的，而是根据后端 `/api/algorithms` 返回的参数元数据动态生成。

支持的参数控件包括：

| 参数类型 | 前端控件 |
| --- | --- |
| `int` | 数字输入 / 滑块 |
| `float` | 数字输入 / 滑块 |
| `odd_int` | 奇数数字输入 / 滑块 |
| `select` | 下拉选择框 |
| `bool` | 开关 |
| 其他类型 | 文本输入框 |

---

### 3. 图像库 `LibraryView.vue`

图像库页面用于浏览后端提供的示例图像。

主要流程：

```txt
获取图像分类
    ↓
渲染左侧分类栏
    ↓
点击分类
    ↓
请求该分类下的图像
    ↓
展示图片列表
    ↓
点击图片全屏预览
    ↓
点击查看参数
    ↓
请求并展示图像参数
```

每张图片下方提供：

- 查看参数；
- 获取图片。

---

### 4. 登录注册页 `LoginView.vue`

当前登录注册页主要用于前端测试。

登录逻辑：

1. 校验用户名和密码；
2. 本地生成测试 token；
3. 保存到 Pinia；
4. 跳转首页。

当前没有真正调用后端登录注册接口。

---

### 5. 用户个人信息页 `UserProfileView.vue`

用户个人信息页用于展示和编辑本地用户信息，包括：

- 基本资料；
- 头像预览；
- 密码设置表单；
- 本地交互提示。

部分功能当前为前端本地模拟，后续可以接入真实用户接口。

---

### 6. 404 页面 `NotFoundView.vue`

当用户访问不存在的路由时，会进入 404 页面。

---

## 十二、样式说明

项目整体采用偏动漫、清新、半透明玻璃拟态风格。

主要样式特点：

- 固定顶部导航栏；
- 半透明背景；
- 圆角卡片；
- 柔和阴影；
- Element Plus 组件二次美化；
- 页面中大量使用 `scoped SCSS`，减少样式污染。

全局基础样式位于：

```txt
src/styles/index.scss
```

---

## 十三、登录状态说明

登录状态由 Pinia 管理，文件为：

```txt
src/stores/authStore.js
```

保存内容包括：

```js
token
userInfo
```

通过：

```js
persist: true
```

实现本地持久化。

退出登录时会清空：

```js
token
userInfo
```

---

## 十四、开发注意事项

### 1. 新增页面

新增页面时，一般需要完成三步：

1. 在 `src/views` 中新建页面组件；
2. 在 `src/router/index.js` 中添加路由；
3. 如果需要显示在导航栏中，修改 `src/components/HeaderNav.vue` 的 `navItems`。

---

### 2. 新增接口

新增接口时，建议在 `src/api` 下新建或修改对应模块文件。

例如：

```js
import http from './http'

export const exampleService = (params) => {
  return http.get('/api/example', { params })
}
```

页面中再引入使用：

```js
import { exampleService } from '@/api/example'
```

---

### 3. 修改项目名称

修改 `.env.development`：

```env
VITE_APP_TITLE=新的项目名称
```

同时可以修改：

- `HeaderNav.vue` 中的 Logo 文本；
- `AppFooter.vue` 中的版权文本；
- `index.html` 中的默认 `<title>`。

---

### 4. 修改后端地址

修改 `.env.development`：

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

如果后端端口变化，例如改为 `9000`，则改成：

```env
VITE_API_BASE_URL=http://127.0.0.1:9000
```

修改后需要重启前端开发服务器。

---

## 十五、常见问题

### 1. 页面能打开，但接口请求失败

检查：

1. 后端 FastAPI 是否已经启动；
2. `.env.development` 中的 `VITE_API_BASE_URL` 是否正确；
3. 浏览器控制台 Network 中的请求地址是否正确；
4. 后端是否允许当前前端地址跨域访问。

---

### 2. 修改 `.env.development` 后没有生效

Vite 环境变量在启动时读取，修改后需要重新运行：

```bash
pnpm dev
```

---

### 3. 工作区没有算法列表

检查后端接口：

```txt
GET /api/algorithms
```

是否正常返回：

```json
{
  "modules": []
}
```

如果 `modules` 为空，前端无法生成算法菜单和参数表单。

---

### 4. 上传图片失败

检查：

1. 图片格式是否支持；
2. 图片大小是否在 10KB 到 5MB 之间；
3. 图片分辨率是否在 128×128 到 4096×4096 之间；
4. 后端 `/api/upload/image` 是否正常；
5. 后端返回值中是否包含 `image_path`。

---

## 十六、可用脚本

```bash
pnpm dev
```

启动开发服务器。

---

## 十七、当前前端项目状态

当前前端已经完成：

- 首页；
- 登录注册页；
- 主布局；
- 页头导航栏；
- 页脚；
- 图像处理工作区；
- 图像库；
- 用户个人信息页；
- 404 页面；
- Axios 请求封装；
- Pinia 登录状态管理；
- 页面标题动态设置；
- 与主要后端接口的前后端对接。

后续可继续扩展：

- 真实用户登录注册接口；
- 用户头像上传接口；
- 图像处理历史记录；
- 图像参数图表化展示；
- 处理结果下载；
- 图像库搜索与筛选；
- 更完整的错误状态展示。
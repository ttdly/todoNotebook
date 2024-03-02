# 一款 TODO 应用

使用 flask+vue 实现的一个代办记录本应用

## 功能

按等级添加待办事项，一共三级，待办事项有`进行`、`中止`、`完成`三种状态。

对待办事项添加记录、查看某一待办事项的所有笔记。

通过日历视图来查看对应日期有增加记录的代办事项。

待办事项的排序规则：等级按照紧急、重要、随意顺序排列，等级相同的情况下按照创建日期从小到大排列。

注意：除了待办事项的状态能够修改以外，所有的数据均无修改和删除功能，除非直接在资源管理器中进行修改。

## 开发

### 前端
`front` 文件夹对应 vue 项目

#### 安装依赖

```bash
pnpm install
```

#### 启动

```bash
pnpm dev
```

### 后端
`server` 文件夹对应 flask 项目

#### 安装依赖
```bash
pip install -r requirements.txt
```
#### 启动
```bash
python app.py
```

### 打包

首先安装 `pyinstaller`

然后在 `front` 目录下运行 `pnpm build`，再在 `server` 目录下运行 `pyinstaller myapp.spec`

`icon.ico` 是应用的图标文件

### 运行

找到 `server/dist/myapp.exe` 双击即可运行。

运行时会留下一个终端界面并且自动打开一个页面，如果想要关闭程序，关掉终端页面即可。
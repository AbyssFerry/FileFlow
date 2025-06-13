# 📁 FileFlow - 智能文件分类工具

> 本地文档太多太乱？让 FileFlow 帮你一键智能分类整理！
---
## 🚀 项目简介

**FileFlow** 是一款基于AI的智能文件分类工具，支持自动解析、分类本地文件、 自然语言查找等。它适用于学生、办公人员等需要管理大量文档的场景。

- 🧠 内容识别 + 元数据提取，精准理解文档含义
    
- 📂 AI 自动多级分类（如：课程资料、论文、简历、合同等）
    
- 🔄 新文件AI自动归类，无需手动整理
    
- 🔍 自然语言快速查找文件，支持“宿舍相关”等语句
    
- 🖥️ 图形界面支持，简单直观操作

---

## 📸 项目演示
[FileFlow 软件演示视频](doc/FileFlow软件演示.mp4)

---

## 🛠️ 功能特点

- ✅ 文档解析：支持 PDF、Word、Excel 格式
    
- ✅ 智能分类：基于大模型的语言理解
    
- ✅ SQLite：本地数据库持久化
    
- ✅ GUI：使用 PyQt5 构建可视化操作界面
    
- ✅ 轻量：极简轻量文件
    

---

## 🧱 项目架构

```
FileFlow                    # 项目根目录
├─ doc/                    # 项目文档，比如设计文档、使用说明等
├─ fileflow_database.db    # SQLite数据库文件，存储项目运行数据
├─ README.md               
├─ requirements.txt        # Python依赖包列表
├─ run_app.py              # 启动程序主脚本
├─ run_app.spec            # PyInstaller打包相关配置
└─ src                     # 源代码目录
   ├─ controllers/        # 控制层代码，负责业务逻辑处理
   ├─ controllers_for_ai/ # 针对AI功能的专门控制模块
   ├─ storage/            # 数据存储相关代码，如数据库操作封装
   └─ ui/                 # 用户界面相关代码，界面设计和交互逻辑


```

---

## 📦 安装使用

### 1. 克隆仓库

```bash
git clone git@gitee.com:abyssferry/file-flow.git
cd FileFlow
```

### 2. 安装依赖

```bash
conda create -n fileflow python=3.12
conda activate fileflow
pip install -r requirements.txt
```

### 3. 启动应用

```bash
python run_app.py
```

---

## 🧪 示例数据

你可以使用项目中的 `sample_docs/` 文件夹进行快速体验，内含：

- 学术论文
    
- 求职简历
    
- 报告与备忘录
    

---
## 🤝 贡献

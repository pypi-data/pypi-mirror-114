# Wisdoms Dapr

用于Dapr FastAPI微服务开发的工具包。

## 包目录结构

- elasticsearch elasticsearch代码抽象
- config.py 项目配置管理
- exceptions.py 统一的异常管理
- logger.py 自定义日志 

## 项目发布

### **发布环境**

> pip install build pip setuptools wheel twine

### **构建pip包**

> python3 -m build

步骤：

1. 切换到打包根目录

2. 执行build命令

3. 检查是否成功构建至dist目录

### **测试pip包**

> pip install dist/*.whl

### **发布pip包**

> twine upload dist/*

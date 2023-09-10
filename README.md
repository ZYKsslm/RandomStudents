# RandomStudents
> 使用Python制作的一个软件，用于方便老师上课点人回答问题


## 简介
由于老师上课需要抽人回答问题，但同学们都非常~~害怕~~腼腆而不敢举手，我便制作了一款小巧简洁的软件可以代替老师点人，防止造成尴尬的局面。

同时，程序还支持调整权重的功能，希望老师不要偏心呢（笑）。

## 安装依赖
1. 有Python环境请直接下载仓库到本地，进入仓库目录后进入终端使用以下命令安装依赖：

```python
pip install -r requirements.txt
```
2. 若没有环境请到release下载打包后的程序

## 使用
请在data.json文件中修改抽取信息。

data.json文件中包含一个字典，键为名字，值为权重。你可以添加你想要的名字。

在软件中更改权重会自动保存。
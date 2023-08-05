# ICL

## 版本

0.0.0

## 简介

该库的目标是实现类似于C++中boost::icl的区间库

boost::icl可以参考https://www.boost.org/doc/libs/1_76_0/libs/icl/doc/html/index.html#boost_icl.introduction

## 目标

按照joining规则实现区间集合ItvSet

按照splitting规则实现区间映射表ItvMap

关于规则的定义可关于boost::icl的链接

## 当前进度

ItvSet基本功能已完成，但缺少足够的测试

## 主要类型

Itv: Interval表示区间

ItvSet：区间集合

## 测试

单元测试使用pytest

测试全部存放在test文件夹中

## 路径

inc/icl 			模块位置

test            测试目录， 按照pytest规则写

## 示例

{[1,5]} ⋃ {[3,7]} = {[1,7]}

{[1,5]} ⋃ {[3,7]} ⋃ {[11, 17]}= {[1,7], [11, 17]}

{[1,5]} ∩ {[3,7]} = {[3,5]}

{[1,7]} - {[3,7]} = {[1, 3), (5, 7]}


```python
ItvSet([Itv(1, 5)]) | ItvSet([Itv(3, 7)]) == ItvSet([Itv(1,7)])
ItvSet([Itv(1, 5)]) & ItvSet([Itv(3, 7)]) == ItvSet([Itv(3,5)])
ItvSet([Itv(1, 7)]) - ItvSet([Itv(3, 5)])  == ItvSet([Itv(1,3), kind='[)'], [Itv(5,7), kind='(]'])
```

## 许可证

该项目签署了Apache License 2.0授权许可，详情请参阅LICENSE

## 联系

个人QQ: 3362336457

Discord开发群: https://discord.gg/f46wHwQduS

QQ开发群: 772588075

欢迎提出任何建议，bug反馈，以及代码贡献。

欢迎想合作开发或者维护的加入群聊。

感谢您的任何贡献。





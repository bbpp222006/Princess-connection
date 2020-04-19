# Princess connection 公主连接

## 简介
此项目为公主连接脚本. 使用opencv图像识别进行按钮分析.

目前的功能只有刷初始号. 以后可能增加新功能. 敬请期待.


## 环境
python包:
```
pip install opencv-python==3.* -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install uiautomator2 
```

windows端需要adb工具.
`adb devices`

若使用模拟器,则需要将模拟器设置为桥接模式.  具体参考这个项目(https://github.com/Jiahonzheng/JGM-Automator)

设置好后命令行运行
`python -m uiautomator2 init`
对模拟器进行初始化  

接着在手机(模拟器)上打开 ATX(小黄车) ，点击 启动 UIAutomator 选项，确保 UIAutomator 是运行的。


## 刷初始号功能
本项目下zhanghao.txt为待刷账号与密码. 
每一行用tab作为账密的分割(其实你可以在源码中修改读取方式)

jieguo.txt是账号上最后三星的结果.

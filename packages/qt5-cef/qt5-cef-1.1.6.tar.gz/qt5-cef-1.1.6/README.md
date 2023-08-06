```
version: 1.1.6

sth tips:
1、cefpython3==57.0 版本，python版本要使用3.7以下版本，3.7版本不支持。
2、cefpython3==66.0 版本，如果mac os的版本小于11(big sur)，则需要开启external_message_pump参数，否则页面会无法正常响应事件循环。
3、cefpython3==66.0 版本，如果页面中出现原生html的select标签元素，点击后会产生闪退现象。
4、mac os打包，使用pyinstaller打包工具，pyinstaller版本使用4.3。
```
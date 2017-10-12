主节点master：
web界面，接收agent的测试结果的接口，数据存储。
监测worker

从节点agent：
定时运行监测worker，把结果通过api上报给主节点。


# summer-project


## 安装

### Anaconda(Python及许多科学计算包的整合工具)

[下载地址](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

Python现在有两个大的版本，2和3；现在几乎全部的package都支持3，所以我们当然用最新的3。
在里面根据系统选择最新的版本，比如linux下我看到最新的版本是Anaconda3-4.4.0-Linux-x86_64.sh 

下载安装好后，先更新一下：

```bash
> conda update --all
```

我们经常会用到的几个package:

- numpy（提供矩阵、数组操作）
  [numpy manual](https://docs.scipy.org/doc/numpy/)
- matplotlib（画图）
  [matplotlib User's Guide](http://matplotlib.org/users/index.html)
- scipy（包括许多科学计算的工具，例如差值、最优化等）
  [scipy tutorial](https://docs.scipy.org/doc/scipy/reference/tutorial/index.html)

### CMake(编译配置工具)

过去编译时我们需要写Makefile，里面的语法写起来很麻烦。而CMake通过编写CMakeLists.txt，自动生成Makefile，里面的语法容易理解的多。

### git(代码管理工具)

- 注册github

[github学生优惠](https://education.github.com/pack) 可以免费建立private项目

## 文档

[Python官方教程（英文）](https://docs.python.org/3/tutorial/index.html)

[Python简明教程](docs/A-Byte-of-Python3_zh.pdf)

[Python教程-廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)

[git简单命令](http://rogerdudler.github.io/git-guide/)

[git教程-廖雪峰](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

[CMake官方教程](https://cmake.org/cmake-tutorial/)

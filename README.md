# summer-project

## Project 1

- 项目内容：
  - 尝试不同的反演方法，比较效果
  - 自己编写一个模型，测试
  - （可选）探索反演结果与数据覆盖之间的关系
- 项目目的：
  - 了解正演与反演的区别与联系
  - 了解几种反演方法的特点
  - 学会使用Python的基本操作

[详细介绍](docs/project1.md)

## 安装

### Anaconda(必须)

[下载地址](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/)

Python现在有两个大的版本，2和3；现在几乎全部的package都支持3，所以我们当然用最新的3。
Anaconda可以看作是Python及许多科学计算工具的整合包，你可以通过它方便的管理package。
在上面的链接中根据系统选择最新的版本，比如linux下我看到最新的版本是Anaconda3-4.4.0-Linux-x86_64.sh 

1. 安装
   ```bash
   > bash ./Anaconda3-4.4.0-Linux-x86_64.sh
   ```
   按照它默认提示做就行了
   
2. 下载安装好后，先更新一下：
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
  
3. 学习Python

Python本身是一门比较容易的编程语言，看看教程大概几天就基本可以使用了。推荐看廖雪峰写的教程和Python的官方教程。
廖雪峰教程中函数式编程、面向对象编程、面向对象高级编程、进程和线程之后的可以先不看。看的过程中，可以把他们给的例子
自己敲一下，可能效果更好一些。教程下面都有链接。而官方教程可以只看1-7章。

### CMake(可选)

过去编译时我们需要写Makefile，里面的语法写起来很麻烦。而CMake通过编写CMakeLists.txt，自动生成Makefile，里面的语法容易理解的多。

### git(可选)

- 注册github

[github学生优惠](https://education.github.com/pack) 可以免费建立private项目

## 文档

[Python官方教程（英文）](https://docs.python.org/3/tutorial/index.html)

[Python教程-廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)

[git简单命令](http://rogerdudler.github.io/git-guide/)

[git教程-廖雪峰](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)

[CMake官方教程](https://cmake.org/cmake-tutorial/)

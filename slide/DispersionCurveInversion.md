title: 基于差分演化算法的面波频散曲线反演
speaker: 潘磊
url: https://github.com/ksky521/nodeppt
transition: zoomin
files: /js/demo.js,/css/demo.css
theme: moon
highlightStyle: monokai_sublime
usemathjax: yes
date: 2017年7月19日

[slide]

# 基于差分演化算法的面波频散曲线反演
## 演讲者：潘磊

[slide]

# 什么是面波？

----
![](/figures/seismology.png)

[slide]
![](/figures/RL_direct.png)

![](/figures/RL_move.png)

[slide]

# 什么是频散曲线？


----

## 2层模型(Aki)-解析解

[note]

$$
\tan \omega H 
\sqrt{\frac{1}{\beta_1^2} - \frac{1}{c^2}} =
\frac{\beta_2^2}{\beta_1^2}
\frac{\sqrt{\frac{1}{c^2} -\frac{1}{\beta_2^2}}}
{\sqrt{\frac{1}{\beta_1^2} - \frac{1}{c^2}}}
$$

$$
X = \frac{H}{\beta_1}\sqrt{1 - \frac{\beta_1^2}{c^2}}
$$

$$
\tan \omega X = const. \frac{\sqrt{(const.)^2 - X^2}}{X}
$$

[/note]

![](/figures/aki2.jpg)
![](/figures/aki.jpg)

[slide]

## 4层模型-合成噪音数据-提取

----
<div class="columns2">
<img src="/figures/d4_data_media.png" width="800" height="300">
<img src="/figures/d4_data_raw.png" width="800" height="300">
</div>

[slide]

## 6层模型-合成噪音数据-提取

----
<div class="columns2">
<img src="/figures/d6_data_media.png" width="800" height="300">
<img src="/figures/d6_data_raw.png" width="800" height="300">
</div>

[slide]

# 正演与反演

----
- 什么是正演？

  已知模型，通过数值计算得到需要的物理量。

- 什么是反演？

  已知物理量，通过某些反演方法得到模型。

[slide]

## 差分进化算法

- Storn and Price, 1995
- *Population*
- *Generation*
- *Mutation*
  $$
  \mathbf{v}\_{i, g} = \mathbf{x}\_{r0, g} + F \cdot (\mathbf{x}\_{r1, g} - \mathbf{x}\_{r2, g}) 
  $$

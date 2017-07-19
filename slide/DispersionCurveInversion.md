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
## 报告人：潘磊

[slide]

## 什么是面波？

----
![](/figures/seismology.png)

[slide]
![](/figures/RL_direct.png)

![](/figures/RL_move.png)

[slide]

## 什么是频散曲线？

----

### 2层模型(Aki)-解析解

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
<div class="columns-2" >
<img src="/figures/d6_data_media.png" width="800" height="300">
<img src="/figures/d6_data_raw.png" width="800" height="300">
</div>

[slide]

## 正演与反演

----
- 什么是正演？

  已知模型，通过数值计算得到需要的物理量。

- 什么是反演？

  已知物理量，通过某些反演方法得到模型。

[slide]

## 正演方法

----

- Thomson-Haskell传播矩阵方法，(Haskell, 1953)
- Schwab-Knopoff方法，(Knopoff,1964; Schwab, 1965)
- 广义反透射系数方法，（陈晓非，1993；凡友华，2003；何耀峰，2005）

[slide]

## 漏根的情况

![](/figures/missing_roots_raw.png)


[slide]

## 反演方法

- 基于导数的单点反演方法
  - 最速下降(steepest descent)
  - 共轭梯度(conjugate gradient)
  - 拟牛顿方法(quasi-Newton)
  - 要求:
    - 目标函数必须二次可导
    - 目标函数必须有唯一的最小值

[slide]

## 最速下降法

![](/figures/Gradient_descent.png)

[slide]

- 不基于导数的单点反演方法
  - 暴力搜索(Brute Force Search)
  - 随机行走(Random Walk)
  - 模拟退火(Simulated Annealing)

[slide]

<div class="columns2">
<figure>
<img src="/figures/brute_force.png" height="300">
<figcaption>暴力搜索</figcaption>
</figure>
<figure>
<img src="/figures/random_walk.png" height="300">
<figcaption>随机行走</figcaption>
</figure>
</div>

[slide]

- 不基于导数的多点反演方法
  - 演化算法
    多用于连续参数的最优化
  - 遗传算法
    适合离散可编码的参数的最优化

[slide]

## 差分演化算法

- Storn and Price, 1995
- 族群(Population)
- 代(Generation)
- 变异(Mutation)
  $$
  \mathbf{v}\_{i, g} = \mathbf{x}\_{r0, g} + F \cdot (\mathbf{x}\_{r1, g} - \mathbf{x}\_{r2, g}) 
  $$

[slide]

[magic]

### 1.初始化族群 

![](/figures/de_initialize.png)

====

### 2.产生扰动 

![](/figures/de_generate_perturbation.png)

====

### 3.变异产生新个体

![](/figures/de_mutation.png)

=====

### 4.挑选，接受新个体 

![](/figures/de_selection.png)

====

### 5.新一次变异产生新个体

![](/figures/de_new_population.png)

====

### 6.挑选，拒绝新个体

![](/figures/de_selection2.png)

[/magic]

[slide]

## 密度与P波速度的影响

| layer | density(a) | Vp(a) | density(b) | Vp(b) |
| :---: |      :---: | :---: |      :---: | :---: |
|     1 |       1.78 |   1.5 |        1.8 |   1.7 |
|     2 |       1.85 |   1.7 |        1.8 |   1.7 |
|     3 |       1.80 |   1.6 |        1.8 |   1.7 |
|     4 |       1.93 |   2.0 |        1.8 |   1.7 |

![](/figures/a_same_b_diff_vp_rho.png)

[note]

 Xia et al. (1999), Knopoff’s method 
 
 - Vs 25% -> Vr by 39%. 
 - density 25% -> Vr by less than 10%.
 - Vp -> less effect (3%).


[/note]

[slide]

## 高阶频散曲线对反演结果的影响

----

<div class="columns2">
<figure>
<img src="/figures/l4_m1_dispercurve.png" height="300"/>
<figcaption>仅基阶参与反演</figcaption>
</figure>
<figure>
<img src="/figures/l4_m3_dispercurve.png" height="300"/>
<figcaption>前3阶参与反演</figcaption>
</figure>
</div>

[slide]

<div class="columns2">
<figure>
<img src="/figures/l4_m1_media.png" height="300">
<figcaption>仅基阶参与反演</figcaption>
</figure>
<figure>
<img src="/figures/l4_m3_media.png" height="300">
<figcaption>前3阶参与反演</figcaption>
</figure>
</div>

[slide]

## 4层数据模型-8层反演模型-数据同一正演方法得到

----

<div class="columns2">
<figure>
<img src="/figures/d4_i8_dispercurve.png" height="300">
<figcaption>反演模型与数据模型对应的频散曲线的对比</figcaption>
</figure>
<figure>
<img src="/figures/d4_i8_media.png" height="300">
<figcaption>反演模型与数据模型的对比</figcaption>
</figure>
</div>

[slide]

## 4层数据模型-4层反演模型-数据不同正演方法得到

----

<div class="columns3">
<figure>
<img src="/figures/d4_data_raw.png" height="200">
<figcaption>从噪音数据中提取的频散曲线</figcaption>
</figure>
<figure>
<img src="/figures/d4_i8_dispercurve.png" height="200">
<figcaption>反演模型与数据模型对应的频散曲线的对比</figcaption>
</figure>
<figure>
<img src="/figures/d4_i8_media.png" height="200">
<figcaption>反演模型与数据模型的对比</figcaption>
</figure>
</div>

[slide]

## 编程要求

- python

[slide]

# 谢谢

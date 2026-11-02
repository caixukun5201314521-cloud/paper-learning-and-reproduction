# 统一用户流失检测中的数据有效性评估:一个指标辅助框架

> **Unifying Data Effectiveness Assessment in User Churn Detection: An Indicator-Assisted Framework**
>
> 期刊:《清华科学与技术》(Tsinghua Science and Technology)· 研究论文
> ISSN 1007-0214 18/23 pp2237−2250 · DOI: 10.26599/TST.2024.9010230
> 第 31 卷,第 4 期,2026 年 8 月
>
> 作者:Mengying Zhou、Qianyu He、Bruno Abrahao、Xin Wang\*、Yang Chen\*( \* 通讯作者)
> 收稿:2024-08-13;修回:2024-11-06;录用:2024-11-13

**译者说明:**本译稿覆盖论文全部正文、图题、表格、致谢与作者简介;参考文献为学术引文,按惯例保留英文原文(翻译后无法检索,失去引用价值)。原 PDF 提取文本中部分数学公式因双栏排版出现乱码,已按上下文重构,并以"【公式经重构】"标注;插图本身为图像无法翻译,仅译图题。表格数值一律照录原文。

---

## 摘要

随着人工智能(AI)在各类任务上展现出令人瞩目的性能,其处理多样化数据类型的能力已得到广泛采用。然而,AI 模型往往缺乏透明性与可解释性,使得针对特定场景识别最有效的数据类别和模型变得困难。现行策略通常依赖常识判断或穷举式搜索,二者都低效且成本高昂。为填补这一空白,我们提出指标辅助框架(INdicator-assisted FramewOrk,INFO)。INFO 使研究者与从业者能够直接识别有效的数据类别,并在涉及多类数据的任务中指导模型选择。通过评估数据固有的信号强度,INFO 提供了评估任务性能的代理度量,从而减少耗时的模型试错与复现工作。我们以用户流失检测这一关键任务为案例,使用来自五个不同领域的真实数据集验证了 INFO 的有效性。实验表明,INFO 能够在大规模试验之前揭示各类数据的效能。INFO 有望成为一种自动化数据工程方法,厘清模型性能与数据集特征之间的关系。

**关键词:**用户流失;可解释人工智能(AI);特征选择;数据挖掘

---

## 1 引言

用户流失检测是电信[1]、在线游戏[2]和社交媒体平台[3]等多个领域的关键任务,因为它会显著影响业务增长与收入。用户流失率降低 5% 可带来约 25% 的利润增长[4]。准确的流失检测能够支持前瞻性干预措施,例如价格调整[5]、运营优化[2]和激励措施[6]。

用户流失(user churn)被定义为:用户在一段时间的正常使用之后脱离某产品[1, 2, 7]。因此,我们可以分析用户脱离之前产生的大量数据来预测流失信号。随着感知、存储与分析技术的进步,流失信号及其信息价值正从多种数据类型中被挖掘出来,包括文本、用户活动、图像、视频和社交连接[8, 9]。

然而,目前尚无统一框架来指导判断数据集中的哪些数据类别对流失检测有效,也没有框架指明应选择哪些模型以获得最优性能。复杂的模型设计使人难以追溯可解释性,也难以在不同环境中快速识别最有效的数据类别与模型。因此,在各种模型之间进行穷举搜索以寻找最优解成为最常用的策略,导致为了评估模型在特定数据集上的性能而进行代价高昂的重复试验。

更具体地说,以下三个因素阻碍了这一过程:**(1)依赖领域特定特征:**以往方法依赖独特的领域特定特征[10, 11],这限制了它们在不同领域之间的泛化能力。例如,一些模型严重依赖语言类数据,而这类数据未必适用于所有场景。**(2)信号强度参差不齐:**即使两个数据集拥有相同的特征集合,它们所编码的信号强度也可能各不相同。例如,社交连接信息在某些平台上可能是强信号,而在交互更少人际色彩的其他平台上可能只提供微弱甚至可忽略的信号。**(3)基准不统一:**研究者通常在来自特定领域的指定数据集上评估自己的方法,导致不同方案之间的基准不一致。这种不一致使得跨数据集比较方法性能变得困难,并且为了评估方法在各种场景下的适用性,必须进行代价高昂的重复试验。

本研究引入一组可解释的指标,无需大规模试验即可统一评估流失检测任务中的数据有效性。这些指标使研究者与从业者能够直接识别应用时哪些数据类别最有效。这些指标背后的设计直觉是:某一数据类别与流失检测任务的相关性,可以用其固有的信息量(informativeness)来表征。每个指标通过计算相应数据类别相对其**空模型**(null model,即基准参照)的偏离程度来量化该类数据的信息量;相对空模型偏离越大,信息量越大。这些指标是通用的,可跨数据集、跨领域使用。指标源自五个方面——"活动周期性"、"活动多样性"、"语言"、"图结构"和"交互情感",依据是以往文献中使用的数据类别。这些指标共同构成了指标辅助框架(INFO)的基础。

我们通过一系列实验评估 INFO,使用来自不同领域的五个真实数据集。每个数据集先用 INFO 进行先验试验评估(prior-trial assessment),再用无偏模型进行后验的二分类实验。先验指标与后验结果之间的一致性验证了 INFO 的有效性。这表明 INFO 是一个有前景的数据工程框架,它厘清了数据有效性与信息量之间的关系,能够指导有效数据类别的选择和复杂模型的设计。我们的贡献总结如下:

- 我们提出五个指标,量化各类数据在流失检测中的能力。这些指标将各类数据的固有信息量直接映射为它们对流失检测任务的贡献,并在应用特定数据类别时充当评估性能的代理。
- 我们基于上述五个指标提出 INFO——一个统一的数据有效性评估框架,能够无需大量模型复现或测试即可直接识别有效的数据类别。
- 我们在来自不同领域的五个真实数据集上验证 INFO。整个过程包括使用 INFO 的先验试验评估,以及后验的二分类实验。先验分析与后验结果之间的一致性证明了 INFO 的有效性。

---

## 2 相关工作

### 2.1 面向用户流失问题的特征选择

特征选择是关键的数据预处理步骤,旨在识别对预测性能最有用的特征集合。有效的模型依赖稳健的特征选择来提升准确率并降低过拟合风险。Zhong 等[12]发现,在必需蛋白预测场景中,更多的输入特征并不必然带来更好的性能;通过剔除无关或有害特征,他们仅用 8 个特征的子集就取得了最优准确率。基于模型的方法(model-based)依据模型性能来选择特征:Qiu 与 Zhang[13]提出根据分类器性能量化特征显著性的特征选择方法。与之相对,免模型方法(model-free)不依赖后续实验性能:Zhou 等[14]提出基于互信息与相关系数的筛选方法,计算候选特征之间的相关性并过滤掉相关性低的特征。Eljialy 等[15]将基于模型与免模型两类方法结合,提出混合式特征选择技术,将过滤法(filter)与包裹法(wrapper)整合,同时兼顾特征之间的关系及其对实验性能的贡献。

### 2.2 用户流失检测建模

另一个相关研究方向是构建对用户流失具有强预测性能的模型,这在电信业[1]、在线游戏[2]和社交媒体平台[11, 16]等多个领域都有研究。主流方法依赖特征工程,利用不同的机器学习[2, 9]和深度学习[3]算法来检测可能的用户流失。这些方法通常提取针对平台特性定制的特征,例如在线游戏中的玩法操作[2]、电信上网卡的行为与使用模式[1],以及视频分享平台上的视频偏好与话题多样性[8]。

---

## 3 指标设计

本节介绍构成 INFO 基础的五个指标及其形式化定义。

### 3.1 动机

感知、存储与分析技术的进步,使得利用多种数据类别来获得更好的任务性能成为可能。以用户流失检测为案例,以往的解决方案基于不同的直觉,利用了不同的主要数据类别,如表 1 所总结。

**表 1 流失任务中五类代表性数据类别**

| 方法 | 建模直觉 | 主要数据类别 |
|---|---|---|
| Wu 等[1] | 使用行为 | 活动周期性 |
| Yang 等[3] | 活动模式 | 活动周期性 |
| Lu 等[8] | 视频多样性 | 活动多样性 |
| Anderson 等[17] | 音乐多样性 | 活动多样性 |
| Lu 等[16] | 感兴趣话题 | 语言 |
| Amiri 与 Daumé[18] | 帖子内容 | 语言 |
| Óskarsdóttir 等[9] | 社交传染 | 图结构 |
| Piao 等[19] | 模体(motif)网络结构 | 图结构 |
| Zhang 等[20] | 社交影响 | 交互情感 |
| Hamilton 等[10] | 评论情感 | 交互情感 |

这些类别是:"活动周期性"、"活动多样性"、"语言"、"图结构"和"交互情感"。同一类别内的方法可能采用不同的模型,但从相同的数据类型中捕获相似的流失信号。这就提供了一个机会:通过直接比较不同数据类别的固有信号强度,来度量各类数据的有效性以及相关模型的适用性。信号强度更强的数据类别对任务性能的贡献更显著。

基于这一动机,我们引入五个指标来量化表 1 中每类数据的信号强度。指标设计的核心思想是为每个类别建立一个空模型:对给定数据集而言,某类数据相对其对应空模型的偏离越大,它对任务性能的贡献越大。各指标的详细定义见后续小节。

### 3.2 指标定义

#### 3.2.1 活动周期性

用户活动中周期性的存在反映了时间数据的信息量[6]。所提出的"活动周期性"指标量化用户行为的规律性。我们以"无周期性"作为空模型,把周期性的存在视为流失检测有价值信息的标志。

来自不同来源的数据集表现出不同的周期粒度。例如,Twitter 活动遵循日周期,而短租平台的数据可能呈现月周期。为适应这些差异,我们采用灵活自适应的方法计算周期性:分别在日、周、月三种粒度上计算周期性系数,然后取最大值作为最终的周期性指标【公式经重构】:

$$\phi=\max(\phi_{\text{day}},\ \phi_{\text{week}},\ \phi_{\text{month}}) \tag{1}$$

其中 $\phi_{\text{day}}$、$\phi_{\text{week}}$、$\phi_{\text{month}}$ 分别表示日、周、月粒度下的周期性系数。这些系数度量数据集在对应时间粒度下的平均周期性,计算方式如下【公式经重构】:

$$\phi=\frac{1}{\lceil l/g\rceil}\sum_{k=1}^{\lceil l/g\rceil}\phi_p,\quad p=k\cdot g \tag{2}$$

其中粒度级别 $g$ 可取 1、7、30,分别代表日粒度、周粒度和月粒度。周期相关系数 $\phi_p$ 按周期窗口长度 $p$ 计算,$p$ 由步长 $k$ 与粒度级别 $g$ 相乘得到。例如,步长 $k=4$、粒度级别 $g=7$ 时,周期窗口长度 $p=28$,表示以周为粒度的四周。为计算 $\phi$,总时间跨度 $l$ 被划分为若干段,记为 $S$;通过度量这些段之间的相关性,来评估用户活动在给定窗口长度 $p$ 下符合周期模式的程度。周期相关系数 $\phi_p$ 定义为【公式经重构】:

$$\phi_p=\frac{2}{n(n-1)}\sum_{i=1}^{n-1}\sum_{j=i+1}^{n}\left|\mathrm{Corr}\left(S_{t_i:t_i+p},\ S_{t_j:t_j+p}\right)\right| \tag{3}$$

其中 $n=\lceil l/p\rceil$。$\mathrm{Corr}(S_{t_i:t_i+p},\ S_{t_j:t_j+p})$ 表示段 $S_{t_i:t_i+p}$ 与段 $S_{t_j:t_j+p}$ 之间的皮尔逊积矩相关系数[21];下标 $t_i$ 表示第 $i$ 段的起始时间。$\phi_p$ 的取值范围为 −1 到 1,越接近 1 表示周期性越强。

#### 3.2.2 活动多样性

除时间规律性外,用户行为的多样性同样能反映用户活动的信息量。多样性的描述跨越一个谱系:一端是探索广泛对象的"通才型"(generalist),另一端是聚焦特定领域的"专才型"(specialist)。这里的"对象"和"领域"是广义的,例如维基百科上的专业知识、Spotify 上的音乐品味,或 Facebook 上的社交互动风格。

我们应用通才-专才得分(GS-score)[22]计算每个用户的活动多样性。GS-score 取值 0 到 1:0 代表极端通才,1 代表极端专才。

当通才组与专才组之间出现明显区分,即两组能被区分开时,多样性才具有信息量。基于这一原则,我们定义"无多样性差异"为空模型,把通才组与专才组活动多样性分布之间的差异作为"活动多样性"类别的指标。为量化这种差异,我们采用 Wasserstein 距离[23]——一种度量两个概率分布之间散度的指标。通才分布与专才分布之间的 Wasserstein 距离定义为【公式经重构】:

$$W(\sigma_g,\ \sigma_s)=\inf_{\gamma\in\Pi(\sigma_g,\sigma_s)}\int c(x;y)\,\mathrm{d}\gamma(x,y) \tag{4}$$

其中 $\sigma_g$ 与 $\sigma_s$ 分别表示通才与专才的分布,$\Pi(\sigma_g,\sigma_s)$ 表示度量空间上所有耦合(测度)的集合,$c(x;y)$ 是把 $\sigma_g$ 分布搬运到 $\sigma_s$ 分布的代价函数,$x$ 与 $y$ 分别是来自 $\sigma_g$ 与 $\sigma_s$ 的样本。

为获得通才组与专才组的多样性分布,我们对全体用户的多样性分布拟合双峰高斯概率函数:拟合出的两个高斯分布 $\sigma_g$ 与 $\sigma_s$ 分别对应通才组与专才组。两个高斯分布之间的 Wasserstein 距离即作为活动多样性的指标。

#### 3.2.3 语言

文本是最常见的数据类别之一。与活动多样性类似,语言多样性也能提供有价值的信息。不同用户群体和平台之间的语言风格差异显著。以往研究[10, 24]发现,流失用户与留存用户的语言风格存在明显不同:语言风格接近社区的用户更不容易流失,而风格偏离的用户更可能离开。

为量化语言风格差异,我们构建快照语言模型(Snapshot Language Model,SLM)[24]。SLM 是一个带 Kneser–Ney 平滑的二元(bigram)语言模型,使用每月发布的全部文本生成。对每条帖子 $p_o$,我们计算其相对当月 SLM($SLM_{m(p_o)}$)的交叉熵,以度量其语言相对社区的偏离,定义如下【公式经重构】:

$$H(p_o;\ SLM_{m(p_o)})=-\frac{1}{n_{p_o}}\sum_{i=1}^{n_{p_o}}\log P_{SLM_{m(p_o)}}(b_i) \tag{5}$$

其中 $b_1, b_2, \ldots, b_n$ 是帖子 $p_o$ 中生成的 bigram,$P_{SLM_{m(p_o)}}(b_i)$ 是每个 bigram $b_i$ 在当月 SLM 下的概率。值越低,表示越接近社区的语言风格。

对"语言"数据类别,我们定义"无语言差异"为空模型,把流失用户与留存用户所发帖子之间的语言差异作为该类别的指标。该指标度量两组用户语言风格之间的距离:差异越大,该类别的信息越多。

计算该指标时,我们先在每个时间窗口上分别计算流失用户与留存用户帖子的交叉熵,得到各自的语言风格分布;再应用前述 Wasserstein 距离[23]度量两组之间语言风格差异,作为指标值。

#### 3.2.4 图结构

个体之间的交互形式多种多样,从这些交互中导出的各类图结构特征常被用作预测变量[9, 19, 25]。图结构通常是同质性(homophily)[26]与关系闭合(relationship closure)[27]的结果:社交网络中的用户倾向于与相似的人互动,因社交影响[9]而更可能出现相似行为。

聚类系数(clustering coefficient)[28]是图论中广泛使用的连接紧密程度度量,描述三角形闭合的可能性,定义为:任一节点的任意两个邻居本身也相互连接的概率。图 $G$ 的聚类系数 $C$ 定义为【公式经重构】:

$$C=\frac{1}{n}\sum_{i=1}^{n}\frac{\tau_G(v_i)}{\tau_G(v_i)+\omega_G(v_i)} \tag{6}$$

其中 $G$ 表示交互图,$\tau_G(v_i)$ 表示 $v_i\in G$ 上闭合三角形的数量,$\omega_G(v_i)$ 表示 $v_i\in G$ 上开放三角形的数量。三角形定义为两两相连的三个节点;开放三角形则是缺少任意一条边的不完整三角形。

聚类系数低意味着网络接近随机、或在社会结构上欠组织,因而信息量较小[29]。对"图结构"数据类别,我们定义随机图为空模型,并使用聚类系数作为指标。在随机图中,当节点数 $N$ 趋于 $+\infty$ 时,聚类系数 $C_{\text{random}}$ 趋于 0,表示没有任何聚类特征。随机图由均匀随机过程生成,信息均匀分布,节点之间几乎不存在区分。相比之下,真实网络通常表现出明显的聚类,其聚类系数远高于同规模的随机图,有时甚至高出若干个数量级。这意味着真实网络包含的结构化信息要多得多,使"图结构"类别成为预测任务中有价值的数据来源。

#### 3.2.5 交互情感

在流失预测任务中,情感(sentiment)是常用的特征[30]。流失者通常因负面体验而离开平台,而留存用户报告的体验更积极[30]。正向与负向的交互情感都能提供有用的流失信号;而没有情感倾向的中性情感,对流失意愿的信号则较弱。

对"交互情感"数据类别,我们定义"无情感波动"为空模型,并提出**偏置熵**(biased entropy)度量来衡量交互情感的信号强度。在经典熵定义的基础上,我们引入中性情感偏移参数,以刻画每个情感取值相对中性情感的偏离。在中性情绪附近,较强的情感极性与分化意味着潜在的区分能力。给定数据集的交互情感指标 $E$ 定义为【公式经重构,原 PDF 此处双栏排版交错,个别符号以原刊为准】:

$$E=-\frac{1}{n_s}\sum_{i=1}^{n_s}(s_i-s_{\text{neu}})^{p}\log_2 p_{s_i} \tag{7}$$

其中 $n_s$ 为情感取值的个数,$s_i$ 为第 $i$ 个情感取值,$p_{s_i}$ 为情感取值 $s_i$ 出现的概率;$n_{\text{level}}$ 表示情感级别的个数。$s_{\text{neu}}$ 表示绝对中性情感值,通常按 $(\max+\min)/2$ 计算。本文中情感得分范围为最小值 $s_{\min}=0$ 到最大值 $s_{\max}=1$,绝对中性值 $s_{\text{neu}}$ 为 0.5。$|s-s_{\text{neu}}|$ 即中性情感偏移参数。$n_{\text{level}}$ 设为 5,表示情感级别的数目[31]。

---

## 4 使用 INFO 进行先验试验评估

利用上述指标,我们构建 INFO 框架,评估数据集中各类数据对流失预测任务的有效性与贡献。本节将 INFO 应用于五个真实数据集,对用户流失检测进行先验试验评估。结果表明 INFO 能有效反映不同数据类别的信息量。

### 4.1 数据集描述

为确保评估的全面性与泛化性,我们使用来自不同领域的五个多样化数据集。数据集的多样性依据以下两条标准保证:**(1)功能类别的多样性:**即数据集来自不同类型的平台,涵盖在线住宿、代码托管、在线百科和基于位置的服务。每个平台提供独特的服务,具有不同的用户行为模式与数据类别。**(2)功能情境的多样性:**即考虑驱动用户交互的不同内在动机。提供相似服务的平台在功能特性上也有差异,例如 Airbnb 上以交易为主的住宿服务与 Couchsurfing 上非货币化的房东-房客交换[32]。这种多样性使我们能够讨论同一数据类别在不同情境下的效能变化。

- **Airbnb** 是在线住宿平台,房东发布带价格的房源,房客预订住处,通过短租实现交易与社交。房东与房客在退房后可以互相评价。我们于 2019 年 1 月 1 日至 2019 年 3 月 19 日通过广度优先搜索从 Airbnb 网站采集了交易与评论数据。
- **Couchsurfing** 是非营利旅行社区,用户免费分享闲置房间,强调社交互动。房东与房客在住宿后互写评价与评分。数据来自文献[33]。
- **GitHub** 是促进开发者协作的代码托管社区。用户使用 git 工具管理文件,git 记录提交(commit)、推送(push)、合并(merge)等活动;用户还可以关注其他开发者与项目以追踪更新。数据来自文献[34, 35]。
- **Wikipedia** 是最大的多语言用户共建在线百科。注册用户与匿名用户均可编辑词条并参与讨论,长期编辑者使用监视列表(watchlist)追踪特定词条的变更。数据来自文献[36]。
- **Foursquare** 是基于位置的服务平台,用户在场所发布签到(check-in)[37],还可以给场所评分、为他人提供参考信息、添加好友。数据来自文献[38]。

表 2 汇总了这五个多样化数据集的统计信息。每个数据集覆盖超过 27,000 名用户,活动记录最多达百万级。对 Airbnb、Couchsurfing、GitHub 和 Wikipedia,我们使用 6 或 12 个月的流失预测窗口;Foursquare 因时间跨度仅 5 个月,采用 1 个月的预测窗口。

**表 2 数据集统计信息**

| 数据集 | 用户数 | 记录数 | 时间跨度(月) | 预测窗口(月) |
|---|---|---|---|---|
| Airbnb | 29,138 | 708,020 | 130 | 12 |
| Couchsurfing | 49,167 | 157,822 | 70 | 6 |
| GitHub | 122,239 | 8,407,824 | 124 | 12 |
| Wikipedia | 32,819 | 1,835,055 | 82 | 12 |
| Foursquare | 27,304 | 184,723 | 5 | 1 |

### 4.2 评估结果

#### 4.2.1 不同粒度下的周期性

对活动周期性,我们在图 1 中绘制了日、周、月三种粒度 $g$ 下的周期相关系数 $\phi$。纵轴值越高,表示对应窗口长度下周期性越强。注意,Airbnb 只分析月粒度,因为其交易记录仅以月为单位提供。

结果表明,周期性随数据集与粒度而变化。Airbnb 与 Couchsurfing 在月粒度上呈现明显周期性,反映与出行模式绑定的用户行为。GitHub 在所有粒度上都能观察到周期性,这大概是因为它作为代码协作平台,开发者表现出很强的日活动模式[39]。Wikipedia 在周、月粒度上呈现明显周期性,突出编辑活动的规律。Foursquare 仅在周粒度上表现出周期性,且波动明显,这可能与该数据集仅 5 个月的时间跨度有关,限制了其捕捉用户长期行为的能力。

更重要的是,INFO 能在更细的粒度上识别最有效的周期窗口长度。每个数据集都有一个代表最强周期性的峰值:Airbnb 与 Couchsurfing 的峰值出现在约 10 个月处,与年度出行季节性模式一致[40];GitHub 与 Wikipedia 的峰值出现在 3 个月处,反映季度性的维护与更新类参与活动。这些结果突出了 INFO 指导下游任务选择合适周期粒度的能力——选择不合适的粒度可能无法捕捉周期性中的有价值信息。

> **图 1** 不同时间粒度下的周期性系数 $\phi$:(a) 日粒度($g=1$);(b) 周粒度($g=7$);(c) 月粒度($g=30$)。

#### 4.2.2 多样性分布模式

如 3.2.2 节所定义,多样性指标评估通才组与专才组之间多样性分布的差异。图 2 展示了五个数据集的多样性分布及其拟合的双峰高斯函数。值得注意的是,并非所有数据集都呈现双峰结构:Couchsurfing 与 GitHub 显示两个清晰峰值,分别代表通才与专才;Wikipedia 的双峰较不明显。相比之下,Airbnb 与 Foursquare 只有一个可见峰,表明用户之间缺乏分化。

特别是,Couchsurfing 与 Airbnb 的对比突出了多样性指标反映不同流失信号强度的能力。在 Couchsurfing 上,两组用户的多样性得分都低于 0.5,反映其非货币化租房模式下用户对多样化交互的活跃探索。相比之下,Airbnb 作为主流住宿网站,已逐渐从共享平台转型为更专业的住宿服务[41],用户多样性得分较低,聚集在单一峰值附近。

与 Couchsurfing 和 Airbnb 不同,GitHub 与 Wikipedia 是典型的知识型专家平台,大多数用户聚焦特定的兴趣领域。因此,与探索型平台相比,它们的多样性得分分布接近 1,表明其用户更像"专家"。GitHub 因存在掌握多种编程语言的用户,仍呈双峰分布。Foursquare 作为签到平台,用户轨迹规律性强,签到地点相对集中,多样性得分接近 1。

> **图 2** 各数据集的双峰分布。(图中可见"双峰分布"与"单峰分布"标注,横轴为用户多样性得分,纵轴为概率密度。)

#### 4.2.3 语言距离

我们把流失用户与留存用户之间的语言风格差异作为语言指标。直觉是:潜在流失用户会逐渐偏离社区的语言风格。语言风格用平均交叉熵表示,基于每月的 SLM 与所发文本计算。

图 3 展示了 Airbnb 与 GitHub 上流失用户与留存用户的语言风格交叉熵。在 Airbnb 上,两组差异很小;而在 GitHub 上,差异更显著且随时间扩大。表 3 对这些差异进行了量化:Airbnb 的语言指标值为 0.018,GitHub 为 0.075。这表明 Airbnb 上流失与留存用户的语言风格相近,而 GitHub 上流失用户的语言风格显著不同,使语言类数据在 GitHub 上对流失检测更有用。

一个有趣的观察是,Airbnb 上语言交叉熵呈**周期性**变化,与 GitHub 上的**单调上升**形成对比。这反映了 Airbnb 上的年度出行模式:在出行高峰月份(7、8 月),季节性用户的涌入使语言风格多样化;随着这些用户离开,语言风格趋于稳定和均一。

> **图 3** Airbnb 与 GitHub 上流失用户与留存用户语言风格交叉熵随时间的变化。散点为单月数据,曲线为据此拟合的平滑趋势:(a) Airbnb;(b) GitHub。

#### 4.2.4 图结构的聚类水平

各数据集的图构建方法如下。Wikipedia 数据集因缺少关系数据无法构图。

- **Airbnb:交易图。**节点为用户,无向边为用户之间的交易。
- **Couchsurfing:交互图。**节点为用户,无向边为用户之间的非营利住宿交互。
- **GitHub:关注-被关注图。**节点为用户,有向边为关注(follower-followee)关系。
- **Foursquare:好友图。**节点为用户,无向边为用户之间的好友连接。

各数据集的聚类系数列于表 3。四个数据集的聚类系数差异显著:Airbnb 图的聚类系数最低,仅 0.001;而作为类似短租平台的 Couchsurfing,系数较高,为 0.133。这种差距归因于 Airbnb 上的交易型交互与 Couchsurfing 上的好友型交互之间的差异。GitHub 与 Foursquare 的聚类系数分别为 0.009 和 0.105。这些发现表明,基于"好友关系"或"兴趣"的图往往比基于"交易"的图更稠密、信息量更大。这一假设在第 5 节的实验结果中得到了进一步支持。

#### 4.2.5 交互情感分布

在我们的五个数据集中,交互情感来自数值型与文本型数据。Couchsurfing 与 Foursquare 天然包含数值评分;对 Airbnb、GitHub 和 Wikipedia,我们使用 VADER[42]——一个面向社交媒体文本的情感分析工具,基于交互或活动中的文本计算 0(最负面)到 1(最正面)的情感得分。

表 3 列出了所有数据集的交互情感指标。GitHub 与 Wikipedia 等协作平台的指标值较低,因为交互以客观、知识性内容为主,相对中性情感的偏离较小。相比之下,Airbnb、Couchsurfing、Foursquare 等娱乐与社交平台的指标值更高,反映更强的情感表达和更大的信息量。

图 4 进一步展示了各数据集情感的累积分布函数(CDF),直观呈现相对中性值的偏离。GitHub 与 Wikipedia 的情感值集中在 0.5 附近,反映其中性、客观、以知识为中心的交互;而 Airbnb、Couchsurfing 与 Foursquare 的情感表现出更强的情绪,并呈现三种不同模式:Airbnb 以正面情绪为主,Couchsurfing 以负面情绪为主,Foursquare 则相对均匀分布。

> **图 4** 交互情感的累积分布函数(CDF)。

**表 3 五个数据集的指标值与流失检测性能。$r_{\text{intra}}$ 与 $r_{\text{inter}}$ 分别为指标与性能在数据集内部和跨数据集之间的皮尔逊相关系数。部分数据集缺少某些特征类型,其值记为 N/A。**

| 数据类别 | Airbnb 指标 | Airbnb F1 | Couchsurfing 指标 | Couchsurfing F1 | GitHub 指标 | GitHub F1 | Wikipedia 指标 | Wikipedia F1 | Foursquare 指标 | Foursquare F1 | $r_{\text{inter}}$ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 活动周期性 | 0.108 | 0.704 | 0.137 | 0.756 | 0.197 | 0.784 | 0.149 | 0.768 | 0.112 | 0.728 | 0.909 |
| 活动多样性 | 0.035 | 0.680 | 0.065 | 0.732 | 0.053 | 0.726 | 0.028 | 0.619 | 0.053 | 0.711 | 0.924 |
| 语言距离 | 0.018 | 0.670 | N/A | N/A | 0.075 | 0.689 | 0.036 | 0.066 | N/A | N/A | 0.767 |
| 图结构 | 0.001 | 0.665 | 0.133 | 0.751 | 0.009 | 0.686 | N/A | N/A | 0.105 | 0.725 | 0.519 |
| 交互情感 | 0.136 | 0.748 | 0.076 | 0.742 | 0.049 | 0.714 | 0.036 | 0.648 | 0.072 | 0.727 | 0.755 |
| $r_{\text{intra}}$ | 0.953 | | 0.831 | | 0.890 | | 0.634 | | 0.854 | | N/A |

---

## 5 后验实验

上一节我们用 INFO 的五个指标广泛分析了各类数据的效能。本节对用户流失预测执行二分类实验,并将实验结果与先验试验指标进行对比,回答以下研究问题:

- **RQ1:**INFO 提供的先验试验指标与后验实验结果之间是否存在明确的一致性?
- **RQ2:**INFO 的先验试验指标能否辅助指导模型选择与特征工程?
- **RQ3:**INFO 能否在**不同数据集之间**直接量化使用某一特定数据类别的特定模型的性能?

### 5.1 实验设置

INFO 旨在揭示原始数据中固有的流失信号。为将复杂特征工程带来的偏差降到最低,我们提取常用的表格化(tabular)特征。例如在图结构特征类别中,我们使用自我中心网络(ego network)而非整图,以降低复杂度。所用特征的细节列于表 4。鉴于流失检测是二分类任务,我们使用非参数的逻辑回归(Logistic Regression,LR)分类器,它同时实现了模型简单性并避免调参偏差。性能用经典指标 F1 分数评估。

**表 4 实验中使用的具体特征**

| 数据类别 | 特征名 | 描述 |
|---|---|---|
| 活动周期性 | 活动记录(Activity record) | 每个时间槽内的记录数 |
| 活动多样性 | GS-score | GS-score 值 |
| 语言 | 交叉熵(Cross-entropy) | 平均交叉熵 |
| 图结构 | Size | ego 节点一步出邻居的节点数 |
| 图结构 | Ties | 与 ego 网络中所有节点的连接数 |
| 图结构 | Pairs | ego 网络中可能的有向连接数 |
| 图结构 | Density | Ties 除以 Pairs |
| 交互情感 | 情感(Sentiment) | 情感值 |

### 5.2 先验指标 vs 后验实验

每个特征类别独立输入 LR 模型,其性能即反映相应数据类别的有效性。表 3 汇总了实验结果以及用 INFO 得到的先验试验指标值。

**先验指标与后验性能之间的高度一致性。**皮尔逊相关系数被用来度量每个数据集**内部**先验指标与后验实验性能之间的相关性。这些结果记为 $r_{\text{intra}}$,展示在表 3 的最后一行。多数 $r_{\text{intra}}$ 值超过 0.8,表明存在强正相关。这种高度一致性凸显了 INFO 的能力:无需复现依赖这些特征类别的模型,即可揭示特征类别的潜力。

此外我们注意到,最有效的数据类别因数据集而异:对 Airbnb,交互情感的信号最强;而对其他四个数据集,活动周期性是主导因素。这说明不同平台上的用户流失检测任务依赖不同的数据类别,也解释了为什么一些训练良好的模型未必适用于所有场景,强调了根据每个数据集的特征选择合适模型的重要性。

**在不同粒度上捕捉周期性的能力。**如 4.2.1 节所述,INFO 表明不同数据集偏好不同的周期粒度。这里我们验证 INFO 自适应捕捉不同粒度周期性的能力,并考察选择合适粒度对预测性能的影响。

表 5 给出了三种粒度下的周期性指标及对应的实验性能。最优粒度因数据集而异:对 Airbnb、Couchsurfing 和 GitHub,月粒度产生最佳指标与性能;而对 Wikipedia 和 Foursquare,周粒度最有效。这些发现与各平台不同的用户活动模式相吻合。

有趣的是,使用**较粗**的粒度可以取得与较细粒度相当甚至更优的分类性能。在 Couchsurfing 和 GitHub 上,月粒度的 F1 分数超过周粒度,说明月度特征已足以提供有用信息。此外,周粒度的性能往往优于日粒度,表明更细的粒度并非总是必要:适当粗粒度的数据已能有效捕捉用户行为周期性,同时降低计算资源开销。

**表 5 时间粒度对性能的影响。分别列出五个数据集在日、周、月粒度下的周期性指标($\phi$)与对应预测性能。部分数据集缺少某些特征类型,其值记为 N/A。**

| 粒度 | Airbnb $\phi$ | Airbnb F1 | Couchsurfing $\phi$ | Couchsurfing F1 | GitHub $\phi$ | GitHub F1 | Wikipedia $\phi$ | Wikipedia F1 | Foursquare $\phi$ | Foursquare F1 |
|---|---|---|---|---|---|---|---|---|---|---|
| 日 | N/A | N/A | 0.014 | 0.748 | 0.124 | 0.776 | 0.012 | 0.736 | 0.017 | 0.727 |
| 周 | N/A | N/A | 0.113 | 0.752 | 0.165 | 0.777 | 0.149 | 0.768 | 0.112 | 0.725 |
| 月 | 0.108 | 0.730 | 0.137 | 0.756 | 0.197 | 0.784 | 0.143 | 0.766 | 0.099 | 0.722 |

**优先筛选有前景的特征。**除识别最有效的数据类别外,INFO 还有助于优先筛选有前景的特征,为优化模型性能提供指导。

五个数据类别的每个特征都被赋予基于其指标值的权重。利用这些权重,我们通过基于权重的方法进行特征选择,并与随机选择对比;两种方法保持相同比例的特征作为模型输入。两种选择方法的性能曲线见图 5。基于指标权重选出的特征始终优于随机选出的特征。值得注意的是,在 GitHub 和 Foursquare 上,即使只使用小比例的权重选择特征,也能取得与使用全部特征相当的竞争力;在 Airbnb 上,仅选择 40% 的特征即获得最佳性能。这些结果突出了 INFO 辅助研究者与从业者优先筛选有前景特征的能力——在获取全部特征困难的场景中尤为可贵,可减少实际场景中的试错成本。

> **图 5** 不同特征选择比例下的 F1 性能。我们在提取的特征集上,分别用随机选择和按指标权重选择,选取一定比例的特征用于预测:(a) Airbnb;(b) Couchsurfing;(c) GitHub;(d) Wikipedia;(e) Foursquare。

### 5.3 跨数据集量化朴素模型性能

上述结果证明了 INFO 在识别**数据集内部**不同数据类别潜力方面的有效性。本小节探讨另一个问题:INFO 能否直接量化某个特定模型**跨不同数据集**的性能?直觉是:依赖某一特定数据类别的模型,应该在该类别指标值强的数据集上表现良好。换言之,当模型构建在特定数据类别上,而该数据类别在给定数据集上的对应指标显示强信号时,该模型应当能迁移到该数据集或领域。

以往的流失检测方法通常利用多类数据并涉及复杂的模型设计[3, 10]。由于 INFO 侧重比较基于单一数据类别的朴素(naive)模型,我们的分析仅限于比较朴素模型的性能。为此,我们采用实验设置中所述的、基于单一数据类别构建的无偏 LR 模型作为朴素模型。

表 3 中最右列报告了指标值与朴素模型跨数据集性能之间的皮尔逊相关系数 $r_{\text{inter}}$。这些结果得出以下发现。

**指标与朴素模型跨数据集性能之间的正相关。**所列皮尔逊相关系数 $r_{\text{inter}}$ 大多超过 0.7,表明指标与跨数据集实验结果之间存在强对应关系。不过,图结构类别的 $r_{\text{inter}}$ 较低,为 0.519。这一差异可能归因于图数据的独特性质:图特征的有效性在很大程度上取决于连接的性质与定义,而后者在不同数据集之间差异很大。这种可变性降低了朴素图模型跨数据集应用时的一致性。

**好友关系使图结构具有信息量。**社交网络是许多在线平台的核心功能。在连接基于好友关系的数据集上,图结构模型表现更好。例如,基于图的模型在 Airbnb 上表现不佳,但在 Couchsurfing 上表现良好。这种差异源于交互的本质:Airbnb 是以货币化为基础、聚焦服务质量的平台,而 Couchsurfing 强调房客与房东之间基于好友的关系[32]。应用于其他数据集的朴素模型同样显示,基于好友关系的图优于基于交易交互的图。这些发现验证了社交传染(social contagion)在用户流失中的作用,并表明货币化的交互并不等于好友连接。

**流失信号体现在情绪中。**情感是交互质量的关键度量。强调用户体验(如 Airbnb)或好友关系(如 Couchsurfing 与 Foursquare)的平台,其预测性能优于以客观交互为中心的平台(如 GitHub 与 Wikipedia)。这与以往将情感视为强流失预测因子的研究一致[10, 20]。值得注意的是,基于文本与基于评分的情感数据都显示出较高的预测能力:Airbnb 上的文本情感与评分同样有效,有时甚至更有效——文本能够捕捉评分可能无法反映的隐性负面情绪,补全缺失的情感信息。

---

## 6 讨论

### 6.1 INFO 在缺失列的不完整数据集上的表现

现实世界中,数据集常因数据采集限制、隐私顾虑或操作约束等因素而存在"特征集不完整"的问题。指标缺失会导致对数据类别信息量的评估不完整,可能削弱 INFO 的预测能力。确保 INFO 在处理不完整数据集时的稳健性,对其在真实场景中的实用价值至关重要。本小节探讨应对缺失列数据集所带来挑战的策略。

当数据集缺少某些特征时,INFO 可以从可用数据中推断缺失的信号。例如,在用户交互稀疏的领域(如金融交易或传感器应用),从非交互数据导出的替代特征可以揭示相关模式。在金融交易中,交易频率、交易量或时间趋势等特征可以替代或补充基于交互的特征。这些替代特征提供了对用户行为的洞察,使 INFO 能够通过活动模式的变化(而非直接交互)检测流失信号。通过利用现有信号,INFO 得以保持评估的完整性,并将适用性扩展到更广泛领域的流失检测。

### 6.2 INFO 在更广泛场景中的适用性

本文中,INFO 已在用户流失检测中证明了自己的有效性。此外,其潜力还可以扩展到更广泛的应用:其可解释的指标可以在客户细分、欺诈检测和预测性维护等任务中提供有价值的洞察。

**面向更广泛预测任务的定制化指标组合。**INFO 的指标可以针对流失检测之外的各种预测任务进行定制。例如,在推荐系统中,"活动周期性"与"活动多样性"可用于用户偏好预测任务,以理解其对推荐准确率的贡献;在欺诈检测中,"图结构"与"活动模式"的异常可能预示欺诈活动;在市场细分中,"语言"与"交互情感"指标可以提供关于沟通风格与情感投入的洞察,帮助识别客户群体并制定有针对性的营销策略。通过将 INFO 的指标适配到具体任务,INFO 能够在各类应用中提供有价值的洞察并提升性能。

**调整指标权重。**此外,INFO 允许灵活调整指标权重,以满足特定预测任务的要求。通过为给定应用优先排序最相关的指标,可以对 INFO 进行微调以提供针对性指导。例如在欺诈检测中,提高与异常交易或不规则网络结构相关指标的权重,可以增强其识别欺诈行为的相关性。通过对 INFO 指标及其权重的扩展与调整,INFO 可以更加通用、适用更广。

---

## 7 结论与未来工作

本文提出 INFO——一个统一框架,用于直接评估并选择适合特定应用领域的有效数据类别。INFO 通过度量数据类别固有的信息量,量化其在流失检测任务中的相关性与有效性。我们识别了五个数据类别,并将其对应指标形式化为 INFO 的基础。通过在来自不同领域的五个数据集上的实验,我们展示了 INFO 直接量化数据类别预测性能的能力。先验指标与后验实验结果之间的强一致性验证了 INFO 的有效性与可靠性。

未来工作将把 INFO 扩展到混合数据类别以增强泛化能力,在更广泛的场景中评估其稳健性,并探索用户粘性与留存的通用规律。

---

## 致谢

本研究受国家自然科学基金(No. 62072115、No. 62472101)、上海市科技创新行动计划项目(No. 22510713600)、上海市科学技术委员会(No. 22dz1204900)、中央高校基本科研业务费(No. 2025110481),以及复旦大学上海市智能信息处理重点实验室(No. IIPL-2025-RD1-03)资助。

---

## 参考文献(保留原文)

[1] F. Wu, F. Lyu, J. Ren, P. Yang, K. Qian, S. Gao, and Y. Zhang, Characterizing internet card user portraits for efficient churn prediction model design, *IEEE Trans. Mobile Comput.*, vol. 23, no. 2, pp. 1735–1752, 2024.

[2] Y. Xiong, R. Wu, S. Zhao, J. Tao, X. Shen, T. Lyu, C. Fan, and P. Cui, A data-driven decision support framework for player churn analysis in online games, in *Proc. 29th ACM SIGKDD Conf. Knowledge Discovery and Data Mining*, New York, NY, USA, 2023, pp. 5303–5314.

[3] C. Yang, X. Shi, L. Jie, and J. Han, I know you'll be back: Interpretable new user clustering and churn prediction on a mobile social application, in *Proc. 24th ACM SIGKDD Int. Conf. Knowledge Discovery & Data Mining*, New York, NY, USA, 2018, pp. 914–922.

[4] F. Reichheld and C. Detrick, Loyalty: A prescription for cutting costs, *Mark. Manag.*, vol. 12, no. 5, pp. 24–25, 2003.

[5] P. Ye, J. Qian, J. Chen, C. Wu, Y. Zhou, S. De Mars, F. Yang, and L. Zhang, Customized regression model for Airbnb dynamic pricing, in *Proc. 24th ACM SIGKDD Int. Conf. Knowledge Discovery & Data Mining*, London, UK, 2018, pp. 932–940.

[6] R. Jakob, N. Lepper, E. Fleisch, and T. Kowatsch, Predicting early user churn in a public digital weight loss intervention, in *Proc. of the CHI Conf. Human Factors in Computing Systems*, Honolulu, HI, USA, 2024, p. 994.

[7] H. Sagtani, M. G. Jhawar, A. Gupta, and R. Mehrotra, Quantifying and leveraging user fatigue for interventions in recommender systems, in *Proc. 46th Int. ACM SIGIR Conf. Research and Development in Information Retrieval*, Taipei, China, 2023, pp. 2293–2297.

[8] Y. Lu, P. Cui, L. Yu, L. Li, and W. Zhu, Uncovering the heterogeneous effects of preference diversity on user activeness: A dynamic mixture model, in *Proc. 28th ACM SIGKDD Conf. Knowledge Discovery and Data Mining*, Washington, DC, USA, 2022, pp. 3458–3467.

[9] M. Óskarsdóttir, K. E. Gísladóttir, R. Stefánsson, D. Aleman, and C. Sarraute, Social networks for enhanced player churn prediction in mobile free-to-play games, *Appl. Netw. Sci.*, vol. 7, no. 1, p. 82, 2022.

[10] W. Hamilton, J. Zhang, C. Danescu-Niculescu-Mizil, D. Jurafsky, and J. Leskovec, Loyalty in online communities, in *Proc. 11th Int. AAAI Conf. Web and Social Media*, Montreal, Canada, 2017, pp. 540–543.

[11] T. Althoff and J. Leskovec, Donor retention in online crowdfunding communities: A case study of DonorsChoose.org, in *Proc. 24th Int. Conf. World Wide Web*, Florence, Italy, 2015, pp. 34–44.

[12] J. Zhong, J. Wang, W. Peng, Z. Zhang, and M. Li, A feature selection method for prediction essential protein, *Tsinghua Science and Technology*, vol. 20, no. 5, pp. 491–499, 2015.

[13] Y. Qiu and C. Zhang, Research of indicator system in customer churn prediction for telecom industry, in *Proc. 11th Int. Conf. Computer Science & Education*, 2016, pp. 123–130.

[14] H. Zhou, X. Wang, and R. Zhu, Feature selection based on mutual information with correlation coefficient, *Appl. Intell.*, vol. 52, no. 5, pp. 5457–5474, 2022.

[15] A. E. M. Eljialy, M. Y. Uddin, and S. Ahmad, Novel framework for an intrusion detection system using multiple feature selection methods based on deep learning, *Tsinghua Science and Technology*, vol. 29, no. 4, pp. 948–958, 2024.

[16] Y. Lu, L. Yu, P. Cui, C. Zang, R. Xu, Y. Liu, L. Li, and W. Zhu, Uncovering the co-driven mechanism of social and content links in user churn phenomena, in *Proc. 25th ACM SIGKDD Int. Conf. Knowledge Discovery & Data Mining*, Anchorage, AK, USA, 2019, pp. 3093–3101.

[17] A. Anderson, L. Maystre, I. Anderson, R. Mehrotra, and M. Lalmas, Algorithmic effects on the diversity of consumption on Spotify, in *Proc. Web Conf.*, Taipei, China, 2020, pp. 2155–2165.

[18] H. Amiri and H. Daumé III, Short text representation for detecting churn in microblogs, in *Proc. 30th AAAI Conf. Artificial Intelligence*, Phoenix, AZ, USA, 2016, pp. 2566–2572.

[19] J. Piao, G. Zhang, F. Xu, Z. Chen, and Y. Li, Predicting customer value with social relationships via motif-based graph attention networks, in *Proc. of the Web Conf.*, Ljubljana, Slovenia, 2021, pp. 3146–3157.

[20] G. Zhang, J. Zeng, Z. Zhao, D. Jin, and Y. Li, A counterfactual modeling framework for churn prediction, in *Proc. 15th ACM Int. Conf. Web Search and Data Mining*, Virtual Event, 2022, pp. 1424–1432.

[21] K. Pearson, Note on regression and inheritance in the case of two parents, *Proc. Roy. Soc. London*, vol. 58, no. 347-352, pp. 240–242, 1895.

[22] I. Waller and A. Anderson, Generalists and specialists: Using community embeddings to quantify activity diversity in online platforms, in *Proc. World Wide Web Conf.*, San Francisco, CA, USA, 2019, pp. 1954–1964.

[23] L. V. Kantorovich, Mathematical methods of organizing and planning production, *Manag. Sci.*, vol. 6, no. 4, pp. 366–422, 1960.

[24] C. Danescu-Niculescu-Mizil, R. West, D. Jurafsky, J. Leskovec, and C. Potts, No country for old members: User lifecycle and linguistic change in online communities, in *Proc. 22nd Int. Conf. World Wide Web*, Rio de Janeiro, Brazil, 2013, pp. 307–318.

[25] F. Qian, Y. Gao, S. Zhao, J. Tang, and Y. Zhang, Combining topological properties and strong ties for link prediction, *Tsinghua Science and Technology*, vol. 22, no. 6, pp. 595–608, 2017.

[26] B. Abrahao, P. Parigi, A. Gupta, and K. S. Cook, Reputation offsets trust judgments based on social biases among Airbnb users, *Proc. Natl. Acad. Sci. USA*, vol. 114, no. 37, pp. 9848–9853, 2017.

[27] G. Kossinets and D. J. Watts, Empirical analysis of an evolving social network, *Science*, vol. 311, no. 5757, pp. 88–90, 2006.

[28] J. Saramäki, M. Kivelä, J.-P. Onnela, K. Kaski, and J. Kertész, Generalizations of the clustering coefficient to weighted complex networks, *Phys. Rev. E Stat. Nonlin. Soft Matter Phys.*, vol. 75, no. 2, p. 027105, 2007.

[29] J. Leskovec, L. Backstrom, R. Kumar, and A. Tomkins, Microscopic evolution of social networks, in *Proc. 14th ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining*, Las Vegas, NV, USA, 2008, pp. 462–470.

[30] X. Wang, J. Zhang, C. Gu, and F. Zhen, Examining antecedents and consequences of tourist satisfaction: A structural modeling approach, *Tsinghua Science and Technology*, vol. 14, no. 3, pp. 397–406, 2009.

[31] E. Guzman and W. Maalej, How do users like this feature? A fine grained sentiment analysis of app reviews, in *Proc. 22nd Int. Requirements Engineering Conf.*, Karlskrona, Sweden, 2014, pp. 153–162.

[32] M. Klein, J. Zhao, J. Ni, I. Johnson, B. M. Hill, and H. Zhu, Quality standards, service orientation, and power in Airbnb and Couchsurfing, *Proc. ACM on Human-Computer Interaction*, Volume 1, Issue CSCW, Virtual Event, 2017, p. 58.

[33] B. State, B. Abrahao, and K. Cook, Power imbalance and rating systems, in *Proc. 10th Int. AAAI Conf. Web and Social Media*, Cologne, Germany, 2016, pp. 368–377.

[34] Q. Gong, Y. Liu, J. Zhang, Y. Chen, Q. Li, Y. Xiao, X. Wang, and P. Hui, Detecting malicious accounts in online developer communities using deep learning, *IEEE Trans. Knowl. Data Eng.*, vol. 35, no. 10, pp. 10633–10649, 2023.

[35] Q. Gong, J. Zhang, Y. Chen, Y. Xiao, X. Fu, P. Hui, X. Li, and X. Wang, A representative user-centric dataset of 10 million GitHub developers, https://research.aalto.fi/en/datasets/a-representative-user-centric-dataset-of-10-million-github-develo, 2018.

[36] J. Leskovec. Complete Wikipedia edit history (up to January 2008), http://snap.stanford.edu/data/wiki-meta.html, 2008.

[37] Y. Chen, J. Hu, Y. Xiao, X. Li, and P. Hui, Understanding the user behavior of Foursquare: A data-driven study on a global scale, *IEEE Trans. Comput. Soc. Syst.*, vol. 7, no. 4, pp. 1019–1032, 2020.

[38] Sarwat foursquare dataset, https://archive.org/details/201309_foursquare_dataset_umn, 2013.

[39] J. Zhang, Y. Chen, Q. Gong, X. Wang, A. Y. Ding, Y. Xiao, and P. Hui, Understanding the working time of developers in IT companies in China and the United States, *IEEE Softw.*, vol. 38, no. 2, pp. 96–106, 2021.

[40] Q. Zhou, Y. Chen, C. Ma, F. Li, Y. Xiao, X. Wang, and X. Fu, Measurement and analysis of the reviews in Airbnb, in *Proc. IFIP Networking Conf. (IFIP Networking) and Workshops*, Zurich, Switzerland, 2018, pp. 1–9.

[41] G. Quattrone, D. Proserpio, D. Quercia, L. Capra, and M. Musolesi, Who benefits from the "sharing" Economy of Airbnb? in *Proc. 25th Int. Conf. World Wide Web*, Montreal, Canada, 2016, pp. 1385–1394.

[42] C. Hutto and E. Gilbert, VADER: A parsimonious rule-based model for sentiment analysis of social media text, in *Proc. 8th Int. AAAI Conf. Web and Social Media*, Ann Arbor, MI, USA, 2014, pp. 216–225.

---

## 作者简介

**Mengying Zhou** 2019 年获兰州大学信息安全专业学士学位,2025 年获复旦大学计算机科学博士学位。现为上海财经大学计算与人工智能学院助理教授。研究兴趣包括边缘 MLSys 与城市计算。

**Qianyu He** 2021 年获复旦大学学士学位,现为复旦大学博士研究生。主要研究方向为大语言模型(LLM)的指令遵循与数学推理能力,以提升其实用性与可靠性。

**Bruno Abrahao** 2014 年获美国康奈尔大学(伊萨卡,纽约州)计算机科学博士学位。现为纽约大学(纽约)助理教授,同时是上海纽约大学人工智能与深度学习中心的成员。曾在斯坦福大学(斯坦福,加州)从事博士后研究,并曾在微软研究院 AI 部门(雷德蒙德,华盛顿州)工作。研究兴趣包括信息系统、商业分析与全球网络。

**Xin Wang** 分别于 1994 年和 1997 年获西安电子科技大学信息论学士学位和通信与电子系统硕士学位,2002 年获日本静冈大学计算机科学博士学位。现为复旦大学计算机科学与人工智能学院教授。主要研究兴趣包括网络服务质量、下一代网络体系结构、移动互联网与网络编码。

**Yang Chen** 分别于 2004 年和 2009 年获清华大学学士与博士学位。现为复旦大学计算机科学与人工智能学院教授、上海市智能信息处理重点实验室副主任。曾在美国杜克大学(达勒姆,北卡罗来纳州)计算机科学系从事博士后研究。现任《Journal of Social Computing》副主编、《ACM Transactions on Social Computing》高级副编辑、《Computer Communications》副编辑;曾担任 SOSP、SIGCOMM、WWW、MobiSys、ICDCS、IJCAI、AAAI、IWQoS、ICCCN、GLOBECOM、ICC 等多个国际会议的组委会/程序委员会成员。在 TPDS、TDSC、TMC、TKDE、TSC、TCSS、TNSM、IEEE Communications Magazine、IEEE Software、Middleware、INFOCOM、ICDE、COSN、CIKM、IWQoS 等国际期刊与会议发表论文 50 余篇。研究兴趣包括社会计算、互联网体系结构与移动计算。

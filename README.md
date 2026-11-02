# 论文学习与代码复现

按论文建分支的学习仓库。每个分支对应一篇论文：论文原文、中文翻译、复现代码、数据获取指南。

**当前分支:`unifying-data-effectiveness-assessment`**

## 本分支对应的论文

> **Unifying Data Effectiveness Assessment in User Churn Detection: An Indicator-Assisted Framework**
> Mengying Zhou, Qianyu He, Bruno Abrahao, Xin Wang, Yang Chen
> *Tsinghua Science and Technology*, Vol. 31, No. 4, pp. 2237–2250, 2026
> DOI: 10.26599/TST.2024.9010230

论文提出指标辅助框架 **INFO**:用五个可解释的先验指标(活动周期性、活动多样性、语言、图结构、交互情感)在大规模实验之前评估各数据类别对流失检测任务的有效性。

## 目录结构

```
paper/        论文原文 PDF(开放获取,CC BY 4.0,转载请注明出处与 DOI)
docs/         中文全文翻译(公式按上下文重构,以原刊为准)
code/         复现代码(smoke_test.py = 五指标工具链冒烟测试)
data/         数据获取指南 + Foursquare 样例数据(各文件前 1000 行)
requirements.txt  Python 环境依赖清单
```

## 环境搭建

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python code/smoke_test.py   # 7 项工具链自检,全过即就绪
```

注意:NLTK 的 punkt 分词器需额外下载;若 `nltk.download` 被 SSRF 防护误拦(代理 fake-IP),用 curl 手动下载
`punkt.zip` / `punkt_tab.zip` 解压到 `~/nltk_data/tokenizers/`。

## 数据说明(重要)

**原始数据不入库**。原因:① 部分文件超过 GitHub 单文件 100MB 硬限制(如 Foursquare 的 socialgraph.dat 为 827MB);
② Foursquare(UMN Sarwat)数据集当年应平台方要求下架,再分发存在合规风险。本地原始数据存放于
`~/Downloads/201309_foursquare_dataset_umn/`,获取方式见 [data/README.md](data/README.md),
`data/foursquare_samples/` 内附各文件前 1000 行样例供跑通代码用。

## 复现进度

- [x] 论文精读 + 中文全文翻译
- [x] 五指标工具链环境搭建(pandas / scipy / networkx / sklearn / vaderSentiment / nltk)
- [x] Foursquare 数据获取与格式体检(时间跨度 2011-12 ~ 2012-04,与论文表 2 一致)
- [x] Wikipedia 数据源确认(SNAP enwiki-20080103.main.bz2)
- [x] Airbnb 替代数据源确认(Inside Airbnb / Kaggle,英文城市)
- [ ] 五指标在 Foursquare 上的计算
- [ ] 朴素模型 LR 后验实验与 r_intra / r_inter 验证

## 分支约定

新增论文时,从默认分支拉出新分支,以论文标题的英文短横线命名,例如
`unifying-data-effectiveness-assessment`。

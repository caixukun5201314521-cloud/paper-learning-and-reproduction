# 数据获取指南

INFO 论文使用五个数据集。原始数据**不提交到本仓库**(体积与合规原因,见主 README),本文件记录每个数据集的获取方式与本地位置。

## 1. Foursquare(UMN Sarwat 数据集)✅ 已下载

- 本地位置:`~Downloads/201309_foursquare_dataset_umn/umn_foursquare_datasets/`
- 文件与规模(数据行数,已与官方描述核对):

| 文件 | 字段 | 行数 |
|---|---|---|
| checkins.dat | id, user_id, venue_id, lat, lon, created_at | 1,021,968 |
| ratings.dat | user_id, venue_id, rating(1–5) | 2,809,581 |
| socialgraph.dat | first_user_id, second_user_id(无向好友边) | 27,098,490 |
| users.dat | id, latitude, longitude | 2,153,471 |
| venues.dat | id, latitude, longitude(**无类别字段**) | 1,143,092 |

- 格式:竖线 `|` 分隔,前 2 行为表头,第 3 行起为数据;时间跨度 2011-12-08 ~ 2012-04-23(论文表 2 的"5 个月"即此)。
- 获取渠道:archive.org 条目已锁定;镜像见 [Academic Torrents](https://academictorrents.com/details/b24c73949308b3f6bdd8fea1a485534392eef338)
  或 [GitHub 镜像](https://github.com/jalbertbowden/foursquare-user-dataset)。
- 合规注意:该数据集 2013 年应 Foursquare 要求下架,学术使用请引用 Sarwat 原始出处,勿公开再分发完整数据。
- 样例:`foursquare_samples/` 内为各文件前 1000 行(表头 + 数据),用于跑通解析代码。

## 2. Wikipedia(SNAP)⬜ 待下载

- 下载:https://snap.stanford.edu/data/wiki-meta.html → **只下 `enwiki-20080103.main.bz2`(8GB)**
- 格式:每条编辑 = 14 行带标签记录;关键字段 REVISION(时间戳/用户)、CATEGORY(分类)、COMMENT(评论文本)
- 时间跨度:2001 ~ 2008-01(与论文表 2 的 82 个月吻合)
- 引用:G. Kossinets, Processed Wikipedia Edit History;Leskovec et al., ICWSM 2010

## 3. Airbnb(公开替代:Inside Airbnb)⬜ 待下载

- 论文原始数据为作者自爬(交易 + 评论),**无公开渠道,只能邮件作者**;文字类指标可用公开替代
- 替代源:[Inside Airbnb](https://insideairbnb.com/get-the-data) 各城市 `reviews.csv.gz`(含评论文本);国内访问不便时用
  [Kaggle: NYC Airbnb Reviews](https://www.kaggle.com/datasets/thedevastator/discovering-new-york-city-through-airbnb-user-re) 或
  [Maven Analytics 10 城 500 万评论](https://mavenanalytics.io/data-playground/airbnb-listings-reviews)
- 选英文城市(纽约/伦敦)——VADER 只支持英文
- 局限:无交易数据 → 图结构指标(交易图)不可复现,语言/情感两指标可复现

## 4. GitHub(Aalto 数据集)⬜ 待核对

- 下载:https://research.aalto.fi/en/datasets/a-representative-user-centric-dataset-of-10-million-github-develo
  (论文引用[35]);引用[34]为 Gong et al., IEEE TKDE 2023

## 5. Couchsurfing ❌ 无公开渠道

- 数据出自 State et al., ICWSM 2016(文献[33]),惯例为向原作者邮件申请

# -*- coding: utf-8 -*-
"""
在本地 Foursquare(UMN Sarwat)数据上运行 INFO 的先验试验指标。
只算先验指标(式 1-7),不跑论文第 5 节的后验分类实验。

四个可算指标 + 一个 N/A:
  1. 活动周期性  式(1)(2)(3)  checkins.dat  →  user_id + created_at
  2. 活动多样性  式(4)         checkins.dat  →  user_id + venue_id(GS-score 用归一化熵代理,见报告说明)
  3. 图结构      式(6)         socialgraph.dat → 好友图聚类系数(抽样估计)
  4. 交互情感    式(7)         ratings.dat   →  偏置熵(评分 1-5 映射到 0-1)
  5. 语言        N/A           本数据集无文本(与论文表 3 一致)

运行: ~/info-repro/.venv/bin/python ~/info-repro/code/foursquare_indicators.py
输出: 终端打印 + results/foursquare_prior_results.json
"""
import json
import math
import random
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.stats import wasserstein_distance
from sklearn.mixture import GaussianMixture

DATA_DIR = Path("/Users/elthan/Downloads/201309_foursquare_dataset_umn/umn_foursquare_datasets")
OUT_DIR = Path(__file__).resolve().parent.parent / "results"
OUT_DIR.mkdir(exist_ok=True)


def iter_rows(path):
    """逐行读取 .dat 文件:竖线分隔、前 2 行表头、字段带空格垫料。"""
    with open(path, encoding="utf-8", errors="replace") as f:
        next(f), next(f)
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("("):   # 跳过空行和末尾的 "(N rows)" 落款
                continue
            yield [c.strip() for c in line.split("|")]


# ====================================================================
# 指标 1:活动周期性(式 1-3)
# ====================================================================
def segment_corr(series, p):
    """式(3):把序列切成若干长度为 p 的段,返回所有段对的 |皮尔逊相关| 平均。
    方差为 0 的段(计数恒定)无法算相关,先剔除。"""
    m = len(series) // p
    if m < 2:
        return np.nan
    segs = series[: m * p].reshape(m, p)
    segs = segs[segs.std(axis=1) > 0]   # 剔除常数段
    if len(segs) < 2:
        return np.nan
    corr = np.abs(np.corrcoef(segs))
    i, j = np.triu_indices(len(segs), 1)
    return float(np.mean(corr[i, j]))


def phi_at_granularity(series, g):
    """式(2):窗口长度 p = k·g(k=1,2,...),对每个 p 算式(3)再平均。"""
    vals = []
    for k in range(1, len(series) // g + 1):
        p = k * g
        if p < 2:
            continue
        v = segment_corr(series, p)
        if np.isfinite(v):
            vals.append(v)
    return float(np.mean(vals)) if vals else np.nan


def activity_periodicity(user_dates):
    # 数据集级日计数序列(论文:"系数度量数据集在对应粒度下的平均周期性")
    daily = Counter()
    for dates in user_dates.values():
        daily.update(dates)
    d0, d1 = date.fromisoformat(min(daily)), date.fromisoformat(max(daily))
    series = np.array(
        [daily.get(str(d0 + timedelta(days=i)), 0) for i in range((d1 - d0).days + 1)],
        dtype=float,
    )
    phis = {g: phi_at_granularity(series, g) for g in (1, 7, 30)}   # 日/周/月
    return {
        "series_days": len(series),
        "phi_day": round(phis[1], 4),
        "phi_week": round(phis[7], 4),
        "phi_month": round(phis[30], 4),
        "phi_final": round(max(phis.values()), 4),                    # 式(1):取最大
        "best_granularity": ["day", "week", "month"][int(np.argmax(list(phis.values())))],
    }


# ====================================================================
# 指标 2:活动多样性(式 4)
# ====================================================================
def activity_diversity(user_venues):
    # GS-score 代理:1 - 归一化熵。0=通才(场所分散),1=专才(场所集中)。
    gs = []
    for venues in user_venues.values():
        if len(venues) < 3:            # 至少 3 次签到、3 个场所,熵才稳定
            continue
        n = sum(venues.values())
        H = -sum((v / n) * math.log(v / n) for v in venues.values())
        gs.append(1.0 - H / math.log(len(venues)))
    gs = np.array(gs)

    # 双峰高斯拟合(式 4 前置步骤):GMM 两成分分别对应通才/专才两组
    gmm = GaussianMixture(n_components=2, random_state=0).fit(gs.reshape(-1, 1))
    labels = gmm.predict(gs.reshape(-1, 1))
    g0, g1 = gs[labels == 0], gs[labels == 1]

    return {
        "n_users_used": len(gs),
        "gs_mean": round(float(gs.mean()), 4),
        "gs_std": round(float(gs.std()), 4),
        "group0_mean": round(float(g0.mean()), 4),
        "group1_mean": round(float(g1.mean()), 4),
        "wasserstein_W": round(float(wasserstein_distance(g0, g1)), 4),  # 式(4)
    }


# ====================================================================
# 指标 3:图结构(式 6)——好友图聚类系数,抽样估计
# ====================================================================
def graph_structure(user_dates, n_sample=30000, seed=0):
    sample = set(random.Random(seed).sample(list(user_dates.keys()),
                                            min(n_sample, len(user_dates))))
    edges = []
    for row in iter_rows(DATA_DIR / "socialgraph.dat"):
        if len(row) != 2:                    # 跳过文件尾部的落款等杂项行
            continue
        a, b = row[0], row[1]
        if a in sample and b in sample:      # 只保留两端都在抽样集内的边(诱导子图)
            edges.append((a, b))
    G = nx.Graph(edges)
    return {
        "n_nodes_sampled": len(sample),
        "n_nodes_in_subgraph": G.number_of_nodes(),
        "n_edges_in_subgraph": G.number_of_edges(),
        "clustering_C": round(nx.average_clustering(G), 4),   # 式(6)
    }


# ====================================================================
# 指标 4:交互情感(式 7)——偏置熵
# ====================================================================
def interaction_sentiment():
    cnt = Counter()
    for row in iter_rows(DATA_DIR / "ratings.dat"):
        if len(row) == 3 and row[2]:         # 跳过落款与脏行
            cnt[int(row[2])] += 1
    total = sum(cnt.values())
    # 评分 r∈1..5 → s=(r-1)/4∈{0,.25,.5,.75,1};中性 s_neu=0.5;n_level=5
    E = 0.0
    for r, c in cnt.items():
        s = (r - 1) / 4
        p = c / total
        E += p * abs(s - 0.5) * (-math.log2(p))    # 偏移量加权的平均惊讶度
    return {
        "rating_dist": {str(r): cnt.get(r, 0) for r in range(1, 6)},
        "n_ratings": total,
        "biased_entropy_E": round(E, 4),
    }


# ====================================================================
def main():
    print("读取 checkins.dat(102 万行)……")
    user_dates = defaultdict(list)
    user_venues = defaultdict(Counter)
    for row in iter_rows(DATA_DIR / "checkins.dat"):
        if len(row) != 6:               # 跳过文件尾部的落款等杂项行
            continue
        uid, vid, created = row[1], row[2], row[5]
        user_dates[uid].append(created[:10])
        user_venues[uid][vid] += 1
    print(f"  用户 {len(user_dates):,} 名,签到 {sum(len(v) for v in user_dates.values()):,} 条")

    print("指标 1/4:活动周期性……")
    periodicity = activity_periodicity(user_dates)
    print(" ", periodicity)

    print("指标 2/4:活动多样性……")
    diversity = activity_diversity(user_venues)
    print(" ", diversity)

    print("指标 3/4:图结构(流式扫 2700 万行好友边,约几分钟)……")
    graph = graph_structure(user_dates)
    print(" ", graph)

    print("指标 4/4:交互情感……")
    sentiment = interaction_sentiment()
    print(" ", sentiment)

    results = {
        "dataset": "Foursquare (UMN Sarwat 201309)",
        "framework": "INFO 先验指标(论文式 1-7)",
        "activity_periodicity": periodicity,
        "activity_diversity": diversity,
        "graph_structure": graph,
        "interaction_sentiment": sentiment,
        "linguistic": "N/A(数据集无文本,与论文表 3 一致)",
    }
    out = OUT_DIR / "foursquare_prior_results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n结果已写入 {out}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
INFO 复现环境冒烟测试:五个指标 + 朴素模型的工具链各跑一个最小例子。
运行: /Users/elthan/info-repro/.venv/bin/python ~/info-repro/smoke_test.py
"""
import numpy as np

print("=" * 60)

# 1. pandas:聚合(用户×月份计数这类表的基础)
import pandas as pd
df = pd.DataFrame({
    "user_id": [1, 1, 1, 2, 2],
    "month":   ["2026-01", "2026-01", "2026-02", "2026-01", "2026-02"],
})
agg = df.groupby(["user_id", "month"]).size().unstack(fill_value=0)
print("[1] pandas 聚合 OK\n", agg.values, sep="")

# 2. scipy 皮尔逊相关:周期性指标(式3)
from scipy.stats import pearsonr
seg_a = np.array([3, 0, 5, 2, 4, 0, 6])   # 某用户第 1 个窗口的周计数
seg_b = np.array([4, 1, 5, 3, 5, 1, 6])   # 第 2 个窗口(形状相似)
r, p = pearsonr(seg_a, seg_b)
print(f"[2] 皮尔逊相关 OK  r = {r:.3f}(两窗口相似度,周期性原料)")

# 3. scipy Wasserstein 距离:多样性/语言指标(式4)
from scipy.stats import wasserstein_distance
gs_generalists = np.random.normal(0.2, 0.05, 500)   # 通才组 GS-score
gs_specialists = np.random.normal(0.8, 0.05, 500)   # 专才组
w = wasserstein_distance(gs_generalists, gs_specialists)
print(f"[3] Wasserstein 距离 OK  W = {w:.3f}(两组分布距离)")

# 4. networkx 聚类系数:图结构指标(式6)
import networkx as nx
G = nx.Graph([(0, 1), (0, 2), (1, 2), (2, 3), (3, 4), (4, 5), (5, 3)])
C = nx.average_clustering(G)
print(f"[4] 聚类系数 OK  C = {C:.3f}")

# 5. VADER:交互情感指标(式7 的打分器)
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()
s_pos = vader.polarity_scores("The room was great and the host was friendly!")["compound"]
s_neg = vader.polarity_scores("Terrible experience, never coming back.")["compound"]
print(f"[5] VADER OK  正面句 compound = {s_pos:+.3f},负面句 = {s_neg:+.3f}")

# 6. nltk:bigram 语言模型 + Kneser-Ney 平滑(SLM,式5)
from nltk.lm import KneserNeyInterpolated
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.tokenize import word_tokenize
sents = [word_tokenize(t) for t in [
    "great host and nice room", "nice room in good location",
    "great location and friendly host", "clean room and great stay",
]]
train, vocab = padded_everygram_pipeline(2, sents)
lm = KneserNeyInterpolated(2)
lm.fit(train, vocab)
import math
p_bigram = lm.score("great", ["host"])          # P(great | host)
xent = -math.log2(p_bigram)                     # 该 bigram 的惊讶度(比特)
print(f"[6] SLM OK  P(great|host) = {p_bigram:.3f},惊讶度 = {xent:.2f} 比特")

# 7. sklearn:朴素模型 LR + F1(第 5 节后验实验)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
n = 400
X = np.column_stack([rng.normal(0, 1, n), rng.normal(0, 1, n)])
X[: n // 2, 0] += 1.5          # 前一半样本(将来"流失")在特征0上偏高
y = np.array([1] * (n // 2) + [0] * (n // 2))
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
lr = LogisticRegression().fit(X_tr, y_tr)
f1 = f1_score(y_te, lr.predict(X_te))
print(f"[7] LR + F1 OK  F1 = {f1:.3f}")

print("=" * 60)
print("全部 7 项通过:INFO 五指标 + 朴素模型的工具链就绪。")

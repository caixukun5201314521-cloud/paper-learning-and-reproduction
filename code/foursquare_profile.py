# -*- coding: utf-8 -*-
"""
Foursquare(UMN Sarwat)数据全景体检:五个文件的规模、字段、时间结构、用户行为分布。
用途:复现前的数据档案,对照论文表 2,定位"复现值与论文值不一致"的数据侧原因。
运行: ~/info-repro/.venv/bin/python ~/info-repro/code/foursquare_profile.py
"""
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

from foursquare_indicators import DATA_DIR, iter_rows

WD = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

print("=" * 62)
print("Foursquare (UMN Sarwat 201309) 数据全景档案")
print("=" * 62)

# ---------- checkins ----------
per_user = Counter()
per_venue = Counter()
per_hour = Counter()
per_weekday = Counter()
per_day = Counter()
n = 0
for row in iter_rows(DATA_DIR / "checkins.dat"):
    if len(row) != 6:
        continue
    uid, vid, ts = row[1], row[2], row[5]
    per_user[uid] += 1
    per_venue[vid] += 1
    per_hour[int(ts[11:13])] += 1
    per_weekday[date.fromisoformat(ts[:10]).weekday()] += 1
    per_day[ts[:10]] += 1
    n += 1

days_sorted = sorted(per_day)
d0 = date.fromisoformat(days_sorted[0])
burst, best = None, (0, None, None)
for d in days_sorted + [str(date.fromisoformat(days_sorted[-1]) + timedelta(days=1))]:
    if burst is None:
        burst = [d, d]
    elif d == str(date.fromisoformat(burst[1]) + timedelta(days=1)):
        burst[1] = d
    else:
        L = (date.fromisoformat(burst[1]) - date.fromisoformat(burst[0])).days + 1
        if L > best[0]:
            best = (L, burst[0], burst[1])
        burst = [d, d]

print(f"""
【checkins.dat 签到记录】
  总条数           {n:,}
  独立用户         {len(per_user):,}
  独立场所         {len(per_venue):,}
  人均签到         {n/len(per_user):.2f} 次
  覆盖日期         {days_sorted[0]} ~ {days_sorted[-1]}(共 {(date.fromisoformat(days_sorted[-1])-d0).days+1} 天,
                   其中仅有签到的天数 {len(per_day)} 天)
  最长连续采集段   {best[1]} ~ {best[2]}({best[0]} 天)
  签到最多的5个用户: {[(u, c) for u, c in per_user.most_common(5)]}
  签到最多的5个场所: {[(v, c) for v, c in per_venue.most_common(5)]}

  每用户签到次数分布(解释论文子样本的筛选):
    1 次     {sum(1 for c in per_user.values() if c==1):>8,} 人({sum(1 for c in per_user.values() if c==1)/len(per_user)*100:.1f}%)
    2 次     {sum(1 for c in per_user.values() if c==2):>8,} 人
    3-5 次   {sum(1 for c in per_user.values() if 3<=c<=5):>8,} 人
    6-10 次  {sum(1 for c in per_user.values() if 6<=c<=10):>8,} 人
    >10 次   {sum(1 for c in per_user.values() if c>10):>8,} 人
    ≥6 次的用户合计 {sum(1 for c in per_user.values() if c>=6):,} 人,
      其签到合计 {sum(c for c in per_user.values() if c>=6):,} 条   ← 论文 27,304 人/184,723 条的量级

  按小时分布(UTC,前 6 多): {[(h, f'{c:,}') for h, c in per_hour.most_common(6)]}
  按星期分布: {[(WD[k], f'{c:,}') for k, c in sorted(per_weekday.items())]}
""")

# ---------- ratings ----------
r_users, r_venues, r_dist = set(), set(), Counter()
rn = 0
for row in iter_rows(DATA_DIR / "ratings.dat"):
    if len(row) == 3 and row[2]:
        r_users.add(row[0])
        r_venues.add(row[1])
        r_dist[int(row[2])] += 1
        rn += 1

print(f"""【ratings.dat 场所评分】
  总条数 {rn:,}   独立用户 {len(r_users):,}   被评场所 {len(r_venues):,}
  分布: {[(r, f'{c:,}') for r, c in sorted(r_dist.items())]}
""")

# ---------- users / venues ----------
u_n = sum(1 for _ in iter_rows(DATA_DIR / "users.dat"))
v_n = sum(1 for _ in iter_rows(DATA_DIR / "venues.dat"))

# ---------- socialgraph:只做行数统计(827MB,内容级统计见图结构指标) ----------
import subprocess
g_n = int(subprocess.run(["wc", "-l", str(DATA_DIR / "socialgraph.dat")],
                         capture_output=True, text=True).stdout.split()[0]) - 2 - 18

print(f"""【users.dat / venues.dat / socialgraph.dat】
  users.dat        {u_n:,} 行(用户及其常驻位置)
  venues.dat       {v_n:,} 行(场所及其坐标,无类别字段)
  socialgraph.dat  {g_n:,} 条好友边(两端均需在 users 中)
""")
print("=" * 62)
print("对照论文表 2(Foursquare 列):论文 27,304 用户 / 184,723 记录 / 5 个月 / 1 个月预测窗口")
print("本数据全集:485,381 用户 / 1,021,966 签到 / 138 天 —— 论文用的是活跃用户子样本")

# -*- coding: UTF-8 -*-
# 公司排名
import model.utils as utils


def extract(text_list, text_page_list, stock_name):
    rank_page_list = []
    # 段落位置百分比，取前 pos_percent 的段落
    pos_percent = 1 / 2
    subs = ["本公司", "本行", stock_name, "公司"]
    verbs = ["排名", "位居", "位列", "居"]
    units = ["位", "名", "前列", "榜首", "首位"]
    candidates = []
    for p in text_list[0:int(pos_percent * len(text_list))]:
        original_p = p  # 找页码时使用
        p = p.replace("；", "。").replace(";", "。")
        s_list = p.split("。")
        for s in s_list:
            if len(s) > 10 and len(s) < 500:
                sub = 0
                for su in subs:
                    if su in s:
                        sub += 1
                        break
                verb = 0
                for v in verbs:
                    if v in s:
                        verb += 1
                        break
                unit = 0
                for u in units:
                    if u in s:
                        unit += 1
                        break

                if sub + verb + unit == 3:
                    segs = utils.split_sentence(s)
                    words = [seg['word'] for seg in segs]
                    verb_ = 0
                    for v in verbs:
                        if v in words:
                            verb_ += 1
                            break
                    unit_ = 0
                    for u in units:
                        if u in words:
                            unit_ += 1
                            break
                    if verb_ + unit_ == 2:
                        s = s.strip() + '。'
                        s = utils.get_striped(s)
                        candidates.append(s)
                        rank_page_list.append(text_page_list[text_list.index(original_p)])

    if len(candidates) == 0:
        return None

    rank_list = candidates
    if len(rank_list) == 0:
        return None

    candidate_list = []
    for i in range(len(rank_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": rank_list[i],
                     "textPage": rank_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司排名",
                 "text": rank_list[0],
                 "candidate": candidate_list,
                 "pages": rank_page_list[0]}
    return knowledge


# 通过观察，排序意义不大
def candidates_filter_sort(candidates):
    candidates_ = []
    for c in candidates:
        if '股东' in c and '持有' in c:
            continue
        if '一致行动人' in c:
            continue
        candidates_.append(c)
    return candidates_


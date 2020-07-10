# -*- coding: UTF-8 -*-
# 公司营销网络
import model.utils as utils


def extract(text_list, text_page_list):
    sales_network_page_list = []
    # 段落位置百分比，取前 pos_percent 的段落
    # pos_percent = 1 / 2
    # subs = ["本公司", "本行", stock_name, "公司"]
    # verbs = ["排名", "位居", "位列", "居"]
    # units = ["位", "名", "前列", "榜首", "首位"]

    keywords = ['销售网络','营销网络']
    candidates = []
    for p in text_list:
        if utils.is_title(p) != -1:
            continue
        original_p = p  # 找页码时使用
        p = p.replace("；", "。").replace(";", "。")
        s_list = p.split("。")
        for s in s_list:
            if len(s) > 10 and len(s) < 500:
                # sub = 0
                # for su in subs:
                #     if su in s:
                #         sub += 1
                #         break
                # verb = 0
                # for v in verbs:
                #     if v in s:
                #         verb += 1
                #         break
                # unit = 0
                # for u in units:
                #     if u in s:
                #         unit += 1
                #         break

                for word in keywords:
                    if word in s:
                        s = s.strip() + '。'
                        s = utils.get_striped(s)
                        candidates.append(s)
                        sales_network_page_list.append(text_page_list[text_list.index(original_p)])

                # if sub + verb + unit == 3:
                #     segs = utils.split_sentence(s)
                #     words = [seg['word'] for seg in segs]
                #     verb_ = 0
                #     for v in verbs:
                #         if v in words:
                #             verb_ += 1
                #             break
                #     unit_ = 0
                #     for u in units:
                #         if u in words:
                #             unit_ += 1
                #             break
                #     if verb_ + unit_ == 2:
                #         s = s.strip() + '。'
                #         s = utils.get_striped(s)
                #         candidates.append(s)
                #         rank_page_list.append(text_page_list[text_list.index(original_p)])

    if len(candidates) == 0:
        return None

    sales_network_list = candidates
    if len(sales_network_list) == 0:
        return None

    candidate_list = []
    for i in range(len(sales_network_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": sales_network_list[i],
                     "textPage": sales_network_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司销售网络",
                 "text": sales_network_list[0],
                 "candidate": candidate_list,
                 "pages": sales_network_page_list[0]}
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

if __name__ == "__main__":
    s = '1.woshiasdnakmd'
    print(utils.is_title(s))
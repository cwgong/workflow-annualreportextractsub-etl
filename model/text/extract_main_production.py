# -*- coding: UTF-8 -*-
# 主要产品
import model.utils as utils


def extract(text_list, text_page_list):
    main_product_page_list = []
    # 定位 【第三（3）节 公司业务概要】 标题
    title_sub_position = None
    title_sub_words = ["第", "节", "公司业务概要"]
    catalogue = '.....'
    for i in range(len(text_list)):
        title_sub_condition = 0
        for word in title_sub_words:
            if word in text_list[i]:
                title_sub_condition += 1
        if title_sub_condition == len(title_sub_words) and catalogue not in text_list[i]:
            title_sub_position = i
            break
    subs = ["公司"]
    adjs = ["主要", "主营"]
    keywods = ["产品", "业务"]
    verbs = ["由", "有", "为", "以"]
    next_p_scope = 20
    candidates = []
    if title_sub_position is not None:  # 制造 recall:  0.973 年报/2018 recall:  0.969

        for p in text_list[title_sub_position: title_sub_position + next_p_scope]:
            original_p = p  # 找页码时使用
            p = p.strip()
            if len(p) > 1000 or len(p) < 10:
                continue
            # 去掉 “公司主营产品为：” 这类语义不完整数据
            if p[-1] != '。':
                continue
            sub_c = 0
            for sub in subs:
                if sub in p:
                    sub_c += 1
                    break
            adj_c = 0
            for adj in adjs:
                if adj in p:
                    adj_c += 1
                    break
            keyword_c = 0
            for keyword in keywods:
                if keyword in p:
                    keyword_c += 1
                    break
            verb_c = 0
            for verb in verbs:
                if verb in p:
                    verb_c += 1
                    break
            if sub_c + adj_c + keyword_c + verb_c == 4:
                segs = utils.split_sentence(p)
                words = [seg['word'] for seg in segs]
                sub_c = 0
                for sub in subs:
                    if sub in words:
                        sub_c += 1
                        break
                adj_c = 0
                for adj in adjs:
                    if adj in words:
                        adj_c += 1
                        break
                keyword_c = 0
                for keyword in keywods:
                    if keyword in words:
                        keyword_c += 1
                        break
                verb_c = 0
                for verb in verbs:
                    if verb in words:
                        verb_c += 1
                        break
                if sub_c + adj_c + keyword_c + verb_c == 4:
                    # print(p)
                    # print('===============')
                    candidates.append(p)
                    # not in list->改为detail？
                    main_product_page_list.append(text_page_list[text_list.index(original_p)])
                    # break

            if "公司主营" in p and "的生产和销售" in p:
                # print(p)
                # print('===============')
                candidates.append(p)
                main_product_page_list.append(text_page_list[text_list.index(p)])
                # break

    if len(candidates) == 0:
        return None

    main_product_list = candidates
    if len(main_product_list) == 0:
        return None
    candidate_list = []
    for i in range(len(main_product_list)):
        is_knowledge = False
        if i == 0:
            is_knowledge = True
        candidate = {"text": main_product_list[i],
                     "textPage": main_product_page_list[i],
                     "isKnowledge": is_knowledge}
        candidate_list.append(candidate)

    knowledge = {"type": "公司主要产品",
                 "text": main_product_list[0],
                 "candidate": candidate_list,
                 "pages": main_product_page_list[0]}
    return knowledge


# 需要对 candidates 进行筛选，暂时搁置
# 公司主要产品为、有；公司主要从事；xx业务：主要产品为：；主要产品：
# neg：产品的主要原材料有；
def candidates_filter_sort(candidates):
    candidates_ = []
    for c in candidates:
        candidates_.append(c)
    return candidates_


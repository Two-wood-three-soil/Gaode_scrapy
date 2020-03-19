import pandas as pd
import difflib
def string_similar(s1, s2):
    return difflib.SequenceMatcher(None,s1, s2).quick_ratio()

jqzq_1015 = pd.read_excel("票付通景区直签表（1015）.xlsx").dropna(subset=["景点名","市"]).reset_index(drop=True)
order_resource = pd.DataFrame(pd.read_excel("2019有订单资源清单-20191023.xls").dropna(subset=["资源名称","市"])).reset_index(drop=True)
land_summary = pd.read_excel("景区名录汇总表（山东、河南、福建）.xlsx").reset_index(drop=True)

jqzq_1015_land = jqzq_1015["景点名"].tolist()
order_resource_land = order_resource["资源名称"].tolist()
land_summary_land = land_summary["景区名称"].tolist()

print(string_similar("aaa","abb"))

# ls_j_dict = {}
# for ls_i,ls_k in enumerate(land_summary_land):
#     for j_i,j_k in enumerate(jqzq_1015_land):
#         # print(ls_k,j_k)
#         if string_similar(ls_k,j_k) > 0:
#             if str(jqzq_1015.loc[j_i,"市"]).find(land_summary.loc[ls_i,"所在地"]) != -1:
#                 land_summary.loc[ls_i,"直签"] = j_k
#                 ls_j_dict[ls_k] = j_k
# print(ls_j_dict)

# ls_or_dict = {}
# for ls_i,ls_k in enumerate(land_summary_land):
#     for or_i,or_k in enumerate(order_resource_land):
# #         print(string_similar(ls_k,j_k))
#         if string_similar(ls_k,or_k) > 0.5:
#             if str(order_resource.iloc[or_i,"市"]).find(land_summary.iloc[ls_i,"所在地"]) != -1:
#                 land_summary.iloc[ls_i,"直签"] = or_k
#                 ls_or_dict[ls_k] = or_k
# print(ls_or_dict)
import jieba
import pandas as pd

pd.set_option('max_colwidth', 200)
pd.set_option('display.max_rows', None)
a = ["今天下雨,我骑车差点摔倒,好在我一把把把把住了！",
     "来到杨过曾经生活的地方,小龙女动情地说,我也想过过过儿过过的生活",
     "多亏跑了两步,差点没上上上海的车",
     "用毒毒毒蛇毒蛇会不会被毒毒死",
     "校长说:校服上除了校徽别别别的,让你们别别别的别别别的你非得别别的！"]
res = [list(jieba.cut(i)) for i in a]
print(res)
ret = [" ".join(i) for i in res]
print(ret)
print(pd.DataFrame(ret))

import json

if __name__ == '__main__':
    update_question = "UPDATE t_res_{subject_key}_question set context = replace(context,'{old_url}','{new_url}') WHERE create_time >= '2018-04-17 00:00:00';"
    update_item = "UPDATE t_res_{subject_key}_item set content = replace(content,'{old_url}','{new_url}') WHERE create_time >= '2018-04-17 00:00:00';"
    f1 = open("F:/update.txt",encoding="utf8",mode="a")
    with open("F:/img.txt", mode="r", encoding="utf8") as f:
        for line in f.readlines():
            line = json.loads(line)
            for key, val in line.items():
                f1.write(update_question.format(subject_key="sx",old_url=key, new_url=val))
                f1.write("\n")
                f1.write(update_item.format(subject_key="sx", old_url=key, new_url=val))
                f1.write("\n")
                f1.write(update_question.format(subject_key="wl", old_url=key, new_url=val))
                f1.write("\n")
                f1.write(update_item.format(subject_key="wl", old_url=key, new_url=val))
                f1.write("\n")
    f1.close()
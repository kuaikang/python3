import requests
import pymysql, time, threading
import contextlib


# 定义上下文管理器，连接后自动关闭连接
@contextlib.contextmanager
def mysql_local(host='localhost', port=3333, user='root', password='kuaikang', db='kuaik', charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=db, charset=charset)
    conn.autocommit(True)
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        conn.commit()
        cur.close()
        conn.close()


def get_question_ids(subject_key, chapter_id):
    with mysql_local() as cur:
        sql = "SELECT question_id from {subject_key}_chapter_question WHERE chapter_id = '{chapter_id}'"
        cur.execute(sql.format(subject_key=subject_key, chapter_id=chapter_id))
        return cur.fetchall()


def get_question(subject_key, question_id):
    with mysql_local() as cur:
        sql = "SELECT context,question_type,difficult,answer_url from {subject_key}_question WHERE question_id = '{question_id}' and answer_url is not null"
        cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
        return cur.fetchall()


def get_tag(subject_key, question_id):
    with mysql_local() as cur:
        sql = "SELECT tag_url from {subject_key}_tag_question WHERE question_id = '{question_id}'"
        cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
        return cur.fetchone()


def get_item(subject_key, question_id):
    with mysql_local() as cur:
        sql = "SELECT context,`option` from {subject_key}_item WHERE question_id = '{question_id}'"
        cur.execute(sql.format(subject_key=subject_key, question_id=question_id))
        return cur.fetchall()


def main(currentSubject, importChapterName, import_Chapter, zujuan_chapter):
    print(importChapterName)
    head = {
        "Content-Type": "application/json"
    }
    with mysql_local() as cur:
        question_ids = get_question_ids(currentSubject, zujuan_chapter)
        for question_id in question_ids:
            question = get_question(currentSubject, question_id.get('question_id'))
            for q in question:  # context,type,difficult,answer_url
                req = {"currentSubject": currentSubject, "questionContent": q.get('context'),
                       "importChapterId": import_Chapter,
                       "questionType": "11"}
                tag = get_tag(currentSubject, question_id.get('question_id'))
                if tag:
                    req["tagUrl"] = tag.get('tag_url')
                else:
                    req["tagUrl"] = ""
                req["importChapterName"] = importChapterName
                req["answerUrl"] = q.get('answer_url')
                req["difficult"] = q.get('difficult')
                items = get_item(currentSubject, question_id.get('question_id'))
                item = []
                for it in items:  # context,`option`
                    item.append({"content": it.get('context'), "option": it.get('option')})
                req["items"] = item
                resp = requests.post(url="http://localhost:28870/exue-question-system/spark/save", headers=head,
                                     json=req)


def trans(subject, data):
    for d in data:
        main(subject, d[0], d[1], d[2])


if __name__ == '__main__':
    li = [['Lesson 1 On the Farm', '030003002017100001001', '78006'],
          ['Lesson 2 Cats and Dogs', '030003002017100001002', '78007'],
          ['Lesson 3 Fish and Birds', '030003002017100001003', '78008'],
          ['Lesson 4 Horses and Rabbits', '030003002017100001004', '78009'],
          ['Lesson 5 Where?', '030003002017100001005', '78010'],
          ['Lesson 6 Can I Help You?', '030003002017100001006', '78014'],
          ['Lesson 7 At the Zoo', '030003002017100002001', '78015'],
          ['Lesson 8 Tigers and Bears', '030003002017100002002', '78016'],
          ['Lesson 9 How Many?', '030003002017100002003', '78017'],
          ['Lesson 10 Where Do They Live?', '030003002017100002004', '78018'],
          ['Lesson 11 What Do They Eat?', '030003002017100002005', '78019'],
          ['Lesson 12 The Clever Monkey', '030003002017100002006', '78020'],
          ["Lesson 13 I'm Hungry!", '030003002017100003001', '78024'],
          ['Lesson 14 Would You Like Some Soup?', '030003002017100003002', '78025'],
          ["Lesson 15 What's Your Favourite Food?", '030003002017100003003', '78026'],
          ["Lesson 17 What's for Breakfast?", '030003002017100003005', '78028'],
          ['Lesson 18 The Magic Stone', '030003002017100003006', '78029'],
          ['Lesson 19 I Like Fruit!', '030003002017100004001', '78033'],
          ['Lesson 20 Hamburgers and Hot Dogs', '030003002017100004002', '78034'],
          ['Lesson 21 In the Restaurant', '030003002017100004003', '78035'],
          ['Lesson 22 How Much Is It?', '030003002017100004004', '78036'],
          ['Lesson 23 How Much Are They?', '030003002017100004005', '78037'],
          ['Lesson 24 A Little Monkey', '030003002017100004006', '78038'],
          ['Lesson 1 How Are You?', '030004002017100001001', '117887'],
          ['Lesson 2 Is This Your Pencil?', '030004002017100001002', '48543'],
          ['Lesson 3 Where Are They?', '030004002017100001003', '48546'],
          ['Lesson 4 How Many Books Are There?', '030004002017100001004', '117888'],
          ['Lesson 5 Where Is Danny?', '030004002017100001005', '117889'],
          ['Lesson 6 Little Zeke', '030004002017100001006', '88158'],
          ['Lesson 7 Months of the Year', '030004002017100002001', '48549'],
          ['Lesson 9 When Is It?', '030004002017100002003', '48551'],
          ['Lesson 10 Rain and Sun', '030004002017100002004', '48552'],
          ["Lesson 11 How's the Weather Today?", '030004002017100002005', '48553'],
          ["Lesson 12 Mr. Moon's Birthday", '030004002017100002006', '88160'],
          ['Lesson 13 How Old Are You?', '030004002017100003001', '48557'],
          ['Lesson 14 Are You Short or Tall?', '030004002017100003002', '48558'],
          ['Lesson 15 Where Do You Live?', '030004002017100003003', '48560'],
          ['Lesson 16 How Do You Go to School?', '030004002017100003004', '117893'],
          ['Lesson 17 What Do You Like to Do?', '030004002017100003005', '117894'],
          ['Lesson 18 Maddy the Monster', '030004002017100003006', '88162'],
          ['Lesson 19 My Favourite Colours', '030004002017100004001', '48565'],
          ['Lesson 20 My Favourite Clothes', '030004002017100004002', '48566'],
          ['Lesson 21 My Favourite Food', '030004002017100004003', '48567'],
          ['Lesson 22 My Favourite Subject', '030004002017100004004', '88165'],
          ['Lesson 23 My Favourite School Work', '030004002017100004005', '48570'],
          ['Lesson 24 The Diffos', '030004002017100004006', '88166'],
          ['Lesson 1 I Am Excited!', '030005002017100001001', '114006'],
          ['Lesson 2 What Are You Doing?', '030005002017100001002', '114007'],
          ['Lesson 3 Who Is Singing?', '030005002017100001003', '114008'],
          ['Lesson 4 Who Is Hungry?', '030005002017100001004', '114009'],
          ['Lesson 5 What Are They Doing?', '030005002017100001005', '114010'],
          ['Lesson 6 Danny is Lost!', '030005002017100001006', '114011'],
          ['Lesson 7 Arriving in Beijing', '030005002017100002001', '48586'],
          ["Lesson 8 Tian'anmen Square", '030005002017100002002', '48588'],
          ['Lesson 9 The Palace Museum', '030005002017100002003', '48589'],
          ['Lesson 10 The Great Wall', '030005002017100002004', '114017'],
          ['Lesson 11 Shopping in Beijing', '030005002017100002005', '48591'],
          ['Lesson 12 A visit to the Great Wall', '030005002017100002006', '114018'],
          ["Lesson 13 Let's Buy Postcards!", '030005002017100003001', '48594'],
          ['Lesson 14 Jenny Writes a Postcard', '030005002017100003002', '48595'],
          ['Lesson 15 Sending the Postcards', '030005002017100003003', '117919'],
          ['Lesson 16 An Email Is Fast', '030005002017100003004', '114023'],
          ["Lesson 17 Danny's Email", '030005002017100003005', '114020'],
          ['Lesson 18 Little Zeke Sends an Email', '030005002017100003006', '114021'],
          ['Lesson 19 Li Ming Comes Home', '030005002017100004001', '48602'],
          ['Lesson 20 Jenny Goes Home', '030005002017100004002', '48603'],
          ['Lesson 21 Look at the Photos!', '030005002017100004003', '114024'],
          ['Lesson 22 Gifts for Everyone', '030005002017100004004', '48606'],
          ['Lesson 23 An Email from Li Ming', '030005002017100004005', '114025'],
          ['Lesson 24 A Gift for Little Zeke', '030005002017100004006', '114026'],
          ['Lesson 1 Ping-pong and Basketball', '030006002017100001001', '48614'],
          ['Lesson 2 At the Sports Shop', '030006002017100001002', '48615'],
          ["Lesson 3 Let's Play!", '030006002017100001003', '114032'],
          ['Lesson 4 Did You Have Fun?', '030006002017100001004', '114033'],
          ['Lesson 5 A Basketball Game', '030006002017100001005', '114034'],
          ['Lesson 6 A Famous Football Player', '030006002017100001006', '114035'],
          ['Lesson 7 Always Have Breakfast!', '030006002017100002001', '48622'],
          ['Lesson 8 Always Brush Your Teeth!', '030006002017100002002', '48623'],
          ['Lesson 9 Eat More Vegetables and Fruit!', '030006002017100002003', '48625'],
          ['Lesson 10 Exercise', '030006002017100002004', '48626'],
          ['Lesson 11 Work Hard!', '030006002017100002005', '48627'],
          ['Lesson 12 Helen Keller', '030006002017100002006', '114036'],
          ['Lesson 13 Summer Is Coming!', '030006002017100003001', '48630'],
          ['Lesson 14 Tomorrow We Will Play', '030006002017100003002', '48633'],
          ["Lesson 15 Jenny's Summer Holiday", '030006002017100003003', '114037'],
          ["Lesson 16 Li Ming's Summer Holiday", '030006002017100003004', '114038'],
          ["Lesson 17 Danny's Summer Holiday", '030006002017100003005', '114039'],
          ['Lesson 18 Three Kites in the Sky', '030006002017100003006', '114040'],
          ['Lesson 19 Buying Gifts', '030006002017100004001', '48638'],
          ['Lesson 20 Looking at Photos', '030006002017100004002', '48639'],
          ['Lesson 21 A Party for Li Ming', '030006002017100004003', '48641'],
          ['Lesson 22 Surprise!', '030006002017100004004', '48642'],
          ['Lesson 23 Good-bye!', '030006002017100004005', '48643'],
          ["Lesson 24 Danny's Surprise Cake", '030006002017100004006', '114041']]
    for i in range(4):
        count = 24
        t = threading.Thread(target=trans, args=("yy", li[count * i:count * i + count],))
        t.start()

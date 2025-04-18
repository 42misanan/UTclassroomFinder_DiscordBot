import csv

while True:
    is_found = False
    target = input('科目番号を指定してください(例/coins3クラ「学問への誘い」: 1227591 を入力), break で終了:')
    with open('kdb_2025-ja.csv', mode='r', encoding='UTF-8') as csvfile:
        classList = csv.DictReader(csvfile)
        result = classList.get(target, '教室')
        if target == 'break': #終了操作
            break

        for row in classList: #リストを検索
            if row['科目番号'] == target: #一致時処理
                if result == "": #教室なしの分岐
                    print(f'{target} {row['科目名']} の教室は 指定されていません. もしかして: オンデマ')
                    is_found = True
                    break
                else: #教室ありの分岐
                    print(f'{target} {row['科目名']} の教室は {result} です')
                    is_found = True
                    break

        if is_found == False: #検索後の不一致時処理
            print('一致するものがありませんでした')

import json
import requests


class Api:
    def __init__(self):
        self.result = 0
        pass

    def get_data(self):
        url = "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="

        start_round = 1
        end_round = 5
        lotto_file = dict()
        self.result = 1
        for i in range(start_round, end_round + 1):
            res = requests.get(url + str(i))
            res_json = res.json()
            if res_json["returnValue"] == "success":
                lotto_file[i] = res_json
            else:
                print("wrong round %s" % i)

        with open(f'./data/data_${end_round}.json', 'w', encoding='utf-8') as f:
            json.dump(lotto_file, f, indent="\t")

        with open(f'./data/data_${end_round}.json', 'r') as f:
            json_data = json.load(f)

        return json.dumps(json_data, indent="\t").replace('\t', ' ')

import json


class Prediction:
    def __init__(self, start_round, end_round):
        with open(f'./data/data_${end_round}.json', 'r') as f:
            json_data = json.load(f)

        self.lotto_history = []
        self.prediction_dict = {}
        for i in range(7):
            self.prediction_dict[i] = 0.0

        for i in range(1, len(json_data)):
            arr = []
            for j in range(1, 7):
                arr.append(json_data[str(i + start_round)]["drwtNo" + str(j)])
            arr.sort()
            self.lotto_history.append(arr)

        self.lotto_history_len = len(self.lotto_history)
        self.replication_count = (self.lotto_history_len * (self.lotto_history_len - 1)) / 2

        self.make_dictionary()

    # nC_2 조합
    def make_dictionary(self):
        for (i, nums) in enumerate(self.lotto_history):
            if self.lotto_history_len == i + 1:
                break
            for next_nums in self.lotto_history[i + 1:]:
                count = 0
                for num in nums:
                    if num in next_nums:
                        count += 1
                self.prediction_dict[count] += 1

        for i in self.prediction_dict:
            self.prediction_dict[i] = self.prediction_dict[i] / self.replication_count

    def check(self):
        return self.prediction_dict

    def statistic_calculate(self, expect_nums):
        user_prediction_dict = {}
        for i in range(7):
            user_prediction_dict[i] = 0.0

        for nums in self.lotto_history:
            for ex_nums in expect_nums:
                count = 0
                if ex_nums in nums:
                    count += 1
            user_prediction_dict[count] += 1

        for i in user_prediction_dict:
            user_prediction_dict[i] = user_prediction_dict[i] / self.lotto_history_len

        diff_sum = 0
        for i in range(7):
            diff = self.prediction_dict[i] - user_prediction_dict[i]
            diff_sum += abs(diff)

        # 확률의 다름 정도가 가장 적은 경우 추출
        angle_possibility = 1 - diff_sum / 2
        if angle_possibility < 0.25:
            angle_answer = '다른 번호를 추천'
        elif angle_possibility < 0.5:
            angle_answer = '어려운 도전'
        elif angle_possibility < 0.75:
            angle_answer = '해볼만한 도전'
        else:
            angle_answer = '번호를 추천'

        return json.dumps({
            'angle_answer': angle_answer,
            'angle_possibility': angle_possibility
        }, ensure_ascii=False).encode('utf8')

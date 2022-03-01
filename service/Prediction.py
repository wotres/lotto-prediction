import json
from itertools import combinations


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

        # todo: 주단위 배치로 처리
        self.make_candidate()
        self.candidate_numbers = self.make_candidate()

        self.recommend_numbers = []
        for nums in self.candidate_numbers:
            _, possibility = self.calculate_statistics(nums)
            if possibility > 0:
                self.recommend_numbers.append([nums, possibility])

        # 후보 번호중 가장 angle 확률이 높게 나온 번호 추출
        max_value = 0
        self.max_recommend_numbers = []
        for i, value in enumerate(self.recommend_numbers):
            if value[1] >= max_value:
                max_value = value[1]
                self.max_recommend_numbers.append(value)

    # 숫자 조합 걸러내기
    def make_candidate(self):
        temp = []
        for i in range(1, 8):
            temp.append(i)
        all_numbers = list(combinations(temp, 6))
        return all_numbers
        # candidate_numbers = []
        # for nums in all_numbers:
        #     # 연속된 숫자 여부
        #     count1 = 0
        #     count10 = 0
        #     count20 = 0
        #     count30 = 0
        #
        #     for num in nums:
        #         if num < 10:
        #             count1 += 1
        #         elif num < 20 and num >= 10:
        #             count10 += 1
        #         elif num < 30 and num >= 20:
        #             count20 += 1
        #         elif num < 40 and num >= 40:
        #             count30 += 1
        #
        #     # 연속된 숫자 여부
        #     ex_num = 0
        #     tf = True
        #     for num in nums:
        #         if num - ex_num == 1:
        #             tf = False
        #             break
        #         else:
        #             ex_num = num
        #
        #     # 해당사항을 통과한다면 후보 번호로 추출
        #     if tf and count1 <= 4 and count10 <= 4 and count20 <= 4 and count30 <= 4:
        #         candidate_numbers.append(nums)

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

    def calculate_statistics(self, expect_nums):
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

        return angle_answer, angle_possibility

    def recommend(self):
        return self.max_recommend_numbers


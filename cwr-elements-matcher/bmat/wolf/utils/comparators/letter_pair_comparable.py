__author__ = 'Dani'

import re

class LetterPairComparable:


    @staticmethod
    def compare(str1, str2):
        """
        :param str1: string param
        :param str2: string param
        :return: lexical similarity value in the range [0,1]
        """
        pairs1 = LetterPairComparable._word_letter_pairs(str1.upper())
        pairs2 = LetterPairComparable._word_letter_pairs(str2.upper())

        intersection = 0
        union = max(len(pairs1), len(pairs2)) * 2

        for pair1 in pairs1:
            for pair2 in pairs2:
                if pair1 == pair2:
                    intersection += 1
                    pairs2.remove(pair2)
                    break
        return (intersection * 2.0) / union  # Result double


    @staticmethod
    def _letter_pairs(str1):
        num_pairs = len(str1) - 1
        if num_pairs == 0:  # if str1 is a single char
            return [str1]
        pairs = []
        for i in range(0, num_pairs):
            pairs.append(str1[i: i + 2])
        return pairs


    @staticmethod
    def _word_letter_pairs(str1):
        """
        :param str1: string param
        :return: list of 2-character strings
        """
        all_pairs = []
        words = re.split("\\s", str1)
        for word in words:
            if word != "":
                all_pairs += LetterPairComparable._letter_pairs(word)
        return all_pairs



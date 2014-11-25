__author__ = 'Dani'

import unicodedata
import re
import math
from comparators.letter_pair_comparable import LetterPairComparable
from comparators.weightned_damerau_levenshtein_distance_coparable import WeightnedDamerauLevenshteinDistanceComparable


class StringUtils(object):

    WRONG_NUMBER_PENALIZATION = 0.85

    NUMBER_PATTERN = re.compile("([0-9]+)")
    ROMAN_PATTERN = re.compile(" ([xvi]{1,5}) |^([xvi]{1,5}) | ([xvi]{1,5})$")
    # PATTERN_DIACRITICAL_MARKS = re.compile("\\p{InCombiningDiacriticalMarks}+", flags=re.UNICODE)  # InCombiningDiacritialMarks = 0300..036F
    # PATTERN_NO_LETTER_NO_NUMBER = re.compile("[^\\p{L}\\p{Nd}\\s]", flags=re.UNICODE)  # Nd --> Decimal digit number. L --> Letter
    PATTERN_NO_NUMBER_NO_LETTER = re.compile("[^a-zA-Z0-9\\s]", flags=re.UNICODE)
    PATTERN_NO_NUMBER_NO_SPECIAL_LETTERS = re.compile("[^\\w0-9\\s]", flags=re.UNICODE)
    PATTERN_WHITE_SPACES = re.compile("(_|  )+")  # In the original code this pattern was " +". I have changed it adding
                                              # one more blank because the patter is always used to replace the matches
                                              # by a single blank. Since " " match, then we would be changing the
                                              # apparitions of " " by an identical string.
    PATTERN_POINT = re.compile("\\.")
    PATTERN_PUNCTUATION_SYMBOLS_WITH_SPACES = re.compile("( *[;,&|/\\+] *)")




    @staticmethod
    def normalize(original):
        if type("a") == type(original):
            return StringUtils._normalize_string(original)
        elif type([]) == type(original):
            result = []
            for a_str in original:
                result.append(StringUtils._normalize_string(a_str))
            return result
        else:
            raise ValueError("Unexpected type while executing 'normalize' method: {}".format(type(original)))


    @staticmethod
    def _normalize_string(str_original, space=True):
        return StringUtils.clean(str_original, space)

    @staticmethod
    def clean(original_str, space=True):
        if original_str is None:
            return ""
        space_str = " " if space else ""

        result = original_str.decode(encoding="utf-8")
        result = unicodedata.normalize('NFD', result)
        result = StringUtils.PATTERN_NO_NUMBER_NO_LETTER.sub(space_str, result).strip()
        result = str(StringUtils.PATTERN_WHITE_SPACES.sub(" ", result))

        if len(result) == 0:
            return StringUtils.PATTERN_WHITE_SPACES.sub(" ", original_str.strip())
        else:
            return result

    @staticmethod
    def compare(str1, str2):
        """
        It accepts as param string objects or iterables containing strings (or a mix)
        In case of comparing strings, it will calculate a floar number and return it.
        In case of iterables, it will compare every possible pair of strings joining
        an element of str1 and str2 and will return the max number obtained.


        :param str1:
        :param str2:
        :return:
        """
        if type("") == type(str1):
            str1 = [str1]
        if type("") == type(str2):
            str2 = [str2]

        current = 0
        max_result = 0
        for elem1 in str1:
            for elem2 in str2:
                current = StringUtils._compare_strings(elem1, elem2)
                if current > max_result:
                    max_result = current
        return max_result

    @staticmethod
    def _compare_strings(str1, str2):
        str1, occurs_number1, str2, occurs_number2, number_penalization = StringUtils._replace_pattern_and_deduce_number_penalization(str1,
                                                                                                      str2,
                                                                                                      StringUtils.NUMBER_PATTERN)
        str1_backup = str1
        str2_backup = str2
        number_penalization_backup = number_penalization
        str1, occurs_roman1, str2, occurs_roman2, number_penalization = StringUtils._replace_pattern_and_deduce_number_penalization(str1,
                                                                                                      str2,
                                                                                                      StringUtils.ROMAN_PATTERN,
                                                                                                      number_penalization)
        if occurs_roman1 != occurs_roman2:  # That could mean that roman numbers are not roman numbers, but words
            str1 = str1_backup
            str2 = str2_backup
            number_penalization = number_penalization_backup

        str1 = re.sub(StringUtils.PATTERN_WHITE_SPACES, " ", str1.strip())
        str2 = re.sub(StringUtils.PATTERN_WHITE_SPACES, " ", str2.strip())

        result = float(max(LetterPairComparable.compare(str1, str2),
                           WeightnedDamerauLevenshteinDistanceComparable.compare(str1, str2)))

        if not math.isnan(result):
            if number_penalization:
                return result * StringUtils.WRONG_NUMBER_PENALIZATION
            else:
                return result

        #TODO: The next else should probably must be sustituted by "else return 0", but
        #TODO: this is the translation of the original algorithm. Check/ask for this
        else:
            if (occurs_number1 != 0 and occurs_number1 == occurs_number2) \
                    or (occurs_roman1 != 0 and occurs_roman2 == occurs_roman1) :
                return 0
            else:
                return 1  # TODO: Sure??

    @staticmethod
    def _replace_pattern_and_deduce_number_penalization(str1, str2, pattern, penalized_previously=False):
        """

        :param str1:
        :param str2:
        :param pattern:
        :param penalized_previously:
        :return:  5 elements:
                1 --> new string1
                2 --> number of substitutions in str1
                3 --> new str2
                4 --> number of substitutions in str2
                5 --> penalization for not having identical matches (bool)
        """

        number_penalization = False

        ## If we already have a penalization then we continue having it, nothing more to check
        # number_penalization = True if the strings has the same number of matches and they are identical.
        # In any other case, number_penalization = False
        if penalized_previously:
            number_penalization = True
        else:
            ite1 = re.finditer(pattern, str1)
            ite2 = re.finditer(pattern, str2)

            match1 = match2 = ""

            while not (match1 is None or match2 is None):
                try:
                    match1 = next(ite1).group()
                except BaseException:
                    match1 = None
                try:
                    match2 = next(ite2).group()
                except BaseException:
                    match2 = None

                if match1 != match2:
                    number_penalization = True
                    break

        # Once we checked penalization we have to remove anyway all the occurences.
        tupl1 = re.subn(pattern, " ", str1)  # Removing matches of pattern
        tupl2 = re.subn(pattern, " ", str2)  # Removing matches of pattern


        return tupl1[0], tupl1[1], tupl2[0], tupl2[1], number_penalization


    @staticmethod
    def isolate_punctuation(str_original):
        result = re.sub(StringUtils.PATTERN_POINT, ". ", str_original)
        result = re.sub(StringUtils.PATTERN_PUNCTUATION_SYMBOLS_WITH_SPACES, " \\1 ", result)
        result = re.sub(StringUtils.PATTERN_WHITE_SPACES, " ", result)
        return result.strip()


    @staticmethod
    def normalize_and_compare(str1, str2):
        return StringUtils.compare(StringUtils.normalize(str1),
                                   StringUtils.normalize(str2))


    @staticmethod
    def remove_puntuation(str_original):
        result = str_original.decode(encoding="utf-8")
        result = re.sub(StringUtils.PATTERN_NO_NUMBER_NO_SPECIAL_LETTERS, " ", result)
        result = re.sub(StringUtils.PATTERN_WHITE_SPACES, " ", result)
        return str(result.encode(encoding="utf-8")).strip()


    @staticmethod
    def reduce_and_compare(str1, str2):
        str1 = StringUtils.normalize(str1)
        str2 = StringUtils.normalize(str2)

        set1 = set()
        set2 = set()
        words1 = str1.split(" ")
        words2 = str2.split(" ")

        resulting_str1 = ""
        resulting_str2 = ""

        for word in words1:
            set1.add(word)

        for word in words2:
            set2.add(word)
            if word not in set1:
                resulting_str2 += word + " "

        for word in words1:
            if word not in set2:
                resulting_str1 += word + " "

        resulting_str1 = resulting_str1.strip()
        resulting_str2 = resulting_str2.strip()

        ratio_of_difference1 = float(len(resulting_str1)) / float(len(str1))
        ratio_of_difference2 = float(len(resulting_str2)) / float(len(str2))

        difference_result = StringUtils.compare(resulting_str1, resulting_str2)

        print str1 + " [" + str(len(str1)) + "] vs " + str2 + " [" + str(len(str2)) + "]"
        print "-------------------"
        print "difs"
        print resulting_str1
        print resulting_str2
        print "difs compare"
        print difference_result
        print "default compare"
        print StringUtils.compare(str1, str2)
        print "ratios"
        print ratio_of_difference1
        print ratio_of_difference2

        max_ratio = max(ratio_of_difference1, ratio_of_difference2)
        result = max_ratio + difference_result * (1 - max_ratio)

        print "res"
        print result
        print "-------------------"

        return result


    @staticmethod
    def lcs(str1, str2):
        str1 = StringUtils.normalize(str1)
        str2 = StringUtils.normalize(str2)

        lenghts = []
        for i in range(0, len(str1) + 1):
            lenghts.append([])
            for j in range(0, len(str2) + 1):
                lenghts[i].append(0)

        for i in range(0, len(str1)):
            for j in range(0, len(str2)):
                if str1[i] == str2[j]:
                    lenghts[i + 1][j + 1] = lenghts[i][j] + 1
                else:
                    lenghts[i + 1][j + 1] = max(lenghts[i + 1][j],
                                                lenghts[i][j + 1])

        index_of_result_chars = []
        x = len(str1)
        y = len(str2)

        while x != 0 and y != 0:
            if lenghts[x][y] == lenghts[x - 1][y]:
                x -= 1
            elif lenghts[x][y] == lenghts[x][y - 1]:
                y -= 1
            else:
                # assert??
                index_of_result_chars.append(x - 1)
                # str_result.join(str1[x - 1])
                x -= 1
                y -= 1
        # We have stored the positions of the target chars in str1. The next sentence bulds efficiently an
        # string joining all those chars. The index had been stored backwards, so we must take them backwards
        # to build the correct final string
        str_result = ''.join(str1[index_of_result_chars[i]] for i in range(len(index_of_result_chars) - 1, -1, -1))
        print (float(len(str_result)) / min(len(str1), len(str2)))
        return str_result

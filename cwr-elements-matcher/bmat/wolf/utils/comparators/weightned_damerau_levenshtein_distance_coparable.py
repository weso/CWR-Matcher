__author__ = 'Dani'

_OP_COST = 2
_SWAP_COST = 1
_MULTIPLIER = 2


class WeightnedDamerauLevenshteinDistanceComparable(object):
    @staticmethod
    def compare(str1, str2):
        if str1 is None or str2 is None or not (type("") == type(str1) == type(str2)):
            raise ValueError("Params should be strings")

        if len(str1) == 0 or len(str2) == 0:  # if empty word
            return 0  # Max distance

        str1_upper = str1.upper()
        str2_upper = str2.upper()

        previous2_cost_array = []
        previous_cost_array = []
        cost_array = []
        aux_array = []

        char1 = None
        char2 = None

        left_multiplier = 1
        was_left_space = True
        top_multiplier = 1
        was_top_space = True

        for i in range(0, len(str1) + 1):
            # Initializing r1 array, but only the first pos matters.
            # the rest of arrays are only manipulated to let them have
            # len(str1) +1  positions and access randomly to them later.
            cost_array.append(0)
            previous_cost_array.append(i * _OP_COST)
            previous2_cost_array.append(0)

        for j in range(1, len(str2) + 1):
            char2 = str2_upper[j - 1]
            cost_array[0] = j * _OP_COST

            top_multiplier = _MULTIPLIER if was_top_space else 1
            was_top_space = char2 == ' '

            for i in range(1, len(str1) + 1):
                char1 = str1_upper[i - 1]
                left_multiplier = _MULTIPLIER if was_left_space else 1
                was_left_space = char1 == ' '

                cost = 0 if char1 == char2 else _OP_COST

                # minimum of cell to the left+1, to the top+1, diagonally left
                # and up +cost
                cost_array[i] = min(cost_array[i - 1] + _OP_COST * left_multiplier,
                                    previous_cost_array[i] + _OP_COST * top_multiplier,
                                    previous_cost_array[i - 1] + cost * max(left_multiplier, top_multiplier))

                if i > 1 and j > 1 \
                        and str1_upper[i - 1] == str2_upper[j - 2] \
                        and str1_upper[i - 2] == str2_upper[j - 1]:
                    cost_array[i] = min(cost_array[i],
                                        previous2_cost_array[i - 2] + _SWAP_COST)
            #  copy current distance counts to 'previous row' distance counts
            aux_array = previous_cost_array
            previous_cost_array = cost_array
            cost_array = previous2_cost_array
            previous2_cost_array = aux_array

        # our last action in the above loop was to switch r0 and r1, so r1 now
        # actually has the most recent cost counts
        return 1.0 - (float(previous_cost_array[len(str1)]) / (_OP_COST * max(len(str1), len(str2))))












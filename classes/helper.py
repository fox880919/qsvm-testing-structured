

class Helper:

    def stringFromArray(self, array):

        # Choose a separator, for example, a comma and a space
        separator = ", "

        # Join them into a single string
        result_string = separator.join(str(f) for f in array)

        # print(result_string)

        return result_string
        # Output: '1.23, 4.5, 67.89, 100.0'
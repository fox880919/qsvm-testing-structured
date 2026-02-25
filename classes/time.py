
from datetime import datetime


class MyTimeHelper:

    def getTimeNow(self):

        # date = datetime.now().strftime('%Y-%m-%d')

        # time = datetime.now().strftime('%H:%M:%S')

        dateAndTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # print('dateAndTime: ', dateAndTime)

        return dateAndTime
    
    def getTimeDifferenceInSeconds(time2, time1):

        timeDifference = time2 - time1

        timeDifferenceInSeconds = int(timeDifference.total_seconds())
        print(f'timeDifferenceInSeconds:{timeDifferenceInSeconds}')




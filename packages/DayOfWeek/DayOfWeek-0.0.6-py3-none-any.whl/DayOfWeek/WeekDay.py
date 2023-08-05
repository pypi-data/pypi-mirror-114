
def Day(FullDate):
    '''
    Returns the day of the week for a date entered,using Zeller's Formula, if it falls between
    01/01/0001 and 31/12/9999 (yeah, thousands of years ).
    This is capable of Error handling.
    You may modify the source given below to your liking, (and may even publish it online, provided
    you abide by the MIT license.)
    '''
    import sys
    DatePart = str(FullDate).split('/')
    Year = int(int(DatePart[2])%100)
    Century = int(int(DatePart[2])//100)
    Month = int(DatePart[1])
    Date = int(DatePart[0])

    '''
    NOTE:

    sys.exit() is known to cause issues with Jupyter kernels. You must modify the sys.exit() lines to overcome these issues.
    Since they involve connecting to kernels(local/external) these kernels might get terminated :(
    You MIGHT see this, provided the date you entered is invalid :

    "An exception has occured, use %tb to see the full traceback."

    '''

    if Date > 31: # Date cannot be greater than 31
        sys.stderr.write("\t \n DateGreater31Error: Date cannot exceed 31 \n ")
        sys.exit()

    elif Date < 0: # negative dates not allowed
        sys.stderr.write('\t \n DateNegativeError: Date cannot be Negative \n')
        sys.exit()

    if Month > 12: # Month numbers don't exceed 12
        sys.stderr.write("\t \n MonthGreater12Error: Month cannot exceed 12 \n ")
        sys.exit()
    elif Month < 0: # Months are numbered from 1 to 12
        sys.stderr.write('\t \n MonthNegativeError: Month cannot be Negative \n')
        sys.exit()
    #Zeller's formula requires these conversions.
    if Month == 1:
        Year -= 1
        Month = 13
    elif Month == 2:
        Year -= 1
        Month = 14
    # errors relating to February's last dates
    if (Month == 2 or Month == 14) and Date >= 30:
        sys.stderr.write('\n February28&29Error: February\'s days are only till 28 (or 29 on leap years) \n')
        sys.exit()
    if (Month == 2 or Month == 14) and Date >= 29 and (Year+1) % 4 != 0:
        sys.stderr.write("\n FebruaryLeapDateError: 29 does not exist for non-leap years \n")
        sys.exit()
    # we know the rhyme - 30 Days of September ... ;)
    condition = Month == 9 or Month == 6 or Month == 4 or Month == 11
    if bool(condition) == 1 and Date > 30:
        sys.stderr.write("\n NoDate31Error: April, June, September and November have only 30 Days \n")
        sys.exit()
    Result = Date + ((13*(Month + 1))//5) + Year + (Year//4) + (Century//4) - 2*Century
    Weekday = Result % 7
    if Weekday == 1:
        print(FullDate,"-> Sunday \n")
        sys.exit()
    elif Weekday == 2:
        print(FullDate,"-> Monday \n")
        sys.exit()
    elif Weekday == 3:
        print(FullDate,"-> Tuesday \n")
        sys.exit()
    elif Weekday == 4:
        print(FullDate,"-> Wednesday \n")
        sys.exit()
    elif Weekday == 5:
        print(FullDate,"-> Thursday \n")
        sys.exit()
    elif Weekday == 6:
        print(FullDate,"-> Friday \n")
        sys.exit()
    # 7 cannot be returned from % operator on 7
    elif Weekday == 0:
        print(FullDate,"-> Saturday \n")
        sys.exit()

D = str(input('Enter Date: '))
Day(D)

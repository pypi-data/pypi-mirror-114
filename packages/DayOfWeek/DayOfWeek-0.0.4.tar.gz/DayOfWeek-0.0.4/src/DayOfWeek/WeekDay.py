
def Day(FullDate):
    import sys
    DatePart = str(FullDate).split('/')
    Year = int(int(DatePart[2])%100)
    Century = int(int(DatePart[2])//100)
    Month = int(DatePart[1])
    Date = int(DatePart[0])
    #FormattedDate = "/".join([str(Date), str(Month),str(str(Century)+str(Year))])
    if Date > 31:
        sys.stderr.write("\t \n DateGreater31Error: Date cannot exceed 31 \n ")
        sys.exit()

    elif Date < 0:
        sys.stderr.write('\t \n DateNegativeError: Date cannot be Negative \n')
        sys.exit()

    if Month > 12:
        sys.stderr.write("\t \n MonthGreater12Error: Month cannot exceed 12 \n ")
        sys.exit()
    elif Month < 0:
        sys.stderr.write('\t \n MonthNegativeError: Month cannot be Negative \n')
        sys.exit()
    if Month == 1:
        Year -= 1
        Month = 13
    elif Month == 2:
        Year -= 1
        Month = 14
    if (Month == 2 or Month == 14) and Date >= 30:
        sys.stderr.write('\n February28&29Error: February\'s days are only till 28 (or 29 on leap years) \n')
        sys.exit()
    if (Month == 2 or Month == 14) and Date >= 29 and (Year+1) % 4 != 0:
        sys.stderr.write("\n FebruaryLeapDateError: 29 does not exist for non-leap years \n")
        sys.exit()

    condition = Month == 9 or Month == 6 or Month == 4 or Month == 13
    if bool(condition) == 1 and Date > 30:
        sys.stderr.write("\n NoDate31Error: April, June, September and November have only 30 Days \n")
        sys.exit()
    Result = Date + ((13*(Month + 1))//5) + Year + (Year//4) + (Century//4) - 2*Century
    Weekday = Result % 7
    if Weekday == 1:
        print(FullDate,"-> Sunday \n")
    elif Weekday == 2:
        print(FullDate,"-> Monday \n")
    elif Weekday == 3:
        print(FullDate,"-> Tuesday \n")
    elif Weekday == 4:
        print(FullDate,"-> Wednesday \n")
    elif Weekday == 5:
        print(FullDate,"-> Thursday \n")
    elif Weekday == 6:
        print(FullDate,"-> Friday \n")
    elif Weekday == 0:
        print(FullDate,"-> Saturday \n")

D = str(input('Enter Date: '))
Day(D)

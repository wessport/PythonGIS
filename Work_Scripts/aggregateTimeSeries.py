# WES PORTER
# 7/5/2017
# RUSLE2 PROJECT - aggregateTimeSeries.py

# SCRIPT SUMMARY: Aggregate timeSeries.py results into annual, quarterly,
#                 monthly, weekly csv files.

# Define workspace
ws = "E:/Wes/Work/Rusle2/AnnAGNPS-RUSLE2_Runs/erosionSummary/outlet_July_5_2017"

header = "CELL,SCENARIO,DATE,AVERAGE,MAX,MIN,SUM" + '\n'

out_file_an = open((ws + "/aggregated_results_annual.csv"),'w')
out_file_an.write(header)
out_file_mo = open((ws + "/aggregated_results_monthly.csv"),'w')
out_file_mo.write(header)
out_file_q = open((ws + "/aggregated_results_quarterly.csv"),'w')
out_file_q.write(header)
out_file_w = open((ws + "/aggregated_results_weekly.csv"),'w')
out_file_w.write(header)

grouping = ['A','Q','M','W']
cells = ['83','312','522','552','1091']

for g in grouping: # Loop through time categories
    for c in cells: # Loop through each selected cell
        for i in range(1,7): # Loop through scenarios 1-6
            dates = []
            avg = []
            maximum = []
            minimum = []
            sum_total = []

            with open(ws + '/' + c +'_scn'+ str(i)+'_'+g+'_ave.csv','r') as in_file_ave:
                next(in_file_ave) # Skips header
                for j in in_file_ave:
                    strFromFile = j.strip()
                    parsedList = strFromFile.split(',')
                    dates.append(parsedList[0])
                    avg.append(parsedList[1])

            with open(ws + '/' + c +'_scn'+ str(i)+'_'+g+'_max.csv','r') as in_file_max:
                next(in_file_max)
                for k in in_file_max:
                    strFromFile = k.strip()
                    parsedList = strFromFile.split(',')
                    maximum.append(parsedList[1])

            with open(ws + '/' + c +'_scn'+ str(i)+'_'+g+'_min.csv','r') as in_file_min:
                next(in_file_min)
                for l in in_file_min:
                    strFromFile = l.strip()
                    parsedList = strFromFile.split(',')
                    minimum.append(parsedList[1])

            with open(ws + '/' + c +'_scn'+ str(i)+'_'+g+'_sum.csv','r') as in_file_sum:
                next(in_file_sum)
                for m in in_file_sum:
                    strFromFile = m.strip()
                    parsedList = strFromFile.split(',')
                    sum_total.append(parsedList[1])

            # Write results to csv files
            for n in range(0,len(dates)):
                if (g == 'A'):
                    out_file_an.write(c+','+str(i)+','+dates[n]+','+avg[n]+','+
                                      maximum[n]+','+minimum[n]+','+
                                      sum_total[n]+'\n')
                if (g == 'Q'):
                    out_file_q.write(c+','+str(i)+','+dates[n]+','+avg[n]+','+
                                     maximum[n]+','+minimum[n]+','+
                                     sum_total[n]+'\n')
                if (g == 'M'):
                    out_file_mo.write(c+','+str(i)+','+dates[n]+','+avg[n]+','+
                                      maximum[n]+','+minimum[n]+','+
                                      sum_total[n]+'\n')
                if (g == 'W'):
                    out_file_w.write(c+','+str(i)+','+dates[n]+','+avg[n]+','+
                                     maximum[n]+','+minimum[n]+','+
                                     sum_total[n]+'\n')

            in_file_ave.close()
            in_file_max.close()
            in_file_min.close()
            in_file_sum.close()

out_file_an.close()
out_file_q.close()
out_file_mo.close()
out_file_w.close()

print('\n~FINI~')

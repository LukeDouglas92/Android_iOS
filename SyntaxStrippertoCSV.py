import csv
import io

lang = "arabic"
txt_file = r"desktop/ios/"+lang+".strings"
csv_file = r"desktop/ios/"+lang+".csv"

in_txt = csv.reader(open(txt_file, "rb"), delimiter = '=')
out_csv = csv.writer(open(csv_file, 'wb'))

out_csv.writerows(in_txt)
print 'done! go check your'+lang+'.csv file'

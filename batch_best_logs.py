import glob
import sys
import os


de =[]
de.extend( glob.glob('*.mol2.tmp'))
de.extend( glob.glob('CONFIG*'))
bad_files_3 = glob.glob('*'+'_BAD')
de.extend(bad_files_3)
bad_files_4 = glob.glob('ga_inp*')
de.extend(bad_files_4)
bad_files_5 = glob.glob('*.log')
de.extend(bad_files_5)

bad_files_6 = glob.glob('*.ic')
de.extend(bad_files_6)
bad_files_7 = glob.glob('*.smi')
de.extend(bad_files_7)
de.extend(glob.glob('core.*'))

for i in de:
  os.remove(i)

bad_files_8 = glob.glob('*.inp')
for i in bad_files_8:
  os.remove(i)

files_list = glob.glob('logfile_'+'*')

num_b = int(sys.argv[1])
file_name = 'batch_log.csv'

if int(num_b) == 1:
    with open(file_name, "w") as f:
        for i in range(len(files_list)):
            with open( files_list[i] , "r") as g:
                tmp= float("inf")
                for line in g:
                    r=line.split()
                    if (float(r[2]) < tmp):
                        tmp= float(r[2])
                        best_line= line
            t = best_line.split()
            f.write(str(t[0])+'\t'+str(t[2])+'\t'+str(t[4])+'\t'+str(t[6])+'\n')
            os.remove(files_list[i])

else:
    with open(file_name, "a+") as f:
        for i in range(len(files_list)):
            with open( files_list[i] , "r") as g:
                tmp= float("inf")
                for line in g:
                    r=line.split()
                    if (float(r[2]) < tmp):
                        tmp= float(r[2])
                        best_line= line
            t = best_line.split()
            f.write(str(t[0])+'\t'+str(t[2])+'\t'+str(t[4])+'\t'+str(t[6])+'\n')
            os.remove(files_list[i])

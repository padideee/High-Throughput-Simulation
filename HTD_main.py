import argparse
import glob
import shutil
import subprocess
import pandas as pd
import numpy as np
import math
import sys
import os


def smile_generate(b, s):
    cmd = ["perl", "smile_gen.pl",'-b', str(b), '-s', str(s)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    p.wait()


def FlexAID(protein, cleft, ligs, population, generation, run):
    cmd = ["python", "beluga_parallel_run.py", protein, cleft, ligs,
            str(run), str(population), str(generation)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    p.wait()


def batch_analyse(batch, cut_off):
    cmd = ["python", "batch_best_logs.py", str(batch)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    p.wait()

    de=[]

    if cut_off != 1:
        de = glob.glob('*.pdb')

    for i in de:
        os.remove(i)


def epoche_analyse(iteration, cut_off):
    file_name = 'batch_log.csv'
    new_file_name = 'epoche_log_'+str(iteration)+'.csv'
    shutil.copyfile(file_name, new_file_name)

    col_names = ['ID','CF','TIME','smile']
    df = pd.read_csv(file_name, sep='\t', names=col_names)

    df.CF = df.CF.astype(float)
    df = df.sort_values(by=['CF'], ignore_index=True)
    l = math.ceil(len(df) * cut_off)
    df_new = df.iloc[:l, :]

    de=[]
    if cut_off != 1:
        de.extend( glob.glob('*.pdb'))

    for i in de:
        os.remove(i)

    log_name = 'top_CF_' + str(iteration) + '.txt'
    np.savetxt(log_name, df_new.values, fmt='%s')

    df_new.ID = df_new.ID.str[:-2]
    df_new.ID = df_new.ID.astype(str) + '\t' +  df_new.smile.astype(str)
    np.savetxt(r'lig_list_new.txt', df_new.ID.values, fmt='%s')
    return len(df_new)


def main():
    parser = argparse.ArgumentParser(description="the arguments.", add_help=False)
    parser.add_argument("-p", "--protein", action="store")
    parser.add_argument("-c", "--cleft", action="store")
    parser.add_argument("-l", "--ligands_file", action="store")
    args = parser.parse_args()

    protein = args.protein
    cleft = args.cleft
    ligs = args.ligands_file

    shutil.copyfile(ligs, 'lig_list_new.txt')

    num_ligs = sum(1 for line in open(ligs))
    print(num_ligs)
    cut_off = []
    populations = []
    generations = []
    runs = []

    try:

        if 10000 < num_ligs <= 600000:
            cut_off = [.01, 1]
            populations = [100, 250]
            generations = [100, 250]
            runs = [1, 1]

        elif 1000 < num_ligs <= 10000:
            cut_off = [.01, 1]
            populations = [250, 1000]
            generations = [250, 1000]
            runs = [1, 1]

        elif num_ligs <= 1000:
            cut_off = [.3, .3, 1]
            populations = [100, 500, 1000]
            generations = [100, 500, 1000]
            runs = [1, 1, 5]


    except:

        print(" The size of Ligand Library is not acceptable. Max size = 600'000 ")
        sys.exit(1)

    for i in range(len(cut_off)):
        batch_size = 1000
        for j in range(0, num_ligs, batch_size):
            smile_generate(j, batch_size)
            FlexAID(protein, cleft, 'lig_list_new.txt', populations[i], generations[i], runs[i])
            batch_analyse(j+1, cut_off[i])
        num_ligs = epoche_analyse(i+1, cut_off[i])


if __name__ == '__main__':

    main()

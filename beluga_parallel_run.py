from multiprocessing import Pool
import subprocess
import shlex
import sys


def execute(command_string, working_directory=None, capture_output=True):
    assert isinstance(command_string, str)
    commands_list = shlex.split(command_string)
    if capture_output:
        return subprocess.run(commands_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory)
    else:
        return subprocess.run(commands_list, cwd=working_directory)


def prepare_cmd(n_processors=40):
    cmds = []

    protein = sys.argv[1]
    cleft = sys.argv[2]
    ligs = sys.argv[3]
    run = sys.argv[4]
    population = sys.argv[5]
    generation = sys.argv[6]

    with open(ligs, 'r') as f:
        for line in f:
            l = line.rstrip()
            l_list = l.split('\t')
            print(l_list)
            cmds.append("perl utility.pl -t {} -l {} -s {} -c {} -b {} -p {} -g {}"
                        .format(protein, str(l_list[0])+'.inp', l_list[1], cleft, run, population, generation))

    p = Pool(n_processors)
    results = p.map(execute, cmds)

    results = [x.stdout.decode('utf-8').strip() for x in results]
    return results


if __name__ == "__main__":

    prepare_cmd()

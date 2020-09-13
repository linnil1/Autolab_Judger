import json
import subprocess
import sys
import time
import signal
import os


scores = {"scores": {}}
file_input = "grade.json"
file_output = "/home/output/feedback"
timeout_limit = 5
DEBUG = True


def run_command(arg):
    return subprocess.Popen(arg,
                            cwd=os.getcwd(),
                            start_new_session=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)


def get_command_status(p, timeout=2.0):
    """
    Get the process status.

    It will be kill if it run excess timeout threshold

    Parameters
    ----------
    p: subprocess
    timeout: float

    Returns
    -------
    outs: encode str
    errs: encode str
    returncode: int
    Timeout: bool
    """
    try:
        # Run command
        outs, errs = p.communicate(timeout=timeout)
        print("OK")
        return outs, errs, p.returncode, False

    except subprocess.TimeoutExpired:
        # Kill it
        print("kill")
        p.terminate()
        p.kill()

        # Fully Kill
        # https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        try:
            outs, errs = p.communicate(timeout=.1)
        except subprocess.TimeoutExpired:
            print("kill all")
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            os.killpg(os.getpgid(p.pid), signal.SIGKILL)

        return "", "", p.returncode, True


def run_py(casename):
    # return run_command(["python3", "py_grade.py", casename])
    return run_command(["su", "autolab", "-c", f"python3 py_grade.py {casename}"])

def run_java(casename):
    return run_command(["su", "autolab", "-c", f"java -cp gson.jar:algs4.jar:. java_grade {casename}"])

def com_java():
    return run_command(["javac", "-cp", "algs4.jar:gson.jar", "java_grade.java", "Solution.java"])


if __name__ == '__main__':
    open(file_output, 'w').close()
    f = open(file_output, 'a')
    cases = json.load(open("data.json"))
    run_type = sys.argv[1]

    # compile java source
    if run_type == "java":
        p = com_java()
        outs, errs, returncode, timeout = get_command_status(p)
        if DEBUG:
            print("DEBUG", outs, errs)
        if timeout:
            f.write("Compile timeout\n")
            sys.exit(0)
        if returncode != 0:
            f.write("Compile Error:\n")
            f.write(errs.decode('ascii'))
            sys.exit(0)

    # run each score
    for case in cases:
        casename = f"case{case['case']}"
        scores["scores"][casename] = 0
        json.dump(case['data'], open(casename + ".in", "w"))
        os.chmod(casename + ".in", 0o707)
        open(casename + ".out", "w").close()
        os.chmod(casename + ".out", 0o707)

        if run_type == "python":
            p = run_py(casename)
        else:
            p = run_java(casename)

        outs, errs, returncode, timeout = get_command_status(p, timeout=timeout_limit)
        if DEBUG:
            print("DEBUG", outs, errs)
            f.write(outs.decode())
            f.write(errs.decode())

        # TLE
        if timeout:
            f.write(casename + ":\tTLE\n")
            continue

        # RE
        if returncode != 0:
            f.write(casename + ":\tRE\t Return Code != 0\n")
            continue

        # RE for json format error
        try: 
            output = json.load(open(casename + ".out"))
            os.remove(casename + ".in")
            os.remove(casename + ".out")
            if len(output['status']) != len(output['time']):
                raise ValueError("RE")
        except Exception as e:
            f.write(casename + ":\tRE\tYour program has runtime problem or Judger crash.\n")
            continue

        # calculate score
        isAC = all(i == "AC" for i in output["status"])
        if isAC:
            scores["scores"][casename] = case["score"]

        # show status
        f.write(casename + ":\n")
        for j in range(len(output["status"])):
            f.write(f"\tSample{j}:\t{output['status'][j]}\t{output['time'][j]:.1f} ms\n")

    # Write overall status
    f.write(json.dumps(scores))

import subprocess


def status():
    cmd = 'git status'
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    result_code = process.returncode
    if result_code != 0:
        print("查看工作区状态错误")
    else:
        print("")


if __name__ == '__main__':
    status()

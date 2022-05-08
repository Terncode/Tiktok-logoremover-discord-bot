import subprocess

def split_name(name):
    splitter = "."
    split = name.split(splitter) 
    ex = split.pop()
    actual_name = splitter.join(split)
    return (actual_name, ex, name)


def run_command(command):
    print(command)
    output=subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    if output.returncode != 0:
        raise RuntimeError(
            output.stderr.decode("utf-8"))

    return output

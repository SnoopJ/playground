"""
This example shows off invoking a command with the subprocess module and
processing the output one line at a time

Inspired by a question in #python on Libera.chat on 22 Feb 2023
"""
import subprocess


bash_src = """
for n in {1..5}; do
    echo $n
    sleep 0.3
done;
"""
cmd = ["bash", "-c", bash_src]


def handle_line(line):
    print(f"processing {line = }")


if __name__ == "__main__":
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

    for line in proc.stdout:
        # NOTE:this is a blocking call, but could be done concurrently where desirable
        handle_line(line)

    print(f"All done, process existed with code {proc.returncode}")

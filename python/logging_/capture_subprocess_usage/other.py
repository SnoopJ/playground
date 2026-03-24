from __future__ import annotations
import subprocess


def _run_second_computation() -> str:
    result = subprocess.Popen(["echo", "42"], text=True, stdout=subprocess.PIPE)
    return result.stdout.read()


def do_something() -> tuple[str, str]:
    result = subprocess.check_output(["echo", "Wow, amazing computation!"], env={"ACME_DATA": "Be careful, the environment might have secrets in it!"})
    result2 = _run_second_computation()
    return (result, result2)

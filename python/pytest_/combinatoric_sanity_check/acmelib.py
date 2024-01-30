import itertools
import random
from enum import Enum


class EFirstParam(str, Enum):
    A = "A"
    B = "B"
    C = "C"


class ESecondParam(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class OutputFormat(str, Enum):
    A = "A"
    B = "B"
    C = "C"


ALL_COMBINATIONS = list(itertools.product(
    list(EFirstParam),
    list(ESecondParam),
    list(OutputFormat),
))
INVALID_COMBINATIONS = {
    (EFirstParam.A, ESecondParam.A, OutputFormat.A),
    (EFirstParam.C, ESecondParam.C, OutputFormat.C),
    (EFirstParam.C, ESecondParam.B, OutputFormat.B),
}
VALID_COMBINATIONS = set(ALL_COMBINATIONS) - INVALID_COMBINATIONS


def run_job(
    param1: EFirstParam,
    param2: ESecondParam,
    output_format: OutputFormat
):
    comb = (param1, param2, output_format)
    if comb in INVALID_COMBINATIONS:
        combtxt = f"{param1.value}{param2.value}->{output_format.value}"
        raise RuntimeError(f"Combination {combtxt} is INVALID")

    return True


if __name__ == "__main__":
    for comb in itertools.chain(VALID_COMBINATIONS, INVALID_COMBINATIONS):
        try:
            run_job(*comb)
            (param1, param2, output_format) = comb
            combtxt = f"{param1.value}{param2.value}->{output_format.value}"
            print(f"Combination {combtxt} is VALID")
        except RuntimeError as exc:
            print(exc)

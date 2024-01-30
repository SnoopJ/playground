import pytest

from acmelib import EFirstParam, ESecondParam, OutputFormat, run_job


ACMELIB_OUTFMT_MAP = {outfmt: False for outfmt in OutputFormat}


_original_run_job = run_job

def _run_job_dummy(p1, p2, outfmt):
    ACMELIB_OUTFMT_MAP[outfmt] = True
    return _original_run_job(p1, p2, outfmt)

run_job = _run_job_dummy


@pytest.mark.parametrize("comb", [
    (EFirstParam.A, ESecondParam.A, OutputFormat.A), # invalid, causes test failure
    (EFirstParam.A, ESecondParam.B, OutputFormat.B), # valid
    (EFirstParam.B, ESecondParam.B, OutputFormat.A), # valid
    # oops, we forgot to add a test scenario that covers the newly introduced OutputFormat.C
])
def test_run_job(comb):
    assert run_job(*comb)


@pytest.mark.order("last")  # pytest-order
def test_saw_all_outputformat():
    missing_output_formats = [name for name, val in ACMELIB_OUTFMT_MAP.items() if not val]
    assert not missing_output_formats, f"Missing some output formats: {missing_output_formats}"

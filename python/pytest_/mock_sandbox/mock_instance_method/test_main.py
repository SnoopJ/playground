from datetime import datetime
from unittest.mock import patch

import main


class FakeClass(main.RealClass):
    def __init__(self, *args, **kwargs):
        self.reftime = datetime.now()
        super().__init__(*args, **kwargs)

    def func(self, *args, **kwargs):
        elapsed_time = datetime.now() - self.reftime
        print(f"Inside fake method (elapsed time: {elapsed_time}):\n\t{self = },\n\t{self.data = }")


def test_main():
    main.main()


def test_main_fake():
    with patch("main.RealClass", FakeClass):
        main.main()

I wrote this sample to demonstrate the for-free combinatorics of [`pytest.mark.parametrize()`](https://docs.pytest.org/en/7.2.x/how-to/parametrize.html#pytest-mark-parametrize)
If you define multiple parameters in separate marks, you get all the
combinations between the separate sets of parameters.

To my delight, I also discovered the somewhat obscure option
`disable_test_id_escaping_and_forfeit_all_rights_to_community_support` to
disable the escaping of test IDs (which contain parameter values) when the
parameters include Unicode text.


### Default behavior

```
$ python3 -m pytest -s -v test_bark.py
============================= test session starts ==============================
platform linux -- Python 3.9.9, pytest-7.1.2, pluggy-1.0.0 -- /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/.direnv/python-3.9.9/bin/python3
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/combinatoric_parameters
collecting ... collected 4 items

test_bark.py::test_oration[meow-\u732b] Behold, the wisdom of 猫: 'meow'    PASSED
test_bark.py::test_oration[meow-\U0001f63a] Behold, the wisdom of 😺: 'meow'    PASSED
test_bark.py::test_oration[\u306b\u3083\u3042\u3042\u3042\u3042\u301c-\u732b] Behold, the wisdom of 猫: 'にゃああああ〜'    PASSED
test_bark.py::test_oration[\u306b\u3083\u3042\u3042\u3042\u3042\u301c-\U0001f63a] Behold, the wisdom of 😺: 'にゃああああ〜'    PASSED

============================== 4 passed in 0.01s ===============================
```

### With `disable_test_id_escaping_and_forfeit_all_rights_to_community_support` enabled

```
$ python3 -m pytest -s -v -o disable_test_id_escaping_and_forfeit_all_rights_to_community_support=true test_bark.py
============================= test session starts ==============================
platform linux -- Python 3.9.9, pytest-7.1.2, pluggy-1.0.0 -- /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/.direnv/python-3.9.9/bin/python3
cachedir: .pytest_cache
rootdir: /var/lib/gitea/data/gitea-repositories/snoopj/playground.git/python/pytest_/combinatoric_parameters
collecting ... collected 4 items

test_bark.py::test_oration[meow-猫] Behold, the wisdom of 猫: 'meow'    PASSED
test_bark.py::test_oration[meow-😺] Behold, the wisdom of 😺: 'meow'    PASSED
test_bark.py::test_oration[にゃああああ〜-猫] Behold, the wisdom of 猫: 'にゃああああ〜'    PASSED
test_bark.py::test_oration[にゃああああ〜-😺] Behold, the wisdom of 😺: 'にゃああああ〜'    PASSED

============================== 4 passed in 0.01s ===============================
```

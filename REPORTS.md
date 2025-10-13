# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------
core/backgammongame.py     244     43     60      5    76%   50-80, 84, 88, 210, 212, 308-313, 407-408, 441
core/board.py              150      2     56      7    96%   98->100, 119->121, 153->152, 164->167, 165->164, 200, 244
core/checker.py            120      1     38      1    99%   195
core/dice.py                25      4      2      0    85%   42, 51, 60, 69
core/player.py              86      3     18      3    94%   40, 50, 140
--------------------------------------------------------------------
TOTAL                      625     53    174     16    88%

1 file skipped due to complete coverage.

```
## Pylint Report
```text
************* Module core.checker
core/checker.py:128:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core/checker.py:141:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core/checker.py:8:0: R0904: Too many public methods (25/20) (too-many-public-methods)
************* Module core.backgammongame
core/backgammongame.py:450:0: C0304: Final newline missing (missing-final-newline)
core/backgammongame.py:12:0: R0902: Too many instance attributes (20/7) (too-many-instance-attributes)
core/backgammongame.py:183:28: W0613: Unused argument 'from_point' (unused-argument)
core/backgammongame.py:183:45: W0613: Unused argument 'to_point' (unused-argument)
core/backgammongame.py:196:24: W0613: Unused argument 'from_point' (unused-argument)
core/backgammongame.py:196:41: W0613: Unused argument 'to_point' (unused-argument)
core/backgammongame.py:216:30: W0613: Unused argument 'player' (unused-argument)
core/backgammongame.py:228:34: W0613: Unused argument 'player' (unused-argument)
core/backgammongame.py:240:27: W0613: Unused argument 'player' (unused-argument)
core/backgammongame.py:362:31: W0613: Unused argument 'player' (unused-argument)
core/backgammongame.py:12:0: R0904: Too many public methods (55/20) (too-many-public-methods)
************* Module core.board
core/board.py:224:36: W0613: Unused argument 'player' (unused-argument)
core/board.py:11:0: R0904: Too many public methods (33/20) (too-many-public-methods)
************* Module core.player
core/player.py:9:0: R0902: Too many instance attributes (8/7) (too-many-instance-attributes)
core/player.py:9:0: R0904: Too many public methods (23/20) (too-many-public-methods)
************* Module tests.test_cli
tests/test_cli.py:300:45: W0613: Unused argument 'mock_stdout' (unused-argument)
tests/test_cli.py:307:45: W0613: Unused argument 'mock_stdout' (unused-argument)
tests/test_cli.py:349:43: W0613: Unused argument 'mock_stdout' (unused-argument)
tests/test_cli.py:355:39: W0613: Unused argument 'mock_stdout' (unused-argument)
************* Module tests.test_checker
tests/test_checker.py:7:0: R0904: Too many public methods (73/20) (too-many-public-methods)
************* Module tests.test_player
tests/test_player.py:6:0: R0904: Too many public methods (45/20) (too-many-public-methods)
************* Module tests.test_backgammongame
tests/test_backgammongame.py:138:0: C0301: Line too long (114/100) (line-too-long)
tests/test_backgammongame.py:422:0: C0304: Final newline missing (missing-final-newline)
tests/test_backgammongame.py:11:0: R0904: Too many public methods (79/20) (too-many-public-methods)
************* Module tests.test_board
tests/test_board.py:8:0: R0904: Too many public methods (67/20) (too-many-public-methods)

-----------------------------------
Your code has been rated at 9.86/10


```

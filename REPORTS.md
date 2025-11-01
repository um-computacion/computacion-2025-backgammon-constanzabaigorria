# Automated Reports
## Coverage Report
```text
Name                     Stmts   Miss Branch BrPart  Cover   Missing
--------------------------------------------------------------------
core/backgammongame.py     469    181    220     25    55%   85, 89, 170, 187, 196-199, 220, 229-236, 251, 256, 266, 275-289, 292-306, 313, 317, 324->329, 326->329, 346, 349, 352, 374, 377, 381-515, 527-617, 711->710, 713->710, 717, 811-812, 845
core/board.py              152      3     56      7    95%   110, 131->133, 172->171, 183->186, 184->183, 223, 267
core/checker.py            120      1     38      1    99%   195
core/dice.py                25      4      2      0    85%   42, 51, 60, 69
core/player.py              86      3     18      3    94%   40, 50, 140
--------------------------------------------------------------------
TOTAL                      852    192    334     36    72%

1 file skipped due to complete coverage.

```
## Pylint Report
```text
************* Module core.checker
core/checker.py:128:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core/checker.py:141:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
core/checker.py:8:0: R0904: Too many public methods (25/20) (too-many-public-methods)
************* Module core.backgammongame
core/backgammongame.py:188:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:191:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:200:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:204:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:211:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:221:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:226:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:237:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:248:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:252:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:257:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:260:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:267:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:272:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:285:93: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:286:0: C0301: Line too long (109/100) (line-too-long)
core/backgammongame.py:302:93: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:303:0: C0301: Line too long (109/100) (line-too-long)
core/backgammongame.py:307:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:311:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:314:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:318:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:320:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:328:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:347:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:350:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:353:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:372:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:375:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:378:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:385:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:401:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:404:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:407:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:418:0: C0301: Line too long (106/100) (line-too-long)
core/backgammongame.py:419:0: C0301: Line too long (144/100) (line-too-long)
core/backgammongame.py:420:0: C0301: Line too long (144/100) (line-too-long)
core/backgammongame.py:421:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:428:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:436:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:449:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:467:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:484:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:487:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:509:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:513:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:529:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:532:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:537:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:541:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/backgammongame.py:545:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
core/backgammongame.py:547:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:549:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:557:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:560:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:567:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:575:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:579:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:587:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:590:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:600:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:605:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:611:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:615:0: C0303: Trailing whitespace (trailing-whitespace)
core/backgammongame.py:12:0: R0902: Too many instance attributes (20/7) (too-many-instance-attributes)
core/backgammongame.py:206:8: R1702: Too many nested blocks (6/5) (too-many-nested-blocks)
core/backgammongame.py:206:8: R1702: Too many nested blocks (7/5) (too-many-nested-blocks)
core/backgammongame.py:184:4: R0912: Too many branches (17/12) (too-many-branches)
core/backgammongame.py:206:8: R1702: Too many nested blocks (7/5) (too-many-nested-blocks)
core/backgammongame.py:240:4: R0914: Too many local variables (17/15) (too-many-locals)
core/backgammongame.py:273:8: R1705: Unnecessary "elif" after "return", remove the leading "el" from "elif" (no-else-return)
core/backgammongame.py:273:11: R1716: Simplify chained comparison between the operands (chained-comparison)
core/backgammongame.py:285:26: R1728: Consider using a generator instead 'max((i for i in home_points_white_idx if self.__board.points[i] and self.__board.points[i][0].get_owner() == self.__current_player), default=None)' (consider-using-generator)
core/backgammongame.py:290:13: R1716: Simplify chained comparison between the operands (chained-comparison)
core/backgammongame.py:302:26: R1728: Consider using a generator instead 'min((i for i in home_points_black_idx if self.__board.points[i] and self.__board.points[i][0].get_owner() == self.__current_player), default=None)' (consider-using-generator)
core/backgammongame.py:240:4: R0911: Too many return statements (14/6) (too-many-return-statements)
core/backgammongame.py:240:4: R0912: Too many branches (20/12) (too-many-branches)
core/backgammongame.py:356:4: R0914: Too many local variables (25/15) (too-many-locals)
core/backgammongame.py:393:11: R0916: Too many boolean expressions in if statement (8/5) (too-many-boolean-expressions)
core/backgammongame.py:393:12: R1716: Simplify chained comparison between the operands (chained-comparison)
core/backgammongame.py:394:12: R1716: Simplify chained comparison between the operands (chained-comparison)
core/backgammongame.py:419:26: R1728: Consider using a generator instead 'max((i for i in home_points_white_idx if board.points[i] and board.points[i][0].get_owner() == jugador), default=None)' (consider-using-generator)
core/backgammongame.py:420:26: R1728: Consider using a generator instead 'min((i for i in home_points_black_idx if board.points[i] and board.points[i][0].get_owner() == jugador), default=None)' (consider-using-generator)
core/backgammongame.py:356:4: R0911: Too many return statements (8/6) (too-many-return-statements)
core/backgammongame.py:356:4: R0912: Too many branches (37/12) (too-many-branches)
core/backgammongame.py:356:4: R0915: Too many statements (91/50) (too-many-statements)
core/backgammongame.py:517:4: R0911: Too many return statements (10/6) (too-many-return-statements)
core/backgammongame.py:517:4: R0912: Too many branches (21/12) (too-many-branches)
core/backgammongame.py:619:30: W0613: Unused argument 'player' (unused-argument)
core/backgammongame.py:766:31: W0613: Unused argument 'player' (unused-argument)
core/backgammongame.py:12:0: R0904: Too many public methods (56/20) (too-many-public-methods)
************* Module core.board
core/board.py:216:0: C0301: Line too long (101/100) (line-too-long)
core/board.py:19:8: C0104: Disallowed name "bar" (disallowed-name)
core/board.py:247:36: W0613: Unused argument 'player' (unused-argument)
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
tests/test_backgammongame.py:424:0: C0304: Final newline missing (missing-final-newline)
tests/test_backgammongame.py:11:0: R0904: Too many public methods (79/20) (too-many-public-methods)
************* Module tests.test_board
tests/test_board.py:212:0: C0301: Line too long (102/100) (line-too-long)
tests/test_board.py:213:0: C0301: Line too long (114/100) (line-too-long)
tests/test_board.py:231:0: C0301: Line too long (108/100) (line-too-long)
tests/test_board.py:8:0: R0904: Too many public methods (67/20) (too-many-public-methods)

-----------------------------------
Your code has been rated at 9.49/10


```

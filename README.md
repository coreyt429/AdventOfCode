# AdventOfCode

My Advent of Code solutions.

After past failed attempts, I took 2023 seriously as a project to transition from Perl to Python.

After completing 2023, I started back at 2015 and am  slowly making my way through.

Starting with the 2016 puzzles, I'm trying to get a clean pylint run from each solution to enforce coding practices. At some point I will review 2023 and 2015 to clean them up, as well as revisit those solutions to improve with new knowledge. Those were heavily borrowed from chatGPT and reddit solutions, and I can do better now.

Notes on chatGPT and these solutions:
  - gpt3.5 and gpt4 are not good at figuring out these puzzles
  - common gpt questions I did find useful:
    - How do I do this <paste Perl code> in python
	- How do I do X in python
	- Explain this <paste python code from solution I don't understand>

Notes on my solutions:
  - I'm attempting to make these solutions easy to read and understand, and will update documentation on previous solutions to meet this goal
  - This is a learning excercise for me, so I will vary coding style, and tools to push myself
  - Early solutions (2023 and 2015) were made with no real python training, and may not be pretty
  - I'm a VoIP Engineer who likes to code, not a computer scientist. I'm really good at functional code, and weaker on creative mathmatical solutions.
  

# 2025 code cleanup status

Timed-out runs (> 30s):
┏━━━━━━━━━━━━━━━━━━┓
┃ Module           ┃
┡━━━━━━━━━━━━━━━━━━┩
│ 2018.21.solution │
│ 2020.19.solution │
│ 2022.16.solution │
└──────────────────┘

Failed runs:
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Module           ┃ Exit code ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 2024.18.solution │ 1         │
│ 2024.19.solution │ 1         │
│ 2024.20.solution │ 1         │
│ 2024.21.solution │ 1         │
└──────────────────┴───────────┘

Missing solution.py files:
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Module           ┃ Path                ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 2022.20.solution │ 2022/20/solution.py │
│ 2022.21.solution │ 2022/21/solution.py │
│ 2022.22.solution │ 2022/22/solution.py │
│ 2022.23.solution │ 2022/23/solution.py │
│ 2022.24.solution │ 2022/24/solution.py │
│ 2022.25.solution │ 2022/25/solution.py │
│ 2023.6.solution  │ 2023/6/solution.py  │
│ 2023.7.solution  │ 2023/7/solution.py  │
│ 2023.8.solution  │ 2023/8/solution.py  │
│ 2023.9.solution  │ 2023/9/solution.py  │
│ 2023.10.solution │ 2023/10/solution.py │
│ 2023.11.solution │ 2023/11/solution.py │
│ 2023.12.solution │ 2023/12/solution.py │
│ 2023.13.solution │ 2023/13/solution.py │
│ 2023.14.solution │ 2023/14/solution.py │
│ 2023.15.solution │ 2023/15/solution.py │
│ 2023.16.solution │ 2023/16/solution.py │
│ 2023.17.solution │ 2023/17/solution.py │
│ 2023.18.solution │ 2023/18/solution.py │
│ 2023.19.solution │ 2023/19/solution.py │
│ 2023.20.solution │ 2023/20/solution.py │
│ 2023.21.solution │ 2023/21/solution.py │
│ 2023.22.solution │ 2023/22/solution.py │
│ 2023.23.solution │ 2023/23/solution.py │
│ 2023.24.solution │ 2023/24/solution.py │
│ 2023.25.solution │ 2023/25/solution.py │
│ 2024.22.solution │ 2024/22/solution.py │
│ 2024.23.solution │ 2024/23/solution.py │
│ 2024.24.solution │ 2024/24/solution.py │
│ 2024.25.solution │ 2024/25/solution.py │
└──────────────────┴─────────────────────┘

Pylint < 10:
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Module           ┃ Score ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
│ 2018.15.solution │ 9.92  │ - refactor
└──────────────────┴───────┘


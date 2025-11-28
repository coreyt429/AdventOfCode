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
│ 2015.22.solution │
│ 2016.11.solution │
│ 2017.17.solution │
│ 2017.22.solution │
│ 2018.6.solution  │
│ 2018.14.solution │
│ 2018.21.solution │
│ 2019.18.solution │
│ 2020.19.solution │
│ 2020.23.solution │
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
│ 2018.15.solution │ 9.92  │
└──────────────────┴───────┘

Solutions using legacy aoc.run() template:
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Module           ┃ Path                ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 2015.1.solution  │ 2015/1/solution.py  │
│ 2015.2.solution  │ 2015/2/solution.py  │
│ 2015.3.solution  │ 2015/3/solution.py  │
│ 2015.4.solution  │ 2015/4/solution.py  │
│ 2015.5.solution  │ 2015/5/solution.py  │
│ 2015.6.solution  │ 2015/6/solution.py  │
│ 2015.7.solution  │ 2015/7/solution.py  │
│ 2015.8.solution  │ 2015/8/solution.py  │
│ 2015.9.solution  │ 2015/9/solution.py  │
│ 2015.10.solution │ 2015/10/solution.py │
│ 2015.11.solution │ 2015/11/solution.py │
│ 2015.12.solution │ 2015/12/solution.py │
│ 2015.13.solution │ 2015/13/solution.py │
│ 2015.14.solution │ 2015/14/solution.py │
│ 2015.15.solution │ 2015/15/solution.py │
│ 2015.16.solution │ 2015/16/solution.py │
│ 2015.17.solution │ 2015/17/solution.py │
│ 2015.18.solution │ 2015/18/solution.py │
│ 2015.19.solution │ 2015/19/solution.py │
│ 2015.20.solution │ 2015/20/solution.py │
│ 2015.21.solution │ 2015/21/solution.py │
│ 2015.22.solution │ 2015/22/solution.py │
│ 2015.23.solution │ 2015/23/solution.py │
│ 2015.24.solution │ 2015/24/solution.py │
│ 2015.25.solution │ 2015/25/solution.py │
│ 2016.1.solution  │ 2016/1/solution.py  │
│ 2016.2.solution  │ 2016/2/solution.py  │
│ 2016.3.solution  │ 2016/3/solution.py  │
│ 2016.4.solution  │ 2016/4/solution.py  │
│ 2016.5.solution  │ 2016/5/solution.py  │
│ 2016.6.solution  │ 2016/6/solution.py  │
│ 2016.7.solution  │ 2016/7/solution.py  │
│ 2016.8.solution  │ 2016/8/solution.py  │
│ 2016.9.solution  │ 2016/9/solution.py  │
│ 2016.10.solution │ 2016/10/solution.py │
│ 2016.11.solution │ 2016/11/solution.py │
│ 2016.12.solution │ 2016/12/solution.py │
│ 2016.13.solution │ 2016/13/solution.py │
│ 2016.14.solution │ 2016/14/solution.py │
│ 2016.15.solution │ 2016/15/solution.py │
│ 2016.16.solution │ 2016/16/solution.py │
│ 2016.17.solution │ 2016/17/solution.py │
│ 2016.18.solution │ 2016/18/solution.py │
│ 2016.19.solution │ 2016/19/solution.py │
│ 2016.20.solution │ 2016/20/solution.py │
│ 2016.21.solution │ 2016/21/solution.py │
│ 2016.22.solution │ 2016/22/solution.py │
│ 2016.23.solution │ 2016/23/solution.py │
│ 2016.24.solution │ 2016/24/solution.py │
│ 2016.25.solution │ 2016/25/solution.py │
│ 2017.1.solution  │ 2017/1/solution.py  │
│ 2017.2.solution  │ 2017/2/solution.py  │
│ 2017.4.solution  │ 2017/4/solution.py  │
│ 2017.5.solution  │ 2017/5/solution.py  │
│ 2017.6.solution  │ 2017/6/solution.py  │
│ 2017.7.solution  │ 2017/7/solution.py  │
│ 2017.8.solution  │ 2017/8/solution.py  │
│ 2017.9.solution  │ 2017/9/solution.py  │
│ 2017.10.solution │ 2017/10/solution.py │
│ 2017.11.solution │ 2017/11/solution.py │
│ 2017.12.solution │ 2017/12/solution.py │
│ 2017.13.solution │ 2017/13/solution.py │
│ 2017.15.solution │ 2017/15/solution.py │
│ 2017.16.solution │ 2017/16/solution.py │
│ 2017.17.solution │ 2017/17/solution.py │
│ 2017.18.solution │ 2017/18/solution.py │
│ 2017.19.solution │ 2017/19/solution.py │
│ 2017.20.solution │ 2017/20/solution.py │
│ 2017.21.solution │ 2017/21/solution.py │
│ 2017.22.solution │ 2017/22/solution.py │
│ 2017.23.solution │ 2017/23/solution.py │
│ 2017.24.solution │ 2017/24/solution.py │
│ 2017.25.solution │ 2017/25/solution.py │
│ 2018.1.solution  │ 2018/1/solution.py  │
│ 2018.2.solution  │ 2018/2/solution.py  │
│ 2018.3.solution  │ 2018/3/solution.py  │
│ 2018.4.solution  │ 2018/4/solution.py  │
│ 2018.5.solution  │ 2018/5/solution.py  │
│ 2018.6.solution  │ 2018/6/solution.py  │
│ 2018.7.solution  │ 2018/7/solution.py  │
│ 2018.8.solution  │ 2018/8/solution.py  │
│ 2018.9.solution  │ 2018/9/solution.py  │
│ 2018.10.solution │ 2018/10/solution.py │
│ 2018.11.solution │ 2018/11/solution.py │
│ 2018.12.solution │ 2018/12/solution.py │
│ 2018.13.solution │ 2018/13/solution.py │
│ 2018.14.solution │ 2018/14/solution.py │
│ 2018.15.solution │ 2018/15/solution.py │
│ 2018.16.solution │ 2018/16/solution.py │
│ 2018.17.solution │ 2018/17/solution.py │
│ 2018.18.solution │ 2018/18/solution.py │
│ 2018.19.solution │ 2018/19/solution.py │
│ 2018.20.solution │ 2018/20/solution.py │
│ 2018.21.solution │ 2018/21/solution.py │
│ 2018.22.solution │ 2018/22/solution.py │
│ 2018.23.solution │ 2018/23/solution.py │
│ 2018.24.solution │ 2018/24/solution.py │
│ 2018.25.solution │ 2018/25/solution.py │
│ 2019.1.solution  │ 2019/1/solution.py  │
│ 2019.2.solution  │ 2019/2/solution.py  │
│ 2019.3.solution  │ 2019/3/solution.py  │
│ 2019.4.solution  │ 2019/4/solution.py  │
│ 2019.5.solution  │ 2019/5/solution.py  │
│ 2019.6.solution  │ 2019/6/solution.py  │
│ 2019.7.solution  │ 2019/7/solution.py  │
│ 2019.8.solution  │ 2019/8/solution.py  │
│ 2019.9.solution  │ 2019/9/solution.py  │
│ 2019.10.solution │ 2019/10/solution.py │
│ 2019.11.solution │ 2019/11/solution.py │
│ 2019.12.solution │ 2019/12/solution.py │
│ 2019.13.solution │ 2019/13/solution.py │
│ 2019.14.solution │ 2019/14/solution.py │
│ 2019.15.solution │ 2019/15/solution.py │
│ 2019.16.solution │ 2019/16/solution.py │
│ 2019.17.solution │ 2019/17/solution.py │
│ 2019.18.solution │ 2019/18/solution.py │
│ 2019.19.solution │ 2019/19/solution.py │
│ 2019.20.solution │ 2019/20/solution.py │
│ 2019.21.solution │ 2019/21/solution.py │
│ 2019.22.solution │ 2019/22/solution.py │
│ 2019.23.solution │ 2019/23/solution.py │
│ 2019.24.solution │ 2019/24/solution.py │
│ 2019.25.solution │ 2019/25/solution.py │
│ 2020.1.solution  │ 2020/1/solution.py  │
│ 2020.2.solution  │ 2020/2/solution.py  │
│ 2020.3.solution  │ 2020/3/solution.py  │
│ 2020.4.solution  │ 2020/4/solution.py  │
│ 2020.5.solution  │ 2020/5/solution.py  │
│ 2020.6.solution  │ 2020/6/solution.py  │
│ 2020.7.solution  │ 2020/7/solution.py  │
│ 2020.8.solution  │ 2020/8/solution.py  │
│ 2020.9.solution  │ 2020/9/solution.py  │
│ 2020.10.solution │ 2020/10/solution.py │
│ 2020.11.solution │ 2020/11/solution.py │
│ 2020.12.solution │ 2020/12/solution.py │
│ 2020.13.solution │ 2020/13/solution.py │
│ 2020.14.solution │ 2020/14/solution.py │
│ 2020.15.solution │ 2020/15/solution.py │
│ 2020.16.solution │ 2020/16/solution.py │
│ 2020.17.solution │ 2020/17/solution.py │
│ 2020.18.solution │ 2020/18/solution.py │
│ 2020.19.solution │ 2020/19/solution.py │
│ 2020.20.solution │ 2020/20/solution.py │
│ 2020.21.solution │ 2020/21/solution.py │
│ 2020.22.solution │ 2020/22/solution.py │
│ 2020.23.solution │ 2020/23/solution.py │
│ 2020.24.solution │ 2020/24/solution.py │
│ 2020.25.solution │ 2020/25/solution.py │
│ 2021.1.solution  │ 2021/1/solution.py  │
│ 2021.2.solution  │ 2021/2/solution.py  │
│ 2021.3.solution  │ 2021/3/solution.py  │
│ 2021.4.solution  │ 2021/4/solution.py  │
│ 2021.5.solution  │ 2021/5/solution.py  │
│ 2021.6.solution  │ 2021/6/solution.py  │
│ 2021.7.solution  │ 2021/7/solution.py  │
│ 2021.8.solution  │ 2021/8/solution.py  │
│ 2021.9.solution  │ 2021/9/solution.py  │
│ 2021.10.solution │ 2021/10/solution.py │
│ 2021.11.solution │ 2021/11/solution.py │
│ 2021.12.solution │ 2021/12/solution.py │
│ 2021.13.solution │ 2021/13/solution.py │
│ 2021.14.solution │ 2021/14/solution.py │
│ 2021.15.solution │ 2021/15/solution.py │
│ 2021.16.solution │ 2021/16/solution.py │
│ 2021.17.solution │ 2021/17/solution.py │
│ 2021.18.solution │ 2021/18/solution.py │
│ 2021.19.solution │ 2021/19/solution.py │
│ 2021.20.solution │ 2021/20/solution.py │
│ 2021.21.solution │ 2021/21/solution.py │
│ 2021.22.solution │ 2021/22/solution.py │
│ 2021.23.solution │ 2021/23/solution.py │
│ 2021.24.solution │ 2021/24/solution.py │
│ 2021.25.solution │ 2021/25/solution.py │
│ 2022.1.solution  │ 2022/1/solution.py  │
│ 2022.2.solution  │ 2022/2/solution.py  │
│ 2022.3.solution  │ 2022/3/solution.py  │
│ 2022.4.solution  │ 2022/4/solution.py  │
│ 2022.5.solution  │ 2022/5/solution.py  │
│ 2022.6.solution  │ 2022/6/solution.py  │
│ 2022.7.solution  │ 2022/7/solution.py  │
│ 2022.8.solution  │ 2022/8/solution.py  │
│ 2022.9.solution  │ 2022/9/solution.py  │
│ 2022.10.solution │ 2022/10/solution.py │
│ 2022.11.solution │ 2022/11/solution.py │
│ 2022.12.solution │ 2022/12/solution.py │
│ 2022.13.solution │ 2022/13/solution.py │
│ 2022.14.solution │ 2022/14/solution.py │
│ 2022.15.solution │ 2022/15/solution.py │
│ 2022.16.solution │ 2022/16/solution.py │
│ 2022.17.solution │ 2022/17/solution.py │
│ 2022.18.solution │ 2022/18/solution.py │
│ 2022.19.solution │ 2022/19/solution.py │
│ 2023.1.solution  │ 2023/1/solution.py  │
│ 2023.2.solution  │ 2023/2/solution.py  │
│ 2023.3.solution  │ 2023/3/solution.py  │
│ 2023.4.solution  │ 2023/4/solution.py  │
│ 2023.5.solution  │ 2023/5/solution.py  │
│ 2024.2.solution  │ 2024/2/solution.py  │
│ 2024.3.solution  │ 2024/3/solution.py  │
│ 2024.4.solution  │ 2024/4/solution.py  │
│ 2024.5.solution  │ 2024/5/solution.py  │
│ 2024.6.solution  │ 2024/6/solution.py  │
│ 2024.7.solution  │ 2024/7/solution.py  │
│ 2024.8.solution  │ 2024/8/solution.py  │
│ 2024.9.solution  │ 2024/9/solution.py  │
│ 2024.10.solution │ 2024/10/solution.py │
│ 2024.11.solution │ 2024/11/solution.py │
│ 2024.12.solution │ 2024/12/solution.py │
│ 2024.13.solution │ 2024/13/solution.py │
│ 2024.14.solution │ 2024/14/solution.py │
│ 2024.15.solution │ 2024/15/solution.py │
│ 2024.16.solution │ 2024/16/solution.py │
│ 2024.17.solution │ 2024/17/solution.py │
│ 2024.18.solution │ 2024/18/solution.py │
└──────────────────┴─────────────────────┘
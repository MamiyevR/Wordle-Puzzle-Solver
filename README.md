# Wordle Puzzle Solver

This is a program for solving random wordle puzzle. We use 2 API to achieve this task.

<ul>
    <li><a href="https://wordle.votee.dev:8000/random/">Guess Random</a></li>
    <li><a href="https://wordsapiv1.p.rapidapi.com/words">Search Word</a></li>
</ul>

Install libraries

```curl
pip install requirements.tx
```

Before running program, please create .env file and put RapidAPI's API key. You can find API key [here](https://rapidapi.com/)
```txt
RAPIDAPI_KEY=
```

While running program, you can specify seed and length of the word using --seed and --size arguments.

e.g.:

```curl
python wordle_solver.py --size 10 --seed 7
```

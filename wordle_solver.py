import os
import requests
import dotenv
import argparse

dotenv.load_dotenv()


class WordleSolver:
    def __init__(self, size: int, seed: int, url: str):
        self.size = size
        self.seed = seed
        self.url = url
        self.absent = set()  # absent chars
        self.correct = ["."] * size  # correct chars for each slot
        self.present = dict(
            [(i, set()) for i in range(size)]
        )  # present chars for each slot

        self.regex = "^[a-z]{" + str(size) + "}$"  # initial regex pattern

    def __guess_random(self, guess: str):
        try:
            response = requests.get(
                self.url, params={"guess": guess, "size": self.size, "seed": self.seed}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print("Failed to guess a word", e)
            return None

    def __present_chars(self):
        present_chars = set()
        for i in range(self.size):
            present_chars.update(self.present[i])

        return present_chars

    def __update(self, results: list[dict]):
        for result in results:
            if result["result"] == "absent":
                self.absent.add(result["guess"])
            elif result["result"] == "present":
                self.present[result["slot"]].add(result["guess"])
            elif result["result"] == "correct":
                self.correct[result["slot"]] = result["guess"]

    def __build_regex(self):
        regex = ["^"]
        all_chars = set("abcdefghijklmnopqrstuvwxyz")
        present_chars = self.__present_chars()

        for char in present_chars:
            regex.append(f"(?=.*{char})")

        for i in range(self.size):
            if self.correct[i] != ".":
                regex.append(f"{self.correct[i]}{{1}}")
            else:
                allowed_char = all_chars - self.absent - self.present[i]
                regex.append(f"[{''.join(allowed_char)}]{{1}}")

        regex.append("$")

        return "".join(regex)

    def __get_word(self):
        url = "https://wordsapiv1.p.rapidapi.com/words"
        headers = {
            "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
            "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
            "content-type": "application/json",
        }

        # TODO: Add error handling
        try:
            response = requests.get(
                url,
                headers=headers,
                params={"letterPattern": self.regex, "limit": 1, "page": 1},
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print("Failed to get new word", e)
            return None

    def solver(self):
        while "." in self.correct:
            # get new word from the api
            new_words = self.__get_word()

            if new_words is None or new_words["results"]["total"] == 0:
                raise Exception("No word found")

            word = new_words["results"]["data"][0]
            # print(f"word: {self.word}")

            # get results from the api
            results = self.__guess_random(word)

            # update the state of the game
            self.__update(results)

            # build the regex pattern
            self.regex = self.__build_regex()
            # print(f"regex: {self.regex}")

        return "".join(self.correct)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", type=int, default=5)
    parser.add_argument("--seed", type=int, default=1)

    args = parser.parse_args()

    size = args.size
    seed = args.seed

    url = "https://wordle.votee.dev:8000/random"
    solver = WordleSolver(size, seed, url)
    print(solver.solver())

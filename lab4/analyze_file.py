import subprocess
import json
import os
import argparse


def main(path):

    stats = []

    for file in os.listdir(path):
        process = subprocess.run(
            [
                "D:\Skrypotwe\AnalyzeFile\\bin\Debug\\net8.0\AnalyzeFile.exe",
            ],
            stdout=subprocess.PIPE,
            text=True,
            input=f"{path}/{file}",
        )

        output = process.stdout

        file_stats = json.loads(output)

        stats.append(file_stats)

    for f in stats:
        print(f)


    files_number = len(stats)
    chars_sum = sum(stat["CharsNumber"] for stat in stats)
    words_sum = sum(stat["WordNumber"] for stat in stats)
    verses_sum = sum(stat["VerseNumber"] for stat in stats)


    #zle zaimplementowane, powinny byc 2 slowniki o strukturze: {znak : liczba wystapien}, {slowo: liczba wystapien}
    top_char = max(set(stat["TheMostCommonChar"] for stat in stats))
    top_word = max(set(stat["TheMostCommonWord"] for stat in stats))

    print(f"Liczba przeczytanych plików: {files_number}")
    print(f"Suma znaków: {chars_sum}")
    print(f"Suma słów: {words_sum}")
    print(f"Suma wierszy: {verses_sum}")
    print(f"Najczęściej występujący znak: '{top_char}'")
    print(f"Najczęściej występujące słowo: '{top_word}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sumuje statystyki dla plikow w podanym folderze."
    )
    parser.add_argument("path")
    args = parser.parse_args()
    main(args.path)

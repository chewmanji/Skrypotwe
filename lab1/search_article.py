import wikipedia
import sys
import warnings

warnings.catch_warnings()

warnings.simplefilter("ignore")

wikipedia.set_lang("en")

def search_articles(topic : str):
    articles = wikipedia.search(query=topic, results = 3)

    try:
        for index, article in enumerate(articles):
            page = wikipedia.page(article, auto_suggest=False) #auto_suggest = False wazne zeby nie otrzymywac niepowiązanych artykułow np foot -> food
            print(f"{index})\nHere's summary of an article titled '{article}':\n")
            print(page.summary)

            print(f"\nHere's a link to the article: {page.url}\n")

    except wikipedia.PageError as e:
        print(f"The page with title '{article}' was not found")

    except wikipedia.DisambiguationError as e:
        print('Ambiguation has occured, check these options:')
        for index, option in enumerate(e.options):
            print(f"{index}) {option}")

    


if __name__ == "__main__":
    print("Ctrl+C to exit")
    while True:
        try:
            topic = input("Enter topic that interests you:\n")
            search_articles(topic)

        except KeyboardInterrupt:
            print("Exiting...")
            sys.exit(0)
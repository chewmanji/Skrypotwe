
namespace TextFileStats
{
    class Program
    {
        static void Main(string[] args)
        {
            // Pobranie ścieżki do pliku
            string? filePath = Console.ReadLine();

            // Sprawdzenie, czy plik istnieje
            if (!File.Exists(filePath))
            {
                Console.WriteLine("File doesn't exists!");
                return;
            }

            // Analiza pliku
            var stats = AnalyzeFile(filePath);

            // Wypisanie wyników
            Console.WriteLine(stats.ToJson());
        }

        static FileStats AnalyzeFile(string filePath)
        {
            // Odczytanie zawartości pliku
            string text = File.ReadAllText(filePath);

            // Policzenie znaków
            int charsNumber = text.Length;

            // Policzenie słów
            int wordsNumber = text.Split(' ', '\t', '\n', '\r').Length;

            // Policzenie wierszy
            int verseNumbers = text.Split('\n').Length;

            // Znajdź najczęściej występujący znak
            char theMostCommonChar = text.GroupBy(c => c).OrderByDescending(g => g.Count()).First().Key;

            // Znajdź najczęściej występujące słowo
            string theMostCommonWord = text.Split(' ', '\t', '\n', '\r')
                .GroupBy(s => s).OrderByDescending(g => g.Count()).First().Key;

            // Zwróć statystyki
            return new FileStats
            {
                FilePath = filePath,
                CharsNumber = charsNumber,
                WordNumber = wordsNumber,
                VerseNumber = verseNumbers,
                TheMostCommonChar = theMostCommonChar,
                TheMostCommonWord = theMostCommonWord
            };
        }
    }

    public class FileStats
    {
        public string? FilePath { get; set; }
        public int CharsNumber { get; set; }
        public int WordNumber { get; set; }
        public int VerseNumber { get; set; }
        public char TheMostCommonChar { get; set; }
        public string? TheMostCommonWord { get; set; }

        public string ToJson()
        {
            return Newtonsoft.Json.JsonConvert.SerializeObject(this);
        }
    }
}

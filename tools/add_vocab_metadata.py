#!/usr/bin/env python3
"""Add study metadata to vocab.json without touching the word pairs.

Each entry keeps its original {"English": "日本語"} pair and gains one or more
"$"-prefixed keys the study app uses to route words into sentence frames:

  $type  semantic class (animal, food, place, adj_i, ...)
  $en    natural English word/phrase used inside generated sentences
  $nat   demonym, for country words ("Australian")
  $play  which verb an instrument takes (ひきます / ふきます / たたきます)
  $num   numeric value for numbers, prices and ages

Entries that are set phrases, particles or classroom language are left as-is.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PATH = ROOT.parent / "vocab.json"

TYPES = {}


def add(kind, names, **extra):
    for name in names:
        if name in TYPES:
            raise SystemExit(f"duplicate mapping: {name}")
        TYPES[name] = dict(type=kind, **extra)


add("animal", [
    "Cat", "Dog", "Mouse", "Bird", "Rabbit", "Cow", "Pig", "Sheep", "Snake", "Horse",
    "Monkey", "Turtle", "Elephant", "Deer", "Crab", "Shark", "Giraffe", "Bee", "Animal", "Pet",
])

add("person", [
    "I", "I, me, myself (male)", "Friend", "Teacher", "Everyone", "Customer", "Waiter",
    "Woman", "Girl", "Man", "Boy", "Girlfriend", "Boyfriend",
])

add("family", [
    "Father (own)", "Mother (own)", "Older brother (own)", "Older sister (own)",
    "Younger brother (own)", "Younger sister (own)", "Grandfather (own)", "Grandmother (own)",
    "Family", "Uncle (own)", "Aunt (own)", "Parents", "Parent(s)", "Cousin", "Relative",
    "Child", "Baby", "Father (other)", "Mother (other)", "Older brother (other)",
    "Older sister (other)", "Younger brother (other)", "Younger sister (other)",
    "Grandfather (other)", "Grandmother (other)", "Uncle (other)", "Aunt (other)",
    "Cousin (other)", "Siblings / brothers & sisters", "Only child", "Wife (other)",
    "Wife (own)", "Sisters", "Couple", "Husband", "Son", "Daughter", "Siblings (other)",
    "Child (other)", "Twins",
])

COUNTRIES = {
    "Australia": "Australian", "Japan": "Japanese", "America": "American",
    "China": "Chinese", "England": "English", "Korea": "Korean", "Germany": "German",
    "Vietnam": "Vietnamese", "France": "French", "India": "Indian", "Russia": "Russian",
    "Spain": "Spanish", "Singapore": "Singaporean", "Malaysia": "Malaysian",
    "Pakistan": "Pakistani", "Sri Lanka": "Sri Lankan", "Nepal": "Nepalese",
    "Jamaica": "Jamaican", "Myanmar": "Burmese", "Bangladesh": "Bangladeshi",
}
for country, demonym in COUNTRIES.items():
    add("country", [country], nat=demonym)

add("language", ["Japanese", "English", "Chinese", "Korean", "German", "French"])

add("food", [
    "Sushi set", "Cutlet curry", "Cuisine/dishes", "(Cooked) rice / meal", "Miso soup",
    "Pickles", "Set meal", "Udon (thick noodles in broth/soup)",
    "Tonkatsu (crumbed pork schnitzel)", "Katsudon (tonkatsu mixture on top of rice)",
    "Vegetables", "Chicken skewers", "Deep fried food", "Deep fried chicken",
    "Tempura (tempura batter fried vegetables, prawns, fish)", "Prawn", "Meat", "Tofu",
    "Curry & rice", "Tempura set meal", "Wagyu steak", "Sushi", "Riceball", "Boxed Lunch",
    "Chicken & Egg Bowl", "Curry", "Omelette Rice", "Ramen",
    "Soba (noodles made from buckwheat flour)", "Okonomiyaki (savoury pancake)",
    "Takoyaki (octopus filled balls)", "Dumplings", "Japanese BBQ", "Grilled Eel",
    "Daifuku (mochi with sweet filling)", "Candy", "Food", "Salad", "Sashimi", "Rice Burger",
    "Tempura meal", "Hamburger Set", "Hamburger", "Hamburg Steak", "Pizza", "Cake", "Apple",
    "Banana", "Watermelon", "Strawberry", "Cherry", "Peach", "Pear", "Bread", "Pineapple",
    "Fish",
])

add("drink", ["Water", "Green tea", "Milk", "Black tea", "Coffee", "Drinks"])

add("sport", ["Tennis", "Baseball", "Basketball", "Volleyball", "Cricket", "Ice skating",
              "Soccer", "Sports", "Swimming"])

add("activity", ["Shopping", "Dance", "Karate", "Kendo", "Calligraphy", "Karaoke",
                 "English conversation", "Study", "Practice", "Extra curricular activities",
                 "Choir", "Cycling", "Jogging"])

add("song", ["Song", "Rock (music)", "J-Pop", "K-pop", "Hip-Hop"])
add("instrument", ["Musical instrument"])

INSTRUMENT_VERB = {
    "Piano": "ひきます", "Guitar": "ひきます", "Flute": "ふきます", "Trumpet": "ふきます",
    "Clarinet": "ふきます", "Saxophone": "ふきます", "Sax": "ふきます", "Drums": "たたきます",
}
for instrument, verb in INSTRUMENT_VERB.items():
    add("instrument", [instrument], play=verb)

add("place", [
    "Friend's house", "School", "Pool", "School/sporting grounds", "Station", "Department Store",
    "Arcade", "Garden", "Shop", "Shrine", "Park", "Temple", "Castle", "Shrine gate", "Place",
    "House", "Library", "Tutoring College", "Church", "Large Buddha Statue", "Atomic Bomb Dome",
])
add("locality", ["Town (shopping area)"])
add("event", ["Festival"])

add("thing", [
    "Book", "History", "Television", "Movie", "Music", "Japanese comics", "Magazine", "Novel", "Newspaper",
    "Homework", "Souvenir", "Money", "Dollar", "Triangle", "Game",
])

add("colour_noun", ["Red", "Blue", "Green", "White", "Brown", "Purple", "Black", "Grey",
                    "Orange", "Yellow", "Pink", "Color", "Rainbow", "Light blue"])
add("colour_adj", ["Red (adjective)", "Blue (adjective)", "White (adjective)",
                   "Yellow (adjective)", "Black (adjective)"])

add("adj_i", [
    "Interesting", "Bright / Cheerful", "Kind / Gentle", "Good", "Intelligent",
    "Enjoyable / Fun", "Cute", "Cool / Good looking", "Tasty/Delicious", "Great", "Big", "Small",
    "New", "Old", "Beautiful", "Busy", "Smelly", "Expensive",
])
add("adj_na", [
    "Quiet", "Famous", "Pretty/Clean", "Convenient", "Bustling", "Healthy", "Weird",
    "Funny, Comedic", "Fresh", "Safe",
])

add("preference", ["Like", "Dislike", "Love (not romantically)", "Hate", "Don't like",
                   "Favourite", "Don't like very much", "So-so"], en={
    "Like": "like", "Dislike": "don't like", "Love (not romantically)": "love", "Hate": "hate",
    "Don't like": "don't like", "Favourite": "like best",
    "Don't like very much": "don't really like", "So-so": "quite like",
})

add("verb", [
    "To go", "To read", "To learn", "To watch/see", "To study", "To listen/hear", "To practise",
    "Play (key/string instruments)", "Play (wind/brass instruments)", "Hit/strike/beat", "Sing",
    "To eat (food)", "To drink (soup/drink)", "To write", "To have (inanimate)", "To live in",
    "Catch a cold", "To love (romantically)", "To come", "To climb",
    "Exists/have (eg. Siblings)", "Doesn't exist/ don't have", "(To) do / play",
])

NUMBERS = {
    "Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7,
    "Eight": 8, "Nine": 9, "Ten": 10, "Twenty": 20, "Thirty": 30, "Forty": 40, "Fifty": 50,
    "Sixty": 60, "Seventy": 70, "Eighty": 80, "Ninety": 90, "One hundred": 100,
    "Two hundred": 200, "Three hundred": 300, "Four hundred": 400, "Five hundred": 500,
    "Six hundred": 600, "Seven hundred": 700, "Eight hundred": 800, "Nine hundred": 900,
    "One thousand": 1000, "Two thousand": 2000, "Three thousand": 3000, "Four thousand": 4000,
    "Five thousand": 5000, "Six thousand": 6000, "Seven thousand": 7000, "Eight thousand": 8000,
    "Nine thousand": 9000, "Ten thousand": 10000, "Hundred thousand": 100000,
    "Million": 1000000, "Ten million": 10000000, "Hundred million": 100000000,
    "Billion": 1000000000,
}
for word, value in NUMBERS.items():
    add("number", [word], num=value)

AGES = {
    "1 year old": 1, "4 years old": 4, "7 years old": 7, "8 years old": 8, "9 years old": 9,
    "10 years old": 10, "20 years old": 20,
}
for word, value in AGES.items():
    add("age", [word], num=value)

PEOPLE_COUNTERS = {
    "1 person": 1, "2 people": 2, "3 people": 3, "4 people": 4, "5 people": 5, "6 people": 6,
    "7 people": 7, "8 people": 8, "9 people": 9, "10 people": 10,
}
for word, value in PEOPLE_COUNTERS.items():
    add("counter_people", [word], num=value)

add("day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
add("day_relative", ["Today", "Tomorrow", "Yesterday"])
add("time", ["Week", "One week", "Weekend"])
add("money_unit", ["Yen"])

add("question", ["What kind of", "Who", "What day (of the week)", "How much", "What", "Where",
                 "How many people?"])

META_ORDER = ["type", "en", "nat", "play", "num"]


def main():
    raw = PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    assert isinstance(data, list)

    lines = ["["]
    tagged = 0
    for i, entry in enumerate(data):
        assert isinstance(entry, dict), entry
        pairs = [(k, v) for k, v in entry.items() if not k.startswith("$")]
        assert len(pairs) == 1, entry
        (english, japanese), = pairs
        out = {english: japanese}
        meta = TYPES.get(english)
        if meta:
            tagged += 1
            out["$type"] = meta["type"]
            for key in META_ORDER[1:]:
                if key in meta:
                    out["$" + key] = meta[key]
        suffix = "," if i < len(data) - 1 else ""
        lines.append("  " + json.dumps(out, ensure_ascii=False) + suffix)
    lines.append("]")
    new_text = "\n".join(lines) + "\n"

    # Safety: pairs must be byte-for-byte identical in content and order.
    reparsed = json.loads(new_text)

    def pairs(items):
        return [next((k, v) for k, v in item.items() if not k.startswith("$")) for item in items]

    assert pairs(reparsed) == pairs(data), "word pairs changed"
    PATH.write_text(new_text, encoding="utf-8")

    unused = [next(iter(e)) for e in data if next(iter(e)) not in TYPES]
    print(f"entries: {len(data)}  tagged: {tagged}  untouched: {len(unused)}")
    by_type = {}
    for meta in TYPES.values():
        by_type[meta["type"]] = by_type.get(meta["type"], 0) + 1
    print("types:", dict(sorted(by_type.items(), key=lambda kv: -kv[1])))
    missing = [name for name in TYPES if name not in {next(iter(e)) for e in data}]
    print("mapped names not found in vocab.json:", missing)


if __name__ == "__main__":
    main()

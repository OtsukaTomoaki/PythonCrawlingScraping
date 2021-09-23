import json

cities = [
    { 'rank': 1, 'city': 'Foo', 'population': 2000 },
    { 'rank': 2, 'city': 'Bar', 'population': 60000 },
    { 'rank': 3, 'city': 'Baz', 'population': 300 },
]
print(json.dumps(cities))

with open('top_cities.json', 'w') as f:
    json.dump(cities, f)
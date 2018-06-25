# TopTrumps
Made for a school thing, not particulary exciting. Simulates a game of top trumps between two people, using a file that contains information on each of the cards.

The files are in a `JSON` format, like so:

```json
{
    "traits": {
        "shield": "A description of shield",
        "wisdom": "A description of wisdom",
        "strength": "A description of the strength"
    },

    "cards": [{
            "name": "Card 1",
            "description": "The first card.",
            "traits": {
                "strength": 50,
                "wisdom": 25,
                "shield": 25
            }
        },
        {
            "name": "Card 2",
            "description": "The second card.",
            "traits": {
                "strength": 25,
                "wisdom": 50,
                "shield": 25
            }
        }
    ]
}
```

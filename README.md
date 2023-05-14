# ZillowParse
Test task on web scraping and data processing

This is a test task that I received and completed:

1. It was necessary to parse 2 store sites and get all their addresses (https://locations.traderjoes.com/, https://www.wholefoodsmarket.com/stores/);
2. Send a request to the zillow.com website via the API according to the criteria that are on the site when searching;
3. Must be an input of X miles (distance from each house to shops);
4. Compare the distance from each house to each store. The distance must not exceed X miles;
5. Collect addresses of stores that fit. Save all data in json.


In order not to parse store sites once again, I attach 2 processed files with store addresses and their coordinates (T_J_stores_coord.json, WFM_stores_coord.json).

An example of uploaded data through the Rapid API is in the zillow.json file.

To test the logic of the code, you can run the ZillowParse.py script (lines 54-101).
You can play around with the values ​​of the choice_miles variable (line 64) to see the difference.


To use the script in full, you can register on the site https://rapidapi.com/apimaker/api/zillow-com1/ and get API-key 
(endpoint /propertyExtendedSearch (Extended search)).
In this case, you can change the search parameters for houses in ZillowParse.py (lines 14-24).


If you have any comments on my work, I will be glad to hear feedback.

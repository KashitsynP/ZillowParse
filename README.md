# ZillowParse
This is a task that I received and completed:

1. It was necessary to parse 2 store sites and get all their addresses (https://locations.traderjoes.com/, https://www.wholefoodsmarket.com/stores/);
2. Send a request to the zillow.com website via the API according to the criteria that are on the site when searching;
3. Must be an input of X miles (distance from each house to shops);
4. Compare the distance from each house to each store. The distance must not exceed X miles;
5. Collect addresses of stores that fit. Save all data in json.



Files WFMParse.py and TJParse.py contain scripts for parsing addresses and coordinates of stores. 
The main logic is in file ZillowParse.py, where Zillow.com site data is processed and store coordinates are compared.

In order not to parse store sites once again, I attach 2 processed files with store addresses and their coordinates (T_J_stores_coord.json, WFM_stores_coord.json).

An example of uploaded data through the Rapid API is in the zillow.json file.

To test the logic of the code, you can run the ZillowParse.py script (lines 62-108).
You can play around with the values ​​of the choice_miles variable (line 67) to see the difference.


To use the script in full, you can register on the site https://rapidapi.com/apimaker/api/zillow-com1/ and get API-key 
(endpoint /propertyExtendedSearch (Extended search)).
In this case, you can change the search parameters for houses in ZillowParse.py (lines 18-28).


If you have any comments on my work, I will be glad to hear feedback.

# MongoDB Populator

This is a tool I made in a databases class to quickly populate a MongoDB database with fake data to run demos with.

The schema is one a music streaming service could use. 

Image of schema is at the bottom of this markdown document. You can also view it in the schemas.py file.

To run, in mongo.py, call the function that you want to do with the parameters you want.

For best results, use one of the for loops to efficiently generate a lot of data.

Also, I recommend using functions in conjunction with other functions to create links between data automatically, since this is where I drew real benefit from the program.

For example:
1. Use `[createartistwithalbums() for _ in range(5)]` to create 5 artists with 1 release each
2. Use `[createuser() for _ in range(20)]` to create 20 users
3. Use `[createplaylistforusers() for _ in range(3)]` to create playlists for existing users with existing songs

Structure:
![database schema](https://github.com/samdotnet/MongoDB-Populator/assets/63370140/ca27bb23-61ba-405d-aae6-21d689d938fc)

*I apologize for the lack of comments.*

## Penn Course Search

A semantic search engine for the penn course database!

### /frontend
React project with all frontend related code and docker config
npm install
npm start

### backend:  
app.py: backend routes  
courses-scraper.py: scraps penn catalog for courses and saves it in courses.csv
embed.py: embeds course info into vector via OPENAI and saves it in courses_embed.csv
review-scraper.py: get course review information for a course & professor and saves it in courses_embed_profs.csv
mongo_load.py: uploads embeddings from courses_embed_profs.csv into MongoDB
query_engine: logic to query for results  
 
db: mongoDB

## TODO:
- [x] Migrate from pinecone to alt vectordb (atlas?)
- [x] Remove unused files
- [x] Refactor query logic to be readble and modular
- [x] detailed readme on running, stack etc. https://github.com/rohanshar77/dbkcourses
- [x] backend into its own directory (maybe move to fastapi?)
- [ ] move hosting to porter.run
- [ ] chron job to auto update db

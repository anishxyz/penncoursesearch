Penn Course Search

A semantic search engine for the penn course database!

/frontend
  React project with all frontend related code and docker config

backend:
app.py: backend routes
courses-scraper.py: scraps penn catalog for courses
embed.py: embeds course info into vector via ada
review-scraper.py: get course review information for a course
query_engine: logic to query for results

db: pinecone (mongo not used)

TODO:
- [ ] Migrate from pinecone to alt vectordb (atlas?)
- [ ] Remove unused files
- [ ] Refactor query logic to be readble and modular
- [ ] detailed readme on running, stack etc. https://github.com/rohanshar77/dbkcourses
- [ ] backend into its own directory (maybe move to fastapi?)
- [ ] move hosting to porter.run
- [ ] chron job to auto update db

!Disclaimer! 

This is a rather long readme so feel free to dive into the project itself. An important piece of information is at the bottom of this there is a section called Project Files which gives brief descriptions of what you will find in those folders. This is the first time I have ever tried to do an end to end data analysis project using various programs while learning new software so any constructive feedback would be appreciated.

This project demonstrates an end-to-end healthcare analytics workflow using synthetic data. Rather than using real patient information, a Pokémon dataset was transformed into a healthcare-style relational database to practice Python programming, SQL querying, database design, and healthcare data analysis. The use of synthetic data allows the project to demonstrate realistic analytical workflows while avoiding the use of protected health information (PHI). Pokémon names are used in place of patient names so that the project can focus on database design and analytical techniques without using any real patient information. Medical diagnoses, treatments, and visit records were then synthetically generated to simulate a simplified healthcare database.

The project began when I decided to create a database of Pokémon so that I could practice SQL queries while learning relational databases. I used Serebii.net, which has an extensive list and description of Pokémon, as the source for the original dataset. After creating the initial table, I wrote a Python script that randomly selected a total of 225 Pokémon for use in the project, with 25 Pokémon selected from each represented region. I omitted the Hisui region because there were not enough Pokémon available, while Orre is not represented because no Pokémon were originally introduced in that region. Pokémon from Kitakami and Blueberry were consolidated into the Paldea region for this project.

Python was then used to transform the sampled Pokémon into a synthetic healthcare-style database by generating patient information, diagnoses, treatments, and visit records. Each table was designed to represent a different part of a simplified healthcare system while maintaining relationships between records. SQL was then used to analyze the database through joins, aggregations, grouping, filtering, and summary statistics to answer healthcare-style analytical questions.

Although this project uses synthetic data, the workflow mirrors many of the steps involved in healthcare analytics projects, including data generation, database creation, SQL analysis, validation, and documentation. The goal was not to draw clinical conclusions but to build a realistic environment for developing technical skills used by healthcare and research data analysts.

For this project I used Python along with the IDE PyCharm and the pandas and NumPy libraries for the creation of the tables using synthetic data and validating the information in the tables ensuring that they each indeed received the amount of data they were supposed to. For the data analysis and queries I used DB Browser (SQLite). I still plan on doing a Power BI visualization but that will come later down the road. 
	
The project contains various folders within the Main branch, all of which are fairly self-explanatory, but here is a brief description. The Data folder holds all the data tables such as the original Pokemon Dataset that displays their stats, abilities, types, etc. but it also houses the tables created after running the Python code. The SQLite folder holds important queries that I wanted to display. (Note that this does not show every single query that I used or tested because I don’t think anyone wants to see queries that show the Name of Patient ID 187.) The Documents folder holds some documents such as a PDF of the seven queries in the folder ‘Analyzing Queries’ which shows a brief analysis of my conclusions of the queries.

Future Works:
Power BI visualization
More advanced queries and analysis

TL;DR:
Project Files
Data: Contains the original Pokémon dataset and the synthetic healthcare CSV tables generated using Python.
Database: Contains the completed SQLite database.
Python Codes: Contains the scripts used to generate and validate the synthetic healthcare data.
SQLite Queries: Contains the table-creation SQL and seven selected analytical queries. These represent only a portion of the queries tested during the project.
Documents: Contains the data dictionary and Query Analysis PDF, which discusses the results and limitations of the seven highlighted SQL queries.


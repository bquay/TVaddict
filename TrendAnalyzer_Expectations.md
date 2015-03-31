# VotingApp
VotingApp
•	Trend Analyzer
o	Add a date-time field to votes when they are added to database
o	Create a chronjob that runs every 10 seconds.  Chronjob should:
	Get a list of vote that have happened in the past three hours by querying vote database for all such votes
	Create an ordered list of [tag or poster]s ordered by number of votes in the list of votes retrieved from database
	Update trending [tag or poster] list with top 3 results from ordered list
o	Display 3 [tag or poster]s with most votes in past 3 hours
•	Test
o	Send three emails, one for each [tag or poster]
o	(wait 10 seconds)
o	Then check results to see trends results
	Expect: 
1.	[tag or poster] 1: 1 vote
2.	[tag or poster] 2: 1 vote
3.	[tag or poster] 3: 1 vote
o	Send one more to one of the already voted on [tag or poster]s (2nd or 3rd in initial list)
o	(wait 10 seconds)
o	Confirm that that “already voted on” [tag or poster] is now at the top of the list
	Expect:
1.	[tag or poster] 2: 2 votes
2.	[tag or poster] 1: 1 vote
3.	[tag or poster] 3: 1 vote
o	Send three votes to a fourth, not-yet-voted-on, [tag or poster]
o	(wait 10 seconds)
o	Confirm that [tag or poster] that received the three votes is now at the top of the list and that one of the [tag or poster]s that received one vote initially is no longer displayed
	Expect:
1.	[tag or poster] 4: 3 votes
2.	[tag or poster] 2: 2 votes
3.	[tag or poster] 1: 1 vote
a

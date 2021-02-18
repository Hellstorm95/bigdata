sh.addShard("shard01/shard01a:27018")
sh.addShard("shard01/shard01b:27018")

sh.addShard("shard02/shard02a:27019")
sh.addShard("shard02/shard02b:27019")

sh.addShard("shard03/shard03a:27020")
sh.addShard("shard03/shard03b:27020")

use covid
sh.enableSharding("covid")
sh.shardCollection("covid.EUData", key={'cases_weekly': 1})
db.EUData.insert({ 
         "dateRep" : "01/01/2021",
         "year_week" : "2021-01",
         "cases_weekly" : 0,
         "deaths_weekly" : 0,
         "countriesAndTerritories" : "Test",
         "geoId" : "T",
         "countryterritoryCode" : "TTT",
         "popData2019" : 0,
         "continentExp" : "Test",
         "notification_rate_per_100000_population_14-days" : "0"})

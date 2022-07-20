import multiprocessing
import database as db
import pandas as pd
import simFuctions as sim

#function to run the sim
def runSim(df ,choice,betType , keys):
    units, wins, loses, unitsOvertime , banList = sim.setDefults()
    #team ban list key
    banList = []
    count = 1
    if('banList' in keys):
        banList,count = bestBanList(df, choice, betType, keys)
    for i in range(len(df)):
        num = sim.decideNum(df, i, betType)
        #key checks
        if sim.isSkipKey(df, keys, banList,i,num) == 1:
            continue
        #check if no more units to bet
        if (units < 1):
            return units , wins, loses,banList, unitsOvertime, count
        units, wins, loses, unitsOvertime = sim.doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i)
    return units , wins, loses,banList, unitsOvertime,count #, keys

#function to get the best key combinations
def bestKeysSim(df_testing, keys, betTypes):
    count =0
    df_top10 = pd.DataFrame(columns=['units','wins','loses','totalbets','winrate',
                                     'unitsovertime','banList','KeySet','betType','choice'])
    keysCombo = sim.makeCombonations(keys)
    for choice in ['under','over']:
        for betType in betTypes:
            #muliprocessing of the sim with a pool of workers
            with multiprocessing.Pool(processes=2) as pool:
                results = [pool.apply_async(runSim, args=(df_testing, choice, betType, key)) for key in keysCombo]
                pool.close()
                pool.join()
                for result in results:
                    units, wins, loses, banList, unitsOvertime, count, keys = result.get()
                    df_top10 = sim.checkIfHigher(df_top10, units, wins, loses,
                                                banList, unitsOvertime, keys, betType, choice)


            for keylist in keysCombo:
                count += 1
                testUnits , testWins, testLoses, testbanlist, testUnitsOvertime,addToCount = runSim(df_testing, choice, betType, keylist )
                count += addToCount
                df_top10 = sim.checkIfHigher(df_top10, testUnits, testWins, testLoses, testbanlist, testUnitsOvertime, keylist, betType, choice)
                    
    return df_top10, count

#keys functions

#function to get the best banList
def bestBanList(df ,choice,betType , keys):
    count =0
    #simulation of a beting strategy
    tournament_name = df['tournament_name'][0]
    teamsList = db.getTeamNames(tournament_name)
    banlistCombo = sim.makeCombonations(teamsList)
    units =100.0
    bestbanlist = []
    for banlist in banlistCombo:
        count += 1
        testUnits = 100
        testUnits = banSim(df, choice, betType, banlist, keys)
        if(testUnits > units):
            units = testUnits
            bestbanlist = banlist
    return bestbanlist, count

#run sim for getting best banlist
def banSim(df ,choice,betType , banList, keys):
    units, wins, loses, unitsOvertime , ignore_this = sim.setDefults()
    for i in range(len(df)):
        num = sim.decideNum(df, i, betType)
        #key checks
        if sim.isSkipKey(df, keys, banList,i,num) == 1:
            continue
        units, wins, loses, unitsOvertime = sim.doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i)
    return units

#print the results of the sim
def printSim(df, i):
    print('outcome: ')
    print(f'units: {str(df["units"][i])}')
    print(f'wins: {str(df["wins"][i])}')
    print(f'loses: {str(df["loses"][i])}')
    print(f'total bets: {str(df["totalbets"][i])}')
    print(f'winrate: {str(df["winrate"][i])}')
    print(f'choice: {str(df["choice"][i])}')
    print(f'key set: {str(df["KeySet"][i])}')
    print(f'exclude list: {str(df["banList"][i])}')

# df_testing = pd.read_sql_query('SELECT * FROM games WHERE tournamentID = 1', db.engine)
# all_keys = ['banList','isFirstOfMatch','isLastOfMatch','isSecondOfMatch','isNotFirstOfMatch','AvgTotalKillsLessThan']
# all_bet_types = ['kills','dragons','barons','tower','gameTime']
# keys = []
# betTypes = ['dragons']
# df_top10, count = bestKeysSim(df_testing, keys,betTypes)
# print(f'number of sims done: {str(count)}')










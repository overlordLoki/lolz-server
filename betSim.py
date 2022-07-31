import database as db
import pandas as pd
import simFunctions as sim
import banSim as bs
#function to run the sim
def runSim(df ,choice,betType,banList , keys):
    units, wins, loses, unitsOvertime = sim.setDefults()
    #team ban list key
    count = 1
    for i in range(len(df)):
        num = sim.decideNum(df, i, betType)
        #key checks
        if sim.isSkipKey(df, keys, banList,i,num) == 1:
            continue
        #check if no more units to bet
        if (units < 1):
            return units , wins, loses,banList, unitsOvertime, count
        units, wins, loses, unitsOvertime = sim.doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i)
    return units , wins, loses, unitsOvertime,count

#function to get the best key combinations
def bestKeysSim(df_testing, keys, betTypes):
    count =0
    df_top10 = pd.DataFrame(columns=['units','wins','loses','totalbets','winrate',
                                     'unitsovertime','banList','KeySet','betType','choice'])
    keysCombo = sim.makeCombonations(keys)
    banList = []
    for choice in ['under','over']:
        for betType in betTypes:
            for keylist in keysCombo:
                if 'banList' in keylist:
                    banList = bs.bestBanList(df_testing, choice, betType, keylist)
                count += 1
                testUnits , testWins, testLoses, testUnitsOvertime,addToCount = runSim(df_testing, choice, betType,banList, keylist )
                count += addToCount
                df_top10 = sim.checkIfHigher(df_top10, testUnits, testWins, testLoses, banList, testUnitsOvertime, keylist, betType, choice)
                    
    return df_top10, count

#keys functions

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

def testingR():
    df_testing = pd.read_sql_query('SELECT * FROM games WHERE tournamentID = 1', db.engine)
    all_keys = ['banList','isFirstOfMatch','isLastOfMatch','isSecondOfMatch','isNotFirstOfMatch','AvgTotalKillsLessThan']
    all_bet_types = ['kills','dragons','barons','tower','gameTime']
    keys = []
    betTypes = ['kills']
    df_top10_keys, count = bestKeysSim(df_testing, keys,betTypes)
    count = count*2
    print(f'number of sims done: {str(count)}')
    return 1

#muliprocessing of the sim with a pool of workers
# with multiprocessing.Pool(processes=2) as pool:
#     results = [pool.apply_async(runSim, args=(df_testing, choice, betType, key)) for key in keysCombo]
#     pool.close()
#     pool.join()
#     for result in results:
#         units, wins, loses, banList, unitsOvertime, count, keys = result.get()
#         df_top10 = sim.checkIfHigher(df_top10, units, wins, loses,
#                                     banList, unitsOvertime, keys, betType, choice)








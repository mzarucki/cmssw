#
# provide online L1 Trigger DQM input from file(s)
#
# V M Ghete 2010-07-09

import FWCore.ParameterSet.Config as cms

###################### user choices ######################

# choose one sample identifier from the list of data samples 
#
sampleIdentifier = '267375_DAS' #266277_DAS 265377_DAS 263675 251251_DAS 265377_DAS 263675 251251_relVal_runTheMatrix_step3 251251 relVal_step3 relVal_CMSSW_8_0_0_pre6 251251 251131 165633-CAFDQM 195378

maxNumberEvents = 1000

###################### end user choices ###################

# initialize list of files, of secondary files, list of selected events and luminosity segments
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
selectedEvents = cms.untracked.VEventRange()
selectedLumis= cms.untracked.VLuminosityBlockRange()


maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(maxNumberEvents)
)

if sampleIdentifier == '273013_DAS': #May 2016
    runNumber = '273013'
    dataset = '/ZeroBias1/Run2016B-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

elif sampleIdentifier == '267375_DAS': #2016 MWGR4
    runNumber = '267375'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

elif sampleIdentifier == '266277_DAS': #2016 MWGR3
    runNumber = '266277'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

elif sampleIdentifier == '265377_DAS': #2016 MWGR2
    runNumber = '265377'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

elif sampleIdentifier == '265377': #2016 MWGR2
    runNumber = '265377'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = False
    readFiles.extend(['file:/afs/cern.ch/work/m/mzarucki/data/Cosmics_Commissioning2016-v1_RAW_1.root',
                      'file:/afs/cern.ch/work/m/mzarucki/data/Cosmics_Commissioning2016-v1_RAW_2.root'])

elif sampleIdentifier == '265380_DAS': #2016 MWGR2
    runNumber = '265380'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

elif sampleIdentifier == '265383_DAS': #2016 MWGR2
    runNumber = '265383'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

elif sampleIdentifier == '264593_DAS': #2016 MWGR1
    runNumber = '264593'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

elif sampleIdentifier == '264479_DAS': #2016 MWGR1
    runNumber = '264479'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

elif sampleIdentifier == '263675_DAS': #2015 HI run #Global Tag: 76X_dataRun2_v15
    runNumber = '263675'
    dataset = '/Cosmics/HIRun2015-v1/RAW'
    dataType = 'RAW'
    useDAS = True

elif sampleIdentifier == '263675': #2015 HI run
    runNumber = '263675'
    dataset = '/Cosmics/HIRun2015-v1/RAW'
    dataType = 'RAW'
    useDAS = False
    readFiles.extend(['file:/afs/cern.ch/work/m/mzarucki/data/HIRun2015_Cosmics_263675_RAW.root'])

elif sampleIdentifier == 'relVal_134.901_RunHLTPhy2015D_step2':
    runNumber = '256677'
    dataset = '/HLTPhysics/Run2015D-v1'
    dataType = 'RAW'
    useDAS = False
    readFiles.extend(['file:/afs/cern.ch/work/m/mzarucki/data/relVal_134.901_RunHLTPhy2015D_step2.root'])

elif sampleIdentifier == 'relVal_134.901_RunHLTPhy2015D_step3': #digi
    runNumber = '256677'
    dataset = '/HLTPhysics/Run2015D-v1'
    dataType = 'DIGI'
    useDAS = False
    readFiles.extend(['file:/afs/cern.ch/work/m/mzarucki/data/relVal_134.901_RunHLTPhy2015D_step3.root'])

elif sampleIdentifier == 'relVal_134.99901_RunHLTPhy2015D_step2': 
    runNumber = '258712'
    dataset = '/HLTPhysics/Run2015D-v1'
    dataType = 'RAW'
    useDAS = False
    readFiles.extend(['file:/afs/cern.ch/work/m/mzarucki/data/relVal_134.99901_RunHLTPhy2015D_step2.root'])

elif sampleIdentifier == 'relVal_134.99901_RunHLTPhy2015D_step3': #digi
    runNumber = '258712'
    dataset = '/HLTPhysics/Run2015D-v1'
    dataType = 'DIGI'
    useDAS = False
    readFiles.extend(['file:/afs/cern.ch/work/m/mzarucki/data/relVal_134.99901_RunHLTPhy2015D_step3.root'])

else:
    print 'Error: sample identifier ', sampleIdentifier, ' not defined.\n'
    errorUserOptions = True 
    runNumber = '0'
    dataset = 'None'
    dataType = 'None'
    useDAS = False
     
#            
# end of data samples 
#            

print "   Run number: ", runNumber
print "   Dataset: ", dataset
print "   Data type: ", dataType

if useDAS:
    import das_client
    import os

    # query DAS
    myQuery =  'file dataset=' + dataset + ' run=' + runNumber
    dasClientCommand = 'das_client.py --limit=0 --format=plain --query='+'"'+myQuery+'"'
    data = os.popen(dasClientCommand)
    filePaths = data.readlines()
            
       
    print '\n   das_client using the query'
    print '      ', myQuery
    print '   retrieved the following files\n'
        
    for line in filePaths :
        print '      ', line
           
    readFiles.extend(filePaths);
        
        
    # nothing added to secondary files by DAS 
    secFiles.extend([
            ])

        
# for RAW data, run first the RAWTODIGI 
if dataType == 'StreamFile':
    source = cms.Source("NewEventStreamFileReader", fileNames=readFiles)
else:               
    source = cms.Source ('PoolSource', 
                            fileNames=readFiles, 
                            secondaryFileNames=secFiles,
                            #lumisToProcess = selectedLumis,
                            #eventsToProcess = selectedEvents
                            )


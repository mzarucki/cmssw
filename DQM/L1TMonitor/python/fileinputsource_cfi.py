#
# provide online L1 Trigger DQM input from file(s)
#
# V M Ghete 2010-07-09

import FWCore.ParameterSet.Config as cms

###################### user choices ######################

# choose one sample identifier from the list of data samples 
#
sampleIdentifier = '265377_DAS' #'265377_DAS' # '263675' #'251251_relVal_runTheMatrix_step3' #'251251' #relVal_step3' #relVal_CMSSW_8_0_0_pre6' #'251251' '251131' '165633-CAFDQM' '195378'

maxNumberEvents = 5000

###################### end user choices ###################

# initialize list of files, of secondary files, list of selected events and luminosity segments
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
selectedEvents = cms.untracked.VEventRange()
selectedLumis= cms.untracked.VLuminosityBlockRange()


maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(maxNumberEvents)
)

if sampleIdentifier == '265377_DAS': #2016 MWGR2
    runNumber = '265377'
    dataset = '/Cosmics/Commissioning2016-v1/RAW'
    dataType = 'RAW'
    useDAS = True 

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

elif sampleIdentifier == '263675_DAS': #Global Tag: 76X_dataRun2_v15
    runNumber = '263675'
    dataset = '/Cosmics/HIRun2015-v1/RAW'
    dataType = 'RAW'
    useDAS = True

elif sampleIdentifier == '263675':
    runNumber = '263675'
    dataset = '/Cosmics/HIRun2015-v1/RAW'
    dataType = 'RAW'
    useDAS = False
    readFiles.extend(['file:/afs/cern.ch/work/m/mzarucki/data/HIRun2015_Cosmics_263675_RAW.root'])

elif sampleIdentifier == '251251_DAS': #Global Tag: auto:run2_hlt_Fake
    runNumber = '251251'
    dataset = '/HLTPhysics/Run2015B-v1/RAW'
    dataType = 'RAW'
    useDAS = True

elif sampleIdentifier == '251251_relVal_runTheMatrix_step3': #digi
    runNumber = '251251'
    dataset = '/HLTPhysics/Run2015B-v1'
    dataType = 'RAW'
    useDAS = False
    readFiles.extend(['file:/afs/cern.ch/work/m/mzarucki/data/relVal_HLT_251251_runTheMatrix.root'])

elif sampleIdentifier == '195378' :
    runNumber = '195378'
    dataset = '/MinimumBias/Run2012B-v1/RAW'
    dataType = 'RAW'
    useDAS = True
    selectedLumis= cms.untracked.VLuminosityBlockRange('195378:1275-195378:maxi')
           
elif sampleIdentifier == '195379' :
    runNumber = '195379'
    dataset = '/MinimumBias/Run2012B-v1/RAW'
    dataType = 'RAW'
    useDAS = True
           
elif sampleIdentifier == '195390' :
    runNumber = '195390'
    dataset = '/MinimumBias/Run2012B-v1/RAW'
    dataType = 'RAW'
    useDAS = True
           
# high PU run 2011   
elif sampleIdentifier == '179828' :
    runNumber = '179828'
    dataset =  '/ZeroBiasHPF0/Run2011B-v1/RAW'
    dataType = 'RAW'
    useDAS = True
        
        
elif sampleIdentifier == '165633-CAFDQM' :
    runNumber = '165633'
    dataset = '/ZeroBiasHPF0/Run2011B-v1/RAW'
    dataType = 'RAW'
    useDAS = False
    readFiles.extend( [ 
            'file:/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/DQMTest/MinimumBias__RAW__v1__165633__1CC420EE-B686-E011-A788-0030487CD6E8.root'
            ]);    
                                                                                                           
elif sampleIdentifier == 'FileStream_105760' :
    runNumber = '105760'
    dataset = 'A_Stream'
    dataType = 'FileStream'
    useDAS = False
    readFiles.extend( [
            'file:/lookarea_SM/MWGR_29.00105760.0001.A.storageManager.00.0000.dat'       
            ] );
                
else :
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

if useDAS :
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
if dataType == 'StreamFile' :
    source = cms.Source("NewEventStreamFileReader", fileNames=readFiles)
else :               
    source = cms.Source ('PoolSource', 
                            fileNames=readFiles, 
                            secondaryFileNames=secFiles,
                            lumisToProcess = selectedLumis,
                            eventsToProcess = selectedEvents
                            )


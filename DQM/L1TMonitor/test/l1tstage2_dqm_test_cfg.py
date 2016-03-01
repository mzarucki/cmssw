# l1tstage2_dqm_test.cfg 
# cfg file to test uGT DQM 
# Mateusz Zarucki 2016

import FWCore.ParameterSet.Config as cms
import sys

#-------------------------------------
#Event Source

# choose the environment you run
#l1DqmEnv = 'live' # live online DQM in P5
l1DqmEnv = 'file' # testing on lxplus

# for 'file' choose also the type of the global tag and (edit) the actual global tag

process = cms.Process("DQM")

# check that a valid choice for environment exists
if not (l1DqmEnv == 'live' or l1DqmEnv == 'file'):
    print 'No valid input source was chosen. Your value for l1DqmEnv input parameter is:'
    print 'l1DqmEnv = ', l1DqmEnv
    print 'Available options: "live", "file" '
    sys.exit()

if l1DqmEnv == 'live' :
    process.load("DQM.Integration.config.inputsource_cfi")
    process.EventStreamHttpReader.SelectEvents = cms.untracked.PSet(
            SelectEvents = cms.vstring("*"))
    process.EventStreamHttpReader.consumerName = 'L1T DQM Consumer'
    process.EventStreamHttpReader.maxEventRequestRate = cms.untracked.double(25.0)
elif l1DqmEnv == 'file' :
    process.load("DQM.L1TMonitor.fileinputsource_cfi")

#-------------------------------------
#DQM Environment

#process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("DQM.Integration.config.environment_cfi")
process.dqmEnv.subSystemFolder = 'L1T2016'
process.dqmSaver.tag = 'L1T2016'
    
if l1DqmEnv == 'live':
    #process.load("DQM.Integration.test.environment_cfi")
    process.DQMStore.referenceFileName = "/dqmdata/dqm/reference/l1t_reference.root" #references needed
    process.load("DQM.Integration.config.FrontierCondition_GT_cfi") # load and configure modules via Global Tag: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions
    es_prefer_GlobalTag = cms.ESPrefer('GlobalTag')
    process.GlobalTag.RefreshEachRun = cms.untracked.bool(True)
elif l1DqmEnv == 'file':
    process.load("DQM.L1TMonitor.environment_file_cff")
    from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag # as gtCustomise 
    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    process.load("DQM.Integration.config.FrontierCondition_GT_Offline_cfi")
    #process.GlobalTag = gtCustomise(process.GlobalTag, 'auto:run2_data_Fake', '')
    #process.GlobalTag.globaltag = cms.string('76X_dataRun2_v15') #'80X_dataRun2_v4'

#-------------------------------------
# L1 Trigger sequences

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")

# standard rawToDigi unpacking sequence
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.rawToDigiPath = cms.Path(process.RawToDigi)
process.RawToDigi.remove("siPixelDigis")
process.RawToDigi.remove("siStripDigis")
process.RawToDigi.remove("scalersRawToDigi")
process.RawToDigi.remove("castorDigis")

#process.load("DQM.L1TMonitor.L1TMonitor_cff")
process.load("DQM.L1TMonitor.L1TStage2_cff") 

#unpacking and monitor sequences
process.stage2UnpackPath = cms.Path(process.caloStage2Digis+process.gmtStage2Digis+process.gtStage2Digis)

#process.l1tMonitorPath = cms.Path(process.l1tMonitorOnline)
process.l1tMonitorPath = cms.Path(process.l1tStage2online)

process.dqmEndPath = cms.EndPath(process.dqmEnv * process.dqmSaver)

#process.output = cms.OutputModule(
#    "PoolOutputModule",
#    splitLevel = cms.untracked.int32(0),
#    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
#    outputCommands = cms.untracked.vstring('keep *',),
#    # outputCommands = cms.untracked.vstring('drop *',
#    #                                        'keep *_*_*_L1TEMULATION'),
#    fileName = cms.untracked.string('stage1_debug.root'),
#    dataset = cms.untracked.PSet(
#        filterName = cms.untracked.string(''),
#        dataTier = cms.untracked.string('')
#        )
#    )
#
#process.output_step = cms.EndPath(process.output)

process.schedule = cms.Schedule(process.rawToDigiPath,
                                process.stage2UnpackPath,
                                process.l1tMonitorPath,
                                process.dqmEndPath)
                                #process.output_step

#---------------------------------------------

# remove module(s) or system sequence from l1tMonitorPath

#process.l1tMonitorOnline.remove(process.l1tGt)

#process.l1tMonitorOnline.remove(process.l1tuGt)

#---------------------------------------------

# un-comment next lines in case you use the file for private tests using data from the L1T server
#process.dqmSaver.dirName = '.'
#process.dqmSaver.saveByRun = 1
#process.dqmSaver.saveAtJobEnd = True

## Message Logger
#process.load('FWCore.MessageService.MessageLogger_cfi')
#process.MessageLogger.debugModules = ['l1tGt'] #l1tuGT
#process.MessageLogger.categories.append('L1TGT') #L1TuGT
#process.MessageLogger.destinations = ['L1TDQM_errors','L1TDQM_warnings','L1TDQM_info','L1TDQM_debug']
#
#process.MessageLogger.L1TDQM_errors = cms.untracked.PSet(
#        threshold = cms.untracked.string('ERROR'),
#        ERROR = cms.untracked.PSet( limit = cms.untracked.int32(-1)))
#
#process.MessageLogger.L1TDQM_warnings = cms.untracked.PSet(
#        threshold = cms.untracked.string('WARNING'),
#        WARNING = cms.untracked.PSet( limit = cms.untracked.int32(0)),
#        ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0)))
#
#process.MessageLogger.L1TDQM_info = cms.untracked.PSet(
#        threshold = cms.untracked.string('INFO'),
#        INFO = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
#        WARNING = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
#        ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0) ),
#        L1TGT = cms.untracked.PSet( limit = cms.untracked.int32(-1))) #L1TuGT
#
#process.MessageLogger.L1TDQM_debug = cms.untracked.PSet(
#        threshold = cms.untracked.string('DEBUG'),
#        DEBUG = cms.untracked.PSet( limit = cms.untracked.int32(0)),
#        INFO = cms.untracked.PSet( limit = cms.untracked.int32(0)),
#        WARNING = cms.untracked.PSet( limit = cms.untracked.int32(0)),
#        ERROR = cms.untracked.PSet( limit = cms.untracked.int32(0)))

#Raw data input
process.gtDigis.DaqGtInputTag = cms.InputTag("rawDataCollector")
process.gtStage2Digis.InputLabel = cms.InputTag("rawDataCollector")

#process customisations
from DQM.Integration.config.online_customizations_cfi import *
process = customise(process)

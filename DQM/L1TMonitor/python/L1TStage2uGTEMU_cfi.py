import FWCore.ParameterSet.Config as cms

l1tStage2uGtEmu = cms.EDAnalyzer("L1TStage2uGT",
    l1tStage2uGtSource = cms.InputTag("simGtStage2Digis"),    
    monitorDir = cms.untracked.string("L1T2016EMU/L1TStage2uGTEMU"),
    verbose = cms.untracked.bool(False)
)

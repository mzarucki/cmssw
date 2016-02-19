import FWCore.ParameterSet.Config as cms

l1tuGt = cms.EDAnalyzer("L1TuGT",
    uGtSource = cms.InputTag("gtStage2Digis"),    
    runInEventLoop=cms.untracked.bool(False),
    runInEndLumi=cms.untracked.bool(True),
    verbose = cms.untracked.bool(False)
)

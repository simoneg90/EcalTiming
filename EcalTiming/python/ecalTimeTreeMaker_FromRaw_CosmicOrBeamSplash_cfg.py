import FWCore.ParameterSet.Config as cms

process = cms.Process("TIMECALIBANALYSIS")


process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
## Get Cosmic Reconstruction
process.load('Configuration/StandardSequences/ReconstructionCosmics_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')


## Raw to Digi
process.load('Configuration/StandardSequences/RawToDigi_Data_cff')

## HLT Filter Splash
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.spashesHltFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    throw = cms.bool(False),
    HLTPaths = ['HLT_EG20*', 'HLT_SplashEcalSumET', 'HLT_Calibration','HLT_EcalCalibration','HLT_HcalCalibration','HLT_Random','HLT_Physics','HLT_HcalNZS','HLT_SplashEcalSumET','HLTriggerFinalPath' ]
)


## Do you want to Pre-Scale
process.load("FWCore.Modules.preScaler_cfi")
process.preScaler.prescaleFactor = 1
## GlobalTag Conditions Related
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

## Process Digi To Raw Step
process.digiStep = cms.Sequence(process.ecalDigis  + process.ecalPreshowerDigis)

## Process Reco
#process.muonSequence = cms.Sequence(process.calolocalreco)
process.caloCosmics.remove(process.hbhereco)
process.caloCosmics.remove(process.hcalLocalRecoSequence)
process.caloCosmics.remove(process.hfreco)
process.caloCosmics.remove(process.horeco)
process.caloCosmics.remove(process.zdcreco)
process.caloCosmics.remove(process.ecalClusters)

process.caloCosmicOrSplashRECOSequence = cms.Sequence(process.caloCosmics )#+ process.egammaCosmics)


# Dump Some event Content
import FWCore.Modules.printContent_cfi
process.dumpEv = FWCore.Modules.printContent_cfi.printContent.clone()

### Print Out Some Messages
process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING')
    ),
    categories = cms.untracked.vstring('ecalTimeTree'),
    destinations = cms.untracked.vstring('cout')
)
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# enable the TrigReport and TimeReport
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
#    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

# dbs search --query "find file where dataset=/ExpressPhysics/BeamCommissioning09-Express-v2/FEVT and run=124020" | grep store | awk '{printf "\"%s\",\n", $1}'
# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
                            #  fileNames = cms.untracked.vstring('file:test_DIGI.root')
  fileNames = cms.untracked.vstring(
#        'file:/afs/cern.ch/work/e/emanuele/public/ecal/splashesEventsRaw.root'),
         #'/store/caf/user/ccecal/TPG/splashes_239754_5events_April2015_MinimumBias.root',),
         #'/store/caf/user/ccecal/TPG/splash_events_run_239895_26_events_beam_1.root',
         #'/store/caf/user/ccecal/TPG/splash_events_run_239895_31_events_beam_2.root'),
        '/store/data/Commissioning2015/MinimumBias/RAW/v1/000/243/479/00000/AE12BB31-0AF3-E411-977C-02163E0139CE.root'),
#        '/store/data/Commissioning2015/MinimumBias/RAW/v1/000/243/484/00000/6CF7FB5C-1EF3-E411-BD0E-02163E01390C.root'),
)

# process.source = cms.Source(
#     "PoolSource",
#     skipEvents = cms.untracked.uint32(0),
#     fileNames = cms.untracked.vstring(
#     #'file:MyCrab/50988619-41DE-E211-9F98-003048FFD770.root'
#     #'root://xrootd.unl.edu//store/data/Run2010B/Cosmics/RAW/v1/000/144/556/C8B5FCA9-F3B5-DF11-B28A-0030487CD16E.root'
#     #'file:Cosmic-Commissioning2014-Cosmics-RAW-v1-AC4963B3-54BE-E311-97F5-02163E00E6E3.root'
#     #'/store/data/Commissioning2015/Cosmics/RAW-RECO/CosmicSP-6Mar2015-v1/10000/248747E6-25CA-E411-B17C-02163E00BD75.root'
#     #'/store/data/Run2010B/Cosmics/RAW/v1/000/144/559/306A4ABD-F3B5-DF11-9CAD-003048F118C6.root'
#     '/store/data/Commissioning2015/Cosmics/RAW/v1/000/232/881/00000/26ADAFFB-3FAB-E411-A313-02163E011DDC.root'
#      ),               
#     # drop native rechits and clusters, to be sure only those locally made will be picked up
#     inputCommands = cms.untracked.vstring('keep *'
#                                           ,'drop EcalRecHitsSorted_*_*_RECO' # drop hfRecoEcalCandidate as remade in this process
#                                           , 'drop recoSuperClusters_*_*_RECO' # drop hfRecoEcalCandidate as remade in this process
#                                           , 'drop recoCaloClusters_*_*_RECO'
#                                           )


# Output definition
process.RECOoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RECOEventContent.outputCommands,
    fileName = cms.untracked.string('test_RECO.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('RECO')
    )
)


## Histogram files
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("/afs/cern.ch/user/s/shervin/public/4Carlotta/ecalCreateTimeCalibs-243479-v1.root"),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

## Dumpevent Event Contents
process.dumpEvContent = cms.EDAnalyzer("EventContentAnalyzer")

### NumBer of events
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))


### Process Full Path
process.p = cms.Path( #process.spashesHltFilter *
                     #+ process.preScaler 
                      process.digiStep 
                     #+ process.muonSequence 
                     + process.caloCosmicOrSplashRECOSequence 
                    )

process.endp = cms.EndPath(process.RECOoutput)

### Schedule ###
process.schedule = cms.Schedule(process.p, process.endp) 

process.looper = cms.Looper("EcalTimingCalibProducer",
                            maxLoop = cms.uint32(1),
                            isSplash = cms.bool(True),
                            makeEventPlots = cms.bool(True),
                            recHitEBCollection = cms.InputTag("ecalRecHit","EcalRecHitsEB"),
                            recHitEECollection = cms.InputTag("ecalRecHit","EcalRecHitsEE"),
                            recHitFlags = cms.vint32([0]), # only recHits with these flags are accepted for calibration
                            recHitMinimumN = cms.uint32(50000),
                            #recHitMinimumN = cms.uint32(2),
                            minRecHitEnergy = cms.double(1),
                            )

processDumpFile = open('processDump.py', 'w')
print >> processDumpFile, process.dumpPython()

import FWCore.ParameterSet.Config as cms
import os, sys, imp, re
import FWCore.ParameterSet.VarParsing as VarParsing

#sys.path(".")

#new options to make everything easier for batch

############################################################
### SETUP OPTIONS

options = VarParsing.VarParsing('standard')
options.register('jsonFile',
                 "",
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "path and name of the json file")
options.register('step',
                 "RECOTIMEANALYSIS",
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Do reco, time analysis or both, RECO|TIMEANALYSIS|RECOTIMEANALYSIS")
options.register('skipEvents',
                 0,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Skip this many events")
options.register('offset',
                 0.0,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.float,
                 "add this to each crystal time")
options.register('minEnergyEB',
                 1.5,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.float,
                 "add this to minimum energy threshold")
options.register('minEnergyEE',
                 3.0,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.float,
                 "add this to minimum energy threshold")
options.register('minChi2EB',
                 50.0,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.float,
                 "add this to minimum chi2 threshold")
options.register('minChi2EE',
                 50.0,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.float,
                 "add this to minimum chi2 threshold")
options.register('isSplash',
                 0,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "0=false, 1=true"
                 )
options.register('streamName',
                 'AlCaPhiSym',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "type of stream: AlCaPhiSym or AlCaP0")
options.register('globaltag',
                 '80X_dataRun2_Prompt_v8',#'80X_dataRun2_HLT_v12',#'80X_dataRun2_Prompt_v8',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Global tag to use, no default")
options.register('loneBunch',
                   0,
                   VarParsing.VarParsing.multiplicity.singleton,
                   VarParsing.VarParsing.varType.int,
                   "0=No, 1=Yes"
                 )
                 
### setup any defaults you want
options.output="output/ecalTiming.root"
options.secondaryOutput="ntuple.root"

if(options.streamName=="AlCaP0"): print "stream ",options.streamName #options.files = "/store/data/Commissioning2015/AlCaP0/RAW/v1/000/246/342/00000/048ECF48-F906-E511-95AC-02163E011909.root"
elif(options.streamName=="AlCaPhiSym"): print "stream ",options.streamName #options.files = "/store/data/Commissioning2015/AlCaPhiSym/RAW/v1/000/244/768/00000/A8219906-44FD-E411-8DA9-02163E0121C5.root"
else: 
    print "stream ",options.streamName," not foreseen"
    exit

#options.files = cms.untracked.vstring
#options.streamName = cms.untracked.vstring
options.maxEvents = -1 # -1 means all events
### get and parse the command line arguments
options.parseArguments()
print options

processname = options.step

doReco = True
doAnalysis = True
if "RECO" not in processname:
	doReco = False
if "TIME" not in processname:
	doAnalysis = False

process = cms.Process(processname)

# if the one file is a folder, grab all the files in it that are RECO
if len(options.files) == 1 and options.files[0][-1] == '/' and not doReco:
	from EcalTiming.EcalTiming.storeTools_cff import fillFromStore
	files = fillFromStore(options.files[0])
	options.files.pop()
	options.files = [ f for f in files if "RECO" in f and "numEvent" not in f]


process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10000)

process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

if(options.isSplash==1):
    ## Get Cosmic Reconstruction
    process.load('Configuration/StandardSequences/ReconstructionCosmics_cff')
    process.caloCosmics.remove(process.hbhereco)
    process.caloCosmics.remove(process.hcalLocalRecoSequence)
    process.caloCosmics.remove(process.hfreco)
    process.caloCosmics.remove(process.horeco)
    process.caloCosmics.remove(process.zdcreco)
    process.caloCosmics.remove(process.ecalClusters)
    process.caloCosmicOrSplashRECOSequence = cms.Sequence(process.caloCosmics )#+ process.egammaCosmics)
else:
    process.load('Configuration/StandardSequences/Reconstruction_cff')
    process.recoSequence = cms.Sequence(process.calolocalreco )#+ process.egammaCosmics)

process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('EcalTiming.EcalTiming.ecalLocalRecoSequenceAlCaStream_cff')
process.load('EcalTiming.EcalTiming.ecalLocalRecoSequenceAlCaP0Stream_cff')

if(options.streamName=="AlCaP0"):
    process.ecalMultiFitUncalibRecHit.EBdigiCollection = cms.InputTag("hltAlCaPi0EBRechitsToDigis","pi0EBDigis")
    process.ecalMultiFitUncalibRecHit.EEdigiCollection = cms.InputTag("hltAlCaPi0EERechitsToDigis","pi0EEDigis")
else:
    process.ecalMultiFitUncalibRecHit.EBdigiCollection = cms.InputTag("hltEcalPhiSymFilter","phiSymEcalDigisEB") 
    process.ecalMultiFitUncalibRecHit.EEdigiCollection = cms.InputTag("hltEcalPhiSymFilter","phiSymEcalDigisEE") 


## Raw to Digi
process.load('Configuration/StandardSequences/RawToDigi_Data_cff')

## HLT Filter Splash
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.spashesHltFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    throw = cms.bool(False),
    HLTPaths = ['HLT_EG20*', 'HLT_SplashEcalSumET', 'HLT_Calibration','HLT_EcalCalibration','HLT_HcalCalibration','HLT_Random','HLT_Physics','HLT_HcalNZS','HLT_SplashEcalSumET','HLTriggerFinalPath' ]
)

# GLOBAL-TAG
process.load("CondCore.CondDB.CondDB_cfi")
from CondCore.DBCommon.CondDBSetup_cfi import *
#from CondCore.CondDB.CondDB_cfi import *
#global tag to be used always
process.GlobalTag = cms.ESSource("PoolDBESSource",
                                 CondDBSetup, #CondDBSetup
                                 connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
                                 globaltag = cms.string(options.globaltag)
)

#global tag to be used for RERECO
#process.GlobalTag = cms.ESSource("PoolDBESSource",
#                                  CondDBSetup,
#                                  connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
#                                  globaltag = cms.string('80X_dataRun2_Prompt_v8'),
#                                  toGet = cms.VPSet(
#                                    cms.PSet(record = cms.string("EcalTimeCalibConstantsRcd"),
#                                    tag = cms.string("EcalIntercalibConstants_Cal_Jun2016_v1"),
#                                    connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_ECALCALIB/RunII-time/Cal_Jun2016/tags/sqlite/EcalIntercalibConstants_Cal_Jun2016_v1.db'),
#                                    )
#                                  ),
#)
#


##  This section is for grabbing the constants from a FrontierPrep for validation
#from CondCore.DBCommon.CondDBSetup_cfi import *
#
## rereco of for EOY
#process.GlobalTag = cms.ESSource("PoolDBESSource",
#		CondDBSetup,
#		connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
#		globaltag = cms.string(options.globaltag),
#		toGet = cms.VPSet(
#			cms.PSet(record = cms.string("EcalTimeCalibConstantsRcd"),
#				tag = cms.string("EcalTimeCalibConstants_v08_offline"),
#				connect = cms.untracked.string('frontier://FrontierPrep/CMS_CONDITIONS')
#				)
#			),
#		)
#
## Process Digi To Raw Step
process.digiStep = cms.Sequence(process.ecalDigis  + process.ecalPreshowerDigis)

## Process Reco



### Print Out Some Messages
#process.MessageLogger = cms.Service("MessageLogger",
#    cout = cms.untracked.PSet(
#        threshold = cms.untracked.string('WARNING')
#    ),
#    categories = cms.untracked.vstring('ecalTimeTree'),
#    destinations = cms.untracked.vstring('cout')
#)

# enable the TrigReport and TimeReport
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

SkipEvent = cms.untracked.vstring('ProductNotFound','EcalProblem')

# dbs search --query "find file where dataset=/ExpressPhysics/BeamCommissioning09-Express-v2/FEVT and run=124020" | grep store | awk '{printf "\"%s\",\n", $1}'
# Input source
print "source files:",options.files
process.source = cms.Source("PoolSource",
	secondaryFileNames = cms.untracked.vstring(),
	fileNames = cms.untracked.vstring(options.files),
	skipEvents = cms.untracked.uint32(options.skipEvents)
)

if(len(options.jsonFile) > 0):
	import FWCore.PythonUtilities.LumiList as LumiList
	process.source.lumisToProcess = LumiList.LumiList(filename = options.jsonFile).getVLuminosityBlockRange()



recofile = str(options.output)
recofile = recofile[:recofile.find(".root")] + "_RECO.root"
# Output definition
process.RECOoutput = cms.OutputModule("PoolOutputModule",
splitLevel = cms.untracked.int32(0),
eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
outputCommands = cms.untracked.vstring('drop *',"keep *_EcalTimingEvents_*_*"),
fileName = cms.untracked.string(recofile),
dataset = cms.untracked.PSet(
   filterName = cms.untracked.string(''),
   dataTier = cms.untracked.string('RECO')
)
)


if doAnalysis:
	## Histogram files
	process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string(options.output),
                                   closeFileFast = cms.untracked.bool(True)
                                   )

### NumBer of events
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

#DUMMY RECHIT
process.dummyHits = cms.EDProducer("DummyRechitDigis",
                                    doDigi = cms.untracked.bool(True),
                                    # rechits
                                    barrelHitProducer      = cms.InputTag('hltAlCaPi0EBUncalibrator','pi0EcalRecHitsEB' ,"HLT"),
                                    endcapHitProducer      = cms.InputTag('hltAlCaPi0EEUncalibrator','pi0EcalRecHitsEE' ,"HLT"),
                                    barrelRecHitCollection = cms.untracked.string("dummyBarrelRechitsPi0"),
                                    endcapRecHitCollection = cms.untracked.string("dummyEndcapRechitsPi0"),
                                    # digis
                                    barrelDigis            = cms.InputTag('hltAlCaPi0EBRechitsToDigis','pi0EBDigis',"HLT"),
                                    endcapDigis            = cms.InputTag('hltAlCaPi0EERechitsToDigisLowPU','pi0EEDigis',"HLT"), #changed hltAlCaPi0EERechitsToDigis in LowPU....changed in the file -.-
                                    barrelDigiCollection   = cms.untracked.string("dummyBarrelDigisPi0"),
                                    endcapDigiCollection   = cms.untracked.string("dummyEndcapDigisPi0"))

##ADDED
# TRIGGER RESULTS FILTER

process.StableParametersRcdSource = cms.ESSource( "EmptyESSource",
    iovIsRunNotTime = cms.bool( True ),
    recordName = cms.string( "L1TGlobalStableParametersRcd" ),
    firstValid = cms.vuint32( 1 )
)

process.GlobalParametersRcdSource = cms.ESSource( "EmptyESSource",
    iovIsRunNotTime = cms.bool( True ),
    recordName = cms.string( "L1TGlobalParametersRcd" ),
    firstValid = cms.vuint32( 1 )
)


process.StableParameters = cms.ESProducer( "StableParametersTrivialProducer",
   NumberL1IsoEG = cms.uint32( 4 ),
   NumberL1JetCounts = cms.uint32( 12 ),
   NumberPhysTriggersExtended = cms.uint32( 64 ),
   NumberTechnicalTriggers = cms.uint32( 64 ),
   NumberL1NoIsoEG = cms.uint32( 4 ),
   IfCaloEtaNumberBits = cms.uint32( 4 ),
   NumberL1CenJet = cms.uint32( 4 ),
   NumberL1TauJet = cms.uint32( 4 ),
   NumberL1Mu = cms.uint32( 4 ),
   NumberConditionChips = cms.uint32( 1 ),
   IfMuEtaNumberBits = cms.uint32( 6 ),
   NumberPsbBoards = cms.int32( 7 ),
   NumberPhysTriggers = cms.uint32( 512 ),
   PinsOnConditionChip = cms.uint32( 512 ),
   UnitLength = cms.int32( 8 ),
   NumberL1ForJet = cms.uint32( 4 ),
   WordLength = cms.int32( 64 ),
   OrderConditionChip = cms.vint32( 1 )
)

process.hltGtStage2ObjectMap = cms.EDProducer( "L1TGlobalProducer",
    L1DataBxInEvent = cms.int32( 5 ),
    JetInputTag = cms.InputTag( 'hltCaloStage2Digis','Jet' ),
    AlgorithmTriggersUnmasked = cms.bool( True ),
    EmulateBxInEvent = cms.int32( 1 ),
    ExtInputTag = cms.InputTag( "hltGtStage2Digis" ),
    AlgorithmTriggersUnprescaled = cms.bool( True ),
    Verbosity = cms.untracked.int32( 0 ),
    EtSumInputTag = cms.InputTag( 'hltCaloStage2Digis','EtSum' ),
    ProduceL1GtDaqRecord = cms.bool( True ),
    PrescaleSet = cms.uint32( 1 ),
    EGammaInputTag = cms.InputTag( 'hltCaloStage2Digis','EGamma' ),
    TriggerMenuLuminosity = cms.string( "startup" ),
    ProduceL1GtObjectMapRecord = cms.bool( True ),
    AlternativeNrBxBoardDaq = cms.uint32( 0 ),
    PrescaleCSVFile = cms.string( "prescale_L1TGlobal.csv" ),
    TauInputTag = cms.InputTag( 'hltCaloStage2Digis','Tau' ),
    BstLengthBytes = cms.int32( -1 ),
    MuonInputTag = cms.InputTag( 'hltGmtStage2Digis','Muon' )
)

process.triggerSelectionLoneBunch = cms.EDFilter( "HLTL1TSeed",
    L1SeedsLogicalExpression = cms.string( "L1_IsolatedBunch" ),
    L1EGammaInputTag = cms.InputTag( 'hltCaloStage2Digis','EGamma' ),
    L1JetInputTag = cms.InputTag( 'hltCaloStage2Digis','Jet' ),
    saveTags = cms.bool( True ),
    L1ObjectMapInputTag = cms.InputTag( "hltGtStage2ObjectMap" ),
    L1EtSumInputTag = cms.InputTag( 'hltCaloStage2Digis','EtSum' ),
    L1TauInputTag = cms.InputTag( 'hltCaloStage2Digis','Tau' ),
    L1MuonInputTag = cms.InputTag( 'hltGmtStage2Digis','Muon' ),
    L1GlobalInputTag = cms.InputTag( "hltGtStage2Digis" )
)




#process.triggerSelectionLoneBunch = cms.EDFilter( "TriggerResultsFilter",
#                                                   triggerConditions = cms.vstring('L1_IsolatedBunch'),#'L1_AlwaysTrue', 'L1_IsolatedBunch'),
#                                                   hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
#                                                   l1tResults = cms.InputTag( "hltGtStage2Digis" ),
#                                                   l1tIgnoreMask = cms.bool( False ),
#                                                   l1techIgnorePrescales = cms.bool( False ),
#                                                   daqPartitions = cms.uint32( 1 ),
#                                                   throw = cms.bool( True )
#                                                   )
#
process.filter=cms.Sequence()
if(options.isSplash==1):
    process.filter+=process.spashesHltFilter
    process.reco_step = cms.Sequence(process.caloCosmicOrSplashRECOSequence)
else:
    if(options.streamName=="AlCaP0"):
      if(options.loneBunch==1):
        process.filter+=process.triggerSelectionLoneBunch
      import RecoLocalCalo.EcalRecProducers.ecalMultiFitUncalibRecHit_cfi
      process.ecalMultiFitUncalibRecHit =  RecoLocalCalo.EcalRecProducers.ecalMultiFitUncalibRecHit_cfi.ecalMultiFitUncalibRecHit.clone()
      process.ecalMultiFitUncalibRecHit.EBdigiCollection = cms.InputTag('dummyHits','dummyBarrelDigisPi0')#,'piZeroAnalysis')
      process.ecalMultiFitUncalibRecHit.EEdigiCollection = cms.InputTag('dummyHits','dummyEndcapDigisPi0')#,'piZeroAnalysis')

      #UNCALIB to CALIB
      from RecoLocalCalo.EcalRecProducers.ecalRecHit_cfi import *
      process.ecalDetIdToBeRecovered =  RecoLocalCalo.EcalRecProducers.ecalDetIdToBeRecovered_cfi.ecalDetIdToBeRecovered.clone()
      process.ecalRecHit.killDeadChannels = cms.bool( False )
      process.ecalRecHit.recoverEBVFE = cms.bool( False )
      process.ecalRecHit.recoverEEVFE = cms.bool( False )
      process.ecalRecHit.recoverEBFE = cms.bool( False )
      process.ecalRecHit.recoverEEFE = cms.bool( False )
      process.ecalRecHit.recoverEEIsolatedChannels = cms.bool( False )
      process.ecalRecHit.recoverEBIsolatedChannels = cms.bool( False )

      process.reco_step = cms.Sequence(process.dummyHits
                                      * process.ecalMultiFitUncalibRecHit
                                      * process.ecalRecHit)
    else:
      #process.reco_step = cms.Sequence(process.reconstruction_step_multiFit)
      if(options.loneBunch==1):
        #process.filter+=process.triggerSelectionLoneBunch
        process.filter*=process.hltGtStage2ObjectMap
        process.filter*=process.triggerSelectionLoneBunch
        process.filter*=process.bunchSpacingProducer
      process.reco_step = cms.Sequence(process.ecalLocalRecoSequenceAlCaStream)
      

### Process Full Path
if(options.isSplash==0):
    process.digiStep = cms.Sequence()



evtPlots = True if options.isSplash else False
#evtPlots= True

#import Electronics mapping
process.load("Geometry.EcalCommonData.EcalOnly_cfi")
process.load("Geometry.EcalMapping.EcalMapping_cfi")
process.load("Geometry.EcalMapping.EcalMappingRecord_cfi")


if doAnalysis:
	process.load('EcalTiming.EcalTiming.ecalTimingCalibProducer_cfi')
	process.timing.timingCollection = cms.InputTag("EcalTimingEvents")
	process.timing.isSplash= cms.bool(True if options.isSplash else False)
	process.timing.makeEventPlots=evtPlots
	process.timing.globalOffset = cms.double(options.offset)
	process.timing.outputDumpFile = process.TFileService.fileName
	process.timing.energyThresholdOffsetEB = cms.double(options.minEnergyEB)
	process.timing.energyThresholdOffsetEE = cms.double(options.minEnergyEE)
	process.timing.storeEvents = cms.bool(True)
	process.analysis = cms.Sequence( process.timing )

process.load('EcalTiming.EcalTiming.EcalTimingSequence_cff')
if doReco:
	process.reco = cms.Sequence( (process.filter 
                      + process.digiStep 
                      + process.reco_step)
                      * process.EcalTimingEventSeq
                      )


process.seq = cms.Sequence()
if doReco:
	process.seq += process.reco
if doAnalysis:
	process.seq += process.analysis
else:
	process.endp = cms.EndPath(process.RECOoutput)

process.p = cms.Path(process.seq)
from datetime import datetime
processDumpFilename = "processDump" + datetime.now().strftime("%M%S%f") + ".py"
processDumpFile = open(processDumpFilename, 'w')
print >> processDumpFile, process.dumpPython()

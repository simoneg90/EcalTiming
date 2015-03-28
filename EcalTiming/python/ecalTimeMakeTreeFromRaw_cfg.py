import FWCore.ParameterSet.Config as cms

process = cms.Process("TIMECALIBANALYSIS")

# gfworks: to get clustering 
process.load('Configuration/StandardSequences/GeometryExtended_cff')
<<<<<<< HEAD
=======

>>>>>>> 7c2e18aec70ab1bee9e87695373770b7b56496b3
# Geometry goodies
process.load("Geometry.CaloEventSetup.CaloGeometry_cff")
process.load("Geometry.CaloEventSetup.CaloGeometry_cfi")
process.load("Geometry.CaloEventSetup.CaloTopology_cfi")
process.load("Geometry.CaloEventSetup.EcalTrigTowerConstituents_cfi")
process.load("Geometry.CMSCommonData.cmsIdealGeometryXML_cfi")  
process.load("Geometry.EcalMapping.EcalMapping_cfi")
process.load("Geometry.EcalMapping.EcalMappingRecord_cfi")

## RAWToDiGI goodies
process.load("RecoLocalCalo.EcalRecProducers.ecalGlobalUncalibRecHit_cfi")
process.load("RecoLocalCalo.EcalRecProducers.ecalDetIdToBeRecovered_cfi")
process.load("RecoLocalCalo.EcalRecProducers.ecalRecHit_cfi")
process.load("RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi")
process.load("CalibCalorimetry.EcalLaserCorrection.ecalLaserCorrectionService_cfi")
process.load("RecoEcal.EgammaClusterProducers.ecalClusteringSequence_cff")
process.load("SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_cfi")
process.load("L1Trigger.Configuration.L1RawToDigi_cff")
process.load("RecoEcal.EgammaCoreTools.EcalNextToDeadChannelESProducer_cff")
process.load("RecoEcal.EgammaClusterProducers.reducedRecHitsSequence_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
#process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
#process.load("RecoLocalCalo.EcalRecProducers.ecalRatioUncalibRecHit_cfi")
process.load("RecoLocalCalo.Configuration.ecalLocalRecoSequence_cff")

# unpacking
process.load("EventFilter.EcalRawToDigi.EcalUnpackerMapping_cfi")
process.load("EventFilter.EcalRawToDigi.EcalUnpackerData_cfi")

## RAWToDiGI goodies
#process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load("RecoLocalCalo.EcalRecProducers.ecalGlobalUncalibRecHit_cfi")
process.load("RecoLocalCalo.EcalRecProducers.ecalDetIdToBeRecovered_cfi")
process.load("RecoLocalCalo.EcalRecProducers.ecalRecHit_cfi")
process.load("RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi")
process.load("CalibCalorimetry.EcalLaserCorrection.ecalLaserCorrectionService_cfi")
process.load("RecoEcal.EgammaClusterProducers.ecalClusteringSequence_cff")
process.load("SimCalorimetry.EcalTrigPrimProducers.ecalTriggerPrimitiveDigis_cfi")
process.load("L1Trigger.Configuration.L1RawToDigi_cff")
process.load("RecoLocalCalo.Configuration.ecalLocalRecoSequence_cff")

## Making Clusters from Digi
process.load('RecoEcal.Configuration.RecoEcal_cff')
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("RecoEcal.EgammaCoreTools.EcalNextToDeadChannelESProducer_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
# Make basic- and super- clustering sequences 
import RecoEcal.EgammaClusterProducers.multi5x5ClusteringSequence_cff
import RecoEcal.EgammaClusterProducers.hybridClusteringSequence_cff

## GlobalTag Conditions Related
process.load("FWCore.Modules.preScaler_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
# Global Tag
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_noesprefer_cff")
#process.GlobalTag.globaltag = 'CRAFT_ALL_V12::All'
#process.GlobalTag.globaltag = 'GR_R_35X_V8A::All'
#process.GlobalTag.globaltag = 'GR_R_42_V2::All'
#process.GlobalTag.globaltag = 'GR_P_V22::All'
#process.GlobalTag.globaltag = 'GR_P_V27::All'
#process.GlobalTag.globaltag = 'GR_P_V42::All'
#process.GlobalTag.globaltag = 'GR_R_72_V2::All'

# Get the Most Recent Global Tag
process.GlobalTag = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        enableReadOnlySessionOnUpdateConnection = cms.untracked.bool(False),
        idleConnectionCleanupPeriod = cms.untracked.int32(10),
        messageLevel = cms.untracked.int32(0),
        enablePoolAutomaticCleanUp = cms.untracked.bool(False),
        enableConnectionSharing = cms.untracked.bool(True),
        connectionRetrialTimeOut = cms.untracked.int32(60),
        connectionTimeOut = cms.untracked.int32(60),
        authenticationSystem = cms.untracked.int32(0),
        connectionRetrialPeriod = cms.untracked.int32(10)
    ),
    BlobStreamerName = cms.untracked.string('TBufferBlobStreamingService'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('EcalDQMChannelStatusRcd'),
        tag = cms.string('EcalDQMChannelStatus_v1_hlt'),
        connect = cms.untracked.string('frontier://FrontierProd/CMS_COND_34X_ECAL')
    ), 
        cms.PSet(
            record = cms.string('EcalDQMTowerStatusRcd'),
            tag = cms.string('EcalDQMTowerStatus_v1_hlt'),
            connect = cms.untracked.string('frontier://FrontierProd/CMS_COND_34X_ECAL')
        )),
    connect = cms.string('frontier://FrontierProd/CMS_COND_31X_GLOBALTAG'),
    globaltag = cms.string('GR_R_72_V2::All')
 )
# No Idea Why it is here!!
process.load("Geometry.CommonDetUnit.globalTrackingGeometry_cfi") 
process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi") 
process.load("Configuration.StandardSequences.MagneticField_38T_cff")


# Make basic- and super- clustering sequences 
import RecoEcal.EgammaClusterProducers.multi5x5ClusteringSequence_cff

#process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")


# L1 Triggers?
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerScalesConfig_cff")
process.load("L1TriggerConfig.L1ScalesProducers.L1MuTriggerPtScaleConfig_cff")
process.load("L1TriggerConfig.L1GtConfigProducers.L1GtBoardMapsConfig_cff")
process.load("L1TriggerConfig.L1GtConfigProducers.L1GtConfig_cff")
process.load("L1TriggerConfig.L1GtConfigProducers.Luminosity.startup.L1Menu_startup2_v2_Unprescaled_cff")

# Dump Some event Content
import FWCore.Modules.printContent_cfi
process.dumpEv = FWCore.Modules.printContent_cfi.printContent.clone()

## Filter Based on Level1 Trigger/ Can Add Dima's Trigger for BeamSplash here!
import EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi
process.gtDigis = EventFilter.L1GlobalTriggerRawToDigi.l1GtUnpack_cfi.l1GtUnpack.clone()

## Do you want to Do Amplitude Dependent Corrrections?
process.ecalGlobalUncalibRecHit.doEBtimeCorrection = cms.bool(False) ## True if running on CMSSW_4XY
process.ecalGlobalUncalibRecHit.doEEtimeCorrection = cms.bool(False) ## True if running on CMSSW_4XY


#process.ecalLocalRecoSequence = cms.Sequence(process.ecalRatioUncalibRecHit*process.ecalDetIdToBeRecovered*process.ecalRecHit+process.ecalPreshowerRecHit)
#process.ecalLocalRecoSequence = cms.Sequence(process.ecalGlobalUncalibRecHit*process.ecalDetIdToBeRecovered*process.ecalRecHit+process.ecalPreshowerRecHit)
#process.ecalRecHit.EEuncalibRecHitCollection = cms.InputTag("ecalGlobalUncalibRecHit","EcalUncalibRecHitsEE")
#process.ecalRecHit.EBuncalibRecHitCollection = cms.InputTag("ecalGlobalUncalibRecHit","EcalUncalibRecHitsEB")
#process.ecalRecHit.EEuncalibRecHitCollection = cms.InputTag("ecalRatioUncalibRecHit","EcalUncalibRecHitsEE")
#process.ecalRecHit.EBuncalibRecHitCollection = cms.InputTag("ecalRatioUncalibRecHit","EcalUncalibRecHitsEB")



# 3x3 clustering for barrel
#process.multi5x5BasicClustersTimePi0Barrel =  RecoEcal.EgammaClusterProducers.multi5x5BasicClusters_cfi.multi5x5BasicClusters.clone(
#    # which regions should be clusterized
#    doEndcap = cms.bool(False),
#    doBarrel = cms.bool(True),
#
#    # gfwork: this is standard, can go away 
#    barrelHitProducer = cms.string('ecalRecHit'),
#    barrelHitCollection = cms.string('EcalRecHitsEB'),
#    endcapHitProducer = cms.string('ecalRecHit'),
#    endcapHitCollection = cms.string('EcalRecHitsEE'),
#    
#    IslandBarrelSeedThr = cms.double(0.5),   # barrelSeedThreshold
#    IslandEndcapSeedThr = cms.double(1.0),   # endcapSeedThreshold
#
#    barrelClusterCollection = cms.string('multi5x5BarrelBasicClusters'),
#    endcapClusterCollection = cms.string('multi5x5EndcapBasicClusters'),
#    clustershapecollectionEE = cms.string('multi5x5EndcapShape'),
#    clustershapecollectionEB = cms.string('multi5x5BarrelShape'),
#    barrelShapeAssociation = cms.string('multi5x5BarrelShapeAssoc'),
#    endcapShapeAssociation = cms.string('multi5x5EndcapShapeAssoc'),
#    )


# 3x3 clustering for endcap
#process.multi5x5BasicClustersTimePi0Endcap =  RecoEcal.EgammaClusterProducers.multi5x5BasicClusters_cfi.multi5x5BasicClusters.clone(
#    # which regions should be clusterized
#    doEndcap = cms.bool(True),
#    doBarrel = cms.bool(False),
#
#    barrelHitProducer = cms.string('ecalRecHit'),
#    barrelHitCollection = cms.string('EcalRecHitsEB'),
#    endcapHitProducer = cms.string('ecalRecHit'),
#    endcapHitCollection = cms.string('EcalRecHitsEE'),
#    
#    IslandBarrelSeedThr = cms.double(0.5),              # endcapSeedThreshold
#    IslandEndcapSeedThr = cms.double(1.0),             # barrelSeedThreshold
#
#    barrelClusterCollection = cms.string('multi5x5BarrelBasicClusters'),
#    endcapClusterCollection = cms.string('multi5x5EndcapBasicClusters'),
#    clustershapecollectionEE = cms.string('multi5x5EndcapShape'),
#    clustershapecollectionEB = cms.string('multi5x5BarrelShape'),
#    barrelShapeAssociation = cms.string('multi5x5BarrelShapeAssoc'),
#    endcapShapeAssociation = cms.string('multi5x5EndcapShapeAssoc'),
#    )


## super clustering for the ECAL BARREL, staring from multi5x5 3x3 clusters
#process.multi5x5SuperClustersTimePi0Barrel =  RecoEcal.EgammaClusterProducers.multi5x5SuperClusters_cfi.multi5x5SuperClusters.clone(
#    doBarrel = cms.bool(True),
#    doEndcaps = cms.bool(False),
#    barrelClusterProducer = cms.string('multi5x5BasicClustersTimePi0Barrel'),
#    barrelClusterCollection = cms.string('multi5x5BarrelBasicClusters'),
#    endcapClusterProducer = cms.string('multi5x5BasicClustersTimePi0Endcap'),
#    endcapClusterCollection = cms.string('multi5x5EndcapBasicClusters')
# )


## super clustering for the ECAL ENDCAP, staring from multi5x5 3x3 clusters
#process.multi5x5SuperClustersTimePi0Endcap =  RecoEcal.EgammaClusterProducers.multi5x5SuperClusters_cfi.multi5x5SuperClusters.clone(
#    doBarrel = cms.bool(False),
#    doEndcaps = cms.bool(True),
#    barrelClusterProducer = cms.string('multi5x5BasicClustersTimePi0Barrel'),
#    barrelClusterCollection = cms.string('multi5x5BarrelBasicClusters'),
#    endcapClusterProducer = cms.string('multi5x5BasicClustersTimePi0Endcap'),
#    endcapClusterCollection = cms.string('multi5x5EndcapBasicClusters')
# )

## Make Digis From RAW
process.ecalDigis = cms.EDProducer("EcalRawToDigi",
    tccUnpacking = cms.bool(True),
    FedLabel = cms.InputTag("listfeds"),
    srpUnpacking = cms.bool(True),
    syncCheck = cms.bool(True),
    feIdCheck = cms.bool(True),
    silentMode = cms.untracked.bool(True),
    InputLabel = cms.InputTag("rawDataCollector"),
    orderedFedList = cms.vint32(601, 602, 603, 604, 605, 
        606, 607, 608, 609, 610, 
        611, 612, 613, 614, 615, 
        616, 617, 618, 619, 620, 
        621, 622, 623, 624, 625, 
        626, 627, 628, 629, 630, 
        631, 632, 633, 634, 635, 
        636, 637, 638, 639, 640, 
        641, 642, 643, 644, 645, 
        646, 647, 648, 649, 650, 
        651, 652, 653, 654),
    eventPut = cms.bool(True),
    numbTriggerTSamples = cms.int32(1),
    numbXtalTSamples = cms.int32(10),
    orderedDCCIdList = cms.vint32(1, 2, 3, 4, 5, 
        6, 7, 8, 9, 10, 
        11, 12, 13, 14, 15, 
        16, 17, 18, 19, 20, 
        21, 22, 23, 24, 25, 
        26, 27, 28, 29, 30, 
        31, 32, 33, 34, 35, 
        36, 37, 38, 39, 40, 
        41, 42, 43, 44, 45, 
        46, 47, 48, 49, 50, 
        51, 52, 53, 54),
    FEDs = cms.vint32(601, 602, 603, 604, 605, 
        606, 607, 608, 609, 610, 
        611, 612, 613, 614, 615, 
        616, 617, 618, 619, 620, 
        621, 622, 623, 624, 625, 
        626, 627, 628, 629, 630, 
        631, 632, 633, 634, 635, 
        636, 637, 638, 639, 640, 
        641, 642, 643, 644, 645, 
        646, 647, 648, 649, 650, 
        651, 652, 653, 654),
    DoRegional = cms.bool(False),
    feUnpacking = cms.bool(True),
    forceToKeepFRData = cms.bool(False),
    headerUnpacking = cms.bool(True),
    memUnpacking = cms.bool(True)
)

## Do you want to Pre-Scale
process.preScaler.prescaleFactor = 1
## Digis & RecHits
process.simEcalTriggerPrimitiveDigis.InstanceEB = "ebDigis"
process.simEcalTriggerPrimitiveDigis.InstanceEE = "eeDigis"
process.simEcalTriggerPrimitiveDigis.Label = "ecalDigis"

process.reducedEcalRecHitsEE.interestingDetIdCollections = [cms.InputTag("interestingEcalDetIdEE")]
process.reducedEcalRecHitsEB.interestingDetIdCollections = [cms.InputTag("interestingEcalDetIdEB")]

process.ecalRecHit.EEuncalibRecHitCollection = "ecalGlobalUncalibRecHit:EcalUncalibRecHitsEE"
process.ecalRecHit.EBuncalibRecHitCollection = "ecalGlobalUncalibRecHit:EcalUncalibRecHitsEB"

# get uncalibrechits with ratio method
import RecoLocalCalo.EcalRecProducers.ecalGlobalUncalibRecHit_cfi
process.ecalUncalibHitGlobal = RecoLocalCalo.EcalRecProducers.ecalGlobalUncalibRecHit_cfi.ecalGlobalUncalibRecHit.clone()
process.ecalUncalibHitGlobal.EBdigiCollection = 'ecalEBunpacker:ebDigis'
process.ecalUncalibHitGlobal.EEdigiCollection = 'ecalEBunpacker:eeDigis'

## Get Rechits e.g From Weights
process.load("CalibCalorimetry.EcalLaserCorrection.ecalLaserCorrectionService_cfi")
process.load("RecoLocalCalo.EcalRecProducers.ecalRecHit_cfi")
process.ecalRecHit.EEuncalibRecHitCollection = "ecalGlobalUncalibRecHit:EcalUncalibRecHitsEE"
process.ecalRecHit.EBuncalibRecHitCollection = "ecalGlobalUncalibRecHit:EcalUncalibRecHitsEB"


## Get Reduce Ecal Rechits
process.load("RecoEcal.EgammaClusterProducers.reducedRecHitsSequence_cff")
process.reducedEcalRecHitsEE.interestingDetIdCollections = [cms.InputTag("interestingEcalDetIdEE")]
process.reducedEcalRecHitsEB.interestingDetIdCollections = [cms.InputTag("interestingEcalDetIdEB")]

#  Producer Of Ntuple
process.load("CalibCalorimetry.EcalTiming.ecalTimeTree_cfi")
process.ecalTimeTree.fileName ='EcalTimeTree'
process.ecalTimeTree.muonCollection = cms.InputTag("muons")
process.ecalTimeTree.runNum = 144980
# gfworks: replathese names
#process.ecalTimeTree.barrelClusterShapeAssociationCollection = cms.InputTag("multi5x5BasicClustersTimePi0Barrel","multi5x5BarrelShapeAssoc")
#process.ecalTimeTree.endcapClusterShapeAssociationCollection = cms.InputTag("multi5x5BasicClustersTimePi0Endcap","multi5x5EndcapShapeAssoc") 
# use full rechit collection, while from AOD reducedEcalRecHitsEx collections are assumed

process.ecalTimeTree.barrelEcalUncalibratedRecHitCollection = "ecalGlobalUncalibRecHit:EcalUncalibRecHitsEB"
process.ecalTimeTree.endcapEcalUncalibratedRecHitCollection = "ecalGlobalUncalibRecHit:EcalUncalibRecHitsEE"
#process.ecalTimeTree.barrelEcalRecHitCollection = cms.InputTag("ecalRecHit","EcalRecHitsEB")
#process.ecalTimeTree.endcapEcalRecHitCollection = cms.InputTag("ecalRecHit","EcalRecHitsEE")
process.ecalTimeTree.barrelEcalRecHitCollection = cms.InputTag("reducedEcalRecHitsEB","")
process.ecalTimeTree.endcapEcalRecHitCollection = cms.InputTag("reducedEcalRecHitsEE","")
process.ecalTimeTree.barrelBasicClusterCollection  = "hybridSuperClusters:hybridBarrelBasicClusters"
process.ecalTimeTree.endcapBasicClusterCollection  = "multi5x5SuperClusters:multi5x5EndcapBasicClusters"
process.ecalTimeTree.barrelSuperClusterCollection  = "correctedHybridSuperClusters"
process.ecalTimeTree.endcapSuperClusterCollection  = "multi5x5SuperClusters:multi5x5EndcapSuperClusters"

## Use Rechits from ecalGlobalUnCalibRecHit
#process.ecalTimeTree.barrelEcalRecHitCollection = cms.InputTag("ecalRecHit","EcalRecHitsEB")
#process.ecalTimeTree.endcapEcalRecHitCollection = cms.InputTag("ecalRecHit","EcalRecHitsEE")

## Use reduceEcalRechHits
process.ecalTimeTree.barrelEcalRecHitCollection = cms.InputTag("reducedEcalRecHitsEB","")
process.ecalTimeTree.endcapEcalRecHitCollection = cms.InputTag("reducedEcalRecHitsEE","")
### Use Made Basic Clusters
process.ecalTimeTree.barrelBasicClusterCollection  = cms.InputTag("hybridSuperClusters","hybridBarrelBasicClusters")
process.ecalTimeTree.endcapBasicClusterCollection  = cms.InputTag("multi5x5SuperClusters","multi5x5EndcapBasicClusters")
## Use Made SuperClusters
process.ecalTimeTree.barrelSuperClusterCollection  = cms.InputTag("correctedHybridSuperClusters","")
#process.ecalTimeTree.endcapSuperClusterCollection = cms.InputTag("correctedMulti5x5SuperClustersWithPreshower","")
process.ecalTimeTree.endcapSuperClusterCollection  = cms.InputTag("multi5x5SuperClusters","multi5x5EndcapSuperClusters")


process.load("RecoVertex.Configuration.RecoVertex_cff")


process.dumpEvContent = cms.EDAnalyzer("EventContentAnalyzer")
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

import RecoEcal.Configuration.RecoEcal_cff

### Sequences ###
## DRaw to Digi
process.ecalPreRecoSequence = cms.Sequence(process.ecalDigis)

## HybridClustering
process.hybridClusteringSequence = cms.Sequence(process.cleanedHybridSuperClusters+process.uncleanedHybridSuperClusters+process.hybridSuperClusters+process.correctedHybridSuperClusters+process.uncleanedOnlyCorrectedHybridSuperClusters)
## 5x5 clustering
process.multi5x5ClusteringSequence = cms.Sequence(process.multi5x5BasicClustersCleaned+process.multi5x5SuperClustersCleaned+process.multi5x5BasicClustersUncleaned+process.multi5x5SuperClustersUncleaned+process.multi5x5SuperClusters)
## Reco sequence
process.ecalRecoSequence = cms.Sequence((process.ecalGlobalUncalibRecHit+process.ecalDetIdToBeRecovered+process.ecalRecHit)+(process.simEcalTriggerPrimitiveDigis+process.gtDigis)+(process.hybridClusteringSequence+process.multi5x5ClusteringSequence)+(process.interestingEcalDetIdEB+process.interestingEcalDetIdEE+process.reducedEcalRecHitsEB+process.reducedEcalRecHitsEE))
## Unpack Raw to Digi
process.ecalPreRecoSequence = cms.Sequence(process.ecalEBunpacker
                                           + process.ecalDigis
                                          )

## HybridClustering
process.hybridClusteringSequence = cms.Sequence(process.cleanedHybridSuperClusters
                                                + process.uncleanedHybridSuperClusters
                                                + process.hybridSuperClusters
                                                + process.correctedHybridSuperClusters
                                                + process.uncleanedOnlyCorrectedHybridSuperClusters
                                               )
## 5x5 clustering
process.multi5x5ClusteringSequence = cms.Sequence(process.multi5x5BasicClustersCleaned
                                                 + process.multi5x5SuperClustersCleaned
                                                 + process.multi5x5BasicClustersUncleaned
                                                 + process.multi5x5SuperClustersUncleaned
                                                 + process.multi5x5SuperClusters
                                                 + process.multi5x5SuperClustersWithPreshower
                                                 )
## Reco sequence
process.ecalRecoSequence = cms.Sequence((process.ecalGlobalUncalibRecHit
                                         + process.ecalDetIdToBeRecovered
                                         + process.ecalRecHit)
                                       + (process.simEcalTriggerPrimitiveDigis
                                          + process.gtDigis)
                                       + (process.hybridClusteringSequence
                                          + process.multi5x5ClusteringSequence)
                                       + (process.interestingEcalDetIdEB
                                          + process.interestingEcalDetIdEE
                                          + process.reducedEcalRecHitsEB
                                          + process.reducedEcalRecHitsEE)
                                       )



### Process PATH
process.p = cms.Path(process.preScaler + process.ecalPreRecoSequence + process.ecalRecoSequence + process.ecalTimeTree)
process.p = cms.Path(process.preScaler 
                     + process.ecalPreRecoSequence 
                     + process.ecalRecoSequence 
                     + process.ecalTimeTree
                    )

### Potentiall Future Collision Reco Process
## Make tracks
##process.maketracks = cms.Sequence((process.gtEvmDigis)+(process.siPixelDigis) +(process.siStripDigis)+ (process.offlineBeamSpot) +(process.trackerlocalreco) +(process.recopixelvertexing) +(process.ckftracks))
### Make PreShower digis
##process.makeESDigis = cms.Sequence(process.ecalPreshowerDigis)
### Make Vertices 
##process.makeVertex = cms.Sequence(process.vertexreco) 

### Potential Process Path
##process.p = cms.Path(
#                     process.preScaler + 
#		     process.ecalPreRecoSequence + 
#		     process.maketracks + 
#		     process.makeESDigis + 
#		     process.ecalRecoSequence +
#		     process.makeVertex +
#		     process.process.ecalTimeTree
#		     )
## Old Process
#process.p = cms.Path(
#    process.ecalDigis *
#    process.gctDigis *
#    process.gtDigis *
#    process.gtEvmDigis *
#    process.siPixelDigis *
#    process.siStripDigis *
#    process.offlineBeamSpot *
#    process.trackerlocalreco *
#    process.recopixelvertexing *
#    process.ckftracks *
#    process.ecalPreshowerDigis *
#    process.ecalLocalRecoSequence *
#    process.ecalClusters *
#    process.vertexreco *
#    #process.dumpEvContent  *
#    process.ecalTimeTree
#  )


### Print Out Some Messages
process.MessageLogger = cms.Service("MessageLogger",
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('WARNING')
    ),
    categories = cms.untracked.vstring('ecalTimeTree'),
    destinations = cms.untracked.vstring('cout')
)
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# enable the TrigReport and TimeReport
process.options = cms.untracked.PSet(
    SkipEvent = cms.untracked.vstring('ProductNotFound')
)

# GF: some legacy reco files to test; replace w/ collision data
# dbs search --query "find file where dataset=/ExpressPhysics/BeamCommissioning09-Express-v2/FEVT and run=124020" | grep store | awk '{printf "\"%s\",\n", $1}'
process.source = cms.Source(
    "PoolSource",
    skipEvents = cms.untracked.uint32(0),
    
    fileNames = cms.untracked.vstring(
    #'file:/data/franzoni/data/423_Run2011A-SingleMu-RAW-RECO-WMu-May10ReReco-v1-0000-02367CF3-DB7B-E011-8E9D-0019BB32F1EE.root'
    #'file:MyCrab/50988619-41DE-E211-9F98-003048FFD770.root'
    #'root://xrootd.unl.edu//store/data/Run2010B/Cosmics/RAW/v1/000/144/556/C8B5FCA9-F3B5-DF11-B28A-0030487CD16E.root'
    'file:Cosmic-Commissioning2014-Cosmics-RAW-v1-AC4963B3-54BE-E311-97F5-02163E00E6E3.root'
    #'file:Cosmic-Commissioning2014-Cosmics-RAW-v1-AC4963B3-54BE-E311-97F5-02163E00E6E3.root'
    #'/store/data/Commissioning2015/Cosmics/RAW-RECO/CosmicSP-6Mar2015-v1/10000/248747E6-25CA-E411-B17C-02163E00BD75.root'
    #'/store/data/Run2010B/Cosmics/RAW/v1/000/144/559/306A4ABD-F3B5-DF11-9CAD-003048F118C6.root'
<<<<<<< HEAD
   #'/store/data/Commissioning2015/Cosmics/RAW/v1/000/232/881/00000/26ADAFFB-3FAB-E411-A313-02163E011DDC.root'
=======
    '/store/data/Commissioning2015/Cosmics/RAW/v1/000/232/881/00000/26ADAFFB-3FAB-E411-A313-02163E011DDC.root'
>>>>>>> 7c2e18aec70ab1bee9e87695373770b7b56496b3
     ),               
     
    # drop native rechits and clusters, to be sure only those locally made will be picked up
    inputCommands = cms.untracked.vstring('keep *'
                                          ,'drop EcalRecHitsSorted_*_*_RECO' # drop hfRecoEcalCandidate as remade in this process
                                          , 'drop recoSuperClusters_*_*_RECO' # drop hfRecoEcalCandidate as remade in this process
                                          , 'drop recoCaloClusters_*_*_RECO'
                                          )


    )


### Schedule ###
process.schedule = cms.Schedule(process.p) 

### Setup source ###

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
options.parseArguments()

if options.inputFiles:
    process.source.fileNames = options.inputFiles
if options.maxEvents != -1:
    process.maxEvents.input = options.maxEvents

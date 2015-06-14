from RecoLocalCalo.Configuration.ecalLocalRecoSequence_cff import *

ecalLocalRecoSequenceAlCaStream = cms.Sequence (ecalMultiFitUncalibRecHit * 
                                                    ecalRecHit)

ecalMultiFitUncalibRecHit.EBdigiCollection = cms.InputTag("HLTEcalPhiSymFilter","phiSymEcalDigisEB")
ecalMultiFitUncalibRecHit.EEdigiCollection = cms.InputTag("HLTEcalPhiSymFilter","phiSymEcalDigisEE")

ecalRecHit.killDeadChannels = False
ecalRecHit.recoverEBFE = False
ecalRecHit.recoverEEFE = False

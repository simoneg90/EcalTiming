// -*- C++ -*-
//
// Package:    CalibCalorimetry/EcalTimingCalibProducer
// Class:      EcalTimingCalibProducer
//
/**\class EcalTimingCalibProducer EcalTimingCalibProducer.cc CalibCalorimetry/EcalTiming/plugins/EcalTimingCalibProducer.cc

 Description: Calculate ecal timing intercalibration

 Implementation:

*/
//
// Original Author:  Shervin Nourbakhsh
//         Created:  Wed, 01 Apr 2015 10:08:43 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDConsumerBase.h"

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
//#include "FWCore/Framework/interface/Handle.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Framework/interface/LooperFactory.h"
#include "FWCore/Framework/interface/ESProducerLooper.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/ESProducts.h"
#include "FWCore/Framework/interface/Event.h"
// input collections
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"

// record to be produced:
#include "CondFormats/DataRecord/interface/EcalTimeCalibConstantsRcd.h"
#include "CondFormats/DataRecord/interface/EcalTimeOffsetConstantRcd.h"
#include "CondTools/Ecal/interface/EcalTimeCalibConstantsXMLTranslator.h"
#include "CondTools/Ecal/interface/EcalTimeCalibErrorsXMLTranslator.h"
#include "CondTools/Ecal/interface/EcalTimeOffsetXMLTranslator.h"
#include "CondTools/Ecal/interface/EcalCondHeader.h"

#include "CondFormats/EcalObjects/interface/EcalTimeCalibConstants.h"
#include "CondFormats/EcalObjects/interface/EcalTimeCalibErrors.h"
#include "CondFormats/EcalObjects/interface/EcalTimeOffsetConstant.h"

#include "CalibCalorimetry/EcalTiming/interface/EcalTimingEvent.h"
#include "CalibCalorimetry/EcalTiming/interface/EcalCrystalTimingCalibration.h"
//
// class declaration
//

class EcalTimingCalibProducer : public edm::ESProducerLooper
{
public:
	EcalTimingCalibProducer(const edm::ParameterSet&);
	~EcalTimingCalibProducer();

	std::shared_ptr<EcalTimeCalibConstants> produce(const EcalTimeCalibConstantsRcd& iRecord);

	virtual void beginOfJob(const edm::EventSetup&);
	virtual void startingNewLoop(unsigned int ) ;
	virtual Status duringLoop(const edm::Event&, const edm::EventSetup&) ;
	virtual Status endOfLoop(const edm::EventSetup&, unsigned int);
	virtual void endOfJob();
private:
	// ----------member data ---------------------------
	edm::EDGetTokenT<EBRecHitCollection> _ecalRecHitsEBToken;
	edm::EDGetTokenT<EERecHitCollection> _ecalRecHitsEEToken;
	// Create calibration container objects
	EcalTimeCalibConstants _timeCalibConstants;
	EcalTimeCalibErrors    _timeCalibErrors;
	EcalTimeOffsetConstant _timeOffsetConstant;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//
/*
void EcalCreateTimeCalibrations::set(edm::EventSetup const& eventSetup)
{
     eventSetup.get<EcalTimeCalibConstantsRcd>().get(origTimeCalibConstHandle);
     eventSetup.get<EcalTimeOffsetConstantRcd>().get(origTimeOffsetConstHandle);
}
*/
//
// constructors and destructor
//
EcalTimingCalibProducer::EcalTimingCalibProducer(const edm::ParameterSet& iConfig) //:
//     _ecalRecHitsEBToken(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("recHitEBCollection"))),
//     _ecalRecHitsEEToken(consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("recHitEECollection")))
{
	_ecalRecHitsEBToken = consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("recHitEBCollection"));
	//the following line is needed to tell the framework what
	// data is being produced
	setWhatProduced(this);
	//now do what ever other initialization is needed
}


EcalTimingCalibProducer::~EcalTimingCalibProducer()
{
	// do anything here that needs to be done at desctruction time
	// (e.g. close files, deallocate resources etc.)
}


//
// member functions
//

// ------------ method called to produce the data  ------------
std::shared_ptr<EcalTimeCalibConstants> EcalTimingCalibProducer::produce(const EcalTimeCalibConstantsRcd& iRecord)
{
	using namespace edm::es;
	//std::auto_ptr<EcalTimeCalibConstants> pMyType;
	//return products(pMyType);
	return NULL;
}



// ------------ method called once per job just before starting to loop over events  ------------
void EcalTimingCalibProducer::beginOfJob(const edm::EventSetup&)
{
}

// ------------ method called at the beginning of a new loop over the event  ------------
// ------------ the argument starts at 0 and increments for each loop        ------------
void EcalTimingCalibProducer::startingNewLoop(unsigned int iIteration)
{
}

// ------------ called for each event in the loop.  The present event loop can be stopped by return kStop ------------
EcalTimingCalibProducer::Status EcalTimingCalibProducer::duringLoop(const edm::Event& iEvent, const edm::EventSetup&)
{
	// here the getByToken of the rechits
	edm::Handle<EBRecHitCollection> ebRecHitHandle;
	iEvent.getByToken(_ecalRecHitsEBToken, ebRecHitHandle);
	edm::Handle<EERecHitCollection> eeRecHitHandle;
	iEvent.getByToken(_ecalRecHitsEEToken, eeRecHitHandle);

	typedef std::map<DetId, EcalCrystalTimingCalibration> EcalTimeCalibrationMap;
	EcalTimeCalibrationMap timeCalibMap;
	// loop over the recHits
// recHit_itr is of type: edm::Handle<EcalRecHitCollection>::const_iterator
	for(auto  recHit_itr = ebRecHitHandle->begin(); recHit_itr != ebRecHitHandle->end(); ++recHit_itr) {
		// for each recHit create a EcalTimingEvent
		EcalTimingEvent timeEvent(recHit_itr->time(), recHit_itr->timeError(), recHit_itr->energy(), false);
		// add the EcalTimingEvent to the EcalCreateTimeCalibrations
		timeCalibMap[recHit_itr->detid()].add(timeEvent);
	}

	for(auto recHit_itr = eeRecHitHandle->begin(); recHit_itr != eeRecHitHandle->end(); ++recHit_itr) {
		EcalTimingEvent timeEvent(recHit_itr->time(), recHit_itr->timeError(), recHit_itr->energy(), true);
	}

	// any etaRing check?
	// any etaRing inter-calibration?
	return kContinue;
}


// ------------ called at the end of each event loop. A new loop will occur if you return kContinue ------------
EcalTimingCalibProducer::Status EcalTimingCalibProducer::endOfLoop(const edm::EventSetup&, unsigned int)
{
	// calculate the calibration constants
	// save the xml
	// create a new eventSetup?
	return kStop;
}

// ------------ called once each job just before the job ends ------------
void
EcalTimingCalibProducer::endOfJob()
{
}

//define this as a plug-in
DEFINE_FWK_LOOPER(EcalTimingCalibProducer);

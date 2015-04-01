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
#include "FWCore/Framework/interface/LooperFactory.h"
#include "FWCore/Framework/interface/ESProducerLooper.h"

#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/ESProducts.h"

#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
//
// class declaration
//

class EcalTimingCalibProducer : public edm::ESProducerLooper
{
public:
	EcalTimingCalibProducer(const edm::ParameterSet&);
	~EcalTimingCalibProducer();

	typedef std::shared_ptr<MyType> ReturnType;

	ReturnType produce(const recordname&);

	virtual void beginOfJob();
	virtual void startingNewLoop(unsigned int ) ;
	virtual Status duringLoop(const edm::Event&, const edm::EventSetup&) ;
	virtual Status endOfLoop(const edm::EventSetup&);
	virtual void endOfJob();
private:
	// ----------member data ---------------------------
	edm::EDGetTokenT<EBRecHitCollection> _ecalRecHitsEBToken;
	edm::EDGetTokenT<EERecHitCollection> _ecalRecHitsEEToken;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
EcalTimingCalibProducer::EcalTimingCalibProducer(const edm::ParameterSet& iConfig):
	_ecalRecHitsEBToken(iConfig.getParameter<edm::InputTag>("recHitEBCollection")),
	_ecalRecHitsEEToken(iConfig.getParameter<edm::InputTag>("recHitEECollection")),
{
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
EcalTimingCalibProducer::ReturnType
EcalTimingCalibProducer::produce(const recordname& iRecord)
{
	using namespace edm::es;
	std::auto_ptr<MyType> pMyType;
	return products(pMyType);

}


// ------------ method called once per job just before starting to loop over events  ------------
void
EcalTimingCalibProducer::beginOfJob(const edm::EventSetup&)
{
}

// ------------ method called at the beginning of a new loop over the event  ------------
// ------------ the argument starts at 0 and increments for each loop        ------------
void
EcalTimingCalibProducer::startingNewLoop(unsigned int iIteration)
{
}

// ------------ called for each event in the loop.  The present event loop can be stopped by return kStop ------------
EcalTimingCalibProducer::Status
EcalTimingCalibProducer::duringLoop(const edm::Event&, const edm::EventSetup&)
{
	// here the getByToken of the rechits

	// loop over the recHits

	// for each recHit create a EcalTimingEvent
	// add the EcalTimingEvent to the EcalCreateTimeCalibrations

	// any etaRing check?
	// any etaRing inter-calibration?

	return kContinue;
}


// ------------ called at the end of each event loop. A new loop will occur if you return kContinue ------------
EcalTimingCalibProducer::Status
EcalTimingCalibProducer::endOfLoop(const edm::EventSetup&, unsigned int)
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

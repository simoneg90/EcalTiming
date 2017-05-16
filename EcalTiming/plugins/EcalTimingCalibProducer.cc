#include "EcalTiming/EcalTiming/plugins/EcalTimingCalibProducer.h"
/*
*/
//
// Original Author:  Shervin Nourbakhsh
//         Created:  Wed, 01 Apr 2015 10:08:43 GMT
//
//



//
// class declaration
//

using namespace std;
using namespace edm;
using namespace cms;



//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
EcalTimingCalibProducer::EcalTimingCalibProducer(const edm::ParameterSet& iConfig) :
	_isSplash(iConfig.getParameter<bool>("isSplash")),
	_makeEventPlots(iConfig.getParameter<bool>("makeEventPlots")),
	_timingEvents(consumes<EcalTimingCollection>(iConfig.getParameter<edm::InputTag>("timingCollection"))),
	_recHitMin(iConfig.getParameter<unsigned int>("recHitMinimumN")),

	///\todo the min energy should be in ADC not in energy
	_minRecHitEnergyStep(iConfig.getParameter<double>("minRecHitEnergyStep")),
        _minRecHitEnergyNStep(iConfig.getParameter<double>("minRecHitEnergyNStep")),
        _energyThresholdOffsetEB(iConfig.getParameter<double>("energyThresholdOffsetEB")),
        _energyThresholdOffsetEE(iConfig.getParameter<double>("energyThresholdOffsetEE")),
        _minEntries(iConfig.getParameter<unsigned int>("minEntries")),
        _globalOffset(iConfig.getParameter<double>("globalOffset")),
	_storeEvents(iConfig.getParameter<bool>("storeEvents")),
	_produceNewCalib(iConfig.getParameter<bool>("produceNewCalib")),
	_outputDumpFileName(iConfig.getParameter<std::string>("outputDumpFile")),
	_maxSkewnessForDump(iConfig.getParameter<double>("maxSkewnessForDump")),
	_ringTools(EcalRingCalibrationTools())
{
}


EcalTimingCalibProducer::~EcalTimingCalibProducer()
{
	// do anything here that needs to be done at desctruction time
	// (e.g. close files, deallocate resources etc.)
}


//
// member functions
//


// ------------ method called once per job just before starting to loop over events  ------------
void EcalTimingCalibProducer::beginJob()
{
	std::cout << "Begin job: createConstants" << std::endl;

	// Initialize histograms at start of Loop
	char histDirName[100];
	sprintf(histDirName, "EcalSplashTiming");
	// Make a new directory for Histograms for each loop
	histDir_ = fileService_->mkdir( histDirName);

	initHists(histDir_);
	initTree(histDir_);

	// reset the calibration
	_timeCalibMap.clear();
}


bool EcalTimingCalibProducer::addRecHit(const EcalTimingEvent& timeEvent, EventTimeMap& eventTimeMap_)
{
	float energyThreshold = getEnergyThreshold(timeEvent.detid()); 
        if( timeEvent.energy() < (energyThreshold) ) return false;

         if(timeEvent.detid().subdetId() == EcalBarrel) {
           EBDetId id(timeEvent.detid());
           // Fill Rechit Energy
           //Event_EneMapEB_->Fill(id.ieta(), id.iphi(), timeEvent.energy()); // 2D energy map
           //Event_TimeMapEB_->Fill(id.ieta(), id.iphi(), timeEvent.time()); // 2D time map
           //RechitEnergyTimeEB->Fill(timeEvent.energy(), timeEvent.time());
           OccupancyEB_->Fill(id.iphi(), id.ieta(), 1);
         } else {
           // create EEDetId
           EEDetId id(timeEvent.detid());
           if(id.zside() < 0) {
             //Event_EneMapEEM_->Fill(id.ix(), id.iy(), timeEvent.energy());
             //Event_TimeMapEEM_->Fill(id.ix(), id.iy(), timeEvent.time());
             //RechitEnergyTimeEEM->Fill(timeEvent.energy(), timeEvent.time());
             OccupancyEEM_->Fill(id.ix(), id.iy(), 1);
              
           } else {
             //Event_EneMapEEP_->Fill(id.ix(), id.iy(), timeEvent.energy());
             //Event_TimeMapEEP_->Fill(id.ix(), id.iy(), timeEvent.time());
             //RechitEnergyTimeEEP->Fill(timeEvent.energy(), timeEvent.time());
             OccupancyEEP_->Fill(id.ix(), id.iy(), 1);
           }
         }

        
	// add the EcalTimingEvent to the EcalCreateTimeCalibrations
	_eventTimeMap.emplace(timeEvent.detid(), timeEvent);

	return true;
}

/**
   fills the energy map and timing maps for EB, EE+ and EE-
 */
void EcalTimingCalibProducer::plotRecHit(const EcalTimingEvent& timeEvent)
{
	if(timeEvent.detid().subdetId() == EcalBarrel) {
		EBDetId id(timeEvent.detid());
		// Fill Rechit Energy
		Event_EneMapEB_->Fill(id.ieta(), id.iphi(), timeEvent.energy()); // 2D energy map
		Event_TimeMapEB_->Fill(id.ieta(), id.iphi(), timeEvent.time()); // 2D time map
		RechitEnergyTimeEB->Fill(timeEvent.energy(), timeEvent.time());
		OccupancyEB_->Fill(id.iphi(), id.ieta(), 1);
	} else {
		// create EEDetId
		EEDetId id(timeEvent.detid());
		if(id.zside() < 0) {
			Event_EneMapEEM_->Fill(id.ix(), id.iy(), timeEvent.energy());
			Event_TimeMapEEM_->Fill(id.ix(), id.iy(), timeEvent.time());
			RechitEnergyTimeEEM->Fill(timeEvent.energy(), timeEvent.time());
			OccupancyEEM_->Fill(id.ix(), id.iy(), 1);

		} else {
			Event_EneMapEEP_->Fill(id.ix(), id.iy(), timeEvent.energy());
			Event_TimeMapEEP_->Fill(id.ix(), id.iy(), timeEvent.time());
			RechitEnergyTimeEEP->Fill(timeEvent.energy(), timeEvent.time());
			OccupancyEEP_->Fill(id.ix(), id.iy(), 1);
		}
	}
}

/**
	@param[in] te EcalTimingEvent
	@param[in] splashDir integer indicating the beam direction in splash events
	@param[in] bunchCorr float correction for global event timing
	@param[out] c corrected timing event
*/
EcalTimingEvent EcalTimingCalibProducer::correctGlobalOffset(const EcalTimingEvent& te, int splashDir, float bunchCorr)
{
	DetId id = te.detid();

	const CaloSubdetectorGeometry *geom = (id.subdetId() == EcalBarrel) ? barrelGeometry_ : endcapGeometry_;

	float z = geom->getGeometry(id)->getPosition().z();
	float mag = geom->getGeometry(id)->getPosition().mag();

	float time = te.time() - (splashDir * z - mag) / SPEEDOFLIGHT; // Adjust time by difference in time of flight for halo/splash

	time += bunchCorr;

	time += _globalOffset;

	return 	EcalTimingEvent (EcalRecHit(id, te.energy(), time ));
}

// ------------ called for each event in the loop.  The present event loop can be stopped by return kStop ------------
bool EcalTimingCalibProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
	//Get Geometry for Rings
	edm::ESHandle<CaloGeometry> pG;
	iSetup.get<CaloGeometryRecord>().get(pG);
	EcalRingCalibrationTools::setCaloGeometry(&(*pG));
	endcapGeometry_ =  pG->getSubdetectorGeometry(DetId::Ecal, EcalEndcap);
	barrelGeometry_ =  pG->getSubdetectorGeometry(DetId::Ecal, EcalBarrel);

	edm::ESHandle<EcalElectronicsMapping> hElecMap;
	iSetup.get<EcalMappingRcd>().get(hElecMap);
	elecMap_ = hElecMap.product();

	// here the getByToken of the rechits
	edm::Handle<EcalTimingCollection> timingCollection;
	iEvent.getByToken(_timingEvents, timingCollection);
#ifdef DEBUG
        std::cout << "Nhits\t" << timingCollection->size() << std::endl;
#endif


	_eventTimeMap.clear(); // reset the map of time from recHits for this event

	// the following maps are used to:
	//  - distinguish between beam1 and beam2 in splash events looking at the relative time shift
	//  - adjust the global time offset if required (for splash events for example).
	//  The global time shift is set such that all the time measurements in the event are relative to one ring
	timeEB.clear();  // reset the map for one ring in EB
	timeEEM.clear(); // reset the map for one ring in EE-
	timeEEP.clear(); // reset the map for one ring in EE+

	// loop over the recHits and add those passing the selection to the list of recHits to be used for timing:  eventTimeMap
	// timeEvent is of type: edm::Handle<EcalTimingEvent>::const_iterator
        for(auto  timeEvent : *timingCollection) {
           // add the recHit to the list of recHits used for calibration (with the relative information)
#ifdef DEBUG
           std::cout << timeEvent << std::endl;
#endif
           if(addRecHit(timeEvent, _eventTimeMap)) {
              if( timeEvent.detid().subdetId() == EcalBarrel)
                 timeEB.add(EcalTimingEvent(timeEvent), false);
              else {
                 EEDetId id(timeEvent.detid());
                 if(id.zside() < 0) {
                    timeEEM.add(EcalTimingEvent(timeEvent), false);
                 } else {
                    timeEEP.add(EcalTimingEvent(timeEvent), false);
                 }
              }
           }
        }

#ifdef DEBUG
	std::cout << "[DEBUG]" << "nRecHits passing selection"
	          << "\t" << _eventTimeMap.size()
	          << "\t" << timeEB.num()
	          << "\t" << timeEEM.num()
	          << "\t" << timeEEP.num()
	          << std::endl;
#endif
	// If we got less than the minimum recHits, continue -> this is to select events with enough activity
	if(_eventTimeMap.size() < _recHitMin) return false;
#ifdef DEBUG
	std::cout << "[DUMP]\t" << timeEB << "\t"  << timeEEM << "\t" << timeEEP << std::endl;
#endif
	// Make a new directory for Histograms for each event if you want plots per event
	char eventDirName[100];
	if(_makeEventPlots) {
		sprintf(eventDirName, "Event_%d", int(iEvent.id().event()) );
		TFileDirectory eventDir = histDir_.mkdir(eventDirName);
		initEventHists(eventDir);
	}

	// for splashes you want to distinguish between beam 1 and beam 2
	// you can use the average time over one ring in EE- and one ring in EE+ for that
	int splashDir = (timeEEP.mean() > timeEEM.mean()) ? 1 : -1; // 1 for beam 1, -1 for beam 2
	float bunchCorr = 0.0f;
	if( std::max(timeEEP.mean(), timeEEM.mean()) > 10.0)
		bunchCorr = -25.0f;

	// Add adjusted timeEvents to CorrectionsMap
	for(auto const & it : _eventTimeMap) {
		// if it is a splash event, set a global offset shift such that the time is coherent between different events
		EcalTimingEvent event = _isSplash ? correctGlobalOffset(it.second, splashDir, bunchCorr) : it.second;

		if(_makeEventPlots) plotRecHit(event);
		_timeCalibMap[it.first].add(event,_storeEvents);

		//Find the CCU(tower) that this crystal belongs to
		unsigned int elecID = getElecID(it.first);
		_HWCalibrationMap[elecID].add(event,false);

	}

	// any etaRing check?
	// any etaRing inter-calibration?
	return true;
}


// ------------ called at the end of each event loop. A new loop will occur if you return kContinue ------------
void EcalTimingCalibProducer::endJob()
{
	std::cout << "EndOfLoop " << std::endl;


	// calculate the calibration constants

	// set the values in _calibConstants, _calibErrors, _offsetConstant

#ifdef DEBUG
	for (auto it : _HWCalibrationMap)
	{
		if	(abs(it.second.mean()) > HW_UNIT * 1.5) std::cout <<  "HW: " << it.first << ' ' << it.second.mean() << std::endl;
	}
#endif

	// remove the entries OOT (time > n_sigma)
	float n_sigma = 2.; /// \todo remove hard coded number
	for(auto calibRecHit_itr = _timeCalibMap.begin(); calibRecHit_itr != _timeCalibMap.end(); ++calibRecHit_itr) {
		FillCalibrationCorrectionHists(calibRecHit_itr); // histograms with shifts to be corrected at each step
		FillHWCorrectionHists(calibRecHit_itr);
		float correction =  - calibRecHit_itr->second.getMeanWithinNSigma(n_sigma, 10);  // to reject tails
		_timeCalibConstants.setValue(calibRecHit_itr->first.rawId(), correction);

		unsigned int ds = DS_NONE;
		if(calibRecHit_itr->second.num() > 50) {
			// check the asymmetry of the distribution: if asymmetric, dump the full set of events for further offline studies
			if(fabs(calibRecHit_itr->second.getSkewnessWithinNSigma(n_sigma, 10)) > _maxSkewnessForDump)  {
				ds |= DS_HIGH_SKEW;

			}

			// check if result is stable as function of energy
			std::vector< std::pair<float, EcalCrystalTimingCalibration*> > energyStability;
			float energyThreshold = getEnergyThreshold(calibRecHit_itr->first);
			if(! calibRecHit_itr->second.isStableInEnergy(energyThreshold, energyThreshold + _minRecHitEnergyStep * _minRecHitEnergyNStep, _minRecHitEnergyStep, energyStability)) {
				ds |= DS_UNSTABLE_EN;
			}
			FillEnergyStabilityHists(calibRecHit_itr, energyStability);
		}

		unsigned int elecID = getElecID(calibRecHit_itr->first);
		if( abs(_HWCalibrationMap[elecID].mean()) > HW_UNIT * 1.5)
		{
			ds |= DS_CCU_OOT;
		}

		if((calibRecHit_itr->first.rawId() == EBCRYex) ||
				(calibRecHit_itr->first.rawId() == EECRYex)) ds |= DS_CRYS;

		int iRing = _ringTools.getRingIndexInSubdet(calibRecHit_itr->first);

		if(calibRecHit_itr->first.subdetId() == EcalBarrel && iRing == EBRING) ds |= DS_RING;
		else if(calibRecHit_itr->first.subdetId() == EcalEndcap && (iRing == EEmRING || iRing == EEpRING )) ds |= DS_RING;

		if(ds != DS_NONE)
		{
			int ix, iy, iz;
			if(calibRecHit_itr->first.subdetId() == EcalBarrel) {
				EBDetId id(calibRecHit_itr->first);
				ix = id.ieta();
				iy = id.iphi();
				iz = 0;
			} else {
				EEDetId id(calibRecHit_itr->first);
				ix = id.ix();
				iy = id.iy();
				iz = id.zside();
			}
			calibRecHit_itr->second.dumpToTree(dumpTree, ix, iy, iz, ds, elecID, iRing);
		}

		// add filing Energy hists here
	}

	// save txt
	time_t     now = time(0);
	struct tm  tstruct;
	char       current_time[80];
	tstruct = *localtime(&now);
	strftime(current_time, sizeof(current_time), "%Y-%m-%d.%X", &tstruct);

	char filename[100];
	//sprintf(filename, "%s.dat", _outputDumpFileName.substr(0, _outputDumpFileName.find(".root")).c_str()); //text file holding constants
	//dumpCalibration(filename);
	sprintf(filename, "%s-corr.dat", _outputDumpFileName.substr(0, _outputDumpFileName.find(".root")).c_str()); //text file holding constants
	dumpCorrections(filename);
}

void EcalTimingCalibProducer::dumpCorrections(std::string filename)
{
	std::ofstream fout(filename);

	// loop over the constants
	// to make more efficient
	for(auto calibRecHit_itr = _timeCalibMap.begin(); calibRecHit_itr != _timeCalibMap.end(); ++calibRecHit_itr) {
		DetId id_ = calibRecHit_itr->first;
		if(id_.subdetId() == EcalBarrel) {
			EBDetId id(id_);
			fout << id.ieta() << "\t" << id.iphi() << "\t" << 0
			     << "\t" << calibRecHit_itr->second.getMeanWithinNSigma(2,10) << "\t" << calibRecHit_itr->second.stdDev() << "\t" << calibRecHit_itr->second.num() << "\t" << calibRecHit_itr->second.meanE()
			     << "\t" << id.rawId() << std::endl;
		} else {
			EEDetId id(id_);
			fout << id.ix() << "\t" << id.iy() << "\t" << id.zside()
			     << "\t" << calibRecHit_itr->second.getMeanWithinNSigma(2,10) << "\t" << calibRecHit_itr->second.stdDev() << "\t" << calibRecHit_itr->second.num() << "\t" << calibRecHit_itr->second.meanE()
			     << "\t" << id.rawId() << std::endl;
		}
	}
	fout.close();
}

void EcalTimingCalibProducer::dumpCalibration(std::string filename)
{
	std::ofstream fout(filename);

	// loop over the constants
	// to make more efficient
#ifdef DEBUG
	DetId findId(RAWIDCRY);
	if(findId.subdetId() == EcalBarrel) {
		EBDetId id(RAWIDCRY);
		fout << "EB: " << id.ieta() << "\t" << id.iphi() << "\t" << id.zside() << "\t" << _timeCalibConstants.barrelItems()[id.denseIndex()] << "\t" << *_timeCalibConstants.find(RAWIDCRY) << "\t" << id.rawId() << std::endl;
	} else {
		EEDetId id(findId);
		fout << "EE: " << id.ix() << "\t" << id.iy() << "\t" << id.zside() << "\t" << _timeCalibConstants.endcapItems()[id.denseIndex()] << "\t" << *_timeCalibConstants.find(RAWIDCRY) << std::endl;
	}
#endif

	for(unsigned int i = 0; i < _timeCalibConstants.barrelItems().size(); ++i) {
		EBDetId id(EBDetId::detIdFromDenseIndex(i)); // this is a stupid thing that I'm obliged to do due to the stupid structure of the ECAL container
		fout << id.ieta() << "\t" << id.iphi() << "\t" << 0 << "\t" << _timeCalibConstants.barrelItems()[i] << "\t" << id.rawId() << std::endl;
	}

	for(unsigned int i = 0; i < _timeCalibConstants.endcapItems().size(); ++i) {
		EEDetId id(EEDetId::detIdFromDenseIndex(i)); // this is a stupid thing that I'm obliged to do due to the stupid structure of the ECAL container
		fout << id.ix() << "\t" << id.iy() << "\t" << id.zside() << "\t" << _timeCalibConstants.endcapItems()[i] << "\t" << id.rawId() << std::endl;	
	}
	fout.close();
}




// FillHistograms

void EcalTimingCalibProducer::FillCalibrationCorrectionHists(EcalTimeCalibrationMap::const_iterator cal_itr)
{
	int ix,iy,iz;
	int rawid = cal_itr->first.rawId();
	if(cal_itr->first.subdetId() == EcalBarrel) {
		EBDetId id(cal_itr->first);
		// Fill Rechit Energy
		EneMapEB_->Fill(id.ieta(), id.iphi(), cal_itr->second.meanE()); // 2D energy map
		TimeMapEB_->Fill(id.ieta(), id.iphi(), cal_itr->second.getMeanWithinNSigma(2,10)); // 2D time map
		TimeErrorMapEB_->Fill(id.ieta(), id.iphi(), cal_itr->second.getMeanErrorWithinNSigma(2,10));

		RechitEneEB_->Fill(cal_itr->second.meanE());   // 1D histogram
		RechitTimeEB_->Fill(cal_itr->second.getMeanWithinNSigma(2,10)); // 1D histogram

		ix = id.ieta();
		iy = id.iphi();
		iz = 0;

	} else {
		// create EEDetId
		EEDetId id(cal_itr->first);
		if(id.zside() < 0) {
			EneMapEEM_->Fill(id.ix(), id.iy(), cal_itr->second.meanE());
			TimeMapEEM_->Fill(id.ix(), id.iy(), cal_itr->second.getMeanWithinNSigma(2,10));
			TimeErrorMapEEM_->Fill(id.ix(), id.iy(), cal_itr->second.getMeanErrorWithinNSigma(2,10));

			RechitEneEEM_->Fill(cal_itr->second.meanE());
			RechitTimeEEM_->Fill(cal_itr->second.getMeanWithinNSigma(2,10));
		} else {
			EneMapEEP_->Fill(id.ix(), id.iy(), cal_itr->second.meanE());
			TimeMapEEP_->Fill(id.ix(), id.iy(), cal_itr->second.getMeanWithinNSigma(2,10));
			TimeErrorMapEEP_->Fill(id.ix(), id.iy(), cal_itr->second.getMeanErrorWithinNSigma(2,10));

			RechitEneEEP_->Fill(cal_itr->second.meanE());
			RechitTimeEEP_->Fill(cal_itr->second.getMeanWithinNSigma(2,10));
		}

		ix = id.ix();
		iy = id.iy();
		iz = id.zside();
	}

	int iRing = _ringTools.getRingIndexInSubdet(cal_itr->first);
	cal_itr->second.dumpCalibToTree(timingTree, rawid, ix, iy, iz, getElecID(cal_itr->first), iRing);
}

void EcalTimingCalibProducer::FillHWCorrectionHists(EcalTimeCalibrationMap::const_iterator cal_itr)
{
	unsigned int elecID = getElecID(cal_itr->first);
	float time = _HWCalibrationMap[elecID].mean();
	if(cal_itr->first.subdetId() == EcalBarrel) {
		EBDetId id(cal_itr->first);
		// Fill Rechit Energy
		HWTimeMapEB_->Fill(id.ieta(), id.iphi(), time); // 2D time map
	} else {
		// create EEDetId
		EEDetId id(cal_itr->first);
		if(id.zside() < 0) {
			HWTimeMapEEM_->Fill(id.ix(), id.iy(), time);
		} else {
			HWTimeMapEEP_->Fill(id.ix(), id.iy(), time);
		}
	}

}
void EcalTimingCalibProducer::FillEnergyStabilityHists(EcalTimeCalibrationMap::const_iterator cal_itr, std::vector< std::pair<float, EcalCrystalTimingCalibration*> > energyStability)
{

	int ix,iy,iz;
  	int rawid = cal_itr->first.rawId();
	//choose which map to store in
	if(cal_itr->first.subdetId() == EcalBarrel) {
		EBDetId id(cal_itr->first);
		ix = id.ieta();
		iy = id.iphi();
		iz = 0;
	} else {
		EEDetId id(cal_itr->first);
		ix = id.ix();
		iy = id.iy();
		iz = id.zside();
	}

	int iRing = _ringTools.getRingIndexInSubdet(cal_itr->first);

	// Add min_energy to the tree which gets filld inside the dump function
	float min_energy = -1.0;
	if(energyStabilityTree->GetBranch("min_energy") == NULL) energyStabilityTree->Branch("min_energy", &min_energy, "min_energy/F");
	energyStabilityTree->SetBranchAddress("min_energy", &min_energy);

	UChar_t index = 0;
	if(energyStabilityTree->GetBranch("index") == NULL) energyStabilityTree->Branch("index", &index, "index/b");
	energyStabilityTree->SetBranchAddress("index", &index);

	for(auto it = energyStability.begin(); it!=energyStability.end(); it++)
	{
		min_energy = it->first;
		it->second->dumpCalibToTree(energyStabilityTree,rawid,ix,iy,iz,getElecID(cal_itr->first),iRing);
		index++;
	}

}
void EcalTimingCalibProducer::initEventHists(TFileDirectory fdir)
{
	Event_EneMapEB_   = fdir.make<TProfile2D>("EneMapEB",   "RecHit Energy[GeV] EB map;i#eta; i#phi;E[GeV]", 171, -85, 86, 360, 1., 361.);
	Event_TimeMapEB_  = fdir.make<TProfile2D>("TimeMapEB",  "Time [ns] EB map; i#eta; i#phi;Time[ns]",  	    171, -85, 86, 360, 1., 361.);
	Event_TimeMapEB_OOT  = fdir.make<TProfile2D>("TimeMapEB_OOT",  "Time [ns] EB map; i#eta; i#phi;Time[ns]",  	    171, -85, 86, 360, 1., 361.);

	Event_EneMapEEP_  = fdir.make<TProfile2D>("EneMapEEP",  "RecHit Energy[GeV] map EE+;ix;iy;E[GeV]", 100, 1, 101, 100, 1, 101);
	Event_TimeMapEEP_ = fdir.make<TProfile2D>("TimeMapEEP", "Time[ns] map EE+;ix;iy; Time[ns]", 	    100, 1, 101, 100, 1, 101);
	Event_TimeMapEEP_OOT  = fdir.make<TProfile2D>("TimeMapEEP_OOT", "Time[ns] map EE+;ix;iy; Time[ns]", 	    100, 1, 101, 100, 1, 101);

	Event_EneMapEEM_  = fdir.make<TProfile2D>("EneMapEEM",  "RecHit Energy[GeV] map EE-;ix;iy;E[GeV]", 100, 1, 101, 100, 1, 101);
	Event_TimeMapEEM_ = fdir.make<TProfile2D>("TimeMapEEM", "Time[ns] map EE-;ix;iy; Time[ns]",        100, 1, 101, 100, 1, 101);
	Event_TimeMapEEM_OOT  = fdir.make<TProfile2D>("TimeMapEEM_OOT", "Time[ns] map EE-;ix;iy; Time[ns]",        100, 1, 101, 100, 1, 101);
}

//
void EcalTimingCalibProducer::initHists(TFileDirectory fdir)
{
	EneMapEB_ = fdir.make<TProfile2D>("EneMapEB", "RecHit Energy[GeV] EB profile map;i#eta; i#phi;E[GeV]", 171, -85, 86, 360, 1., 361.);
	TimeMapEB_ = fdir.make<TProfile2D>("TimeMapEB", "Mean Time [ns] EB profile map; i#eta; i#phi;Time[ns]", 171, -85, 86, 360, 1., 361.);

	EneMapEEP_ = fdir.make<TProfile2D>("EneMapEEP", "RecHit Energy[GeV] profile map EE+;ix;iy;E[GeV]", 100, 1, 101, 100, 1, 101);
	TimeMapEEP_ = fdir.make<TProfile2D>("TimeMapEEP", "Mean Time[ns] profile map EE+;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
	EneMapEEM_ = fdir.make<TProfile2D>("EneMapEEM", "RecHit Energy[GeV] profile map EE-;ix;iy;E[GeV]", 100, 1, 101, 100, 1, 101);
	TimeMapEEM_ = fdir.make<TProfile2D>("TimeMapEEM", "Mean Time[ns] profile map EE-;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);

	TimeErrorMapEB_ = fdir.make<TProfile2D>("TimeErrorMapEB", "Error Time [ns] EB profile map; i#eta; i#phi;Time[ns]", 171, -85, 86, 360, 1., 361.);

	TimeErrorMapEEP_ = fdir.make<TProfile2D>("TimeErrorMapEEP", "Error Time[ns] profile map EE+;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
	TimeErrorMapEEM_ = fdir.make<TProfile2D>("TimeErrorMapEEM", "Error Time[ns] profile map EE-;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);

	RechitTimeEEM_ = fdir.make<TH1F>("RechitTimeEEM", "RecHit Mean Time[ns] EE-;RecHit Time[ns]; Events", 200, -50.0, 50.0);
	RechitTimeEEP_ = fdir.make<TH1F>("RechitTimeEEP", "RecHit Mean Time[ns] EE+;RecHit Time[ns]; Events", 200, -50.0, 50.0);
	RechitTimeEB_ = fdir.make<TH1F>("RechitTimeEB", "RecHit Mean Time[ns] EB;RecHit Time[ns]; Events", 200, -50.0, 50.0);

	RechitEneEEM_ = fdir.make<TH1F>("RechitEneEEM", "RecHit Energy[GeV] EE-;Rechit Energy[GeV]; Events", 200, 0.0, 100.0);
	RechitEneEEP_ = fdir.make<TH1F>("RechitEneEEP", "RecHit Energy[GeV] EE+;Rechit Energy[GeV]; Events", 200, 0.0, 100.0);
	RechitEneEB_ = fdir.make<TH1F>("RechitEneEB", "RecHit Energy[GeV] EB;Rechit Energy[GeV]; Events", 200, 0.0, 100.0);

	RechitEnergyTimeEEM = fdir.make<TH2F>("RechitEnergyTimeEEM", "RecHit Energy vs Time EE-;Rechit Energy[GeV]; Time[ns]; Events", 200, 0.0, 1000.0, 100, -15, 30);
	RechitEnergyTimeEEP = fdir.make<TH2F>("RechitEnergyTimeEEP", "RecHit Energy vs Time EE+;Rechit Energy[GeV]; Time[ns]; Events", 200, 0.0, 1000.0, 100, -15, 30);
	RechitEnergyTimeEB  = fdir.make<TH2F>("RechitEnergyTimeEB",  "RecHit Energy vs Time EB; Rechit Energy[GeV]; Time[ns]; Events", 200, 0.0, 100.0,  100, -15, 30);

	// HW Histograms
	
	HWTimeMapEEP_ = fdir.make<TProfile2D>("HWTimeMapEEP", "Mean HW Time[ns] profile map EE+;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
	HWTimeMapEEM_ = fdir.make<TProfile2D>("HWTimeMapEEM", "Mean HW Time[ns] profile map EE-;ix;iy; Time[ns]", 100, 1, 101, 100, 1, 101);
	HWTimeMapEB_  = fdir.make<TProfile2D>("HWTimeMapEB",  "Mean HW Time[ns] EB profile map; i#eta; i#phi;Time[ns]", 171, -85, 86, 360, 1., 361.);


	OccupancyEB_  = fdir.make<TH2D>("OccupancyEB", "Occupancy EB; i#phi; i#eta; #Hits", 360, 1., 361., 171, -85, 86);
	OccupancyEEM_ = fdir.make<TH2D>("OccupancyEEM", "OccupancyEEM; iy; ix; #Hits", 100, 1, 101, 100, 1, 101);
	OccupancyEEP_ = fdir.make<TH2D>("OccupancyEEP", "OccupancyEEP; iy; ix; #Hits", 100, 1, 101, 100, 1, 101);
}

//
void EcalTimingCalibProducer::initTree(TFileDirectory fdir)
{
	dumpTree = fdir.make<TTree>("dumpTree", "");
	timingTree = fdir.make<TTree>("timingTree", "");
	energyStabilityTree = fdir.make<TTree>("energyStabilityTree", "");
}

//define this as a plug-in
DEFINE_FWK_MODULE(EcalTimingCalibProducer);

#ifndef ecaltimingevent_hh
#define ecaltimingevent_hh

#include <iostream>

/** \class EcalTimingEvent EcalTiming.cc EcalTiming.cc
 *
 * Basic timing information: contains the time information of one recHit
 */

class EcalTimingEvent
{
public:
	float _energy; ///< energy of the recHit
	float _time;   ///< time of the recHit
//	float _chi2;   ///< chi2
	float _timeError;  ///< time error saved in the recHit
	//float _expectedPrecision;

	/* EcalTimingEvent() : */
	/* 	energy(-1), */
	/* 	time(-1), */
	/* 	chi2(-1), */
	/* 	timeError(-1), */
	/* 	expectedPrecision(-1) */
	/* { */
	/* } */

	/// default constructor
	EcalTimingEvent (float time_, float timeError_, float energy_): //, bool ee) :
		_energy (energy_),
		_time (time_),
		//_chi2 (-1),
		_timeError (timeError_)
	{
		/* if (ee) { */
		/* 	_expectedPrecision = 33 / (_energy / 2.0); */
		/* } else { */
		/* 	_expectedPrecision = 33 / (_energy / 1.2); */
		/* } */
	}

	/// to print the content of the EcalTimingEvent
	friend ostream& operator << (ostream& os, const EcalTimingEvent& event)
	{
		os << event._time << "\t" << event._timeError << "\t" << event._energy;
		return os;
	}


	/* bool operator== (const EcalTimingEvent &first) const */
	/* { */
	/* 	// only check amp, time, sigmaT */
	/* 	if (first._energy == this->_energy && */
	/* 	        first._time == this->_time && */
	/* 	        first._timeError == this->_timeError) { */
	/* 		return true; */
	/* 	} */

	/* 	return false; */
	/* } */

};

#endif


#ifndef ecaltimingevent_hh
#define ecaltimingevent_hh

#include <iostream>
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"

/** \class EcalTimingEvent EcalTiming.cc EcalTiming.cc
 *
 * Description: basic timing information
 */

class EcalTimingEvent //: EcalRecHit
{
public:
	float _energy;
	float _time;
	float _chi2;
	float _sigmaTime;
	float _expectedPrecision;


	EcalTimingEvent (float time_, float sigmaTime_, float energy_, bool ee) :
		_energy (energy_),
		_time (time_),
		_chi2 (-1),
		_sigmaTime (sigmaTime_)
	{
		if (ee) {
			_expectedPrecision = 33 / (_energy / 2.0);
		} else {
			_expectedPrecision = 33 / (_energy / 1.2);
		}
	}

	friend ostream& operator << (ostream& os, const EcalTimingEvent& event)
	{
		os << event._time << "\t" << event._sigmaTime << "\t" << event._energy;
		return os;
	}

	bool operator== (const EcalTimingEvent &first) const
	{
		// only check amp, time, sigmaT
		if (first._energy == this->_energy &&
		        first._time == this->_time &&
		        first._sigmaTime == this->_sigmaTime) {
			return true;
		}

		return false;
	}

};

#endif


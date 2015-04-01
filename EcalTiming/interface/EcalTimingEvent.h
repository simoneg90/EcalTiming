#ifndef ecaltimingevent_hh
#define ecaltimingevent_hh

/** \class EcalTimingEvent EcalTiming.cc EcalTiming.cc
 *
 * Description: basic timing information
 */

class EcalTimingEvent
{
public:
	float _energy;
	float _time;
	float _chi2;
	float _sigmaTime;
	float _expectedPrecision;

	/* EcalTimingEvent() : */
	/* 	energy(-1), */
	/* 	time(-1), */
	/* 	chi2(-1), */
	/* 	sigmaTime(-1), */
	/* 	expectedPrecision(-1) */
	/* { */
	/* } */

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


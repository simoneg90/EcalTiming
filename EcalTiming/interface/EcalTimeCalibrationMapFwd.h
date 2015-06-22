/** In this file the time Map is defined
 */

class EcalTimingEvent;
class EcalCrystalTimingCalibration;
class EcalElectronicsId;

// Map of detId and Crystal time
typedef std::map<DetId, EcalCrystalTimingCalibration> EcalTimeCalibrationMap;
typedef std::map<EcalElectronicsId, EcalCrystalTimingCalibration> EcalHWCalibrationMap;


typedef std::map<DetId, EcalTimingEvent> EventTimeMap;


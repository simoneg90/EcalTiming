#include "DataFormats/Common/interface/Wrapper.h"

#include "EcalTiming/EcalTiming/interface/EcalTimingEvent.h"

namespace
{
    struct dictionary
    {
        EcalTimingEvent dummy11;
        std::vector<EcalTimingEvent> dummy12;
        edm::Wrapper<EcalTimingCollection> dummy13;
    };

}


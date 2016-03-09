#ifndef L1TUGT_H
#define L1TUGT_H

/**
 * \class L1TuGT
 *
 * Description: DQM for L1 Micro Global Trigger.
 *
 * \author Mateusz Zarucki
 *
 */

// System include files
#include <memory>
#include <unistd.h>
#include <vector>
#include <utility>

// User include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Utilities/interface/typedefs.h"
#include "DataFormats/L1Trigger/interface/BXVector.h"

//L1 trigger includes
//#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetup.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "DataFormats/L1TGlobal/interface/GlobalExtBlk.h"

//DQM includes
#include "DQMServices/Core/interface/DQMEDAnalyzer.h"
#include "DQMServices/Core/interface/DQMStore.h"
#include "DQMServices/Core/interface/MonitorElement.h"

//
// Class declaration
//

class L1TuGT: public DQMEDAnalyzer {

public:
   L1TuGT(const edm::ParameterSet& ps); // constructor
   virtual ~L1TuGT(); // destructor

protected:
   virtual void dqmBeginRun(const edm::Run&, const edm::EventSetup&);
   virtual void beginLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&);
   virtual void bookHistograms(DQMStore::IBooker &ibooker, edm::Run const&, edm::EventSetup const&) override;
   virtual void analyze(const edm::Event&, const edm::EventSetup&);
   virtual void endLuminosityBlock(const edm::LuminosityBlock&, const edm::EventSetup&); // end section

private:
   
   // Input parameters
   edm::EDGetTokenT<GlobalAlgBlkBxCollection> l1tuGtSource_; // input tag for L1 uGT DAQ readout record
  
   // Switches to choose the running of various methods
   //bool runInEventLoop_;
   //bool runInEndLumi_;
   
   bool verbose_; // verbosity switch
   
   // Number of events processed
   int nrEvJob_;
   int nrEvRun_;
   
   std::string histFolder_; // Histogram folder for L1 uGT plots
   
   // Booking of histograms for the module
   MonitorElement* algo_bits_;
   MonitorElement* algo_bits_corr_;
   MonitorElement* algo_bits_bx_;
   MonitorElement* algo_bits_lumi_;
  
   //MonitorElement* event_number_;
   //MonitorElement* event_lumi_;
   //MonitorElement* trigger_number_;
   //MonitorElement* trigger_lumi_;
   //MonitorElement* evnum_trignum_lumi_;
   MonitorElement* orbit_lumi_;
   //MonitorElement* setupversion_lumi_;

   MonitorElement* prescaleFactorSet_;
   //MonitorElement* m_monL1PfIndicesPerLs;
 
};

#endif

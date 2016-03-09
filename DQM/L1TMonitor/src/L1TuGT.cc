/**
 * \class L1TuGT
 *
 * Description: DQM for L1 Micro Global Trigger.
 *
 * \author Mateusz Zarucki
 * \author J. Berryhill, I. Mikulec
 * \author Vasile Mihai Ghete - HEPHY Vienna
 *
 */

#include "DQM/L1TMonitor/interface/L1TuGT.h"

//Constructor
L1TuGT::L1TuGT(const edm::ParameterSet& params):
   l1tuGtSource_(consumes<GlobalAlgBlkBxCollection>(params.getParameter<edm::InputTag>("uGtSource"))),
   //runInEventLoop_(params.getUntrackedParameter<bool>("runInEventLoop", false)),
   //runInEndLumi_(params.getUntrackedParameter<bool>("runInEndLumi", false)),
   verbose_(params.getUntrackedParameter<bool> ("verbose", false)),
   nrEvJob_(0), nrEvRun_(0)
{
   histFolder_ = params.getUntrackedParameter<std::string> ("HistFolder", "L1T2016/L1TuGT");
}

//Destructor
L1TuGT::~L1TuGT() {
}

void L1TuGT::dqmBeginRun(edm::Run const& iRun, edm::EventSetup const& evtSetup) {
   nrEvRun_ = 0;
}

void L1TuGT::beginLuminosityBlock(const edm::LuminosityBlock& iLumi, const edm::EventSetup& evtSetup) { 
   //empty
}

void L1TuGT::bookHistograms(DQMStore::IBooker &ibooker, edm::Run const&, edm::EventSetup const& evtSetup) {
   
   // Book histograms
   const int TotalNrBinsLs = 1000;
   const double totalNrBinsLs = static_cast<double>(TotalNrBinsLs);
   //FIXME: Take number of Algorithms from EventSetup
   const int L1TnumAlgs = 512;
   const double upL1TnumAlgs = static_cast<double>(L1TnumAlgs)-0.5;

   ibooker.setCurrentFolder(histFolder_);
    
   algo_bits_ = ibooker.book1D("algo_bits", "uGT algorithm trigger bits", L1TnumAlgs, -0.5, upL1TnumAlgs);
   algo_bits_->setAxisTitle("Algorithm trigger bits", 1);
   
   algo_bits_corr_ = ibooker.book2D("algo_bits_corr","uGT algorithm trigger bit correlation", L1TnumAlgs, -0.5, upL1TnumAlgs, L1TnumAlgs, -0.5, upL1TnumAlgs);
   algo_bits_corr_->setAxisTitle("Algorithm trigger bits", 1);
   algo_bits_corr_->setAxisTitle("Algorithm trigger bits", 2);
   
   algo_bits_bx_ = ibooker.book2D("algo_bits_bx", "uGT algorithm trigger bits vs BX", L1TnumAlgs, -0.5, upL1TnumAlgs, 5, -2.5, 2.5);
   algo_bits_bx_->setAxisTitle("Algorithm trigger bits", 1);
   algo_bits_bx_->setAxisTitle("BX", 2); //(0=L1A)
   
   algo_bits_lumi_ = ibooker.book2D("algo_bits_lumi","uGT algorithm trigger bit rate per LS", TotalNrBinsLs, 0., totalNrBinsLs, L1TnumAlgs, -0.5, upL1TnumAlgs);
   algo_bits_lumi_->setAxisTitle("Luminosity segment", 1);
   algo_bits_lumi_->setAxisTitle("Algorithm trigger bits", 2);
 
   //event_number_ = ibooker.book1D("event_number", "uGT event number (from last resync)", 100, 0., 50000.);
   //event_number_->setAxisTitle("Event number", 1);

   //event_lumi_ = ibooker.bookProfile("event_lumi", "uGT event number (from last resync) vs LS", TotalNrBinsLs, 0., totalNrBinsLs, 100, -0.1, 1.e15, "s");
   //event_lumi_->setAxisTitle("Luminosity segment", 1);
   //event_lumi_->setAxisTitle("Event number", 2);

   //trigger_number_ = ibooker.book1D("trigger_number","uGT trigger number (from start run)", 100, 0., 50000.);
   //trigger_number_->setAxisTitle("Trigger number", 1);

   //trigger_lumi_ = ibooker.bookProfile("trigger_lumi", "uGT trigger number (from start run) vs LS", TotalNrBinsLs, 0., totalNrBinsLs, 100, -0.1, 1.e15, "s");
   //trigger_lumi_->setAxisTitle("Luminosity segment", 1);
   //trigger_lumi_->setAxisTitle("Trigger number", 2);

   //evnum_trignum_lumi_ = ibooker.bookProfile("evnum_trignum_lumi", "uGT event/trigger number ratio vs LS", TotalNrBinsLs, 0., totalNrBinsLs, 100, -0.1, 2., "s");
   //evnum_trignum_lumi_->setAxisTitle("Luminosity segment", 1);
   //evnum_trignum_lumi_->setAxisTitle("Event/trigger number ratio", 2);

   orbit_lumi_ = ibooker.bookProfile("orbit_lumi", "uGT orbit number vs LS", TotalNrBinsLs, 0., totalNrBinsLs, 100, -0.1, 1.e15, "s");
   orbit_lumi_->setAxisTitle("Luminosity segment", 1);
   orbit_lumi_->setAxisTitle("Orbit number", 2);

   //setupversion_lumi_ = ibooker.bookProfile("setupversion_lumi", "uGT setup version vs LS", TotalNrBinsLs, 0., totalNrBinsLs, 100, -0.1, 1.e10, "i");
   //setupversion_lumi_->setAxisTitle("Luminosity segment", 1);
   //setupversion_lumi_->setAxisTitle("Setup version", 2);

   // prescale factor index monitoring
   prescaleFactorSet_ = ibooker.book2D("PrescaleFactorSet", "Index of prescale factor set", TotalNrBinsLs, 0., totalNrBinsLs, 25, 0., 25.);
   prescaleFactorSet_->setAxisTitle("Luminosity segment", 1);
   prescaleFactorSet_->setAxisTitle("PF set index", 2);
    
   //m_monL1PfIndicesPerLs = ibooker.book1D("L1PfIndicesPerLs", "Number of prescale factor indices used per LS", 10, 0., 10.);
   //m_monL1PfIndicesPerLs->setAxisTitle("Number of PF indices used per LS", 1);
   //m_monL1PfIndicesPerLs->setAxisTitle("Entries", 2);
 
}

void L1TuGT::analyze(const edm::Event& evt, const edm::EventSetup& evtSetup) {
   //FIXME: Remove duplicate definition of L1TnumAlgs 
   const int L1TnumAlgs = 512;
  
   nrEvJob_++;
   
   if (verbose_) {
      edm::LogInfo("L1TuGT") << "L1TuGT DQM: Analyzing" << std::endl;
   }
   
   // Get the LS block number (to be used in many histograms)
   const int lsNumber = evt.luminosityBlock();
   
   // Open uGT readout record
   edm::Handle<GlobalAlgBlkBxCollection> uGtAlgs;
   evt.getByToken(l1tuGtSource_, uGtAlgs);
   
   if (!uGtAlgs.isValid()) {
      edm::LogInfo("L1TuGT") << "Cannot find uGT readout record";
      return;
   }
   // Get uGT algo bit statistics
   else {

      //algo_bits_->Fill(-1.); // fill underflow to normalize //FIXME: needed? 
      
      for (int ibx=uGtAlgs->getFirstBX(); ibx <= uGtAlgs->getLastBX(); ++ibx) {
         for (auto itr = uGtAlgs->begin(ibx); itr != uGtAlgs->end(ibx); ++itr) { //FIXME: redundant loop over 1-dim vector?
            
            orbit_lumi_->Fill(lsNumber, itr->getOrbitNr());
            prescaleFactorSet_->Fill(lsNumber, itr->getPreScColumn());
             
            //Fills algorithm bits histograms
            for(int algoBit = 0; algoBit < L1TnumAlgs; algoBit++) {
               if(itr->getAlgoDecisionFinal(algoBit)) {
                  algo_bits_->Fill(algoBit);
                  algo_bits_lumi_->Fill(lsNumber, algoBit);
                  algo_bits_bx_->Fill(algoBit, itr->getbxNr()); //FIXME: or ibx or getbxInEventNr()?
                  
                  for(int algoBit2 = 0; algoBit2 < L1TnumAlgs; algoBit2++) {
                     if(itr->getAlgoDecisionFinal(algoBit2)) {
                        algo_bits_corr_->Fill(algoBit, algoBit2);
                     }
                  }
               }  
            }
         }
      }
   }
}

// End section
void L1TuGT::endLuminosityBlock(const edm::LuminosityBlock& iLumi, const edm::EventSetup& evtSetup) {
   //empty
}

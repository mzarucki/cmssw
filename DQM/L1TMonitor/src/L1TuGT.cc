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
   runInEventLoop_(params.getUntrackedParameter<bool>("runInEventLoop", false)),
   runInEndLumi_(params.getUntrackedParameter<bool>("runInEndLumi", false)),
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
   
   //algo_bits_corr_ = ibooker.book2D("algo_bits_corr","uGT algorithm trigger bit correlation", 128, -0.5, 127.5, 128, -0.5, 127.5);
   //algo_bits_corr_->setAxisTitle("Algorithm trigger bits", 1);
   //algo_bits_corr_->setAxisTitle("Algorithm trigger bits", 2);
   
   algo_bits_lumi_ = ibooker.book2D("algo_bits_lumi","uGT algorithm trigger bit rate per LS", TotalNrBinsLs, 0., totalNrBinsLs, L1TnumAlgs, -0.5, upL1TnumAlgs);
   algo_bits_lumi_->setAxisTitle("Luminosity segment", 1);
   algo_bits_lumi_->setAxisTitle("Algorithm trigger bits", 2);
   
}

void L1TuGT::analyze(const edm::Event& evt, const edm::EventSetup& evtSetup) {
   //FIXME: Remove duplicate definition of L1TnumAlgs 
   const int L1TnumAlgs = 512;
  
    nrEvJob_++;
   
   if (verbose_) {
      edm::LogInfo("L1TuGT") << "L1TuGT: Analyzing" << std::endl;
   }
   
   // Get the LS block number (to be used in many histograms)
   const int lsNumber = evt.luminosityBlock();
   
   // Open uGT readout record
   edm::Handle<BXVector<GlobalAlgBlk>> uGtAlgs;
   evt.getByToken(l1tuGtSource_, uGtAlgs);
   
   if (!uGtAlgs.isValid()) {
      edm::LogInfo("L1TuGT") << "Cannot find GlobalAlgBlk readout record";
      return;
   }
   // Get uGT algo bit statistics
   else {
      for (int ibx=uGtAlgs->getFirstBX(); ibx <= uGtAlgs->getLastBX(); ++ibx) {

         for (auto itr = uGtAlgs->begin(ibx); itr != uGtAlgs->end(ibx); ++itr ) {

            for(int algBit = 0; algBit < L1TnumAlgs; algBit++) {

               if(itr->getAlgoDecisionFinal(algBit)) {
                  algo_bits_->Fill(algBit);
                  algo_bits_lumi_->Fill(lsNumber, algBit);
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

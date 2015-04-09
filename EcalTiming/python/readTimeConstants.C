#include "Riostream"
#include "TFile"
#include "TProfile2D"
#include "TH2F"

void readTimeConstants()
 {

 // read basic.dat file
 //  file has 5 coulumns of data
 //  but we want to read only first 4 collumns
 
 TString dir = gSystem->UnixPathName(gInterpreter->GetCurrentMacroName());
 dir.ReplaceAll("readTimeConstants.C","");
 dir.ReplaceAll("/./","/");
 ifstream in;
 //in.open(Form("%sbasic.dat",dir.Data()));
 in.open(Form("dumpConstants-0.dat",dir.Data()));

  int x;
  int y;
  int z;
 Float_t t, id;
 Int_t nlines = 0;

 TFile *f = new TFile("TimeCalibs.root","RECREATE");
 TH2F* calibMapEB = new TH2F("calibMapEB","Mean Time map EB [ns];i#phi;i#eta",360,1.,361.,171,-85,86);
 calibMapEB->Sumw2();
 TH2F* calibMapEEM = new TH2F("calibMapEEM","Mean Time map EE-; ix; iy",100,1,101,100,1,101);
 calibMapEEM->Sumw2();
 TH2F* calibMapEEP = new TH2F("calibMapEEP","Mean Time map EE+ ;ix;iy",100,1,101,100,1,101);
 calibMapEEP->Sumw2();

 //while (!in.eof()) {
 while (1) {
      in >> x >> y >> z >> t >> id ;
      if (!in.good()) break;
     // if (nlines < 5)  printf("x=%3i, y=%3i, z=%1i\n, t=%8f\n",x,y,z,t);continue;
      if(z == 0) { 
                     calibMapEB->Fill(y,x,t);
		     //printf("x=%3i, y=%3i, z=%1i\n, t=%8f\n",x,y,z,t);
		     }
      else{
          if( z < 1) { calibMapEEM->Fill(x,y, t);}
	  else{ calibMapEEP->Fill(x,y,t);}
	  }
      nlines++;

   }   


 printf(" found %d points\n",nlines);
 in.close();


//Move empty bins out of the way -- EB
  int nxbins = calibMapEB->GetNbinsX();
  int nybins = calibMapEB->GetNbinsY();
  for (int p=1;p<=nxbins;++p)
  {
    for (int q=1;q<=nybins;++q)
    {
      double binentsM = calibMapEB->GetBinContent(p,q);
      if(binentsM==0)
      {
        calibMapEB->SetBinContent(p,q,-1000);
      }
    }
  }

  //Move empty bins out of the way -- EE
  nxbins = calibMapEEM->GetNbinsX();
  nybins = calibMapEEM->GetNbinsY();
  for (int n=1;n<=nxbins;++n)
  {
    for (int m=1;m<=nybins;++m)
    {
      double binentsM = calibMapEEM->GetBinContent(n,m);
      if(binentsM==0)
      {
        calibMapEEM->SetBinContent(n,m,-1000);
      }
      double binentsP = calibMapEEP->GetBinContent(n,m);
      if(binentsP==0)
      {
        calibMapEEP->SetBinContent(n,m,-1000);
      }
    }
  }

int min = -10;

int max = 10;

calibMapEB->GetZaxis()->SetRangeUser(min, max); // ... set the range ...
calibMapEEM->GetZaxis()->SetRangeUser(min, max); // ... set the range ...
calibMapEEP->GetZaxis()->SetRangeUser(min, max); // ... set the range ...
 f->Write();

 }

#!usr/bin/python
import sys, math, os
import ROOT
from ROOT import TFile, TH1, TH1F, TCanvas, TLegend, TGraph, TGraphErrors, gROOT, gPad, TAttText, TText, TGaxis, TMath
from array import array

gROOT.Reset()
infile="inputfile.txt"#"inputfile_complete.txt"
#date=[]
timeEBPlus=[]
timeEBMinus=[]
timeEEPlus=[]
timeEEMinus=[]
stdvEBPlus=[]
stdvEBMinus=[]
stdvEEPlus=[]
stdvEEMinus=[]
luminosity=[]
occEBPlus=[]
fakeHisto   = TH1F("fakeHisto", "date", 3,0,3)
fakeHisto_1 = TH1F("fakeHisto_1", "run number", 3,0,3)
fakeHisto_2 = TH1F("fakeHisto_2", "run number for date", 3,0,3)
h1_lumi     = TH1F("h1_lumi", "run lumi", 3,0,3)
counter=.5
#g1_EBPlus  = TGraphErrors(0)
#g1_EBMinus = TGraphErrors(0)
#g1_EEPlus  = TGraphErrors(0)
#g1_EEMinus = TGraphErrors(0)
x=[]

t = TText()
t_numb = TText()
t.SetTextAngle(70)
t.SetTextSize(0.02)
t.SetTextAlign(33)
t_numb.SetTextAngle(85)
t_numb.SetTextSize(0.02)
t_numb.SetTextAlign(33)

t1 = TText()
t1.SetTextAngle(70)
t1.SetTextSize(0.025) #0.025
t1.SetTextAlign(33)

t2 = TText()
t2.SetTextAngle(85)
t2.SetTextSize(0.025)
t2.SetTextAlign(33)

yMax=.4
yMin=-1.3
#can2 = TCanvas('test2','test',10,10,800,800)#1)
#fakeHisto.SetBit(kCanRebin)
for line in open(infile):
    column = line.split()
    print column[0], column[1]###, column[2]
    date=column[1].replace("_"," ")
    fakeHisto.Fill(date,0)
 ###   h1_lumi.Fill(date,float(column[2]))
    #X = fakeHisto.GetXaxis().GetBinCenter(int(counter+.5));
    #y = gPad.GetUymin() - 0.2*fakeHisto.GetYaxis().GetBinWidth(1);
    #t.DrawText(X,y,date);
    fakeHisto_1.Fill(column[0], 0)
    fakeHisto_2.Fill(column[0], 0)
    print date
    f = TFile.Open("/afs/cern.ch/work/s/sgelli/private/CMSSW_Timing/src/EcalTiming/EcalTiming/test/output/"+column[0]+"_AlCaPhiSym_reduced.root")
    #occEBPlus = f.Get('occEBP')
    #occEBMinus = f.Get('occEBM')
    #occEEPlus = f.Get('occEEP')
    #occEEMinus = f.Get('occEEM')
    h_EBPlus = f.Get('timeEBPlus_1')
    h_EBMinus = f.Get('timeEBMinus_1')
    h_EEPlus = f.Get('timeEEPlus_1')
    h_EEMinus = f.Get('timeEEMinus_1')
    timeEBPlus.append(h_EBPlus.GetMean())
    timeEBMinus.append(h_EBMinus.GetMean())
    timeEEPlus.append(h_EEPlus.GetMean())
    timeEEMinus.append(h_EEMinus.GetMean())
    h_stdv_EBPlus = f.Get('EBPlus_stdv')
    h_stdv_EBMinus = f.Get('EBMinus_stdv')
    h_stdv_EEPlus = f.Get('EEPlus_stdv')
    h_stdv_EEMinus = f.Get('EEMinus_stdv')
    stdvEBPlus.append(h_EBPlus.GetMean())
    stdvEBMinus.append(h_EBMinus.GetMean())
    stdvEEPlus.append(h_EEPlus.GetMean())
    stdvEEMinus.append(h_EEMinus.GetMean())
    #g1_EBPlus.SetPoint(int(counter+.5), counter, h_EBPlus.GetMean())
    #g1_EBPlus.SetPointError(int(counter+.5), 0, h_EBPlus.GetRMS()/math.sqrt(occEBPlus.GetBinContent(1)))
    #g1_EBMinus.SetPoint(int(counter+.5), counter, h_EBMinus.GetMean())
    #g1_EBMinus.SetPointError(int(counter+.5), 0, h_EBMinus.GetRMS()/math.sqrt(occEBMinus.GetBinContent(1)))
    #g1_EEPlus.SetPoint(int(counter+.5), counter, h_EEPlus.GetMean())
    #g1_EEPlus.SetPointError(int(counter+.5), 0, h_EEPlus.GetRMS()/math.sqrt(occEEPlus.GetBinContent(1)))
    #g1_EEMinus.SetPoint(int(counter+.5), counter, h_EBPlus.GetMean())
    #g1_EEMinus.SetPointError(int(counter+.5), 0, h_EEMinus.GetRMS()/math.sqrt(occEEMinus.GetBinContent(1)))
    print timeEBPlus[int(counter-.5)]
    print counter
    x.append(counter)
    os.system("echo "+column[0]+" "+str(timeEBPlus[int(counter-.5)])+" "+str(timeEBMinus[int(counter-.5)])+" "+str(timeEEPlus[int(counter-.5)])+" "+str(timeEEMinus[int(counter-.5)])+" >> distr_tot.txt")
    counter+=1



vy1_EBPlus = array('d', timeEBPlus)
vy1_EBMinus = array('d', timeEBMinus)
vy1_EEPlus = array('d', timeEEPlus)
vy1_EEMinus = array('d', timeEEMinus)
vx1 = array('d', x)
print len(vx1)
g1_EBPlus  = TGraph(len(vx1),vx1,vy1_EBPlus)
g1_EBMinus = TGraph(len(vx1),vx1,vy1_EBMinus)
g1_EEPlus  = TGraph(len(vx1),vx1,vy1_EEPlus)
g1_EEMinus = TGraph(len(vx1),vx1,vy1_EEMinus)

#graphs for stdv
vy1_stdv_EBPlus = array('d', timeEBPlus)
vy1_stdv_EBMinus = array('d', timeEBMinus)
vy1_stdv_EEPlus = array('d', timeEEPlus)
vy1_stdv_EEMinus = array('d', timeEEMinus)
vx1 = array('d', x)
g1_stdv_EBPlus  = TGraph(len(vx1),vx1,vy1_stdv_EBPlus)
g1_stdv_EBMinus = TGraph(len(vx1),vx1,vy1_stdv_EBMinus)
g1_stdv_EEPlus  = TGraph(len(vx1),vx1,vy1_stdv_EEPlus)
g1_stdv_EEMinus = TGraph(len(vx1),vx1,vy1_stdv_EEMinus)

g1_EBPlus.SetMarkerStyle(20)
g1_EBMinus.SetMarkerStyle(20)
g1_EEPlus.SetMarkerStyle(20)
g1_EEMinus.SetMarkerStyle(20)

g1_EBPlus.SetMarkerColor(1)
g1_EBMinus.SetMarkerColor(2)
g1_EEPlus.SetMarkerColor(3)
g1_EEMinus.SetMarkerColor(4)

fakeHisto.GetXaxis().SetLabelOffset(99)
fakeHisto_1.GetXaxis().SetLabelOffset(99)
fakeHisto_2.GetXaxis().SetLabelOffset(99)

fakeHisto_1.GetYaxis().SetRangeUser(yMin,yMax)
fakeHisto_2.GetYaxis().SetRangeUser(yMin,yMax)
fakeHisto.SetLineColor(0)
fakeHisto_1.SetLineColor(0)
fakeHisto_2.SetLineColor(0)
fakeHisto.LabelsDeflate()
fakeHisto_1.LabelsDeflate()
fakeHisto_2.LabelsDeflate()
fakeHisto.SetStats(0)
fakeHisto_1.SetStats(0)
fakeHisto_2.SetStats(0)
w = 800;
h = 800;
can = TCanvas('test','test',5,5,2000,800)
#can.SetWindowSize(w + (w - can.GetWw()), h + (h - can.GetWh()));
can.SetBottomMargin(.15)
can.SetRightMargin(0.09)
can.SetLeftMargin(0.09)
fakeHisto.GetYaxis().SetRangeUser(yMin,yMax)
#fakeHisto.GetXaxis().SetTextAngle(180)
fakeHisto.Draw()
counter1=0
counterDate=0
y = gPad.GetUymin() - 1.35*fakeHisto.GetYaxis().GetBinWidth(1);
string_tmp=""
outF = open('outForLaser.txt', 'w')
for line in open(infile):
  column = line.split()
  date=column[1].replace("_"," ")
  date=date.replace("'","")
  X = fakeHisto.GetXaxis().GetBinCenter(counter1);
  if date==string_tmp: 
    t.DrawText(X+.8,y,"      ");
  else:
    print >> outF, column[0], column[1].replace("'","")
    if counterDate%2 == 0: #to just print every 2 different days avoiding a messy x-axis
      t.DrawText(X+.8,y,date);
      counterDate+=1
    else:
      t.DrawText(X+.8,y,"      ");
      counterDate+=1
    #t.DrawText(X+.8,y,date);
  #y = gPad.GetUymin() + .5*fakeHisto.GetYaxis().GetBinWidth(1);
  #t_numb.DrawText(X+.8,y,column[0]);
  string_tmp=date
  counter1+=1

outF.close()
g1_EBPlus.Draw("zp")

g1_EBMinus.Draw("zpSAME")
g1_EEPlus.Draw("zpSAME")
g1_EEMinus.Draw("zpSAME")

can.SaveAs("history_date.png")
can.SaveAs("history_date.pdf")

can1 = TCanvas('test1','test',5,5,2000,600)
#can1.SetTopMargin(.15)
can1.SetBottomMargin(.15)
can1.SetRightMargin(0.01)
can1.SetLeftMargin(0.05)
#can.SetWindowSize(1000 + (2000 - can.GetWw()), 600 + (600 - can.GetWh()));
#can1.SetGridy(1)
fakeHisto_1.Draw()
#t1.SetTextSize(.02)
y = gPad.GetUymin() - 1.35*fakeHisto_1.GetYaxis().GetBinWidth(1);
counter1=0
for line in open(infile):
   column = line.split()
   X = fakeHisto_1.GetXaxis().GetBinCenter(counter1);
   #t1.DrawText(X+.8,y,column[0]);

   if counter1%5 == 0: #to just print every 5 run_number avoiding a messy x-axis
      t1.DrawText(X+.8,y,column[0]);
   else:
      t1.DrawText(X+.8,y,"      ");
   counter1+=1

g1_EBPlus.Draw("zp")
g1_EBMinus.Draw("zpSAME")
g1_EEPlus.Draw("zpSAME")
g1_EEMinus.Draw("zpSAME")

#fakeHisto_1.Draw("SAME")

can1.SaveAs("history_runnumber.png")
can1.SaveAs("history_runnumber.pdf")



can2 = TCanvas('test1','test',5,5,2000,600)
can2.SetBottomMargin(.15)
can2.SetRightMargin(0.01)
can2.SetLeftMargin(0.05)

fakeHisto_1.Draw()
y = gPad.GetUymin() - 1.03*fakeHisto_1.GetYaxis().GetBinWidth(1);
counter1=0
for line in open(infile):
  column = line.split()
  X = fakeHisto_1.GetXaxis().GetBinCenter(counter1);
  
  t2.DrawText(X+.8,y,column[0]);
  counter1+=1
 
g1_EBPlus.Draw("zp")
g1_EBMinus.Draw("zpSAME")
g1_EEPlus.Draw("zpSAME")
g1_EEMinus.Draw("zpSAME")






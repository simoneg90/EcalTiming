import ROOT
from EcalTiming.EcalTiming.PlotUtils import customROOTstyle,customPalette

import sys

customROOTstyle()
ROOT.gROOT.SetBatch(True)
filename = sys.argv[1]

detectors = {-1:"EEM", 0:"EB", 1:"EEP"}

outdir = "plots"
if len(sys.argv) > 2:
	outdir = sys.argv[2]

file = ROOT.TFile.Open(filename)

def float2name(x):
	return ("%.1f" % x).replace('.','_')

def initHist(name,title,iz):
	if iz == 0:
		return ROOT.TProfile2D("EB_" + name,title,360,1,361,171,-85,86)
	elif iz == -1:
		return ROOT.TProfile2D("EEM_" + name,title,100,1,101,100,1,101)
	elif iz == 1:
		return ROOT.TProfile2D("EEP_" + name,title,100,1,101,100,1,101)
	else:
		print "bad iz value",iz
		return None
	
def initHists(hist_dict,key, name, title):
	if key in hist_dict:
		return
	cut,iz = key
	hist_dict[key] = initHist(name,title,iz)

tree = file.Get("TriggerResults/EcalSplashTiming_0/energyStabilityTree")
c = ROOT.TCanvas()
time = dict()
occupancy = dict()
energy = dict()
counter = 0
for event in tree:
	if not counter % (tree.GetEntries()/10): print counter, '/', tree.GetEntries()
	counter += 1
	index = ord(event.index)
	cut_str = str(index)
	iz = ord(event.iz)
	if iz == 255: iz = -1
	key = (index,iz)
	initHists(time,key,"time_" + cut_str, "Timing: step" + cut_str)
	initHists(occupancy,key,"occupancy_" + cut_str, "Occupancy: step" + cut_str)
	initHists(energy,key,"energy_" + cut_str, "Energy: step" + cut_str)
	
	if iz == 0:
		x = event.iy
		y = event.ix
	else:
		x = event.ix
		y = event.iy

	time[key].Fill(x, y, event.time)
	occupancy[key].Fill(x, y, event.num)
	energy[key].Fill(x, y, event.energy)


c = ROOT.TCanvas()
for key in time:
	time[key].SetAxisRange(-10,10,"Z")
	time[key].SetZTitle("[ns]")
	time[key].Draw("colz")
	c.SaveAs(outdir + "/" + time[key].GetName() + ".png")

c.SetLogz(True)
occu_max = max( [ occupancy[key].GetMaximum() for key in occupancy])
for key in occupancy:
	occupancy[key].SetAxisRange(0,occu_max,"Z")
	occupancy[key].SetZTitle("Events")
	occupancy[key].Draw("colz")
	c.SaveAs(outdir + "/" + occupancy[key].GetName() + ".png")

c.SetLogz(False)
en_max = max( [ energy[key].GetMaximum() for key in energy])
en_max = 5.0
for key in energy:
	energy[key].Draw("colz")
	energy[key].SetAxisRange(0,en_max,"Z")
	energy[key].SetZTitle("[GeV]")
	c.SaveAs(outdir + "/" + energy[key].GetName() + ".png")

for iz in [-1,0,1]:
	keys = sorted([ (cut,iz) for cut,i in time if i == iz])
	for i in range(1,len(keys)):
		c.SetLogz(False)
		customPalette()
		hrel = initHist("time_rel_%d_%d" % (i, i-1))
		h1 = time[keys[i]]
		h0 = time[keys[i-1]]
		hrel.Add(h1,h0,1,-1)
		hrel.SetAxisRange(-.2,.2,"Z")
		hrel.SetTitle(detectors[iz] + " Time Diff Step%d - Step%d" % (i, i-1))
		hrel.Draw("colz")
		c.SaveAs(outdir + "/" + hrel.GetName() + ".png")
		
		if i != 1:
			hrel0 = initHist("time_rel_%d_%d" % (i, 0))
			hrel.SetAxisRange(-.2,.2,"Z")
			hrel0.SetTitle(detectors[iz] + " Time Diff Step%d - Step%d" % (i,0))
			hrel0.Draw("colz")
			c.SaveAs(outdir + "/" + hrel0.GetName() + ".png")

		c.SetLogz(True)
		ROOT.gStyle.SetPalette(55)
		hnum = occupancy[keys[i]]
		hnumold = occupancy[keys[i-1]]
		hnumold.Add(hnum,-1)
		hnumold.SetTitle(detectors[iz] + " Num Diff Step%d - Step%d" % (keys[i][0],keys[i-1][0]))
		hnumold.SetAxisRange(0,hnumold.GetBinContent(hnumold.GetMaximumBin()),"Z")
		hnumold.Draw("colz")
		c.SaveAs(outdir + "/" + hnum.GetName() + "_" + str(keys[i-1][0]) + "_rel.png")

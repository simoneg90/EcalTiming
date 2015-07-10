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

def initHists(hist_dict,key, name, title):
	if key in hist_dict:
		return
	cut,iz = key
	if iz == 0:
		hist_dict[key] = ROOT.TProfile2D("EB_"  + name,title,171,-85,86,360,1,361)
	elif iz == -1:
		hist_dict[key] = ROOT.TProfile2D("EEM_" + name,title,100,1,101,100,1,101)
	elif iz == 1:
		hist_dict[key] = ROOT.TProfile2D("EEP_" + name,title,100,1,101,100,1,101)
	else:
		print "bad iz value",iz


tree = file.Get("TriggerResults/EcalSplashTiming_0/energyStabilityTree")
c = ROOT.TCanvas()
time = dict()
occupancy = dict()
energy = dict()
counter = 0
for event in tree:
	if not counter % (tree.GetEntries()/10): print counter, '/', tree.GetEntries()
	counter += 1
	cut = event.min_energy
	cut_str = float2name(cut)
	iz = ord(event.iz)
	if iz == 255: iz = -1
	key = (cut,iz)
	initHists(time,key,"time_" + cut_str, "Timing with E > %.1f" % cut)
	initHists(occupancy,key,"occupancy_" + cut_str, "Occupancy with E > %.1f" % cut)
	initHists(energy,key,"energy_" + cut_str, "Energy with E > %.1f" % cut)

	time[key].Fill(event.ix, event.iy, event.time)
	occupancy[key].Fill(event.ix, event.iy, event.num)
	energy[key].Fill(event.ix, event.iy, event.energy)


c = ROOT.TCanvas()
for key in time:
	time[key].Draw("colz")
	time[key].GetZaxis().SetRangeUser(-10,10)
	c.SaveAs(outdir + "/" + time[key].GetName() + ".png")

c.SetLogz(True)
occu_max = max( [ occupancy[key].GetMaximum() for key in occupancy])
for key in occupancy:
	occupancy[key].Draw("colz")
	occupancy[key].GetZaxis().SetRangeUser(0,occu_max)
	c.SaveAs(outdir + "/" + occupancy[key].GetName() + ".png")

c.SetLogz(False)
en_max = max( [ energy[key].GetMaximum() for key in energy])
en_max = 5.0
for key in energy:
	energy[key].Draw("colz")
	energy[key].GetZaxis().SetRangeUser(0,en_max)
	c.SaveAs(outdir + "/" + energy[key].GetName() + ".png")

customPalette()
for iz in [-1,0,1]:
	keys = sorted([ (cut,iz) for cut,i in time if i == iz])
	for i in range(1,len(keys)):
		h = time[keys[i]]
		hold = time[keys[i-1]]
		hold.Add(h,-1)
		hold.Scale(-1)
		hold.GetZaxis().SetRangeUser(-.2,.2)
		hold.SetTitle(detectors[iz] + " Diff  (E > %.1f) - (E > %.1f) " % (keys[i][0],keys[i-1][0]))
		hold.Draw("colz")
		c.SaveAs(outdir + "/" + h.GetName() + "_rel.png")

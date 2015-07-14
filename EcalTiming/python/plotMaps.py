import ROOT
from EcalTiming.EcalTiming.PlotUtils import customROOTstyle, customPalette
import math

import os
import sys
import errno
import shutil


detectors = {-1: "EEM", 0: "EB", 1: "EEP"}


def float2name(x):
	return ("%.1f" % x).replace('.', '_')


def initMap(name, title, iz):
	if iz == 0:
		h = ROOT.TProfile2D("EB_" + name, title, 360, 1, 361, 171, -85, 86)
		xtitle = "i#phi"
		ytitle = "i#eta"
	elif iz == -1:
		h = ROOT.TProfile2D("EEM_" + name, title, 100, 1, 101, 100, 1, 101)
		xtitle = "ix"
		ytitle = "iy"
	elif iz == 1:
		h = ROOT.TProfile2D("EEP_" + name, title, 100, 1, 101, 100, 1, 101)
		xtitle = "ix"
		ytitle = "iy"
	else:
		print "bad iz value", iz
		return None
	h.SetXTitle(xtitle)
	h.SetYTitle(ytitle)
	return h


def inittime1d(name, title, iz):
	if iz == 0:
		det = "EB_"
	elif iz == -1:
		det = "EEM_"
	elif iz == 1:
		det = "EEP_"
	else:
		print "bad iz value", iz
		return None
	h = ROOT.TH1F(det + name, title, 50, -10, 10)
	h.SetXTitle("Time [ns]")
	h.SetYTitle("Events")
	return h


def initiRing(name, title, iz):
	if iz == 0:
		h = ROOT.TProfile("EB_" + name, title, 171, -85, 86)
	elif iz == -1:
		h = ROOT.TProfile("EEM_" + name, title, 39, 0, 39)
	elif iz == 1:
		h = ROOT.TProfile("EEP_" + name, title, 39, 0, 39)
	else:
		print "bad iz value", iz
		return None
	h.SetXTitle("iRing")
	h.SetYTitle("Mean Time [ns]")
	return h

def initEvsT(name, title, iz):
	if iz == 0:
		det = "EB" 
	elif iz == -1:
		det = "EEM" 
	elif iz == 1:
		det = "EEP" 
	else:
		print "bad iz value", iz
		return None
	h = ROOT.TH2F(det + name, title, 50,0,20,100,-10,10) 
	h.SetXTitle("Energy [GeV]")
	h.SetYTitle("Time [ns]")
	return h

def initHists(hist_dict, init_func, key, name, title):
	if key in hist_dict:
		return
	iz = key
	hist_dict[key] = init_func(name, title, iz)


def plotMaps(file, tree, outdir):
	c = ROOT.TCanvas()
	# dictionaries to store histograms
	time = dict()
	occupancy = dict()
	energy = dict()
	iRing = dict()
	time1d = dict()
	EvsT = dict()
	counter = 0

	print "Found", tree.GetEntries(), "entries"
	total_rechits = 0
	if tree.GetEntries() == 0: sys.exit(-1)
	for event in tree:
		if not counter % (tree.GetEntries()/10): print counter, '/', tree.GetEntries()
		counter += 1
		if event.num == 0: continue
		total_rechits += event.num
		# make dictionary key
		iz = ord(event.iz)
		if iz == 255: iz = -1
		key = iz
		if math.isnan(event.time): 
			print "Found nan", event.rawid, event.ix, event.iy, iz, event.num
			continue
		# initialize histograms (if they haven't been made yet
		initHists(time, initMap, key, "time", "Time [ns]")
		initHists(occupancy, initMap, key, "occupancy", "Occupancy")
		initHists(energy, initMap, key, "energy", "Energy [GeV]")

		initHists(iRing, initiRing, key, "iRing", "iRing")
		initHists(time1d, inittime1d, key, "time1d", "time1d")
		initHists(EvsT, initEvsT, key, "EvsT", "EvsT")
		
		# fill histograms
		if iz == 0:
			x = event.iy
			y = event.ix
		else:
			x = event.ix
			y = event.iy
		

		time[key].Fill(x, y, event.time)
		occupancy[key].Fill(x, y, event.num)
		energy[key].Fill(x, y, event.energy)

		iRing[key].Fill(event.iRing, event.time)
		time1d[key].Fill(event.time)
		EvsT[key].Fill(event.energy, event.time)

	print "Run contained",total_rechits, "rechits" 
	c = ROOT.TCanvas()
	for key in time:
		time[key].SetAxisRange(-10, 10, "Z")
		time[key].SetZTitle("[ns]")
		time[key].Draw("colz")
		c.SaveAs(outdir + "/" + time[key].GetName() + ".png")

	c.SetLogz(True)
	occu_max = max( [ occupancy[key].GetMaximum() for key in occupancy])
	for key in occupancy:
		occupancy[key].SetAxisRange(0, occu_max, "Z")
		occupancy[key].SetZTitle("Events")
		occupancy[key].Draw("colz")
		c.SaveAs(outdir + "/" + occupancy[key].GetName() + ".png")

	c.SetLogz(False)
	en_max = max( [ energy[key].GetMaximum() for key in energy])
	en_max = 5.0
	for key in energy:
		energy[key].Draw("colz")
		energy[key].SetAxisRange(0, en_max, "Z")
		energy[key].SetZTitle("[GeV]")
		c.SaveAs(outdir + "/" + energy[key].GetName() + ".png")

	for key in iRing:
		graph = ROOT.TGraphErrors(iRing[key])
		graph.Draw("AP")
		iRing[key].Draw()
		c.SaveAs(outdir + "/" + iRing[key].GetName() + ".png")
	
	for key in EvsT:
		EvsT[key].Draw("colz")
		c.SaveAs(outdir + "/" + EvsT[key].GetName() + ".png")

	ROOT.gStyle.SetOptStat(1111)
	for key in time1d:
		time1d[key].Draw()
		c.SaveAs(os.path.join(outdir, time1d[key].GetName() + ".png"))

if __name__ == "__main__":

	customROOTstyle()
	ROOT.gROOT.SetBatch(True)
	filename = sys.argv[1]

	outdir = "plots"
	if len(sys.argv) > 2:
		outdir = sys.argv[2]
	elif filename.startswith("output"):
		# use same path as input file with output -> plots
		outdir = os.path.normpath(os.path.join("plots" , '/'.join(filename.split('/')[1: -1])))

	def mkdir_p(path):
		try:
			os.makedirs(path)
		except OSError as exc: # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else: raise

	mkdir_p(outdir)
	shutil.copy("plots/index.php", outdir)

	file = ROOT.TFile.Open(filename)
	tree = file.Get("TriggerResults/EcalSplashTiming_0/timingTree")
	plotMaps(file, tree, outdir)




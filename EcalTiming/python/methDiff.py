import ROOT
import  EcalTiming.EcalTiming.loadOldCalib as cal
from EcalTiming.EcalTiming.PlotUtils import customROOTstyle, makePlotFolder
import sys,os
import shutil
import errno
import numpy as np

colors = [ROOT.kBlack, ROOT.kBlue, ROOT.kRed, ROOT.kGreen, ROOT.kCyan, ROOT.kMagenta, ROOT.kOrange - 3, ROOT.kYellow -2, ROOT.kGreen - 3, ROOT.kCyan - 3]

def mapDiff(outdir, map1, map2, name1, name2, errs=[]):

	diffMap = cal.addCalib(map1, map2, -1, 1)
	
	ROOT.gStyle.SetOptStat(1100)
	if errs:
		resMap = cal.divideCalib(map1, errs)
		cal.plot1d(resMap,outdir, "resmap" + name2 + "_" + name1, -2, 2, xtitle="diff/timeError")
	cal.plot1d(diffMap, outdir,  "diff" + name2 + "_" + name1, -2, 2)
	ROOT.gStyle.SetOptStat(0)
	cal.plot2d(diffMap, outdir,  "diffMap" + name2 + "_" + name1, -1, 1)
	ringdiff = cal.plotiRing(diffMap, outdir,  "iRing" + name2 + "_" + name1)
	return ringdiff

def plotAvePerMap(hist_name, maps, names):

	nmaps = len(maps)
	if nmaps != len(names):
		print "LENGTH MISMATCH"
		return

	Boff_start1 = "254292"
	Boff_end1   = "254608"
	Boff_start2 = "255981"
	Boff_end2   = "256237"
	aves = dict()
	#aves[0]      = ("EB_ave_"  + hist_name, "EB",  np.zeros(nmaps))
	aves[(0,-1)] = ("EBM_ave_" + hist_name, "EB-", np.zeros(nmaps))
	aves[(0,1)]  = ("EBP_ave_" + hist_name, "EB+", np.zeros(nmaps))
	aves[-1]     = ("EEM_ave_" + hist_name, "EE-", np.zeros(nmaps))
	aves[1]      = ("EEP_ave_" + hist_name, "EE+", np.zeros(nmaps))
	sds = dict()
	#sds[0]      = ("EB_stddev_"  + hist_name, "EB",  np.zeros(nmaps))
	sds[(0,-1)] = ("EBM_stddev_" + hist_name, "EB-", np.zeros(nmaps))
	sds[(0,1)]  = ("EBP_stddev_" + hist_name, "EB+", np.zeros(nmaps))
	sds[-1]     = ("EEM_stddev_" + hist_name, "EE-", np.zeros(nmaps))
	sds[1]      = ("EEP_stddev_" + hist_name, "EE+", np.zeros(nmaps))
	
	for i in range(nmaps):
		ave,stddev = cal.calcMean(maps[i])
		for k in aves:
			aves[k][2][i] = ave[k]
			sds[k][2][i] = stddev[k]

	
	x1 = ROOT.gStyle.GetPadLeftMargin();
	x2 = 1 - ROOT.gStyle.GetPadRightMargin();
	y2 = 1 - ROOT.gStyle.GetPadTopMargin();
	y1 = y2 - .1
	leg = ROOT.TLegend(x1,y1,x2,y2)
	leg.SetNColumns(5)
	c = ROOT.TCanvas("c","c",1600,1200)
	h = ROOT.TH1F("test","",1000,-.1,1.1)
	h.SetLineColor(0)
	h.SetFillColor(19)
	leg.AddEntry(h,"Boff","f")
	x = np.linspace(0,1,nmaps)
	h.GetXaxis().SetTitle("")
	h.GetYaxis().SetTitle("Average Time[ns]")
	for i in range(nmaps):
		bin = h.FindBin(x[i])
		h.GetXaxis().SetBinLabel(bin,names[i])
		if names[i] == Boff_start1:
			b1_x1 = x[i]
		if names[i] == Boff_start2:
			b2_x1 = x[i]
		if names[i] == Boff_end1:
			b1_x2 = x[i]
		if names[i] == Boff_end2:
			b2_x2 = x[i]

	h.SetTitle("")
	h.SetMinimum(-.5)
	h.SetMaximum(.5)
	h.Draw()
	box1 = ROOT.TBox(b1_x1,-0.5,b1_x2,0.5)
	box2 = ROOT.TBox(b2_x1,-0.5,b2_x2,0.5)
	box1.Draw()
	box2.Draw()
	ci = 0
	mg_ave = ROOT.TMultiGraph()
	for name,leg_name,ave in aves.values():
		g = ROOT.TGraph(nmaps,x,ave)
		g.SetLineColor(colors[ci % len(colors)])
		g.SetLineWidth(2)
		mg_ave.Add(g)
		leg.AddEntry(g,leg_name,"lp")
		ci += 1
	leg.Draw()
	mg_ave.Draw("LP")
	c.SaveAs(outdir + "/ave_" +  hist_name + ".png")

	h.GetYaxis().SetTitle("Standard Deviation [ns]")
	h.SetMinimum(0)
	h.SetMaximum(.5)
	h.SetTitle("")
	h.Draw()
	box1 = ROOT.TBox(b1_x1,0,b1_x2,0.5)
	box2 = ROOT.TBox(b2_x1,0,b2_x2,0.5)
	box1.Draw()
	box2.Draw()
	ci = 0
	mg_stddev = ROOT.TMultiGraph()
	for name,__,stddev in sds.values():
		g = ROOT.TGraph(nmaps,x,stddev)
		g.SetLineColor(colors[ci % len(colors)])
		g.SetLineWidth(2)
		mg_stddev.Add(g)
		ci += 1
	leg.Draw()
	mg_stddev.Draw("LP")
	c.SaveAs(outdir + "/stddev_" +  hist_name + ".png")

def listDiff(hist_name, maps1, maps2, names1, names2, errs=[]):
	mg = dict()
	mg[0]  = ("EB_" + hist_name,ROOT.TMultiGraph())
	mg[-1] = ("EEM_" + hist_name,ROOT.TMultiGraph())
	mg[1]  = ("EEP_" + hist_name,ROOT.TMultiGraph())

	
	x1 = ROOT.gStyle.GetPadLeftMargin();
	x2 = 1 - ROOT.gStyle.GetPadRightMargin();
	y1 = ROOT.gStyle.GetPadBottomMargin();
	y2 = y1 + .1
	leg = ROOT.TLegend(x1,y1,x2,y2)
	leg.SetNColumns(4)
	nmaps = len(maps1)
	if nmaps != len(maps2) or nmaps != len(names1) or nmaps!= len(names2):
		print "LENGTH MISMATCH"
		return

	for i in range(nmaps):
		ringDiff = mapDiff(outdir, maps1[i], maps2[i], names1[i], names2[i], errs=errs[i] if errs else [])
		for j in ringDiff:
			g = ROOT.TGraphErrors(ringDiff[j])
			g.SetLineColor(colors[i % len(colors)] )
			mg[j][1].Add(g)
		leg.AddEntry(g,names2[i] + " - " + names1[i])

	for name,g in mg.values():
		c = ROOT.TCanvas("c","c",1600,1200)
		g.Draw("ALP")
		g.GetXaxis().SetTitle("#eta Ring")
		g.GetYaxis().SetTitle("Average Time[ns]")
		leg.Draw()
		c.SaveAs(outdir + "/" +  name + ".png")

if __name__ == "__main__":
	customROOTstyle()
	ROOT.gROOT.SetBatch(True)
	file_pattern = sys.argv[1]

	dir, basename = os.path.split(file_pattern)
	dir = dir.split('/')
	print dir[-1:]
	outdir = '/'.join(dir[:-1]) + "/plots/" + "/" + sys.argv[2] + "/"
	outdir = os.path.normpath(outdir)

	print outdir
	makePlotFolder(outdir)

	subs =  sys.argv[3:]
	files = [ file_pattern % s for s in subs ]
	maps =  [ cal.getCalibFromFile(file) for file in files ]
	maps_err =  [ cal.getErrorFromFile(file) for file in files ]
	
	print files
	print outdir
   #do diff each step
	plotAvePerMap("PerRun", maps, subs)
	#listDiff( sys.argv[2], maps[:-1], maps[1:], subs[:-1], subs[1:], errs=maps_err[:-1])
   #do diff with respect to first
	#listDiff(sys.argv[2] + "_base", maps[:1]*(len(maps)-1), maps[1:], subs[:1]*(len(maps) -1), subs[1:], errs=maps_err[:-1])


import ROOT
import CalibCalorimetry.EcalTiming.TokenRing as TokenRing
from CalibCalorimetry.EcalTiming.PlotUtils import customROOTstyle, drawMultipleGrid

def makeMap(tree, attribute):
	EB = ROOT.TProfile2D(attribute + "EB",attribute + " EB",360,1,361,85*2,-84,86) 
	EEP = ROOT.TProfile2D(attribute + "EEP",attribute + " EEP", 100, 1, 101, 100, 1, 101)
	EEM = ROOT.TProfile2D(attribute + "EEM",attribute + " EEM", 100, 1, 101, 100, 1, 101)

	for crystal in tree:
		att = getattr(crystal, attribute)
		if crystal.ix != -999:
			if crystal.iz == 1:
				EEP.Fill(crystal.ix, crystal.iy, att)
			else:
				EEM.Fill(crystal.ix, crystal.iy, att)
		else:
			EB.Fill(crystal.iphi, crystal.ieta, att)
	return [EEM, EB, EEP]

def makeTRMap(tree):
	attribute = "TR"
	EB = ROOT.TProfile2D(attribute + "EB",attribute + " EB",360,1,361,85*2,-84,86) 
	EEP = ROOT.TProfile2D(attribute + "EEP",attribute + " EEP", 100, 1, 101, 100, 1, 101)
	EEM = ROOT.TProfile2D(attribute + "EEM",attribute + " EEM", 100, 1, 101, 100, 1, 101)

	for crystal in tree:
		att = getattr(crystal, attribute)
		if att < 0:
			continue
		if crystal.ix != -999:
			if crystal.iz == 1:
				EEP.Fill(crystal.ix, crystal.iy, att)
			else:
				EEM.Fill(crystal.ix, crystal.iy, att)
		else:
			EB.Fill(crystal.iphi, crystal.ieta, att)
	return [EEM, EB, EEP]


customROOTstyle()
ROOT.gROOT.SetBatch(True)

f = ROOT.TFile("EcalTPGParam.root", "UPDATE")

tpgmap = f.Get("tpgmap")

import numpy as n

TR = n.array([0],n.int32)

TR_branch = tpgmap.Branch('TR', TR, 'TR/I')

for crystal in tpgmap:
	fed = crystal.fed
	CCU = crystal.CCU
	TR[0] = 0
	TR[0] = TokenRing.fed_ccu2tr[(fed,CCU)]
	TR_branch.Fill()

tpgmap.Write("",ROOT.TObject.kOverwrite)

CCU = makeMap(tpgmap, "CCU")
fed = makeMap(tpgmap, "fed")
tokenring = makeTRMap(tpgmap)

fedEEM = [601,609]
fedEB = [610,645]
fedEEP = [646,654]
fedlimits = [fedEEM, fedEB, fedEEP]

CCUEEM = [1,42]
CCUEB = [1,72]
CCUEEP = [1,42]
CCUlimits = [CCUEEM, CCUEB, CCUEEP]

drawMultipleGrid(fed + CCU, "plots/elec-fed-CCU.png",limits=fedlimits + CCUlimits)
drawMultipleGrid(tokenring, "plots/elec-tokenring.png", limits = [[1,8],[1,8],[1,8]])


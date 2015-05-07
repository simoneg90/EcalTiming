import ROOT
from CalibCalorimetry.EcalTiming.PlotUtils import customROOTstyle

def saveEventTimingPlots(eventdir):
	customROOTstyle()
	ROOT.gROOT.SetBatch(True)

	eventName = eventdir.GetName()
	timehist = {
			"EB":eventdir.Get('TimeMapEB'),
			"EEP": eventdir.Get('TimeMapEEP'),
			"EEM": eventdir.Get('TimeMapEEM'),
			"EB_OOT":eventdir.Get('TimeMapEB_OOT'),
			"EEP_OOT": eventdir.Get('TimeMapEEP_OOT'),
			"EEM_OOT": eventdir.Get('TimeMapEEM_OOT'),
			}

	text = {}

	c = ROOT.TCanvas("c"+eventName, "c"+eventName, 1500,1100)
	c.Divide(3,2)
	iPad = 0

	
	t = ROOT.TText(0,0,"")
	t.Draw()
	t.SetTextSize(.1)
	for hist_name in ["EEM","EB","EEP"]:
		h = timehist[hist_name]
		h_oot = timehist[hist_name + "_OOT"]

		iPad += 1
		c.cd(iPad)
		h.Draw("colz")
		t.DrawTextNDC(0,0,eventName + ' ' + hist_name)

		c.cd(iPad+3)
		h_oot.GetZaxis().SetRangeUser(-100,100)
		h_oot.Draw("colz")

	print eventName, [timehist[name].Integral()/timehist[name].GetEntries() for name in ["EEM","EB","EEP"]]

	c.SaveAs("plots/" + eventName+".pdf")
	c.SaveAs("plots/" + eventName+".png")


if(__name__ == "__main__"):
	f = ROOT.TFile("ecalCreateTimeCalibs.root")
	dir = f.Get("TriggerResults/EcalSplashTiming_0")
	latex = open("EventPlots.tex",'w')
	for key in dir.GetListOfKeys():
		if key.IsFolder():
			eventdir = dir.Get(key.GetName())
			saveEventTimingPlots(eventdir)
	
			latex.write(r'\frame{\frametitle{' + key.GetName().replace('_', ' ') + '}\n')
			latex.write(r'\begin{figure}' + "\n")
			latex.write(r'\includegraphics[keepaspectratio,width=\textwidth,height=\textheight]{' + key.GetName() +'}\n')
			latex.write(r'\end{figure}}' + "\n")

	latex.close()


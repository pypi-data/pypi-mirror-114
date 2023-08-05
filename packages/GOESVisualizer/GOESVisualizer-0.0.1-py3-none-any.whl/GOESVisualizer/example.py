from GOESVisualizer import GSVis

GSobj = GSVis('west',2021,7,21,20,-125,-117,35,45)
# only plot
GSobj.plotGS(False)
# or only save
GSobj.plotGS(True,'sample.png')

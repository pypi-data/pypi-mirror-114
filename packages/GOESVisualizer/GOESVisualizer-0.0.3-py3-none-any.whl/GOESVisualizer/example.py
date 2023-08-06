from GOESVisualizer import GSVis

#GSobj = GSVis('west',2021,7,20,20,-125,-117,35,45)
GSobj = GSVis('east',2021,7,26,18,-77,-58,40,50)
# only plot
GSobj.plotGS()
# or only save
GSobj.plotGS(True,'sample.png')

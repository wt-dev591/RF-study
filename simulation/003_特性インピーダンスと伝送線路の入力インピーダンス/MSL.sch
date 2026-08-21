<Qucs Schematic 26.1.1>
<Properties>
  <View=-114,90,1068,797,1.41995,50,133>
  <Grid=10,10,1>
  <DataSet=MSL.dat>
  <DataDisplay=MSL.dpl>
  <OpenDisplay=0>
  <Script=MSL.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <SUBST Subst1 1 440 440 -30 24 0 0 "4.6" 1 "1.6 mm" 1 "35 um" 1 "0.01" 1 "1.7e-8" 1 "0" 1>
  <MLIN MS1 1 520 270 -26 15 0 0 "Subst1" 1 "2.880mm" 1 "10 mm" 1 "Hammerstad" 0 "Kirschning" 0 "26.85" 0 "DC" 0>
  <Pac P1 1 380 300 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 MHz" 0 "26.85" 0 "true" 0 "false" 0>
  <Pac P2 1 660 300 18 -26 0 1 "2" 1 "50 Ohm" 1 "0 dBm" 0 "1 MHz" 0 "26.85" 0 "true" 0 "false" 0>
  <GND * 1 380 330 0 0 0 0>
  <GND * 1 660 330 0 0 0 0>
  <.SP SP1 1 630 420 0 50 0 0 "log" 1 "1 GHz" 1 "10 GHz" 1 "201" 1 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
  <Eqn Eqn1 1 670 580 -28 15 0 0 "dBS21=dB(S[2,1])" 1 "dBS11=dB(S[1,1])" 1 "yes" 0>
</Components>
<Wires>
  <380 270 490 270 "" 0 0 0 "">
  <550 270 660 270 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 52 490 248 190 3 #c0c0c0 1 00 1 1e+09 2e+09 1e+10 1 -69.2226 20 6.27233 1 -1 0.5 1 315 0 225 1 0 0 "" "" "">
	<"dBS11" #0000ff 1 3 0 0 0>
	<"dBS21" #ff0000 1 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>

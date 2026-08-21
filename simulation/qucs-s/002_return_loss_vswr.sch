<Qucs Schematic 26.1.1>
<Properties>
  <View=18,-211,1258,942,0.874365,0,319>
  <Grid=10,10,1>
  <DataSet=S11.dat>
  <DataDisplay=S11.dpl>
  <OpenDisplay=0>
  <Script=S11.m>
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
  <Pac P1 1 200 230 18 -26 0 1 "1" 1 "50 Ohm" 1 "0 dBm" 0 "1 MHz" 0 "26.85" 0 "true" 0 "false" 0>
  <GND * 1 200 390 0 0 0 0>
  <R R1 1 380 230 15 -26 0 1 "75 Ohm" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <L L1 1 380 310 10 -26 0 1 "0.769 nH" 1 "" 0>
  <Eqn Eqn1 1 140 620 -28 15 0 0 "dBS11=dB(S[1,1])" 1 "RL=-dB(S[1,1])" 1 "VSWR=(1+abs(S[1,1]))/(1-abs(S[1,1]))" 1 "power_reflection_coefficient=abs(S[1,1])^2*100" 1 "yes" 0>
  <.SP SP1 1 210 440 0 50 0 0 "list" 1 "1 GHz" 0 "" 0 "5.17" 0 "no" 0 "1" 0 "2" 0 "no" 0 "no" 0>
</Components>
<Wires>
  <200 200 380 200 "" 0 0 0 "">
  <200 390 380 390 "" 0 0 0 "">
  <200 260 200 390 "" 0 0 0 "">
  <380 260 380 280 "" 0 0 0 "">
  <380 340 380 390 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 650 350 240 160 3 #c0c0c0 1 00 1 1e+09 2e+09 1e+10 1 -15 5 -7.23104 1 -1 1 1 315 0 225 1 0 0 "" "" "">
	<"dBS11" #0000ff 0 3 0 0 0>
	  <Mkr 5.17e+09 11 -155 3 0 0>
  </Rect>
  <Smith 670 870 200 200 3 #c0c0c0 1 00 1 0 1 1 1 0 4 1 1 0 1 1 315 0 225 1 0 0 "" "" "">
	<"S[1,1]" #0000ff 1 3 0 0 0>
	  <Mkr 5.17e+09 182 -171 3 0 0>
  </Smith>
  <Rect 660 570 240 160 3 #c0c0c0 1 00 1 0 0.2 1 1 -0.1 0.5 1.1 1 -0.1 0.5 1.1 315 0 225 1 0 0 "" "" "">
	<"RL" #0000ff 1 3 0 0 0>
	  <Mkr 5.17e+09 258 -172 3 0 0>
	<"VSWR" #ff0000 1 3 0 0 0>
	  <Mkr 5.17e+09 261 -44 3 0 0>
	<"power_reflection_coefficient" #ff00ff 1 3 0 0 0>
	  <Mkr 5.17e+09 261 -107 3 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>

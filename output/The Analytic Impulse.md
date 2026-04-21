# The Analytic Impulse

---

## Page 1

## The Analytic Impulse

## ANDREWDUNCAN**

Cerwin-Vega!Inc.,Simi Valley,CA 93065,USA

A complex analytic function is to its real part as a solidobjcct is to its shadow.The analytic impulse △(t)isa complex"function"whose real part is the familiar Dirac symbol 8(t).This impulse finds application in energy-time calculations.The nature of thisimpulse and its application to finding energy-time curves are examined in the continuous,z-transform,and DFT domains.A simple window is also discussed which leadstoa smoother impulse△(1).

## OINTRODUCTION

The analytic impulse △(t) is the complex-valued extensionof thereal-valued function8(t)[1].Itsreal part is that same delta; its imaginary part will be examined further. This function finds one application in audio in the calculation of the energy-time curve (ETC) [2], [3]of a system.To summarize this idea briefly,the ETC is the envelope (as opposed to the magnitude) of the impulseresponse.To find thatenvelope,we combine the magnitude of the impulse response in an rms fashion with the magnitude ofits Hilbert transform.The complex(or quadrature) sum of the impulse response with its Hilbert transform is called the analytic impulseresponse(AlR) of the system, and the ETC is the magnitudeof theAIR.

The motivation for using the ETC derives from the utility of envelopes ineliminating interference effects. that appear in the time domain.Fig.1 shows the impulse response ofa simulated system.Itis composed of two damped sinusoids,a high-amplitude oscillation that dies away rapidly and a delayed lower amplitude one that lingers.Because of interference it is not easy to discern this visually. Using the techniques described in this paper we find the ETC (Fig. 2). In this graph the information wewant is casy to see.However,we note that the energy-time graph is noncausal, that is, it starts to leap up before1=O,in opposition to our

*Presentedat the 8lst Convention of the Audio Engineering Socicty,Los Angeles,1986November 12-16;revised 1987 December 29.

**Present address:Department of Mathematics,University of California,Santa Cruz,CA 95064.

intuitive notions about what such a curve should mean. We will see that in finding such a curve there is an inevitable smearing of impulses in the time domain, and that what ishappening is that the sharp rise at= Ois actually"leaking backward."

## 1THE MECHANICS

Here we describe the mechanism of finding theETC and discuss theutility of△(t)in carryingout theprocedure.In the following sections we justify the procedure and investigate thenature of△(t) inthedifferent domains. To find the AIR of a system, given its impulse response, we use (r) in one of two equivalent ways:

1) We multiply the system's frequency response by the spectrum of △(t) and then perform an inverse transform (Fourier,2,or DFT),which gives us the AIR in

Fig.l.Superpositionof two damped sinusoids with different attack times.

<!-- image -->

---

## Page 2

the time domain.

- 2)Weconvolvethe system'simpulse responsewith △(t),which yields the AIR.

If we let h(t) be the system's impulse response and H(f) its frequency response,we have

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

The term AIRcanbeparsedin two differentways. Forlinear systems the two interpretationsareidentical. We introduced the AIRabove as the analytic"impulse response,"a complex function whose real part is the impulse response.This interpretation follows (roughly) alyticimpulse"response,the(complex) response of a system to a complex impulse,namely,△(t).This interpretation corresponds to Eq.(1b).In this light,△(t) appears as the AIR of an ideal system. This is to say, the function△(t)plays a dual role.From oneperspective it is the toolwe use to calculate theAIRforagiven system.But at the same time,we may regard it as the data itself, the response of a system with everywhereflat frequency response.

From theAIRitisa short step to theETC.The AIR isacomplexfunction ofarealvariable(time).Itsreal part is the impulse response of the system in question,

<!-- image -->

Snoothedenergy-tine

Fig.2.ETC of function of Fig.1.

and its imaginarypart turns out to be theHilbert transform of the impulse response.TheETC,a realnonnegative function of time,is the magnitudeof theAIR. Forexample,theETCof an ideal system will be the magnitude of △(t).For this reason aninvestigation of the nature and properties of△（t)proves to be very useful.We start with the purely real predecessors of #(t).

## 2THEDELTAFUNCTIONS

Itisgenerallyconsidereddesirabletohave symmetry in one's equations.Forinstance,we introduce negative numbersso wemightsay thereis exactlyone solution ofalinear equation.Further,we admit complexnumbers so thatevery nth-orderpolynomial hasexactly nzeros. In this spirtwe create8(t) so that theFourier transform will have a kernel:a function whose image under the mapping is a unit constant.Fig.3 shows this relation, with the double arrowindicatingthedirectionof the forward transform.Intuitively,S(t)isanarrow pulse As it has positive but no negative values,it has a dc component.Since it rises and falls very rapidly,it has a great deal of high-frequency energy.Following the precedent of referring to negative or imaginary"numbers,Iwill call 8(t)and itsrelatives functions,although strictly speaking this is not correct.This function can be thought of as the limit of a sequence of (true) functions,as the derivative of the unit step function,or in distinctive ways.In the discrete-time domains,the difficulty of a rigorous delta function is gone.In the time domain of the z transform(Fig.4)we havea wellbehaved infinite sequence,zero everywhere except at one sample.In the discrete Fourier transform (DFT) domain(Fig.5),time is implicitlyperiodic,and sowe have a finite,cyclic sequence.Werefer to a circular plotofacyclicfunction,suchasinFig.5,asaBracewell ring[4,p.363].To stress the quantized nature of the independent variable,weuse square brackets,and call the variable . takes on only integer values.In the discrete frequency domain,we shall use the letter v,

Fig.3.Dirac delta function and its spectrum.

<!-- image -->

---

## Page 3

## 3ANALYTICFUNCTIONS

An analytic function is to itsreal part as a solid object is toits shadow.For example,consider the function cos(wt).Thecomplexextension ofcos(wt)is

<!-- formula-not-decoded -->

In a way, ejr is the most continuous complex function we can find with cos(@t) as its real part.Fig.6 shows the solidfigure thatresultswhen both parts of thefunction are plotted against time.The figure's projections show both thereal and the imaginaryparts as functions of time.Therear projection plane shows the function

Fig.4.Discrete-time infinite-sample delta function 8[].

<!-- image -->

plotted on thecomplexplane,with timeasaparameter (a Nyquist diagram).HenningMoller refers toNyquist diagrams ofloudspeaker impedance plots as Heyser spirals,after the graphs that Richard Heyser used in Audiomagazinetoanalyzeloudspeakerperformance. Following that line,we used torefer to suchgraphs as shown in Fig.6asgeneralized Heyser spirals,but the termproved tooformalandcumbersome andhasbeen shortenedtoHeysercorkscrew.Similar three-dimensional plotshavealsobeenused byHeyser[2].

Themagnitudeofcos(wt)variesfrom-1to+1 and at times it is zero.However,we feel that its envelope is constant.Our intuition is satisfied by defining the envelopetobethemagnitudeofthefullcomplexfunc-

Fig.5.Discrete-timefinite-sample delta function8[T]for 64-pointDFTinBracewellringformat.

<!-- image -->

Fig.6.Heyser corkscrew of ej.

<!-- image -->

---

## Page 4

tion el.Ina Heysercorkscrew this magnitude appears astheradial distance of thecentral figure to the time axis.FromFig.6itis clear thatthe envelopeofcos(@r) is always1.Aplot of thisradius as a function of time istheETCof thefunction.

Theconnection between thereal and imaginaryparts is called the Hilbert transform.The connection between thereal part and the wholeis best illustrated by examining the relation.

<!-- formula-not-decoded -->

which is an inversion ofEq.2.To get the complex extension of cos(wt) we express it in its exponential form, suppress thenegative frequency termej,and double the positive frequency part,as shown in Fig. 7.This complex-valuedfunction whosereal part is the original function of time is called the analytic signal, although this is something ofa misnomer,as noted below.Any real function of timewill have a spectrum that is two-sided and symmetric. To get the analytic signal,we go into the frequency domain,remove the negative-frequency components,and double theresult (except at the dcpoint).This corresponds to performing the operation in Eq.(la),where {△(t)},the spectrum of△(t),is a function that has a value of O fornegative

<!-- image -->

1Hz

Fig. 7. Spectra of cos(2πt)and ej

REAL

TMAGIHARY

SINC(t)

frequencies,1 for dc,and 2 for positive frequencies. Performing this operationis referred to as causalizing the spectrum.In this way, the term causal has been generalized toreferto a function that iszerofornegative argument.If the argument is time,this corresponds to conventional usage.In fact,aswe shall see,a function cannot be causal in both time and frequency.

Asamatterofnomenclature,thetermanalyticrefers toa complexfunction of a complexvariable that has a special smoothnessproperty,thatof being everywhere differentiable.In principle,given a reasonably smooth real function of a single variable,there is a unique analyticfunction whose real part along a specified axis is the same as the original function.One finds this analyticfunctionbyfirstapplyingtheHilbert transform and then integrating the Cauchy-Riemann equations toextend thefunction to theentirecomplexplane.In the process described,we stop short of finding the entire analyticcontinuation ofour signal,but the term analytic signal has behind it the inertia of history.The notion of an analytic signal asonewith no negative-frequency terms will also beused in the discrete domains,where the concept of differentiability is meaningless.

## 4THECONTINUOUSDOMAINS

In the continuous domains we may say,in light of the foregoing, that if the real impulse 8（r) is a signal with a flat spectrum of 1,then the analytic impulse (t)is asignalwith a spectrum thatiszero for negative frequencies,1 for dc,and2 forpositive frequencies. This is correct,but it will be more illuminating to approach this limit slowly.Fig.8shows a signal that has positive and negativefrequency content only up to Hz (that is,a bandwidth of 1 Hz and a unit area).The algebraicexpression of thissignal is

<!-- formula-not-decoded -->

Ifwe remove the negative-frequency components,we get a transform pair as in Fig.9,shown in both linear andlogarithmicphasemagnitude(ETC) displays.This

&lt;--&gt;&gt;

<!-- image -->

1Hz WIDE EVEN VINDOW

Fig.8.Sinc(t) and its spectrum.

t=O

10s

---

## Page 5

function is given by

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

This function is sometimes also described as [4,p. 391]

<!-- formula-not-decoded -->

a form which,if studied,will reveal certain convolution properties of the imaginary part.In Fig.10 we see the same function andnote itshelical form.

Passing to the limit,we let the band edge move indefinitely to the right,giving us the transform pair shown in Fig.11.The spectrum is now a function called CAUS(f)and the signalis thecontinuous analytic impulse,

<!-- formula-not-decoded -->

We see immediately that theimaginary part of△(t),

sometimesreferred to asa doublet ord(t),is notcausal, andhence the magnitude of△（t)[the ETCof8()] on the upper left handof Fig.ll must also be noncausal. InAppendixI thereisafurther discussionofwhyd(t) does not vanishfornonzero argument.For the moment, as the magnitudeof△(t)represents the ETCofanideal system,we may conclude that the ETCof any loudstrength in the continuous and discrete domains.Although the evidence for this is plentiful [2],[4]-[6], it appears onlyin fragments,in widely scattered texts, usually addressingvery different topics.Further,there is some confusion about thenecessity of this effect. Perhaps theresolutionofour instruments is toolow, ormaybeamore sophisticatedwindowingwouldmake ourETC start at t=O.The foregoing analysis shows that this is not so in continuous domains.The following addresses the same issue in the discrete domains.

## 5THEZ-TRANSFORMDOMAINS

Ournext step is to make time discrete,that is,we nowknow thevalue of the signal atinteger multiples ofa samplinginterval.Without loss ofgenerality we canreplacetwith ,an integervariable.There are still an infinite number of samples,but now a countable infinity.Theeffectofsamplingin timeis tomake the spectrum periodic.In fact,the spectrum is now the z transform evaluated on theunit circle.Fig.12shows CAUS(f)for this situation and its inverse transform

Fig.9.Analytic sinc function asinc(t),its ETC,and its spectrum.

<!-- image -->

---

## Page 6

Fig.10.Heysercorkscrew ofasinc(t).

<!-- image -->

Fig.11.Continuous-time analytic impulse time infinite-sample analytic impulse],its ETC,and its spectrum.

<!-- image -->

J.AudioEng.Soc.,Vol.36,No.5,1988May

---

## Page 7

[].Inalgebraic form[5,p.360],[6,p.71],

<!-- formula-not-decoded -->

or,equivalently,

<!-- formula-not-decoded -->

Now let us compare Eqs.(5a) and (7a).We see that in this"intermediate"domain ofquantized time and continuous frequency the analyticimpulse has exactly thesameformasthecompletelycontinuousimpulse beforelimiting.One onlyneedwriteaTwheretwould normallyappear.Fig.13isan overlayofFigs.9and 12and shows even more clearly what Eq.（7b) tends to obscure:[]is justa sampledversionof the analytic sincfunction.However,we see thatEq.(7b)isreminiscentofEq.(6).Thesuddenappearanceof thefactor 2in the imaginary part can beexplained by noting that d[T]alternatesbetweenOand2/π,thusgivinganav-

<!-- image -->

OUERLAYOFMAGPHASE

Fig.13.Overiay of Figs.9and 12.

<!-- image -->

Fig.12.Discrete-time infinite-sample analytic impulse △x[],its ETC,and its z transform evaluated on unit circle.

<!-- image -->

---

## Page 8

erage value of 1/π (see also Appendix I).

Ifwe step back fromFig.12 and enlarge our field of view, we get a picture like Fig. 14. This figure shows thatit takesroughly 60 samples for the envelope of eventhebriefesttransienttodecayto40dBbelowthe peakvalue.This suggests that there isapractical limit to theresolution ofan energy-timemeasurement made with sampled signals.

## 6THEDFTDOMAINS

Our final step,one thatiswell justified bythedemands ofphysical reality,is to consider only a finite number of signal samples. This final restriction changes the spectrum from periodic continuous toperiodic discrete. The discrete nature of the spectrum,in turn,forces us toconclude that thetimefunctionisimplicitlyperiodic. Nowboth domains are again of the same form.The number of samples Nis the same forboth signal and spectrum.

Fig.14.Wider view of Fig.12.

<!-- image -->

haved[]=2/π=0.6366..,which differsbyless than 0.1%.Because of this,Fig. 14 and the upper left of Fig.12 may serve asETCs for the analytic impulse in theDFT domains for large N.Any measurement technique that yields information about signal and spectrum thatisrestricted to discrete samples,and this includesbothFFT(aparticularlyefficientway of doing a similarlylimitedresolution.

Wecannotnowexpect△v[t]to have thesame algebraic form as[T].What wasT=±now corresponds to=±N/2,the antipodal point.Eqs.（7a) and(7b)need tobe modified inorder that theenvelope of△[]vanishes at this point.In fact,

<!-- formula-not-decoded -->

which is shown in Fig.15.This looks very different from Eq.(7).The difference in form between Eqs.(7) and (8) was one initial stimulus to my investigations: However,these two cquations arenumerically almost identical.For example,in the 64-point DFT domain, thefirstnonzerovalueofd64[T]iscot（π/64)/32=0.6361 ...In the infinite-point z-transform time domain we

## 7WINDOWING

Thus the analytic impulse,discrete or continuous, has a magnitude that does not vanishfor negative time. Equivalently the ETC for the ideal transducer,to say

Fig.15.Discrete-time finite-sample analytic impulse4[],its ETC,and its spectrum for 64-point DFT.

<!-- image -->

---

## Page 9

nothing of the practical one, is not causal.This means that the interpretation of that envelope asa graph of energy versus time is only approximate. The best we can do is ask:what can we do to make such a graph look better?For example,we may make the skirts of a peak steeper,to help us visually sort closely spaced peaks,at the expense of making the peaks themselves somewhat broader. This is obviously a tradeoff,and ifdesired it can be accomplished with techniques of windowing.

By windowing wemean themultiplication in the time or frequency domain of a measured functionby another function,called the window.Generally the windowgoestoOwherethedata aretobedeemphasized, and to 1 where the data are to be emphasized.For example,a cosine-squared(orraised-cosine) bell,called a Hann window after Julius von Hann,is one of the most common windows used in FFT processing. Fig. 16 shows a Hann window in a 64-point DFT domain. The particularly simple form of this function in a periodicdomain isrevealedbytheBracewellringformat.

Wefirst investigate theeffect ofwindowingonthe analyticimpulse itself.Wewill later see that thewindowed impulse or its spectrum may beused to find a windowed ETC for physical data.To windowx[], we multiply its spectrum by a cosine-squared shape. Thevalue of thewindow isO at the two edges of[]'s spectrum and I at the center. The results of this windowing are shown in Fig. 17. The algebraic expression for this smoothed analytic impulse is

Fig,16.Hann windowHANN[x]=cos²（πx/N)=V[1+ cos(2mx/N])for64-pointDFT.

<!-- image -->

in Sec.Iand say that the smoothed"analytic impulse response"is the same as the"smoothed analytic impulse"response.Algebraically,

<!-- formula-not-decoded -->

where W(f) is the window function.Equivalently, smoothing merely involves substituting(t)(or one of its discreterelatives)for△(t) in the usualequations for finding the AIR.

The art ofwindowing consists of picking a window

<!-- formula-not-decoded -->

The real part of the impulse has become more spread out, but the imaginary part is more localized, and as a result the magnitude peak has narrower skirts,but is more broad at the top.Fig.18 shows awiderview of the magnitude, over the same range as Fig.14,and Fig.19 gives a still wider view.

Thiswindowmay be applied toreal-life data in the DFT domains.Fig.20 shows the smoothed analytic impulse and its spectrum fora 64-point DFT.As before, the numerical difference between infinite-and finitesample domains is very small.

Tofind thesmoothedenvelopeofameasuredimpulse response,wemay usean argument similar to the one thatbestembodies the desiredtradeoffsbetween smoothness andresolution.TheHannwindow shown isoneofthemostelementaryof these.Otherwindows of interest include the Hann squared,the Blackmun, and the Kaiser.For futher discussion,see,for example, [6].

## 8RESOLUTION

The simplestdescription ofresolvingpower in an ETCis thewidthofaspike caused bya delta function in the impulse response.Forexample,without smooth-

---

## Page 10

<!-- image -->

Fig.17. Smoothed discrete-time infinite-sample analytic impulse [],its ETC,and its z transform evaluated on unit circle.

Fig.18. Magnitude of [T] on 60-dB scale.

<!-- image -->

Fig.19.Magnitudeof△[T] on 180-dB scale.

<!-- image -->

ing,the-30-dbwidthis 42 samples in time;with the smoothing discussed,itis 10 samples.With the typical experimenter's lab equipment,the total number of samples Nis fixed,and the equipment's display window orprintoutwill showthedata samplesspaced atequal intervalssoastofill thespaceallotted.Inparticular, changing theequipment'sfrequencyrange or sampling windowwillnotchangethespacingofsamplesinthe display.In thiscase a peakinETCwill have awidth thatisaconstantfractionofthedisplaywidth,regardiess offrequencysetting.Inotherwords,if theexperimenter turnsupthesamplingrateonthelabFFTinhopesof narrowing theapparentwidthofapeakin theenergy-time function, it will have no effect. However, in terms of absolute time,thepeakwill benarrower since theentiredisplaywillnowcover asmallerintervalof time.

## 9EXAMPLES

Fig.21 shows the ETC of a high-quality tweeter, measured with a 1024-point FFT sampling at 256kHz, with no weighting and 256 averages(necessary due to a noisy "anechoic"chamber). In Fig. 22 the abovementioned windowing has been used on the spectrum before finding the ETC. The smoothed ETC has a sharper attack, and some secondary peaks that were "riding" on the skirts of the first peak are now lower down. However, the smoothed ETC also has a wider peak, which seems to absorb a neighboring peak.

---

## Page 11

Of particular interest is the peak at 160 μs,which shows up clearly in the smoothed function,but not in the unsmoothed one.This corresponds to a path differenceforasoundwaveofroughly5mm,whichis the distanceto the edgeof the(unmounted) tweeter fange,where the acoustic load changes from a halfspace to a full space.An experimenter with access to this ETCmight suspect that the outgoing acoustic impulse is partially refracted at the edge of the flange, reaching themicrophone having traveled50 mmfarther than the direct signal.In an attempt to verify this guess, themeasurementwasrepeatedwith thetweeter mounted at theend of a long tube of sound-absorbent material. Fig.23 shows the smoothed ETC for this measurement, withtherefractiongone.

## 10CONCLUSIONS

In any domain we might care to use, the ETC of a system, calculated as the envelope of the impulse response,is noncausal.This is not a problem of physics or engineering,buta necessary consequence of the mathematicsinvolved.Theproblem arises whenwe insist on using themath to describe aphysical process weknow tobe causal in time.To interpret ourfindings, we must know where it is that the numbers stop talking about the real world,and (like historians) start talking about each other.

We may investigate this numerical discourse mathematically by the judicious selection of theoretical functions torepresent prototypical physical measurements.The convolution properties enjoyed by 8(t) make it an excellent choice for this purpose. Since the set {8(t-a)}formsanorthonormal basisforawideclass of functions,a discussion of signal-processing techniquesapplied to 8(t) alone will have a much wider applicability.Further,8(t) may itself be viewed as a physical measurement:the impulse response of an ideal system.

From 8(t)weexpanded our consideration to thefully complex △(t),and we investigated theoretically the properties of the envelope of a general or nonideal system'simpulseresponse.△(t) appears both as a tool forfinding this envelope and as an idealmeasurement itself:a benchmark to becomparedwith expectations or actual measurements.Wehave seen how the mathematical process ofwindowingmaymakevisual interpretation of that envelope easier.Since graphic display is generally the ultimate destiny ofnumerical calculation,windowing appears as a fundamental tool for such processing.

## 11ACKNOWLEDGMENT

Iwould like to give special thanks to Dr.Marshall Buck andEugene Czerwinskifor their support anden-

<!-- image -->

Fig.21.ETCof high-quality tweeter,measured with 1024 sampleFFT sampling at 256kHz;no weighting.

Fig.22.ETC for same twccter as in Fig.21.but with raisedcosine smoothingin frequency domain.

<!-- image -->

Fig.20. Smoothed discrete-time finite-sample analytic impulse ] and its spectrum for 64-point DFT.

<!-- image -->

---

## Page 12

couragement. Thanks are also due Dr. John Vanderkooy and Dr. StanleyLipshitz for their helpful discussions aboutwindowing.Finally,IamgratefultoDaniel Hirsch and theStevensonProgram onNuclearPolicyatthe University of California at Santa Cruzfor theuse of their facilities.

## 12REFERENCES

- [1]P.A.M.Dirac,ThePrinciples of Quantum Mechanics,3rd ed.(Oxford University Press,Oxford, England,1947).
- [2] R.C.Heyser,"Determination of Loudspeaker Signal Arrival Times,Parts I,I,and III,"J.Audio Eng.Soc.,vol.19,pp.734-743(1971 Oct.);pp. 829-834(1971Nov.);Pp.902-905(1971 Dec.).
- [4] R.N.Bracewell,The Fourier Transform and Its Applications,2nd ed.(McGraw-Hill,New York, 1978).
- [3] S. P. Lipshitz, T. C. Scott, and J. Vanderkooy, "Increasing theAudio Measurement Capability of FFT Analyzers by Microcomputer Postprocessing," J. Audio Eng.Soc.,vol.33,pp.626-648（1985 Sept.).
- [5]A.V.Oppenheim and R.W.Schafer,Digital Signal Processing (Prentice-Hall,Englewood Cliffs, NJ,1975).
- [6] L.R.Rabiner and B. Gold,Theory and Application of Digital Signal Processing(Prentice-Hall, Englewood Cliffs,NJ,1975).

## APPENDIXI

It has been suggested by Heyser[2] that the analytic impulse ought to look likeFig.24.In fact,this reference introducestwo analyticimpulses:oneis the function discussed in this paper and the other is a function with bounded totalenergy.Iwould liketoexamineina little more detail why the doublet function does not vanish for nonzero time,andexplore the question of bounded energy.

In Figs.9ar.d 10 we saw the analytic sincfunction asinc(t). The imaginary part of this function,cosinc(t),

<!-- image -->

SMOOTHED,WITH EXTRA SOUND-ABSORBENT MATERIAL

Fig.23.ETC for same tweeter as inFig.21,measured with tweeter mounted at end of long sound-absorbing tube; smoothing used.

has localextrema that oscillate between O and (approximately) 2/πt.As we tend to the limit,the band edge ofthe spectrummoves totheright,and the extrema of the signal move closer together.At the limit,we might feel that the signal becomesinfinitely discontinuous, but a property of the Fourier integral saves us. This is the property that at a discontinuity, the integral converges to the average of theleft-and theright-hand limits.Thus the inverse transform of CAUS(f) has the form given in Eq.5.The real part does converge to zero for10, but the imaginary part converges to the "average"value ofl/t.

Let us bemore explicit about the limiting process. We are in effect expanding the frequency function, or shrinking the frequency scale,and hence expanding the time scale.Ifwelet II(f)be the spectrum of asinc(t), the limitingprocessis

<!-- formula-not-decoded -->

In the context of the theory of generalizedfunctions, this is a rigorous definition of the analytic impulse, and its real part does converge to the familiar delta function.If we substitute a = 1/α,we get [2,eq.35]. This function does not have unit energy.To see this, itismerelynecessary toobserve that theareaunder its spectrum (Fig.1l,right side)is infinite.One may alsocarry out the energy integral in the time domain to convince oneself.How then do we explain [2,eq. 32],which arrives at the opposite conclusion？A look at [2,eq.30] will reveal that this equation has an additional 1/√a term init.Buta is the term thatgoesto infinity.Thus we have slipped in an additional convergence term.In this case it is correct to say that the function so defined has unit area,but at the expense of introducing a rival impulse function.Heyser [2] seems to suggest that these distinct functions are one and the same.But it iscontradictory for a signal to have equal nonzero energy density at all frequencies and still have bounded total energy.To further the confusion,the comment in[2,fig.A-3] concedes that the envelope of the'doublet goes as l/t,but this is juxtaposedwithapicture of therivalimpulsefunction (the same as myFig.24).

Fig.24.Essentially duplicate of [2,fig.A.3].

<!-- image -->

---

## Page 13

## APPENDIXII

Following are the equations used in this paper to carry out the required transforms. The continuous Fourier transforms;

<!-- formula-not-decoded -->

theztransform,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Note thatthisconventionfortheDFTmeans thatthe area under a function squared is not the same as the area under its transform squared-a factor Nmust be includedin theParseval-Rayleighformula.Alternate conventionscould have a l/√Non both sides or the 1/Non the other side.Thisconventionmakes the forward transform ofaunit impulseequal toaconstant spectrum of one,analogous to the continuous case.

## THEAUTHOR

<!-- image -->

Andrew Duncan was bom in London,U.K.,in 1960. He received a B.S.degree in engineering and-applied sciences from the California Institute of Technology in1983.Hetaught high school physics for 2years in Pasadena, California,while studying at Caltech,and for anotheryear after graduation.He then worked for 2years,with Marshall Buck,as a programmer at Cerwin-Vega Inc.Mr.Duncan is currentlya doctoral student inmathematicsat the Universityof California at Santa Cruz,where he is studying the application of group theory to the thcory of tonal harmony. He has also worked as a consultant at E-mu Systems,Inc.in the area of digital pitch shifting.

A member of the AES and the AMS,Mr. Duncan has interests in the combination ofmusic and mathematics.He plays the acoustic guitar,the electric bass, and the Chapman Stick,while studying the music of, respectively.John Fahey,Phil Lesh,and J.S.Bach on these instruments.His current interests include group representations of tonal and modal movement in the equally tempered scale and applications of tiling theory tofingeringpatterns on string instruments.

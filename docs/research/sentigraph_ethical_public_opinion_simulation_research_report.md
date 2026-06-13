# Sentigraph Ethical Public Opinion Simulation Research Report

## Executive summary

**A. Executive summary.** For Sentigraph, the most defensible architecture is not a single theory but a **hybrid agent-based model** that combines: continuous opinion updating for gradual attitude movement; discrete threshold rules for visible public actions such as reposting, commenting, joining a pile-on, or accepting a correction; homophily and bounded-confidence mechanisms for echo-chamber formation; source-credibility and framing effects for message evaluation; attention decay and self-exciting event dynamics for short-run surges; and a crisis-response layer that simulates transparent interventions such as clarification, apology, compensation, progress updates, third-party evidence, and misinformation correction. Foundational work across these layers comes from DeGroot, Friedkin-Johnsen, Hegselmann-Krause, Deffuant-Weisbuch, Granovetter, Watts, Centola and Macy, McPherson et al., Bakshy et al., Cinelli et al., Coombs and Holladay, Benoit, Lewandowsky and van der Linden, Walter et al., and the ODD / ODD+D / ODD+2D agent-based modeling documentation line. citeturn32view0turn32view1turn34view0turn32view3turn32view4turn36view2turn36view4turn21search3turn37view0turn35view7turn35view6turn30view10turn31search16turn17search6turn18search11turn19search0

The **best MVP** is a restrained, interpretable simulator rather than a maximal one. In practice, that means: a Friedkin-Johnsen backbone for prior-belief persistence; a bounded-confidence gate to prevent unrealistic universal mixing; a Granovetter/Watts threshold layer for public expression and cascades; a homophilous but bridge-aware network; source credibility and framing in message scoring; a topic-attention decay process; and an intervention package library grounded in SCCT, Image Repair, apology research, and evidence-based misinformation correction. That stack is strong enough for scenario comparison while staying explainable and calibratable. citeturn32view1turn34view2turn32view4turn36view2turn21search3turn37view0turn35view3turn37view6turn35view5turn11search9turn25search15turn35view7turn35view6turn39view2turn30view10turn31search16

The major additions you made beyond classic opinion-dynamics theory are exactly the right ones. In particular, **validation and documentation**, **platform mediation**, **dynamic network evolution**, **temporal self-excitation**, **evaluation metrics**, and **abuse prevention** are not optional extras; they are what separate a toy simulator from a system that can be defended to technical reviewers, policy teams, and ethics stakeholders. The ODD family of protocols and recent validation work are especially important because agent-based models are often criticized for poor reproducibility and weak empirical grounding. citeturn17search0turn17search1turn30view7turn18search11turn19search0turn30view8turn20search11turn20search3turn19search5

The strongest warning in the literature for Sentigraph is methodological: **homophily and contagion are generically confounded in observational social-network data**, which means you should not overclaim that one community “caused” another community’s opinion shift unless you have unusually strong identification or experimental evidence. That has direct design implications: Sentigraph should present outputs as **scenario-conditioned simulations with uncertainty**, not causal certainty; it should dock complex modules against simpler baselines; and it should log which outcomes are data-estimated versus assumption-driven. citeturn36view0turn36view1turn32view5turn30view8turn19search5

The ethical boundary is clear. Sentigraph should support **aggregate-level crisis-response evaluation**, not people-level persuasion optimization. It should never recommend fake-consensus tactics, bot amplification, covert influencer seeding, impersonation, microtargeted emotional exploitation, or suppression strategies. Its outputs should be transparent, uncertainty-labeled, auditable, privacy-preserving, and always routed through human review before any real-world recommendation is acted upon. Recent work on simulation credibility and responsible social modeling strongly supports that stance. citeturn20search3turn19search5turn30view8turn28search1

## Foundational theories and papers

**B. Table of theories and papers.** The table below groups closely related constructs when they are best implemented as one Sentigraph module rather than as isolated theories. Module abbreviations: **APB** = agent personality / bias model; **NI** = network influence model; **MI** = message influence model; **EC** = echo chamber model; **RF** = risk forecast model; **IS** = intervention simulation model; **AD** = attention decay model. Use abbreviations: **Sim** = simulation; **Fcst** = forecasting; **Intv** = intervention comparison; **Crisis** = crisis communication strategy.

| Theory and representative source | Year and field | Core idea, key variables, equations or model rules | Sentigraph mapping, supported uses, priority | Limitations and ethical constraints |
|---|---|---|---|---|
| **DeGroot consensus model.** DeGroot, M. H. *Reaching a Consensus.* *Journal of the American Statistical Association* 69(345): 118–121. citeturn0search0turn32view0 | 1974; statistics, mathematical sociology | Repeated weighted averaging: \(x(t+1)=Ax(t)\), with \(A\) row-stochastic and \(a_{ij}\) encoding influence / trust. Key variables: opinion \(x_i\), tie weight \(a_{ij}\), network topology. citeturn32view0 | Base **NI** kernel; useful as a transparent baseline and docking target. Supports **Sim** and short-horizon **Fcst**; indirect **Intv** and **Crisis**. **Priority: MVP** as a baseline only. | Unrealistically consensus-seeking; no stubbornness, thresholding, framing, or attention. Ethically safe only when used for aggregate exploration, not people-level persuadability scoring. citeturn32view0turn32view5 |
| **Friedkin-Johnsen social influence model.** Friedkin, N. E., & Johnsen, E. C. *Social Influence and Opinions.* *Journal of Mathematical Sociology* 15: 193–206. citeturn0search1turn32view1 | 1990; mathematical sociology | Adds **stubbornness / initial-opinion anchoring**: \(x(t+1)=Gx(0)+(I-G)Ax(t)\). Key variables: initial opinion \(x_i(0)\), susceptibility \(1-g_i\), stubbornness \(g_i\), influence matrix \(A\). Persistent disagreement is a feature, not a bug. citeturn32view1 | Best core for **APB + NI + RF + IS** because crisis publics rarely forget priors overnight. Supports **Sim**, modest **Fcst**, strong **Intv**, direct **Crisis**. **Priority: MVP**. | Still linear and stylized; needs nonlinearity for echo chambers and action thresholds. Ethically, do not convert stubbornness into a targeting score for manipulative outreach. citeturn32view1turn36view1 |
| **Hegselmann-Krause bounded confidence.** Hegselmann, R., & Krause, U. *Opinion Dynamics and Bounded Confidence Models, Analysis, and Simulation.* *JASSS* 5(3). citeturn34view0turn34view2 | 2002; computational social science | Agents average only over those inside a confidence interval \(\varepsilon\). The model can yield consensus, polarization, or fragmentation depending on confidence width and initial conditions. Key variables: opinion \(x_i\), confidence interval \(\varepsilon_i\), admissible-neighbor set \(I_i\). citeturn34view0turn34view2 | Core **EC** mechanism; use it to gate who seriously considers which narratives. Supports **Sim**, indirect **Fcst**, strong **Intv** and **Crisis** for testing whether clarification can bridge communities. **Priority: MVP-lite or V2**. | Highly sensitive to initialization and confidence parameters; synchronous averaging is stylized. Ethically, use for understanding fragmentation, not for designing divisive segmentation. citeturn34view0turn34view2 |
| **Deffuant-Weisbuch bounded confidence.** Deffuant, G., Neau, D., Amblard, F., & Weisbuch, G. *Mixing Beliefs Among Interacting Agents.* *Advances in Complex Systems* 3(1–4): 87–98. citeturn30view3turn32view3 | 2000; complex systems | Random pairwise encounters. If \(|x_i-x_j|\le \delta\), both move partway toward each other: \(x_i' = x_i + \mu(x_j-x_i)\), \(x_j' = x_j + \mu(x_i-x_j)\). Key variables: opinion distance, confidence threshold \(\delta\), convergence parameter \(\mu\). citeturn32view3 | Best for comment-thread or reply-chain micro-interactions in **NI** and **EC**. Supports **Sim** and **Intv**; weaker direct **Crisis** value than FJ. **Priority: V2**. | Pairwise random mixing may under-represent broadcast/media dynamics. Ethically fine for conversational simulation, but not for optimizing adversarial one-to-one persuasion. citeturn32view3 |
| **Voter model.** Origins: Clifford & Sudbury (1973); Holley & Liggett (1975), summarized in later voter-model treatments. citeturn41search1turn41search3 | 1970s; probability, statistical physics | Very simple binary imitation: choose an agent and copy a random neighbor’s state. Key variables: discrete state \(y_i\in\{0,1\}\), network edges. Good for binary narrative adoption or slogan competition. citeturn41search1turn41search3 | Useful as a minimalist discrete **NI** and narrative-dominance baseline in **RF**. Supports **Sim**; limited **Fcst** and **Crisis**. **Priority: later research / baseline module**. | Too simple for confidence, credibility, or multi-valued sentiment. Ethically safe as a baseline but poor as a main public-opinion engine. citeturn41search1turn41search3 |
| **Threshold model of collective behavior.** Granovetter, M. *Threshold Models of Collective Behavior.* *American Journal of Sociology* 83(6): 1420–1443. citeturn30view4turn32view4 | 1978; sociology | Collective action can hinge on heterogeneous adoption thresholds. Small changes in threshold distributions can produce huge aggregate differences. Key variables: threshold \(\theta_i\), observed participation proportion, equilibrium adoption level. citeturn32view4 | Essential for whether agents **publicly speak, repost, condemn, defend, or accept a correction**. Core to **MI + RF + IS**. Supports **Sim**, **Fcst**, **Intv**, and **Crisis**. **Priority: MVP**. | Binary and stylized; threshold distributions are hard to estimate directly. Ethically, never use threshold modeling to plan fake social proof or manufactured bandwagons. citeturn32view4 |
| **Watts threshold model and global cascades.** Watts, D. J. *A Simple Model of Global Cascades on Random Networks.* *PNAS* 99(9): 5766–5771. citeturn35view0turn36view2turn36view3 | 2002; network science | Agents adopt when at least a threshold fraction of neighbors have adopted; global cascades require a percolating vulnerable cluster. Key variables: local threshold \(\phi_i\), degree \(k_i\), vulnerable cluster size. citeturn36view2turn36view3 | Strong for **RF**: estimating whether a small shock, correction, or anger spike can become system-wide. Supports **Sim**, **Fcst**, **Intv**; indirect **Crisis**. **Priority: V2**. | Derived on random-network assumptions; weaker fit for platform-curated feeds without adaptation. Ethically, interpret as risk analysis, never as a playbook for deliberate cascade engineering. citeturn36view2turn36view3 |
| **Complex contagion and social reinforcement.** Centola, D., & Macy, M. *Complex Contagions and the Weakness of Long Ties.* *American Journal of Sociology* 113(3): 702–734. citeturn35view1turn36view4 | 2007; sociology, networks | Many social behaviors require **multiple reinforcing exposures**, not a single contact. Wide bridges and clustered overlap can help more than long weak ties when adoption needs confirmation. Key variables: reinforcement count, threshold, cluster overlap, bridge width. citeturn36view4 | Crucial for modeling uptake of apology acceptance, misinformation correction, and collective de-escalation. Supports **Sim**, **Fcst**, **Intv**, **Crisis**. **Priority: V2**, but conceptually important from day one. | Harder to calibrate than simple contagion; different behaviors likely require different reinforcement thresholds. Ethically, reinforcement modeling must never be used to script pressure campaigns. citeturn36view4 |
| **Homophily, selective exposure, and algorithmically mediated exposure.** McPherson, M., Smith-Lovin, L., & Cook, J. M. *Birds of a Feather: Homophily in Social Networks.* *Annual Review of Sociology* 27: 415–444; Stroud, N. J. *Polarization and Partisan Selective Exposure.* *Journal of Communication* 60(3): 556–576; Bakshy, E., Messing, S., & Adamic, L. A. *Exposure to Ideologically Diverse News and Opinion on Facebook.* *Science* 348(6239): 1130–1132. citeturn3search3turn23search12turn30view6 | 2001–2015; sociology, communication, computational social science | Similarity shapes tie formation; media users seek and prefer congruent content; platform ranking and friend networks both affect cross-cutting exposure. Key variables: assortativity, ideological distance, source affinity, exposure probability, click / view choice. citeturn23search12turn30view6 | Core for **APB + NI + EC + RF** and for cross-cutting exposure metrics. Supports **Sim**, modest **Fcst**, strong **Intv** and **Crisis** scenario testing. **Priority: MVP**. | Homophily and influence are difficult to disentangle causally. Ethically, the module should diagnose narrowing exposure, not optimize it. citeturn36view0turn36view1 |
| **Echo chambers across platforms.** Cinelli, M., et al. *The Echo Chamber Effect on Social Media.* *PNAS* 118(9). citeturn37view0turn26search22 | 2021; computational social science | Different platform affordances create different information-spread and echo-chamber dynamics. The study operationalizes echo chambers across Facebook, Twitter, Reddit, and Gab using large comparative data. citeturn37view0 | Directly informs **EC + NI + MI + RF** and platform-specific parameterization. Supports **Sim**, **Fcst**, **Intv**; indirect **Crisis**. **Priority: V2**. | Platform-specific results may not transfer cleanly to future systems; measurement choices matter. Ethically, use this to compare platform risks, not to port tactics from one platform to another. citeturn37view0 |
| **Bridge nodes, weak ties, and structural holes.** Granovetter, M. *The Strength of Weak Ties.* *American Journal of Sociology* 78(6): 1360–1380; Burt, R. S. *Structural Holes: The Social Structure of Competition.* Harvard University Press. citeturn21search2turn21search6 | 1973–1992; sociology, network theory | Brokers and bridges connect otherwise segregated communities. Weak ties can expand reach, while structural holes create brokerage opportunities. Key variables: bridge centrality, between-community degree, brokerage score, structural-hole exposure. citeturn21search2turn21search6 | Useful for **NI + EC + IS**: identify where truthful cross-community clarification is most likely to travel. Supports **Sim**, **Intv**, **Crisis**. **Priority: MVP metrics, V2 dynamics**. | Weak ties help simple contagion more than complex contagion; brokerage may not imply trust. Ethically, bridge nodes should be modeled as public intermediaries, not covert influence targets. citeturn36view4 |
| **Causal-identification warning.** Shalizi, C. R., & Thomas, A. C. *Homophily and Contagion Are Generically Confounded in Observational Social Network Studies.* *Sociological Methods & Research* 40(2): 211–239. citeturn36view0turn36view1 | 2011; causal inference, network analysis | Observational correlations among connected people generally do not reveal whether similarity came from influence, selection, or omitted variables. citeturn36view0turn36view1 | Supports **RF**, validation, uncertainty labeling, and causal-humility guardrails across all modules. Supports **Fcst** and **Intv** by constraining interpretation. **Priority: MVP governance**. | Not a behavioral rule by itself; it is a warning against overclaiming. Ethically, it should block Sentigraph from offering false causal certainty. citeturn36view0turn36view1 |
| **Confirmation bias and motivated reasoning.** Nickerson, R. S. *Confirmation Bias: A Ubiquitous Phenomenon in Many Guises.* *Review of General Psychology* 2(2): 175–220; Kunda, Z. *The Case for Motivated Reasoning.* *Psychological Bulletin* 108(3): 480–498. citeturn37view2turn37view3 | 1990–1998; cognitive and social psychology | People seek, interpret, and evaluate evidence in ways that favor prior beliefs or desired conclusions. Key variables: congruence bias, motivated scrutiny, asymmetric evidence weighting. citeturn37view2turn37view3 | Core **APB + MI** variables: bias-congruent message boost, correction resistance, asymmetric trust updates. Supports **Sim**, **Fcst**, **Intv**, **Crisis**. **Priority: MVP**. | Latent and person-specific; often only weakly inferable from behavior traces. Ethically, these variables should stress-test truthful interventions, not personalize manipulation. citeturn37view2turn37view3 |
| **Prospect theory, negativity bias, availability, and anchoring.** Kahneman, D., & Tversky, A. *Prospect Theory: An Analysis of Decision under Risk.* *Econometrica* 47(2): 263–291; Rozin, P., & Royzman, E. *Negativity Bias, Negativity Dominance, and Contagion.* *Personality and Social Psychology Review* 5(4): 296–320; Tversky, A., & Kahneman, D. *Judgment under Uncertainty: Heuristics and Biases.* *Science* 185(4157): 1124–1131. citeturn37view4turn4search3turn5search8 | 1974–2001; behavioral economics, cognitive psychology | Losses and negative cues loom larger than gains; vivid, available examples distort perceived risk; anchors bias later judgment. Key variables: loss aversion \(\lambda\), negative-weight multiplier, availability salience, anchor susceptibility. citeturn37view4turn5search8 | Useful for **APB + MI + RF + AD**: why crisis bad news spikes faster, feels more urgent, and decays more slowly. Supports **Sim**, modest **Fcst**, strong **Intv** and **Crisis**. **Priority: MVP for negativity / loss aversion; V2 for anchoring**. | Effects are context-sensitive. Ethically, Sentigraph should never recommend heightened fear framing simply because it “works.” citeturn37view4turn4search3 |
| **Framing theory.** Entman, R. M. *Framing: Toward Clarification of a Fractured Paradigm.* *Journal of Communication* 43(4): 51–58. citeturn5search10turn5search13turn37view6 | 1993; communication studies | Frames make selected aspects of reality more salient and guide problem definition, causal interpretation, moral evaluation, and remedy. Key variables: frame type, salience, causal attribution, remedy emphasis. citeturn5search13 | Fundamental **MI + IS + Crisis** module for comparing clarification, apology, compensation, evidence, and progress-update frames. Supports **Sim**, **Intv**, **Crisis**. **Priority: MVP**. | Frame effects vary by audience priors and media context. Ethically, framing must stay transparent and evidence-based, not deceptive through omission. citeturn5search13turn35view6 |
| **Illusory truth, mere exposure, and repetition effects.** Fazio, L. K., et al. *Knowledge Does Not Protect Against Illusory Truth.* *Journal of Experimental Psychology: General*; Zajonc, R. B. *Attitudinal Effects of Mere Exposure.* *Journal of Personality and Social Psychology* 9(2, Pt. 2). citeturn37view7turn6search1 | 1968–2015; cognitive psychology | Repetition increases perceived truth and familiarity; repeated exposure can increase positive affect. Key variables: exposure count, repetition spacing, fluency, credibility increment, familiarity. citeturn37view7turn6search1 | Needed for **MI + AD + IS**: repeated official updates can help, but repetition of false claims can also entrench them. Supports **Sim**, **Intv**, **Crisis**. **Priority: MVP for repetition accounting**. | Effects are not the same for all content types. Ethically, never simulate “repeat falsehood for reach” tactics; cap exposure benefits for unverified claims. citeturn37view7turn28search1 |
| **Psychological reactance and public commitment.** Brehm’s reactance theory, reviewed by Steindl et al., *Understanding Psychological Reactance*; public-commitment effects in attitude change work. citeturn6search18turn7search2 | 1966 onward; social psychology, persuasion | Threats to autonomy can trigger resistance and pushback; publicly committed positions become harder to revise without face-saving pathways. Key variables: reactance \(\rho_i\), threat perception, commitment level, face-saving cost. citeturn6search18turn7search2 | Important for **APB + MI + IS + Crisis**: avoid scolding, coercive, or patronizing corrective messages; add face-saving exits. Supports **Sim**, **Intv**, **Crisis**. **Priority: MVP**. | Hard to estimate directly. Ethically, the point is to reduce coercion and preserve dignity, not to engineer obedience while circumventing autonomy. citeturn6search18turn7search2 |
| **Spiral of silence, social identity, moral grandstanding.** Noelle-Neumann, E. *The Spiral of Silence: A Theory of Public Opinion.* *Journal of Communication* 24(2): 43–51; Tajfel, H., & Turner, J. C. *The Social Identity Theory of Intergroup Behavior*; Grubbs, J. B., et al. *Moral Grandstanding in Public Discourse.* citeturn37view10turn40view0turn38search17turn7search1 | 1974 onward; communication, social psychology, moral psychology | People may withhold expression when they fear isolation; group identities shape in-group/out-group alignment; some public moral talk is status-seeking and conflict-amplifying. Key variables: latent opinion vs expressed opinion, isolation sensitivity, identity strength, status-seeking, outrage reward. citeturn37view10turn40view0turn7search1 | Essential for separating **private belief** from **public posting** in **APB + MI + EC + RF**. Supports **Sim**, **Fcst**, **Intv**, **Crisis**. **Priority: V2**, but the latent/expressed split is worth MVP if feasible. | Difficult to validate from public data alone. Ethically, never use this layer to suppress minorities or manage appearance rather than substance. citeturn37view10turn36view1 |
| **Source credibility, two-step flow, opinion leaders.** Hovland, C. I., & Weiss, W. *The Influence of Source Credibility on Communication Effectiveness.* *Public Opinion Quarterly* 15(4): 635–650; Katz, E. *The Two-Step Flow of Communication: An Up-To-Date Report on an Hypothesis.* *Public Opinion Quarterly* 21(1): 61–78. citeturn35view3turn10search5turn8search6turn10search15 | 1951–1957; communication, public opinion | Message effects depend heavily on who says them; many people are influenced indirectly via opinion leaders and interpersonal intermediaries. Key variables: source trustworthiness, expertise, leader centrality, relay probability. citeturn10search5turn8search6 | Critical **MI + NI + IS + Crisis** module: third-party experts, local bridge figures, and trusted institutions should be modeled separately from the focal organization. Supports **Sim**, **Intv**, **Crisis**. **Priority: MVP**. | Credibility is contextual and can change during a crisis. Ethically, only use transparent, disclosed third-party evidence; never covert influencer operations. citeturn35view3turn13search11 |
| **Emotional contagion.** Kramer, A. D. I., Guillory, J. E., & Hancock, J. T. *Experimental Evidence of Massive-Scale Emotional Contagion Through Social Networks.* *PNAS* 111(24): 8788–8790. citeturn9search0turn9search4 | 2014; computational social science | Exposure to others’ emotionally valenced content shifts subsequent emotional expression. Key variables: emotional valence, exposure share, contagion coefficient. citeturn9search4 | Useful for **MI + AD + RF** as a low-amplitude affect-transfer layer. Supports **Sim** and some **Fcst**; indirect **Intv** and **Crisis**. **Priority: later research / cautious V2**. | Effect sizes are not obviously large, and the study itself triggered major ethical criticism. Sentigraph should use only transparent, nonexperimental public-data inference and keep this module bounded. citeturn9search4turn9news37 |
| **Agenda-setting, issue-attention cycle, salience decay, event competition.** McCombs, M. E., & Shaw, D. L. *The Agenda-Setting Function of Mass Media.* *Public Opinion Quarterly* 36(2): 176–187; Downs, A. *Up and Down with Ecology: The “Issue-Attention Cycle.”* *The Public Interest*; Asur, S., Huberman, B. A., Szabo, G., & Wang, C. *Trends in Social Media: Persistence and Decay*; Xu et al. topic-competition work. citeturn35view5turn11search9turn25search15turn11search14 | 1972 onward; communication, public policy, social computing | Media and social attention determine what people think about; issues rise, peak, and decay; topics compete for limited attention. Key variables: topic salience, novelty, competition term, decay half-life, media prominence. citeturn35view5turn11search9turn25search15 | Core **AD + RF + MI** module. Needed for issue fatigue, outrage fatigue, and whether one crisis crowds out another. Supports **Sim**, **Fcst**, **Intv**, **Crisis**. **Priority: MVP**. | Aggregate salience is easier to model than individual cognition. Ethically, simulate attention competition descriptively; do not recommend attention diversion tactics. citeturn35view5turn11search9 |
| **SCCT, Image Repair, and social-media crisis communication.** Coombs, W. T., & Holladay, S. J. *Helping Crisis Managers Protect Reputational Assets: Initial Tests of the Situational Crisis Communication Theory.* *Management Communication Quarterly* 16(2): 165–186; Benoit, W. L. *Image Repair Discourse and Crisis Communication.* *Public Relations Review* 23(2): 177–186; Eriksson, M. *Lessons for Crisis Communication on Social Media.* *International Journal of Strategic Communication* 12(5): 526–551. citeturn35view7turn35view6turn39view1 | 1997–2018; crisis communication, public relations | SCCT ties response strategy to perceived crisis responsibility; Image Repair provides a taxonomy of response types; social-media crisis research emphasizes dialogue, timing, source, monitoring, and continuing importance of traditional media. citeturn35view7turn35view6turn39view1 | This is the direct backbone for the **IS + Crisis** module. Supports **Sim**, moderate **Fcst**, strong **Intv**, direct **Crisis**. **Priority: MVP**. | Much of the literature is organization-centric and reputation-centric. Ethically, use only truth-promoting strategies: clarification, acknowledgment, remedy, verification, and update cadence. citeturn35view7turn35view6turn39view1 |
| **Apology, compensation, and third-party verification.** Coombs, W. T., & Holladay, S. J. *Comparing Apology to Equivalent Crisis Response Strategies*; Kiambi et al. work comparing sympathy, compensation, and apology; Heinze, J., Uhlmann, E. L., & Diermeier, D. *Credibility Transfer During a Corporate Crisis*; trusted endorsements research by Mena. citeturn14search16turn14search8turn13search11turn13search7turn39view2 | 2008 onward; crisis communication, persuasion | Responsibility admission and sympathetic expression can reduce anger; compensation matters but interacts with prior reputation and attribution; announced independent investigation can transfer credibility; trusted endorsements alter perceived credibility. citeturn39view2turn14search8turn13search11turn13search7 | Directly supports **IS + Crisis** scenario design: apology variants, FAQ, compensation, third-party audit, progress updates. Supports **Sim**, **Intv**, **Crisis**. **Priority: MVP for apology and third-party evidence; V2 for richer compensation logic**. | Effects are context-dependent and can look hollow if unsupported by action. Ethically, only simulate interventions that correspond to real operational remedies and evidence. citeturn13search11turn39view2 |
| **Inoculation, prebunking, debunking, fact-checking, backfire debate.** McGuire’s inoculation line as reviewed by Lewandowsky & van der Linden, *Countering Misinformation and Fake News Through Inoculation and Prebunking*; Roozenbeek & van der Linden’s *Bad News* and video-based inoculation studies; Walter et al. *Fact-Checking: A Meta-Analysis of What Works and for Whom*; Chan & Albarracín’s correction meta-analysis; Wood & Porter’s *The Elusive Backfire Effect*. citeturn30view10turn35view9turn29search17turn31search16turn27search4turn16search6turn28search17turn28search9 | 2019–2023; misinformation research, political communication | Preemptive warnings about manipulation tactics can build resistance; fact-checking and corrections work on average, though not perfectly; continued influence often remains; strong backfire effects appear rarer than once feared. citeturn30view10turn35view9turn31search16turn27search4turn16search6 | Core **MI + IS + Crisis** module for correction timing, frequency, and source choice. Supports **Sim**, **Fcst**, **Intv**, and direct **Crisis**. **Priority: MVP**. | Effects are typically modest, decay over time, and depend on trust and repetition. Ethically, correction modules must inform and protect, not preemptively manipulate people into a desired political alignment. citeturn30view10turn31search16turn28search1 |
| **ABM methodology, documentation, calibration, validation.** Grimm et al. ODD protocol (2006, 2010, 2020); Müller et al. *Describing Human Decisions in Agent-Based Models*; Laatabi et al. *ODD+2D*; Windrum et al. *Empirical Validation of Agent-Based Models*; Collins et al. *Methods That Support the Validation of Agent-Based Models.* citeturn17search0turn17search1turn17search6turn18search11turn19search0turn20search11turn30view8 | 2006–2024; agent-based modeling, simulation science | ODD standardizes model descriptions; ODD+D adds human decision logic; ODD+2D formalizes data-to-agent mapping; recent validation work emphasizes docking, empirical validation, sampling, visualization, bootstrapping, causal analysis, and stakeholder credibility. citeturn17search6turn18search11turn19search0turn30view8 | Supports every Sentigraph module and is non-negotiable for rigor. Strongly supports **Sim**, **Fcst**, **Intv**, and governance. **Priority: MVP from day one**. | Adds process overhead, but skipping it makes results hard to defend. Ethically, document assumptions, uncertainty, and intended scope in a model card. citeturn30view8turn20search3turn19search5 |
| **Dynamic network evolution, Hawkes/self-exciting diffusion, platform mediation, cross-platform spread.** Farajtabar et al. *COEVOLVE*; Zhao et al. *SEISMIC*; Bakshy et al.; Cinelli et al.; Murdock et al. cross-platform ABM. citeturn25search16turn25search9turn30view6turn37view0turn26search4 | 2015–2024; machine learning, social computing, network science | Information diffusion and network evolution can coevolve; point processes model self-excitation after posts/reshares; platform structure and affordances change exposure; users can spread across multiple platforms. Key variables: base intensity \(\mu\), excitation kernel \(\alpha e^{-\beta \Delta t}\), rewiring probability, platform action type, migration propensity. citeturn25search16turn25search9turn37view0turn26search4 | Best for **RF + AD + NI + EC** once MVP is stable. Supports **Sim**, stronger short-run **Fcst**, **Intv** testing under platform differences. **Priority: V2 / later research**. | Data-hungry, platform-specific, and easy to overfit. Ethically, never use this layer to reverse-engineer ranking exploitation or cross-platform amplification tactics. citeturn25search16turn20search3 |

## Sentigraph model design

**C. Model variables that can be used in Sentigraph.** A practical Sentigraph state space should distinguish between **latent belief**, **expressed stance**, **readiness to act**, **attention**, **trust/credibility**, and **network position**. At minimum, define for each agent: a continuous latent opinion \(x_i\in[-1,1]\); an expressed public position \(e_i\) that can differ from \(x_i\) because of spiral-of-silence pressures or face-saving constraints; a stubbornness / prior-anchor parameter \(g_i\); a bounded-confidence width \(\varepsilon_i\); an action threshold \(\theta_i\); a confirmation-bias coefficient \(\beta_i\); a motivated-reasoning coefficient \(m_i\); a negativity multiplier \(\nu_i\); a reactance coefficient \(\rho_i\); a source-trust vector \(c_{i,s}\); an identity-strength vector \(I_i\); a public-commitment score \(k_i\); an attention budget \(A_i(t)\); an issue-fatigue term \(f_i(t)\); and an activity rhythm or posting propensity \(\lambda_i(t)\). Those variables map cleanly onto the FJ, HK, Granovetter/Watts, credibility, confirmation-bias, prospect/negativity, reactance, spiral-of-silence, and attention-decay literatures. citeturn32view1turn34view2turn32view4turn36view2turn35view3turn37view2turn37view3turn37view4turn6search18turn37view10turn11search9turn25search15

**D. Suggested agent schema.** A good starting schema is:

```yaml
Agent:
  id: string
  community_id: string
  platform_membership: [twitter_like, reddit_like, forum_like, news_comment_like]
  latent_opinion: float        # [-1, 1]
  expressed_opinion: float     # public stance, may differ from latent_opinion
  prior_anchor: float          # x_i(0)
  stubbornness: float          # g_i
  confidence_radius: float     # epsilon_i
  action_threshold: float      # theta_i
  confirmation_bias: float
  motivated_reasoning: float
  negativity_weight: float
  reactance: float
  public_commitment: float
  identity_vector: {group_a: float, group_b: float, ...}
  trust_by_source: {official: float, media: float, expert: float, peer: float, bridge_node: float}
  attention_budget: float
  fatigue: float
  activity_intensity: float
  narrative_states:
    rumor_belief: float
    correction_acceptance: float
    trust_in_actor: float
    anger: float
    sympathy: float
  network_metrics:
    degree: int
    bridge_score: float
    brokerage_score: float
    cross_cutting_exposure_rate: float
```

This schema is grounded in opinion anchoring and susceptibility from FJ, confidence-gating from HK and Deffuant, threshold action from Granovetter and Watts, identity and expression dynamics from Tajfel/Turner and Noelle-Neumann, source credibility and opinion-leader effects from Hovland/Weiss and Katz, and salience/fatigue dynamics from Downs and trend-decay work. citeturn32view1turn34view2turn32view3turn32view4turn36view2turn40view0turn37view10turn35view3turn8search6turn11search9turn25search15

**E. Suggested message and event schema.** The simulator should treat messages as structured objects rather than plain text blobs. That lets you compare claims, frames, sources, and intervention packages without overfitting to wording.

```yaml
Message:
  id: string
  event_id: string
  timestamp: datetime
  source_type: [organization, regulator, journalist, fact_checker, expert, peer, bridge_node]
  intervention_type: [organic_post, clarification, faq, apology, compensation, progress_update,
                      third_party_verification, correction, prebunking, rumor]
  frame:
    problem_definition: string
    attribution: [victim, accidental, preventable, contested]
    remedy: [none, clarify, apologize, compensate, investigate, correct, update]
  stance_direction: float          # pushes toward/away from trust or belief
  evidence_strength: float
  specificity: float
  emotional_valence: float         # negative to positive
  identity_affirmation: float
  autonomy_threat: float           # higher => more reactance risk
  novelty: float
  repetition_signature: string
  platform_affordance: [post, repost, quote, comment, like, dislike, downvote, share]
  visibility_seed: float
```

The best theoretical anchors here are Entman’s framing model, SCCT’s attribution-based response matching, Benoit’s image-repair taxonomy, Eriksson’s review of message/source/timing, source credibility theory, and the inoculation/debunking literature. The reason to make **autonomy_threat** explicit is to prevent “helpful” corrections from triggering reactance; the reason to make **repetition_signature** explicit is to model both progress-update benefits and illusory-truth risks. citeturn5search13turn35view7turn35view6turn39view1turn35view3turn30view10turn37view7

**F. Suggested network schema.** Sentigraph needs both a graph and a feed layer. The graph captures durable ties; the feed layer captures what people actually see.

```yaml
Network:
  nodes: Agent[]
  edges:
    - src: agent_id
      dst: agent_id
      tie_weight: float
      tie_type: [follow, friend, reply, quote, mention, group_membership]
      trust_weight: float
      conflict_history: float
      homophily_score: float
      bridge_flag: bool

FeedPolicy:
  platform_id: string
  ranking_mode: [chronological, engagement_biased, community_biased, hybrid]
  visibility_decay_half_life: float
  repost_multiplier: float
  quote_multiplier: float
  reply_multiplier: float
  correction_boost: float
  misinformation_penalty: float
```

This split is supported by research showing that friend-network composition, choice behavior, and platform ranking each shape cross-cutting exposure differently, and that platforms differ in affordances such as likes, comments, retweets, and group interactions. It also lets you test whether a response works because it is **credible**, because it travels through **bridge nodes**, or because it was simply **more visible**. citeturn30view6turn37view0turn21search2turn21search6turn36view4

**G. Suggested intervention schema.** Interventions should be explicit packages with operational attributes, not one-dimensional labels.

```yaml
Intervention:
  id: string
  launch_time: datetime
  type: [clarification, faq, apology, compensation, progress_update,
         third_party_verification, correction, prebunking]
  responsible_party: source_type
  responsibility_admission: float
  empathy_level: float
  compensation_level: float
  evidence_package_strength: float
  third_party_investigation: bool
  cadence: [one_off, daily, milestone_based]
  target_scope: [aggregate_public, affected_users, media, bridge_communities]
  transparency_label: bool
```

This structure follows SCCT, image-repair and apology research, third-party verification findings, and social-media crisis communication guidance emphasizing message, source, and timing. For Sentigraph, the most important comparison is not “which tactic persuades most,” but “which truthful package restores trust fastest, corrects falsehoods best, and does least harm.” citeturn35view7turn35view6turn39view1turn39view2turn13search11

## Simulation logic and validation

**H. Suggested simulation update rules.** A prudent Sentigraph update cycle is a **hybrid of continuous opinion, discrete action, and dynamic attention**.

A strong default continuous update is a **bounded-confidence Friedkin-Johnsen hybrid**:

\[
x_i(t+1)=g_i x_i(0) + (1-g_i)\sum_{j\in \mathcal{N}_i^\varepsilon(t)} \tilde{w}_{ij}(t)\,x_j(t),
\]

where \(\mathcal{N}_i^\varepsilon(t)\) includes only sources inside the agent’s confidence radius, except that highly trusted expert or verified corrective sources can be assigned a reduced gate instead of a full exclusion. This combines prior-belief persistence from FJ with HK-style interaction filtering. citeturn32view1turn34view2

For dyadic discussion or reply-thread interactions, keep an optional **Deffuant micro-step**:

\[
x_i' = x_i + \mu_i(x_j-x_i), \qquad x_j' = x_j + \mu_j(x_i-x_j)
\]

whenever pairwise difference is below a dyadic discussion threshold. This is a good fit for conversational interactions that are weaker than broadcast exposure but more persuasive than passive viewing. citeturn32view3

Public behavior should be discrete, not continuous. Let visible actions such as **posting**, **reposting**, **endorsing a correction**, or **joining a hostile wave** follow a threshold/reinforcement rule. One clean option is:

\[
\Pr(y_i(t+1)=1)=\sigma\!\left[
\alpha_1 S_i(t) + \alpha_2 R_i(t) + \alpha_3 C_i(t) + \alpha_4 N_i(t)
-\alpha_5 \rho_i - \alpha_6 f_i(t)
\right],
\]

where \(S_i\) is social proof or activated-neighbor share, \(R_i\) is reinforcement count, \(C_i\) is source credibility, \(N_i\) is negative salience, \(\rho_i\) is reactance, and \(f_i(t)\) is fatigue. This is not a canonical equation from one paper; it is a practical synthesis of threshold, complex-contagion, source-credibility, negativity, and reactance findings. citeturn32view4turn36view2turn36view4turn35view3turn37view4turn6search18

Attention should be stateful. A topic-level attention variable can be updated as:

\[
A_k(t+1)=\gamma_k A_k(t)+\text{shock}_k(t)+\text{selfExcite}_k(t)-\omega_k \text{competition}_k(t)-\phi_k \text{fatigue}_k(t).
\]

Use **Downs** for rise-and-fade intuition, **trend persistence/decay** for salience half-life, and a **Hawkes-style self-excitation term** for bursty reshare dynamics:

\[
\lambda_k(t)=\mu_k+\sum_{n:t_n<t}\alpha_k e^{-\beta_k(t-t_n)}.
\]

That gives Sentigraph a principled way to represent issue-attention cycles, breaking-news bursts, and correction windows. citeturn11search9turn25search15turn25search9

Message scoring should also be explicit. A useful visibility-and-credibility score is:

\[
\text{score}_{i,m}(t)=V_m(t)\cdot c_{i,s(m)}\cdot h_i(m)\cdot a_i(t)\cdot d_m(t),
\]

where \(V_m\) is platform visibility, \(c_{i,s(m)}\) is source trust, \(h_i(m)\) is bias-congruence / identity fit, \(a_i(t)\) is available attention, and \(d_m(t)\) is novelty-decay or repetition adjustment. This lets the simulator distinguish **what was posted** from **what was seen and believed**. citeturn30view6turn37view0turn35view3turn37view2turn37view3turn37view7

Network rewiring should be optional in MVP and richer in V2. If enabled, ties can update via follow/unfollow/block/mute rules driven by homophily, conflict, and bridge value. Coevolutionary network work suggests that opinion dynamics and relationship dynamics can reshape each other, but that layer is data-heavy and easy to overfit, so it belongs after a stable static-network version exists. citeturn24search10turn24search15turn25search16turn24search13

**Evaluation metrics for simulation output.** For Sentigraph, the most useful output metrics are not generic “accuracy” alone but **opinion-structure**, **diffusion**, **correction**, and **harm** measures. A good minimal set is: polarization index across communities; opinion entropy; network modularity; cross-cutting exposure rate; narrative dominance share; sentiment volatility; misinformation persistence; correction uptake rate; trust recovery curve; apology acceptance probability; reputational-risk score; intervention-harm score; and an ethical-risk score that flags when a scenario depends on concentrated influence through very few bridge nodes or on assumptions with poor empirical support. These metrics are directly motivated by the polarization, echo-chamber, salience-decay, crisis, and misinformation literatures you identified. citeturn37view0turn30view6turn35view7turn39view1turn31search16turn27search4

**L. Calibration and validation plan.** Sentigraph should ingest three classes of real-world data: **content data** such as posts, official statements, fact checks, and timestamps; **network / exposure data** such as follows, replies, repost trees, and if available impression or view data; and **ground-truth calibration data** such as polling or survey panel measurements, trust trackers, crisis timelines, moderation logs, or known correction windows. ODD+2D is particularly relevant here because it was built to formalize how raw empirical data are transformed into agent states and behavioral rules. citeturn19search0turn30view6turn37view0turn25search9turn35view7turn31search16

The parameters most plausibly estimated from data are: network topology and edge weights; community structure; assortativity / homophily; source-credibility priors by source class; message-decay half-life; Hawkes excitation and decay parameters; baseline activity rhythms; public-action threshold distributions at the aggregate level; and short-run shifts in anger, trust, or correction uptake after interventions. Parameters that usually remain assumption-heavy are individual reactance, private commitment, latent identity salience in a specific event, true private opinion where only expression is observed, and the exact strength of motivated reasoning at the person level. Those should be separated visually in system outputs as “estimated” versus “assumed.” citeturn19search0turn30view8turn25search9turn6search18turn37view3turn37view10

Validation should happen in layers. First, perform **structural validation**: confirm that the implemented rules match the conceptual model and are documented in ODD. Second, do **historical replay validation**: run the simulator on past crisis timelines and compare observed versus simulated peaks, correction uptake, trust recovery direction, and cross-community spillover. Third, use **docking** against simpler baselines such as DeGroot-only, threshold-only, or Hawkes-only models. Fourth, run **sensitivity and ablation tests** to determine whether outputs are robust to homophily, confidence-radius, threshold, attention-decay, and source-credibility assumptions. Collins et al. explicitly identify docking, empirical validation, sampling, visualization, bootstrapping, and causal analysis as important validation supports for ABM. citeturn30view8turn32view5turn17search6turn20search11

A practical historical-validation workflow for Sentigraph would be: choose several well-documented public crises; reconstruct the topic graph and intervention timeline; fit only the network, activity, and decay parameters on the first segment; then hide later phases and test whether the model can reproduce broad-direction outcomes such as anger amplification, cross-community penetration, correction uptake, and trust rebound after apology or evidence release. The right question is not “did the model predict every post,” but “did it reproduce the timing, direction, and relative magnitude of meso-level public-opinion transitions under known intervention sequences?” That is much closer to what ABMs are good at. citeturn35view7turn39view1turn31search16turn27search4turn30view8

## Ethical boundaries and abuse prevention

**I. Ethical boundary section.** Sentigraph should explicitly define itself as a **descriptive and comparative crisis-response simulator**, not a persuasion engine. The allowed use is to compare transparent interventions such as clarification, acknowledgment, FAQ, correction, progress updates, compensation, or third-party review under uncertainty. The disallowed use is to identify which population slice is most pliable, which emotional trigger is most destabilizing, or which ranking / seeding strategy would maximize compliance or crowd hostility. Recent work on credible and responsible social modeling strongly supports explicit statement of model purpose, limits, uncertainty, and scope. citeturn20search3turn19search5turn30view8

**M. Abuse-risk assessment.** The clearest misuse paths are straightforward: using the simulator to test fake-consensus campaigns, synthetic grassroots operations, covert influencer strategies, reaction-maximizing copy, bot-amplified swarm behavior, or individualized manipulation. Functions that should therefore be blocked include: people-level persuasion scoring; account-level “most influenceable users” lists; simulated bot or sockpuppet injection; stealth message-seeding recommendations; tactics for exploiting reactance, identity threat, or isolation fear; and any recommendation that withholds correction because letting false narratives spread would create a more useful emotional state. Those are precisely the kinds of lines an ethical public-opinion simulator should refuse to cross. citeturn20search3turn19search5turn28search1turn30view10

Outputs should be **aggregate-only** by default: confidence-banded scenario trajectories, community-level diffusion metrics, fairness / harm checks, uncertainty intervals, and comparative intervention summaries. Sentigraph should never output named individuals, “high-yield” targets, or tactical guidance for exploiting bridge nodes or authority figures. If bridge-node analysis is used at all, it should be framed as “which public intermediaries might help truthful, disclosed clarification cross a structural divide,” not “who can be weaponized for reach.” citeturn21search2turn21search6turn36view4turn20search3

The simulator should also generate an **audit trail** for every run: data sources, fitted parameters, assumed parameters, intervention package, uncertainty treatment, and known methodological risks such as homophily–contagion confounding or platform-data incompleteness. Human review should be mandatory before any recommendation is externalized, and that review should include at least a domain owner, a communications lead, and an ethics or governance reviewer. That requirement is especially important because validation research emphasizes that credibility is relational: users trust a model when its construction, assumptions, and purpose are inspectable. citeturn36view0turn36view1turn30view8turn20search3

## Implementation roadmap

**J. Recommended MVP implementation roadmap.** Build the first working simulator in phased layers, not all at once.

**Phase one: required MVP model selection.** Implement these modules first:
- **Friedkin-Johnsen core** for latent opinion persistence under social influence. citeturn32view1
- **Bounded-confidence gate** to stop unrealistic all-to-all mixing and to produce fragmentation when communities are far apart. citeturn34view2
- **Granovetter-style action thresholds** for visible behaviors such as reposting, condemning, defending, and accepting corrections. citeturn32view4
- **Homophilous static network with bridge metrics** and a separate feed-visibility layer. citeturn21search2turn30view6turn37view0
- **Source credibility + framing** in message scoring. citeturn35view3turn5search13
- **Attention decay / issue salience** for event rise and fade. citeturn11search9turn25search15
- **Intervention library** grounded in SCCT, Image Repair, apology, progress updates, third-party verification, and correction / prebunking. citeturn35view7turn35view6turn39view1turn13search11turn30view10
- **ODD documentation + docking + sensitivity analysis** from the first prototype onward. citeturn17search6turn30view8

This MVP is enough to compare crisis-response scenarios honestly and defensibly. It is also sufficiently modular that you can later swap alternative influence kernels without rewriting the entire system. citeturn30view8turn17search6

**Phase two: V2 modules.** After MVP is stable, add:
- **Deffuant micro-interaction layer** for conversational threads. citeturn32view3
- **Watts cascade diagnostics** for global-cascade risk and vulnerable-cluster analysis. citeturn36view3
- **Complex contagion** for behaviors requiring reinforcement, especially correction acceptance or coordinated de-escalation. citeturn36view4
- **Latent vs expressed stance split** from spiral-of-silence and public-commitment work. citeturn37view10turn7search2
- **Platform-specific affordance parameters** and community-specific echo-chamber calibration. citeturn37view0turn30view6
- **Hawkes self-excitation** for near-real-time forecast envelopes around surges. citeturn25search9

**Phase three: later research.** Hold these until the model is already validated on historical events:
- full **dynamic rewiring** with follow/unfollow/block/mute. citeturn24search15turn25search16
- full **cross-platform diffusion and migration** modeling. citeturn26search4
- high-dimensional identity / outrage / grandstanding reward systems. citeturn7search1turn40view0
- generative language-agent modules or anything LLM-heavy, because current reviews continue to identify validation as the central challenge for generative social simulation. citeturn20search14

**N. Which models should be interchangeable strategy modules.** Sentigraph will be strongest if several modules remain swappable:
- **Opinion kernel:** DeGroot vs FJ vs HK vs Deffuant. citeturn32view0turn32view1turn34view2turn32view3
- **Action rule:** voter vs Granovetter vs Watts vs complex contagion. citeturn41search1turn32view4turn36view2turn36view4
- **Attention model:** simple exponential decay vs trend-decay vs Hawkes. citeturn25search15turn25search9
- **Intervention layer:** SCCT / Image Repair / correction-only / hybrid evidence-first packages. citeturn35view7turn35view6turn30view10

Keeping these interchangeable is good science and good governance: it makes Sentigraph easier to validate, easier to explain, and harder to misuse as a black-box “optimization oracle.” citeturn30view8turn20search3

## Bibliography with links

**K. Bibliography with links.** The entries below are a compact core bibliography for building the first serious version of Sentigraph. The citation markers link to open-access or official source pages.

DeGroot, Morris H. 1974. “Reaching a Consensus.” *Journal of the American Statistical Association* 69(345): 118–121. citeturn0search0

Friedkin, Noah E., and Eugene C. Johnsen. 1990. “Social Influence and Opinions.” *Journal of Mathematical Sociology* 15: 193–206. citeturn0search1

Hegselmann, Rainer, and Ulrich Krause. 2002. “Opinion Dynamics and Bounded Confidence Models, Analysis, and Simulation.” *Journal of Artificial Societies and Social Simulation* 5(3). citeturn34view0

Deffuant, Guillaume, David Neau, Frédéric Amblard, and Gérard Weisbuch. 2000. “Mixing Beliefs Among Interacting Agents.” *Advances in Complex Systems* 3(1–4): 87–98. citeturn30view3

Granovetter, Mark. 1978. “Threshold Models of Collective Behavior.” *American Journal of Sociology* 83(6): 1420–1443. citeturn30view4

Watts, Duncan J. 2002. “A Simple Model of Global Cascades on Random Networks.” *Proceedings of the National Academy of Sciences* 99(9): 5766–5771. citeturn35view0

Centola, Damon, and Michael Macy. 2007. “Complex Contagions and the Weakness of Long Ties.” *American Journal of Sociology* 113(3): 702–734. citeturn35view1

McPherson, Miller, Lynn Smith-Lovin, and James M. Cook. 2001. “Birds of a Feather: Homophily in Social Networks.” *Annual Review of Sociology* 27: 415–444. citeturn3search3

Bakshy, Eytan, Solomon Messing, and Lada A. Adamic. 2015. “Exposure to Ideologically Diverse News and Opinion on Facebook.” *Science* 348(6239): 1130–1132. citeturn21search3turn30view6

Cinelli, Matteo, et al. 2021. “The Echo Chamber Effect on Social Media.” *Proceedings of the National Academy of Sciences* 118(9). citeturn26search22turn37view0

Shalizi, Cosma Rohilla, and Andrew C. Thomas. 2011. “Homophily and Contagion Are Generically Confounded in Observational Social Network Studies.” *Sociological Methods & Research* 40(2): 211–239. citeturn36view0turn36view1

Nickerson, Raymond S. 1998. “Confirmation Bias: A Ubiquitous Phenomenon in Many Guises.” *Review of General Psychology* 2(2): 175–220. citeturn37view2

Kunda, Ziva. 1990. “The Case for Motivated Reasoning.” *Psychological Bulletin* 108(3): 480–498. citeturn37view3

Kahneman, Daniel, and Amos Tversky. 1979. “Prospect Theory: An Analysis of Decision under Risk.” *Econometrica* 47(2): 263–291. citeturn37view4

Tversky, Amos, and Daniel Kahneman. 1974. “Judgment Under Uncertainty: Heuristics and Biases.” *Science* 185(4157): 1124–1131. citeturn5search8

Entman, Robert M. 1993. “Framing: Toward Clarification of a Fractured Paradigm.” *Journal of Communication* 43(4): 51–58. citeturn5search10turn5search13

Fazio, Lisa K., et al. 2015. “Knowledge Does Not Protect Against Illusory Truth.” *Journal of Experimental Psychology: General.* citeturn37view7

Zajonc, Robert B. 1968. “Attitudinal Effects of Mere Exposure.” *Journal of Personality and Social Psychology* 9(2, Pt. 2). citeturn6search1

Noelle-Neumann, Elisabeth. 1974. “The Spiral of Silence: A Theory of Public Opinion.” *Journal of Communication* 24(2): 43–51. citeturn7search11turn37view10

Hovland, Carl I., and Walter Weiss. 1951. “The Influence of Source Credibility on Communication Effectiveness.” *Public Opinion Quarterly* 15(4): 635–650. citeturn10search5turn35view3

Katz, Elihu. 1957. “The Two-Step Flow of Communication: An Up-To-Date Report on an Hypothesis.” *Public Opinion Quarterly* 21(1): 61–78. citeturn8search6turn10search15

McCombs, Maxwell E., and Donald L. Shaw. 1972. “The Agenda-Setting Function of Mass Media.” *Public Opinion Quarterly* 36(2): 176–187. citeturn12search1turn35view5

Downs, Anthony. 1972. “Up and Down with Ecology: The ‘Issue-Attention Cycle.’” *The Public Interest* 28. citeturn11search1turn11search9

Asur, Sitaram, Bernardo A. Huberman, Gábor Szabó, and Chunyan Wang. 2011. “Trends in Social Media: Persistence and Decay.” *ICWSM.* citeturn25search15

Coombs, W. Timothy, and Sherry J. Holladay. 2002. “Helping Crisis Managers Protect Reputational Assets: Initial Tests of the Situational Crisis Communication Theory.” *Management Communication Quarterly* 16(2): 165–186. citeturn35view7

Benoit, William L. 1997. “Image Repair Discourse and Crisis Communication.” *Public Relations Review* 23(2): 177–186. citeturn35view6

Eriksson, Mats. 2018. “Lessons for Crisis Communication on Social Media: A Systematic Review of What Research Tells the Practice.” *International Journal of Strategic Communication* 12(5): 526–551. citeturn39view1

Lewandowsky, Stephan, and Sander van der Linden. 2021. “Countering Misinformation and Fake News Through Inoculation and Prebunking.” *European Review of Social Psychology.* citeturn30view10turn28search14

Roozenbeek, Jon, and Sander van der Linden. 2019. “Fake News Game Confers Psychological Resistance Against Online Misinformation.” *Palgrave Communications* 5(65). citeturn29search2turn29search8

Roozenbeek, Jon, et al. 2022. “Psychological Inoculation Improves Resilience Against Misinformation.” *Science Advances* 8(34). citeturn29search17

Walter, Nathan, Jonathan Cohen, R. Lance Holbert, and Yasmin Morag. 2020. “Fact-Checking: A Meta-Analysis of What Works and for Whom.” *Political Communication* 37(3): 350–375. citeturn28search3turn31search16

Chan, Man-pui Sally, and Dolores Albarracín. 2023. “A Meta-Analysis of Correction Effects in Science-Relevant Misinformation.” *Nature Human Behaviour* 7(9): 1514–1525. citeturn27search4turn27search9

Wood, Thomas, and Ethan Porter. 2019. “The Elusive Backfire Effect: Mass Attitudes’ Steadfast Factual Adherence.” *Political Behavior* 41: 135–163. citeturn16search6turn16search18

Grimm, Volker, et al. 2006. “A Standard Protocol for Describing Individual-Based and Agent-Based Models.” *Ecological Modelling.* citeturn17search0

Grimm, Volker, et al. 2010. “The ODD Protocol: A Review and First Update.” *Ecological Modelling* 221: 2760–2768. citeturn17search1

Grimm, Volker, et al. 2020. “The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism.” *JASSS* 23(2): 7. citeturn17search6turn30view7

Müller, Birgit, et al. 2013. “Describing Human Decisions in Agent-Based Models—ODD + D, an Extension of the ODD Protocol.” *Environmental Modelling & Software* 48: 37–48. citeturn18search11turn19search8

Laatabi, Abdelghani, et al. 2018. “An ODD Based Protocol for Mapping Data to Empirical ABMs.” *Journal of Artificial Societies and Social Simulation* 21(2): 9. citeturn19search0

Windrum, Paul, Giorgio Fagiolo, and Alessio Moneta. 2007. “Empirical Validation of Agent-Based Models.” *Journal of Artificial Societies and Social Simulation* 10(2): 8. citeturn20search11

Collins, Andrew, et al. 2024. “Methods That Support the Validation of Agent-Based Models.” *Journal of Artificial Societies and Social Simulation* 27(1): 11. citeturn30view8

Farajtabar, Mehrdad, et al. 2015. “COEVOLVE: A Joint Point Process Model for Information Diffusion and Network Co-Evolution.” *NeurIPS.* citeturn25search16

Zhao, Qiaozhu, et al. 2015. “SEISMIC: A Self-Exciting Point Process Model for Predicting Tweet Popularity.” *KDD.* citeturn25search9

Murdock, Ian, et al. 2024. “An Agent-Based Model of Cross-Platform Information Diffusion and Moderation.” *Social Network Analysis and Mining* 14. citeturn26search4turn26search8
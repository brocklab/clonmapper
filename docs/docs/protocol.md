---
hide:
  - navigation
---
## Introduction

Insight into the clonal composition of a cells during key events
such as development, infection, tumor progression, or treatment response,
is critical to understanding the nature of the interaction between
the population of cells and the selective forces shaping it.
While advances in genomics and transcriptomics and the advent
of single-cell RNA sequencing (scRNA-seq) have vastly increased
the resolution at which we can understand cellular processes,
they lack the ability to directly assign clonal relationships.
To meet this need, lineage tracing technologies, such as DNA barcoding,
have been developed to label and track individual cells and their progeny [@blundell2014]^,^[@kebschull2018].
In DNA barcoding, each individual cell in a population is labeled
with a unique random string of nucleotides that is integrated
into the genome and heritable by its daughter cells.
The ensemble of all DNA barcodes in the cell population can be quantified
by next-generation sequencing (NGS) to determine
how clonal abundance changes over time.

While highly informative, DNA barcoding and other lineage tracing techniques
are still limited in that interesting lineages of cells cannot be easily
isolated from the bulk population for clonally pure analysis.
Here, we describe a detailed protocol for **ClonMapper**,
a workflow that enables precise identification and isolation
of populations of interest from heterogeneous mammalian cells [@alkhafaji2018].
ClonMapper is a functionalized variant of DNA barcoding in which the DNA barcode
is a CRISPR-Cas9 compatible single-guide RNA (sgRNA).
The sgRNA-barcode has multiple functionalities: (1) It is an integrated DNA barcode,
(2) It is transcribed and captured in scRNA-seq workflows, and
(3) It can be used to actuate lineage-specific genes of interest using
an activator variant of Cas9 [@chavez2015].
This protocol describes the use of ClonMapper
for lineage-specific activation of GFP,
enabling isolation of clonal cells from a heterogeneous population.

The sgRNA barcode is engineered using the CROPseq method [@datlinger2017] such
that the sgRNA barcode is transcribed by both RNA polymerase III and
RNA polymerase II, creating a functional sgRNA barcode transcript and a
polyadenylated transcript containing the barcode, respectively.

Cells are first transduced with lentivirus containing
a ClonMapper sgRNA barcode vector at a low multiplicity of infection (MOI)
to minimize the integration of multiple barcodes per cell.
In both versions of the vector, the sgRNA barcode is co-expressed
with blue fluorescent protein (BFP) for easy identification and collection of
barcoded cells via flow cytometry and fluorescence-activated cell sorting (FACS).
Once established, the barcoded cell population is available for experimental manipulation.
Clonal dynamics may be measured by NGS analysis and gene expression signatures
of clonal populations may be resolved by scRNA-seq. Once a barcode of interest
is identified from NGS or scRNA-seq, the barcode identifier can be exploited
for isolation of the clone.
This is achieved by transfecting the cell population with a plasmid containing
an activator variant of Cas9 (dCas9-VPR) and a second plasmid containing the
Cas9-homing PAM sites adjacent to the identified barcode upstream of green
fluorescent protein (sfGFP) reporter.
Expression of sfGFP will occur only in cells that are producing the matching
sgRNA barcode, allowing precise identification and FACS isolation of cells
from lineages of interest.
## Materials

Equipment

1. Electroporator
1. Mammalian cell incubator
1. Bacterial cell incubator with shaking
1. Thermocycler
1. Gel electrophoresis box
1. Bioanalyzer
1. Illumina sequencer
1. Flow cytometer with filters for BFP (Ex: 380/20, Em: 460/40)

Disposables

1. Sterile filtered pipette tips
1. 1.5 mL microcentrifuge tubes (sterile)
1. 1.8 mL Screw top cryovials (sterile)
1. 20 mL Luer-tapered syringe (sterile)
1. 0.45 $\mu$m polyethersulfone (PES) syringe filter
1. 30,000 molecular weight cutoff (MWCO) PES concentrator capable of processing 20 mL

Biologics

1. Electrocompetent *e. coli* suitable for unstable DNA (restriction minus,
   endonuclease deficient, and recombination deficient)
1. Cells of interest [^1]

[^1]:  Make sure cells are transducible with lentivirus. Timing of lentiviral exposure and detectable expression of transgene will vary across cell types.

Plasmids

1. CROPseq gRNA expression transfer vector,
   Cropseq-BFP-WPRE-TS-hU6-BsmbI (Addgene \#137993;Brock Lab AA112)
1. Lentiviral packaging plasmid, VSV-G (Addgene #14888)
1. Lentiviral packaging plasmid, psPAX2 (Addgene #12260)
1. dCas9-VPR (Addgene #63798)
1. Recall-miniCMV-sfGFP (Addgene \#137995;Brock Lab AA158)

Primers

(*see* **Table 1**)

Buffers

1. Buffer 3.1: 100 mM NaCl, 50 mM Tris-HCl,
   10 mM MgCl~2~, 100 $\mu$g/ml BSA, pH 7.9 at 25°C
2. NEB 5X Q5 Reaction Buffer
3. 10X T4 PNK Buffer
4. 10 mM dNTPs
5. 1X Tris-acetate-EDTA (TAE)
6. FACS Buffer: 5% FBS, 1-5 mM EDTA, 95% Phosphate-Buffered Saline

Enzymes

1. BsmBI (10,000 U/mL)
1. BbsI (10,000 U/mL)
1. NEB Q5 polymerase
1. T4 ligase (400,000 U/mL )
1. T7 ligase (3,000,000 U/mL)
1. PNK (10,000 U/mL)

Other Reagents

1. Lipofectamine^TM^ 2000
1. Lipofectamine^TM^ 3000
1. Nuclease-free water
1. Agarose
1. DNA Clean and Concentrator kit
1. 2xYT microbial growth medium
1. Dulbecco's Modified Eagle Medium (DMEM)
1. OptiMEM^TM^ reduced serum medium
1. Fetal Bovine Serum (FBS)
1. Carbenicillin
1. Solid Phase Reversible Immobilization (SPRI) paramagnetic beads for PCR cleanup
1. 70% molecular biology grade ethanol in nuclease-free water
1. 10 mg/mL hexadimethrine bromide
1. 0.05% Trypan blue
1. Plasmid Midi-Prep Kit
1. DNA gel purification kit

Computational

1. Linux Computing Environment (Such as University HPC)
1. Python >=3.8
1. Cell Ranger (for 10X analysis)
1. [Pycashier](https://github.com/brocklab/pycashier)
## Methods

### sgRNA Barcode Library Plasmid Pool Assembly

1. Perform a 4X extension reaction to generate the double-stranded
   gRNA insert. Mix the below reagents to create a 50 $\mu$L reaction.[^2]

    | Reagent | volume ($\mu$L) |
    |---|---|
    | 5X Q5 Reaction Buffer | 10 |
    | 10 mM dNTPs | 1 |
    | 100 $\mu$M CROPseq-PrimeF-BgL-BsmBI | 2
    | 100$\mu$M CROPseq-RevExt-BgL-BsmBI | 1
    | Q5 Polymerase | 0.5 |
    | nuclease-free water | to 50 |

1. Run the extension reaction on a thermocycler using the following settings,
   repeating steps 2-3 for 10 cycles:

    | Step | Temp (°C) | Time |
    |---|---|---|
    | 1 | 98 | 2 min |
    | 2 | 65 | 30 sec |
    | 3 | 72 | 10 sec |
    | 4 | 72 | 2 min |
    | 5 | 4 | hold |

1. Clean and concentrate double-stranded gRNA insert PCR product
   and elute in 30 $\mu$L nuclease-free water.
   Confirm dsDNA assembly on 2% agarose gel
   by running single stranded DNA against PCR product.
1. Digest 5-10 $\mu$g of CROPseq vector backbone in a reaction containing
   20 $\mu$L Digestion Buffer 3.1, 8 $\mu$L BsmBI,
   and nuclease-free water to 200 $\mu$L for 4 hours at 55°C
    
1. Run the digested backbone on a 1-1.5% low melting point agarose gel,
   then follow the instructions on a DNA gel purification kit to extract
   and purify the linearized plasmid band.
1. Ligate double stranded gRNA insert into linearized transfer vector backbone
   at a molar ratio of 10:1 in a 50X Golden Gate assembly reaction
   by mixing the below reagents[^3]:

    | Reagent | volume ($\mu$L) |
    |---|---|
    | 1.25 pmol linearized backbone | variable |
    | 12.5 pmol gRNA insert | variable |
    | T4 Ligase Buffer | 50 |
    | T7 Ligase | 25 |
    | BsmBI | 25 |
    | nuclease-free water | to 500 |

1. Run the Golden Gate assembly reaction on a thermocycler
   overnight using the following settings, repeating steps 1-2 for 99 cycles:

    | Step | Temp (°C) | Time |
    |---|---|---|
    | 1 | 42 | 2 min |
    | 2 | 16 | 5 min |
    | 4 | 55 | 30 min |
    | 5 | 4 | hold |

1. Clean barcoding library plasmid pool using a DNA clean and
   concentrator kit and elute in 22 $\mu$L warm, nuclease-free water.[^4]
1. Prepare for *e. coli* electroporation by pre-warming recovery media to room
   temperature, thawing electrocompetent *e. coli* on ice,
   and pre-chilling 2 mm electroporation cuvettes on ice.[^5]
1. Aliquot 100 $\mu$L of E.coli into the chilled 0.2 cm electroporation cuvette,
   add 5 $\mu$L of purified assembled plasmid, and stir with pipet tip.[^6]
1. Transform e. coli by electroporating with 1 pulse at 2.5 kV.[^7]
1. Add 2 mL Recovery Media and gently pipet up and down immediately after
   electroporation, and transfer to a sterile 50ml conical tube.
1. Repeat steps 10-12 three times
1. Allow cells to recover for 30 min at 37 °C with shaking at 250 rpm.
1. Pre-warm 2xYT agar plates with 100 $\mu$g/mL carbenicillin.
1. After recovery, perform dilution plating
   1:10^4^, 1:10^5^, 1:10^6^ on carbenicillin agar plates.
1. Incubate plates overnight at 37 °C.
1. Put the remaining transformant mixture into 500 mL 2xYT
   with 100 $\mu$g/mL carbenicillin in a 2 L flasks.
1. Incubate flasks at 30 °C overnight with shaking at 250 rpm.
1. The culture can be pelleted or midi/maxi prepped for usage.
1. Calculate transformation efficiency from dilution plating.[^8]

[^2]: Always use filtered pipette tips when working with
  DNA to prevent cross-contamination.
[^3]: A 1X Golden Gate assembly reaction is setup by mixing 25 fmol digested
  gRNA transfer vector (*from step 3.1.4*), 250 fmol double stranded gRNA
  barcode DNA (*from step 3.1.1*), 1 $\mu$L T4 ligase buffer,
  0.5 $\mu$L T7 ligase, 0.5 $\mu$L BsmBI,
  and nuclease-free water to 10 $\mu$L.
[^4]: Letting the water sit on the column for 3-5 minutes before
  elution increases yield. Re-run elution product through
  column 3 times to maximize yield.
[^5]: Make sure to use *E. coli* suitable for use with unstable DNA.
[^6]: Do not pipet up and down. Ensure bubbles are not added to the mix
  which can cause electrical arcing and cell death during electroporation.
[^7]: Optimal time constants should be between 4.2-5.4 ms. This protocol
  was optimized with the EC2 setting on the Bio-Rad MicroPulser^TM^ Electroporator.
[^8]: Transformation efficiency (TE) is defined as the number of colonies
  produced with transformation with 1 $\mu$g of plasmid DNA.
  To calculate TE, count the number of colonies formed on the plate,
  calculate the amount of DNA used in $\mu$g, and determine your
  dilution factor. With those variable, TE = Colonies/$\mu$g/Dilution.

### SgRNA Barcode Sampling

The diversity of the initial plasmid pool should be assessed to ensure a
high diversity library. To do this, PCR is performed with primers containing
Illumina indices that anneal to regions flanking the barcodes.

1. Midi-prep one tube of transformed e. coli from step [*sgRNA Barcode Library Plasmid Pool Assembly*](#sgrna-barcode-library-plasmid-pool-assembly)
   according to manufacturer's instructions.

1. Generate the phasing primer mixture 'CM-FWD-S1-PAS' by mixing equimolar amounts
   of CM-FWD-S1-PASx0, CM-FWD-S1-PASx4, CM-FWD-S1-PASx7, and CM-FWD-S1-PASx8.[^9]

1. Prepare **stage 1** PCR reaction to amplify barcodes by mixing the following reagents:

    | Reagent | volume ($\mu$L) |
    |---|---|
    | 5X Q5 Reaction Buffer | 10 |
    | 10 mM dNTPs | 1 |
    | CM-FWD-S1-PAS | 2.5 |
    | CM-REV-S1 | 2.5 |
    | Q5 Polymerase | 0.5 |
    | 100 ng DNA | variable |
    | nuclease-free water | to 50 |

1. Amplify barcodes by running 50 $\mu$L reaction on a thermocycler
   using the following settings[^11], repeating steps 2-4 for 8 cycles[^12]:

    | Step | Temp (°C) | Time |
    |---|---|---|
    | 1 | 95 | 5 min |
    | 2 | 98 | 10 sec |
    | 3 | 63 | 30 sec |
    | 4 | 72 | 15 sec |
    | 5 | 72 | 2 min |
    | 6 | 15 | hold |

1. Clean stage 1 reaction as described in
   [sgRNA barcode sampling](#sgrna-barcode-sampling) steps 4-20.
1. Prepare **stage 2** PCR reaction to attach index sequences
   and Illumina adapters by mixing the following reagents:

    | Reagent | volume ($\mu$L) |
    |---|---|
    | 5X Q5 Reaction Buffer | 10 |
    | 10 mM dNTPs | 1 |
    | CM-FWD-S2-i5 | 2.5 |
    | CM-REV-S2-i7 | 2.5 |
    | Q5 Polymerase | 0.5 |
    | 4 ng **stage 1** amplicon | variable |
    | nuclease-free water | to 50 |

1. Amplify the barcodes by running the 50 $\mu$L reaction
   on a thermocycler using the above cycling parameters
   from **stage 1**, repeating steps 2-4 for 10 cycles [^12].
1. Transfer 50 $\mu$L PCR amplification product to a
   nuclease-free microcentrifuge tube
1. Allow SPRI beads to come to room temperature.
1. Add 35 $\mu$L (0.7X) paramagnetic SPRI beads and mix
   well with vortexing or pipetting up and down 10 times.
1. Incubate at room temperature for 5 minutes.
1. Place the tube on a magnetic rack and allow solution to clear (5-10 minutes).
1. While the tube is on the rack transfer the clear supernatant
   to a new tube without disturbing the bead pellet.
1. Add 45 $\mu$L (1.6-0.7x) paramagnetic SPRI beads to the supernatant
   from step 10 and mix well with vortexing or pipetting up and down 10 times.
1. Incubate at room temperature for 5 minutes.
1. Place the tube on a magnetic rack and allow solution to clear (5-10 minutes).
1. With the tube still in the rack, aspirate the clear supernatant.
1. With the tube still in the rack, add 180 $\mu$L of 80% ethanol and
   allow it to sit for 30 seconds.[^13]
1. With the tube still in the rack, aspirate the ethanol and repeat step 14.
1. Remove supernatant and allow bead to dry for no **more** than 5 minutes.[^14]
1. Remove tube from the magnetic rack and elute DNA
   by adding 42 $\mu$L of nuclease-free water.
1. Incubate at room temperature for 10 minutes.
1. Transfer tube to magnetic rack and collect 40 $\mu$L of purified
   PCR product after solution has cleared (5-10 minutes).[^15]
1. Quantify DNA yield with a high sensitivity fluorometry kit
   ensuring yield between 0.5-10 ng/$\mu$L.
1. Load sample on to BioAnalyzer chip according to the manufacturer's protocol
   and ensure a clear peak around 225 bp.[^16]
1. Submit sample for Illumina sequencing.


[^9]: Universal phase amplicon sequencing primers are used to add more
  diversity to the sequencing reads which helps prevents sequencing errors.
[^11]: Pre-heat thermocycler to 98 °C before adding tubes to heat block.
[^12]: The number of cycles will depend on the starting template amount.
  A nested PCR reaction may have to be performed to enhance barcode specificity.
[^13]: 80% ethanol should be prepared fresh for each PCR cleanup.
[^14]: Do not over dry the beads, this can result in a loss of yield and quality.
[^15]: Beads may become trapped within the meniscus of the water.
  Pipetting slowly will keep the beads against the wall of the tube
  and leave them in the remaining 2 $\mu$L of water.
[^16]: If there are considerable peaks at 120 bp or less,
  SPRI bead cleanup can be repeated with 1.1X beads to
  further purify PCR sample, but this will greatly reduce yield.

### SgRNA Barcoding Lentivirus Production

1. 48 hours before transfection, plate 0.22-0.25 x 10^6^ low-passage HEK-293T
   cells in DMEM supplemented with 10% FBS **without antibiotics** in each well
   of a sterile 6-well tissue culture treated plate such that cells will be
   70-80% confluent at the time of transfection.
1. On the morning of transfection, replace media on HEK-293T cells with
    2 mL of fresh Opti-MEM^TM^ (or your cells growth medium)
    supplemented with 10% FBS **without antibiotics**.
1. In the afternoon, warm Opti-MEM^TM^, Lipofectamine^TM^ 2000,
   and VSV-G, psPAX, and sgRNA barcoding plasmid to room temperature.[^17]^,^[^18]
1. Per well of a 6 well plate,
   prepare "Tube A" containing 150 $\mu$L Opti-MEM^TM^
   and 9 $\mu$L Lipofectamine^TM^ 2000.[^19]
1. Incubate "Tube A" at room temperature for 5 minutes.
1. Per well of a 6 well plate,
   prepare "Tube B" containing 150 $\mu$L Opti-MEM^TM^,
   1.5 $\mu$g psPax, 0.4 $\mu$g VSV-G, 3-5 $\mu$g sgRNA barcoding plasmid.
1. Slowly add "Tube B" dropwise to "Tube A" and
   carefully mix by gently inverting 10 times
1. Incubate at room temperature for 20 minutes.
1. Add 300 $\mu$L of the transfection mix slowly
   and dropwise to each well of HEK-293T cells.
1. 16-18 hours post-transfection, carefully remove and dispose of media
   containing Lipofectamine^TM^ 2000 complexes and slowly replenish with
   DMEM supplemented with 20% FBS **without antibiotics**.[^20]^,^[^21]
1. 48 hours post-transfection, harvest viral containing supernatant
   and store in a 50 mL conical tube at 4 °C.[^22]^,^[^23]^,^[^24]
1. Spin down collected viral containing supernatant at 500 x g
   for 10 min at 4 °C to remove residual HEK-293T cells.
1. Remove plunger from 20 mL syringe and attach to a 0.45 $\mu$m PES syringe filter.
1. Transfer viral supernatant to the 20 mL syringe.
1. Filter viral supernatant through 0.45 $\mu$m PES syringe filter
   into a fresh 50 mL conical tube to remove any remaining cell debris.
1. Concentrate virus ~20X in 30,000 MWCO PES ultrafiltration centrifugal
   concentrator by loading 20 mL of filtered viral supernatant into
   concentrator chamber and spinning at 4000 x g for 60-75 minutes
   at 4 °C until ~1 mL of media remains in filter.[^25]
1. Aliquot 25-50 $\mu$L of concentrated virus in
   threaded cryovials and store at -80 °C.[^26]^,^[^27]

[^17]: Lentivirus can promiscuously infect cells, including your skin!
  Use a cuffed-sleeve lab coat and double-glove (one glove under sleeve cuffs,
  one glove over) at every step involving use of virus.
[^18]: Ethanol does not kill lentivirus.
  Always keep a working stock of 100% bleach in the BSL-2 culture hood
  in which virus is being handled. Soak pipet tips, serological pipets,
  and other disposables that come in contact with virus in 100% bleach
  and irradiate with UV for at least 30 minutes before disposal as
  biohazardous waste. Wipe down virus containing tissue culture plates
  with disinfecting wipes certified to kill HIV such as CaviCide before
  removing from culture hood.
[^19]: Slowly dilute Lipofectamine^TM^ complexes dropwise
  with Opti-MEM^TM^ media with occasional flicking of the tube.
[^20]: You are working with live virus at this stage and beyond.
  Stringently adhere to all biosafety procedures. Bleach and UV
  all media and containers exposed to live virus and virus producing reagents.
[^21]: Cells exposed to lentivirus are fragile and
  extra care must be taken in removing and adding media.
[^22]: Virus should be stored in labeled secondary containment.
[^23]: Virus-producing HEK-293T cells should be bleached and
  UV irradiated in culture for at least 30 minutes to
  inactivate remaining virus before disposal.
[^24]: Never use a vacuum line to disposal of virus waste
  as this may produce aerosols.
[^25]: Spin times will vary based on centrifuge angle.
  Spinning at 4 °C will increase the amount of time it takes
  for media to pass through filter
  (We have noted that 22 mL takes about 75 minutes).
[^26]: Even just a single freeze-thaw cycle can drastically
  alter viral titer, be sure to minimize freeze-thaw cycles.
[^27]: Virus should be completed frozen and then thawed
  before calculating viral titer.

### Determine sgRNA Viral Titer

See [^28]^,^[^29]

#### Titering on Adherent Cells (Forward Procedure)

[^30]

1. 24-48 hours before performing viral transduction seed your
   cell line of interest in a 12-well plate such that it is
   near 60-70% confluent at time of transduction.
1. Prior to transduction, one well of the replicate 12 wells should
   be dissociated and counted using trypan blue exclusion on a
   hemocytometer to know approximate number of live cells at
   time of transduction.[^31]^,^[^32]
1. Create stock of media containing your cells' standard growth medium
   supplemented with 20% FBS containing 0-10 $\mu$g/mL hexadimethrine
   bromide (1:1000 dilution from hexadimethrine bromide stock to get 10 $\mu$g/mL).[^33]
1. Place 600 $\mu$L of hexadimethrine bromide containing medium
   into separate microcentrifuge tubes.
1. Add virus in increasing amounts to each tube.
1. Replace media on cells of interest with virus and
   hexadimethrine bromide containing dilutions.
1. Incubate for 16 hrs at 37 °C, then carefully remove viral containing
   supernatant and replace with complete growth medium.[^35]^,^[^36]
1. Incubate for an additional 32 hrs at 37 °C, then remove medium
   and wash each well gently with PBS.[^37]
1. Dissociate the cells from the plate
   and centrifuge at 300 x g for 5 minutes at 4 °C.
1. Wash cell pellets with PBS and repeat spin.
   Perform this step three times to ensure removal
   of trace virus before flow cytometry.
1. Resuspend cells in chilled FACS Buffer.[^38]
1. Keep cells on ice and continue to step [*Flow Cytometry to Determine Viral Titer*](#flow-cytometry-to-determine-viral-titer)

[^28]: Viral titer will vary between cell type and with each new virus preparation.
[^29]: Lentivirus susceptibility and timing should first be determined
  on your cells of interest using a control plasmid such as
  a constitutively active GFP. Some cells will require longer
  or shorter incubation times with the virus and some cells will
  take longer to produce the transgenic reporter protein.

[^30]: To perform reverse titer on adherent cells, follow the steps
  for titering on suspension cells through step 3.4.2.5,
  then return to the adherent protocol at step 3.4.1.6.
[^31]: It is very important to know the number of cells at the time
  of transduction. This number is used to calculate viral titer.
[^32]: Trypan blue exclusion is performed by mixing equal parts 0.05%
  Trypan blue with your cell suspension, usually 10 $\mu$L of each,
  then load 10 $\mu$L of the stained suspension into the hemocytometer.
[^33]: Hexadimethrine bromide is a cationic solution that assists
  in viral adsorption to cells [@davis2002].
  Hexadimethrine bromide can be toxic to some cells.
  Hexadimethrine bromide sensitivity should be assessed via serial dilution
  to determine maximum tolerable hexadimethrine bromide dose before
  determining viral titer. Most cells respond well to 6-8 $\mu$g/mL
  hexadimethrine bromide.
[^34]: Ensure one well is kept uninfected as a negative control.
  A range of 0.5-200 $\mu$L is usually sufficient to find viral titer,
  e.g. 0, 0.5, 1, 5, 10, 25, 50, 100, 150, 200 $\mu$L.
[^35]: Lentiviral exposure time will vary across cell type dependent
  on growth dynamics and properties intrinsic to the cells.
  Optimize lentiviral exposure time with constitutively active
  GFP virus before transduction with sgRNA barcoding library virus.
[^36]: Lentiviral exposure times range between 12-48 hours.
  Lentiviral exposure time should be minimized to reduce
  the occurrence of multiple viral integrations.
[^37]: Lentivirus transduced cells are very fragile
  and should be handled with added care.
[^38]: EDTA and FBS in FACS buffer help to prevent cell clumping.
  For extra-sticky cells, use 5 mM EDTA in FACS buffer.


#### Titering on Suspension Cells

1. Count your cells of interest using a hemocytometer.
1. Create stock of media containing your cells' standard growth medium
  supplemented with 20% FBS containing 0-10 $\mu$g/mL hexadimethrine bromide
  (1:1000 dilution from hexadimethrine bromide stock for 10 $\mu$g/mL).[^33]
1. Resuspend 1.20 x 10^6^ cells in 7.2 mL of containing hexadimethrine bromide
   media such that the final solution contains 1 x 10^5^ cells in 600 $\mu$L.
1. Plate 600 $\mu$L of cell solution in 10 wells
   of a tissue culture treated 12-well plate
1. Add virus in increasing amounts to each well and mix well.[^34]
1. Incubate for 16 hrs at 37 °C.[^35]^,^[^36]
1. Transfer cell suspensions to sterile 1.7 mL microcentrifuge tubes
   and spin down at 500 x g for 5 minutes at 4 °C.[^39]
1. Resuspend each cell pellet with complete growth medium
   and transfer to fresh 12-well plate.
1. Incubate for an additional 32 hrs at 37 °C, then transfer wells to
   microcentrifuge tubes and spin down at 400 x g for 5 minutes at 4 °C.[^40]
1. Wash cell pellets with PBS and repeat spin.[^41]
1. Resuspend cells in chilled FACS Buffer.[^38]
1. Keep cells on ice and continue to step [*Flow Cytometry to Determine Viral Titer*](#flow-cytometry-to-determine-viral-titer)

[^39]: Use a pipette to remove lentivirus containing supernatant
  and dispose of in bleach. Do not vacuum aspirate, vacuums can cause dangerous viral aerosols.
[^40]: Lentivirus transduced cells are very fragile
  and should be handled with added care when pipetting.
[^41]: Perform this step three times to ensure removal of trace virus before flow cytometry.

#### Flow Cytometry to Determine Viral Titer

1. Pass cells resuspended in FACS buffer through a 35 $\mu$m nylon mesh strainer
   into a 5 mL flow cytometry test tube.[^42]
1. Use control samples to set laser voltages on FSC-A, SSC-A,
   and BFP such that nearly all cells are seen within FSC-A vs. SSC-A plot and
   both negative and positive populations can be seen and distinguished
   on the BFP channel.[^43]
1. After setting voltages with control samples, run transduced samples from
   lowest viral to highest. Set the cytometer to record at least 10,000 events
   for each sample. Record %BFP-positive for each titration.
1. Create a plot showing volume of virus on the x-axis and %BFP-positive on the y-axis.[^44]
1. Calculate viral titer in titering units (TU) per mL using **Equation 1**
  using a pair of values within the linear region of the titer curve.[^45]

[^42]: Ensure proper controls for flow. Minimally have a positive control
  expressing BFP and a negative control expressing no fluorescent proteins.
[^43]: BFP populations will be normally distributed. For titer calculations,
  it is useful to set tight gates such that 99.98%
  of the negative control cells are captured in the negative gate.
[^44]: Plot will appear logarithmic. Only values within the linear region
  of the plot should be used to calculate viral titer (usually between 10-40% BFP-positive).
[^45]: Example: If 5 $\mu$L of virus added to 100,000 cells resulted
  in 30% BFP-positive cells within the linear region of the titer curve,
  then the viral titer would be (100,000 x 0.30) / (0.005 mL) = 6.0 x 10^6^ TU/mL

$$\frac{\text{TU}}{\text{mL}}\text{=}\frac{\left(\text{Number of cells at time of transduction} \right)\text{ × }\left( \text{Fraction of Positive Cells} \right)}{\left( \text{Volume of virus }\left\lbrack \text{mL} \right\rbrack \right)}$$

### SgRNA Barcode Transduction

1. After calculating the viral titer (TU/mL) on your cell line of interest,
  determine the final number of cells you require for your experiment using
  and transduce cells at a multiplicity of infection (MOI) of 0.1 (**Equation 2**)
  to minimize the occurrence of multiple barcode integrations.[^46]^,^[^47]
1. Use control samples to set laser voltages on FSC-A, SSC-A,
   and BFP such that nearly all cells are seen within FSC-A vs. SSC-A plot
   and both negative and positive .populations can be seen and distinguished
   on the BFP channel.[^42]
1. Set sort gate on BFP-positive cells indicative of a productive sgRNA barcode.[^48]
1. Sort cells on BFP-positive gate via FACS.
1. Maintain sorted cells in culture with complete growth medium.

$$\text{MOI [TU/cell] = }\frac{\left( \text{Volume of Virus needed [mL]} \right)\text{ × }\left( \text{Titer of Virus [TU/mL]} \right)}{\left( \text{Number of cells exposed to virus} \right)}\text{ = 0.1}$$

[^46]: Example: If your viral titer was 6.0 x 10^6^ TU/mL and you wanted
  to infect 3.0 x 10^6^ cells at an MOI of 0.1, you would need to subject
  the 3.0 x 10^6^ cells to 50 $\mu$L of virus.
[^47]: A low MOI of 0.1 or below helps prevent occurrence
  of multiple barcode integrations. In order to uniquely recall cell lineages
  it is important to maximize the probability that there is one or zero barcodes
  per cell at the time of transduction. The probability of barcode integration
  can be modeled as a Poisson distribution [@fehse2004;@kustikova2003].
[^48]: When sorting for sgRNA barcoded cells, use more stringent gating than used
  for titer determination. Ensure that 0% of negative control samples appear in the sorting gate.


### Targeted sgRNA Barcode Sampling of Cells

#### Preparing Samples for Sequencing

1. To assess cell barcode diversity harvest cells from culture
   and collect into cell pellet.[^49]
1. Isolate genomic DNA from cell pellet using kit
   or standard protocol and proceed to PCR amplification.
1. Prepare CM-FWD-S1-PAS by creating
1. Prepare **stage 1** PCR reaction to amplify barcodes by mixing the following reagents[^50]:

    | Reagent | volume ($\mu$L) |
    |---|---|
    | 5X Q5 Reaction Buffer | 10 |
    | 10 mM dNTPs | 1 |
    | CM-FWD-S1-PAS | 2.5 |
    | CM-REV-S1 | 2.5 |
    | Q5 Polymerase | 0.5 |
    | 2 $\mu$g DNA | variable |
    | nuclease-free water | to 50 |

1. Amplify barcodes by running 50 $\mu$L reaction on a thermocycler
   using the following setting[^11], repeating steps 2-4 for 20 cycles[^12]:

    | Step | Temp (°C) | Time |
    |---|---|---|
    | 1 | 95 | 5 min |
    | 2 | 98 | 10 sec |
    | 3 | 63 | 30 sec |
    | 4 | 72 | 15 sec |
    | 5 | 72 | 2 min |
    | 6 | 15 | hold |

1. Clean stage 1 reaction as described in
   [sgRNA barcode sampling](#sgrna-barcode-sampling) steps 4-20.
1. Prepare **stage 2** PCR reaction to attach index sequences
   and Illumina adapters by mixing the following reagents:

    | Reagent | volume ($\mu$L) |
    |---|---|
    | 5X Q5 Reaction Buffer | 10 |
    | 10 mM dNTPs | 1 |
    | CM-FWD-S2-i5 | 2.5 |
    | CM-REV-S2-i7 | 2.5 |
    | Q5 Polymerase | 0.5 |
    | 4 ng **stage 1** amplicon | variable |
    | nuclease-free water | to 50 |

1. Amplify the barcodes by running the 50 $\mu$L reaction
   on a thermocycler using the above cycling parameters
   from **stage 1**, repeating steps 2-4 for 10 cycles. [^12]
1. Clean stage 2 reaction as described
   in [sgRNA Barcode Sampling](#sgrna-barcode-sampling) steps 6-22.

[^49]: It is important to ensure that you have enough cells
  to sufficiently sample your population depending upon the initial barcode diversity.
[^50]: DNA amount used will be dependent on the nature
  of the cell population and desired sampling depth.
  To capture rare events, a maximum of 2 $\mu$g of DNA per reaction can be used
  and multiple reactions can be done. Given that a single diploid human genome
  is estimated at ~6.6 pg, 2 $\mu$g of genomic DNA represents that of ~300,000 cells.
  To capture only highly represented clonal populations, less DNA can be used.

#### Processing Barcode Sequencing Data

See [pycashier](https://github.com/brocklab/pycashier) for more info about
how to get started processing fastq data to get barcode information.

### Recall Plasmid Assembly

1. 3 pairs of overlapping oligos containing the barcode sequence of interest
   flanked by overlapping sequences should be ordered according to **Table 1**.[^56]
1. In separate tubes, mix each of the 100 $\mu$M oligo pairs together:

- Tube AB: 10 $\mu$L Bg-AB-fwd + 10 $\mu$L Bg-AB-rev
- Tube BC: 10 $\mu$L Bg-BC-fwd + 10 $\mu$L Bg-BC-rev
- Tube CD: 10 $\mu$L Bg-CD-fwd + 10 $\mu$L Bg-CD-rev

3. Heat each to 80 °C and let cool to create DNA blocks containing a barcode,
   a PAM site, and overhang sequences.[^57]
1. Ligate DNA blocks together creating the barcode array
   by mixing the following reagents: 

    | Reagent | volume ($\mu$L) |
    |---|---|
    | Tube "AB" | 10 |
    | Tube "BC" | 10 |
    | Tube "CD" | 10 |
    | 10 mM dNTPs | 5 |
    | 10x T4 PNK Buffer | 5 |
    | T4 PNK | 1 |
    | nuclease-free water | 9 |

1. Incubate at 37 °C for 45 minutes.
1. Add 2 $\mu$L T7 DNA ligase to the 50 $\mu$L mixture
   and incubate at room temperature overnight.
1. Run ligation product in a 2% agarose gel
   and gel purify band from approximately 170 bp.

1. Ligate the barcode array into the recall plasmid backbone at a molar ratio
   of 10:1 in a Golden Gate assembly reaction by mixing 25 fmol Recall-miniCMV-sfGFP,
   250 fmol assembled barcode array, 1 $\mu$L T4 ligase buffer,
   0.5 $\mu$L T7 ligase, 0.5 $\mu$L BbsI, and nuclease-free water to 10 $\mu$L.

1. Run the Golden Gate assembly reaction on a thermocycler
   using the following settings, repeating steps 1-2 for 35 cycles:

    | Step | Temp (°C) | Time |
    |---|---|---|
    | 1 | 42 | 2 min |
    | 2 | 16 | 5 min |
    | 3 | 55 | 30 min |
    | 4 | 4 | hold |


1. Transform bacteria with golden gate product.
   See [Addgene](https://www.addgene.org/protocols/bacterial-transformation/)
   for standard protocol.
1. Verify insertion of barcode array
   into Recall-miniCMV-sfGFP backbone via Sanger sequencing.

[^56]: The barcode sequence should be ordered to match
  the extracted barcode for the fragments labeled as 'extraction'
  and in reverse-complement for oligos labeled as 'reversed'.
[^57]: This process anneals the single stranded DNA oligos together,
  creating short double stranded DNA blocks that will be ligated together in the next step.

### Recall and Isolation of Barcoded Lineages

See [^59]^,^[^60]

1. 24-48 hours before performing recall transfection seed your cell line
   of interest in growth medium in a 6-well plate such that
   it is near 60-80% confluent at time of transfection.
1. Per well of a 6 well plate,
   prepare "Tube A" containing 100 $\mu$L Opti-MEM^TM^
   and 9 $\mu$L Lipofectamine^TM^ 3000.[^19]
1. Incubate "Tube A" at room temperature for 5 minutes.
1. Per well of a 6 well plate,
   prepare "Tube B" containing 125 $\mu$L Opti-MEM^TM^,
   225 ng Recall plasmid (*from Section 3.8*),
   275 ng dCas9-VPR plasmid and 2 $\mu$L$\mu$g DNA of p3000.
1. Slowly add "Tube B" dropwise to "Tube A"
   and carefully mix by gently inverting 10 times.
1. Incubate at room temperature for 20 minutes.
1. Add 225 $\mu$L of the transfection mix slowly
   and dropwise to each well of adherent cells.
1. 16-18 hours post-transfection,
   carefully remove media containing Lipofectamine^TM^ 3000/DNA complexes
   and slowly replenish with growth medium supplemented with 20% FBS without antibiotics.
1. 48-72 hours post-transfection, dissociate cells from the plate
   and wash cells with PBS twice at 300 x g for 5 minutes at 4 °C before
   resuspending in chilled FACS buffer.[^38]
1. Pass cells resuspended in FACS buffer through a 35 $\mu$m nylon mesh strainer
   into a 5 mL flow cytometry test tube and keep on ice.
1. Use control samples to set laser voltages on FSC-A, SSC-A, BFP, and GFP
   on FACS sorter such that nearly all cells are seen within FSC-A vs.
   SSC-A plot and both negative and positive populations can be seen
   and distinguished on the BFP and the GFP channel. Set compensations based
   on single positive populations.[^61]
1. Set sort gate on GFP and BFP double positive gate indicative of a recalled cell.[^62]
1. Sort cells in GFP and BFP double positive gate.[^63]
1. Maintain sorted cells in culture with complete growth medium.

[^59]: Lipofectamine effiency can vary significantly between cell lines.
  It's recommended you optimize transfection with a plasmid containing a constitutively promoter.
[^60]: This protocol is optimized for adherent cell lines. If using suspension lines,
  electroporation can be done to introduce the plasmids to your cells.
  Be sure to optimize electroporation parameters on your cells
  for maximized plasmid expression and minimized cell death before
  recall electroporation. If electroporating, total plasmid load
  per cell may vary by cell type. Example: CD8 T cells respond well
  to 2.5 $\mu$g of each plasmid (5 $\mu$g total DNA load) per 5 x 10^5^ cells.
[^61]: Ensure proper controls for flow.
  Minimally have a positive control singularly positive for BFP,
  a positive control singularly positive for GFP,
  and a negative control expressing no fluorescent proteins.
[^62]: When sorting for recalled cells, use stringent gating.
  Ensure that 0% of negative control and single positive samples appear in the sorting gate.
[^63]: Single cell sorting can be performed for isolation and growth of clonal populations.





| Step | Name | Sequence (5'-->3') | Notes |
|:---:|:---|:---|:---|
| 3.1 | CROPseq-PrimeF-BgL-BsmBI | GAGCCTCGTCTCCCACCG**NNNNNNNNNNNNNNNNNNNN**GTTTTGAGACGCATGCTGCA | The N20 sequence is a random string of oligonucleotides |
| 3.1 | CROPseq-RevExt-BgL-BsmBI | TGCAGCATGCGTCTCAAAAC |  |
| 3.1 | 10X PrimeF-BgL-BbsI | GCCTGAAGACCTCACCG**NNNNNNNNNNNNNNNNNNNN**GTTTTAGTCTTCCATGCTGC | The N20 sequence is a random string of oligonucleotides |
| 3.1 | 10X-RevExt-BgL-BbsI | TGCAGCATGGAAGACTAAAAC |  |
| 3.2, 3.7 | CM-FWD-S1-PAS | equimolar mixture of CM-FWD-S1 PAS primers |  |
| 3.2, 3.7 | CM-FWD-S1-PASx0 | TCGTCGGCAGCGTCAGATGTGTATAAGAGACAGCTTGTGGAAAGGACGAAACAC |  |
| 3.2, 3.7 | CM-FWD-S1-PASx4 | TCGTCGGCAGCGTCAGATGTGTATAAGAGACAGGCAACTTGTGGAAAGGACGAAACAC |  |
| 3.2, 3.7 | CM-FWD-S1-PASx7 | TCGTCGGCAGCGTCAGATGTGTATAAGAGACAGAGCCACCCTTGTGGAAAGGACGAAACAC |  |
| 3.2, 3.7 | CM-FWD-S1-PASx8 | TCGTCGGCAGCGTCAGATGTGTATAAGAGACAGTAGTGAATCTTGTGGAAAGGACGAAACAC |  |
| 3.2, 3.7 | CM-REV-S1 | GTCTCGTGGGCTCGGAGATGTGTATAAGAGACAGGGACTAGCCTTATTTTAACTTGCTATTTCTAGCTC |  |
| 3.2, 3.7 | CM-FWD-S2-i5 | AATGATACGGCGACCACCGAGATCTACAC**NNNNNNNN**TCGTCGGCAGCGTC | The N8 sequence is where the i5 Illumina index should be placed |
| 3.2, 3.7 | CM-REV-S2-i7 | CAAGCAGAAGACGGCATACGAGAT**NNNNNNNN**GTCTCGTGGGCTCGG | The N8 sequence is where the i7 Illumina index should be placed |
| 3.8 | BgN20-AB-fwd | TACTCGACCAAGAACCGCA**NNNNNNNNNNNNNNNNNNNN**AGGTGGATTAGTTCTCT | Insert barcode in place of N20 |
| 3.8 | BgN20-AB-rev | AAGCAGAGAACTAATCCACCT**NNNNNNNNNNNNNNNNNNNN**TGCGGTTCTTGGTCG | Insert reverse-complement barcode in place of N20 |
| 3.8 | BgN20-BC-fwd | GCTTGTCCTGCGGTTACCC**NNNNNNNNNNNNNNNNNNNN**AGGCTGTAATCCAGCTG | Insert barcode in place of N20 |
| 3.8 | BgN20-BC-rev | AGCGCAGCTGGATTACAGCCT**NNNNNNNNNNNNNNNNNNNN**GGGTAACCGCAGGAC | Insert reverse-complement barcode in place of N20 |
| 3.8 | BgN20-CD-fwd | CGCTGTGGTATCACTCGTC**NNNNNNNNNNNNNNNNNNNN**AGGCTCAGCTAAGGTGC | Insert barcode in place of N20 |
| 3.8 | BgN20-CD-rev | CATTGCACCTTAGCTGAGCCT**NNNNNNNNNNNNNNNNNNNN**GACGAGTGATACCAC | Insert reverse-complement barcode in place of N20 |


Table: Oligonucleotides




| Name | Vendor | Catalog No. |
|:---|:---:|:---:|
| AMPure XP Reagent | Beckman Coulter | A63880 |
| BbsI-HF | NEB | R3539S |
| BsmBI-v2 | NEB | R0739S |
| NEBuffer r3.1 |  NEB |  B6003S |
| Q5 Hot Start Polymerase | NEB | M0493S |
| T4 Ligase | NEB | M0202S |
| T4 PNK | NEB | M0201S |
| T7 Ligase | NEB | M0318S |
| Genomic DNA Mini Kit | ThermoFisher | K182001 |
| Lipofectamine 2000 | ThermoFisher | 11668030 |
| Lipofectamine 3000 | ThermoFisher | L3000001 |
| OptiMEM | ThermoFisher | 31985070 |
| Typan Blue Stain | ThermoFisher | T10282 |
| 2xYT medium | Millpore Sigma | Y2377-250G |
| Carbenicillin | Millpore Sigma | C1389-250MG |
| DMEM |  Millpore Sigma | D5671 |
| Hexadimethrine bromide | Millpore Sigma | TR-1003-G |
| Plasmid Plus Kit (Midi) | Qiagen | 12941 |
| DNA Clean and Concentrator-5 | Zymo | D4013 |


Table: Recommended Reagents


## Acknowledgements 

This work has been supported by funding through the NIH (R21CA212928 to AB).
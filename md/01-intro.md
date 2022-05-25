# Introduction

Insight into the clonal composition of a cells during key events -- such as development, infection, tumor progression, or treatment response -- is critical to understanding the nature of the interaction between the population of cells and the selective forces shaping it. While advances in genomics and transcriptomics and the advent of single-cell RNA sequencing (scRNA-seq) have vastly increased the resolution at which we can understand cellular processes, they lack the ability to directly assign clonal relationships. To meet this need, lineage tracing technologies, such as DNA barcoding, have been developed to label and track individual cells and their progeny [@blundell2014;@kebschull2018]. In DNA barcoding, each individual cell in a population is labeled with a unique random string of nucleotides that is integrated into the genome and heritable by its daughter cells. The ensemble of all DNA barcodes in the cell population can be quantified by next-generation sequencing (NGS) to determine how clonal abundance changes over time.

While highly informative, DNA barcoding and other lineage tracing techniques are still limited in that interesting lineages of cells cannot be easily isolated from the bulk population for clonally pure analysis. Here, we describe a detailed protocol for the Control of Lineages by Barcode Enabled Recombinant Transcription (COLBERT), a workflow that enables precise identification and isolation of populations of interest from heterogeneous mammalian cells [@alkhafaji2018]. An overview of COLBERT is shown in **Fig. 1**. COLBERT is a functionalized variant of DNA barcoding in which the DNA barcode is a CRISPR-Cas9 compatible single-guide RNA (sgRNA). The sgRNA-barcode has multiple functionalities: (1) It is an integrated DNA barcode, (2) It is transcribed and captured in scRNA-seq workflows, and (3) It can be used to actuate lineage-specific genes of interest using an activator variant of Cas9 [@chavez2015]. This protocol describes the use of COLBERT for lineage-specific activation of GFP, enabling isolation of clonal cells from a heterogeneous population.

This protocol describes two variants of the COLBERT system, one compatible with single-cell RNA sequencing workflows that use polyA capture and another with specific compatibility with 10X Genomics systems. In the polyA capture version, the sgRNA barcode is engineered using the CROPseq method [@datlinger2017] such that the sgRNA barcode is transcribed by both RNA polymerase III and RNA polymerase II, creating a functional sgRNA barcode transcript and a polyadenylated transcript containing the barcode, respectively. In the 10X Genomics version, the sgRNA is engineered to contain a capture sequence that allows targeted capture by the Chromium Single Cell 3' v3 Gel Beads [@10xgenomics].

Cells are first transduced with lentivirus containing either the CROPseq sgRNA barcoding vector or the 10X Capture sgRNA barcoding vector at a low multiplicity of infection (MOI) to minimize the integration of multiple barcodes per cell. In both versions of the vector, the sgRNA barcode is co-expressed with blue fluorescent protein (BFP) for easy identification and collection of barcoded cells via flow cytometry and fluorescence-activated cell sorting (FACS). Once established, the barcoded cell population is available for experimental manipulation. Clonal dynamics may be measured by NGS analysis and gene expression signatures of clonal populations may be resolved by scRNA-Seq. Once a barcode of interest is identified from NGS or scRNA-seq, the barcode identifier can be exploited for isolation of the clone. This is achieved by transfecting the cell population with a plasmid containing an activator variant of Cas9 (dCas9-VPR) and a second plasmid containing the Cas9-homing PAM sites adjacent to the identified barcode upstream of green fluorescent protein (sfGFP) reporter. Expression of sfGFP will occur only in cells that are producing the matching sgRNA barcode, allowing precise identification and FACS isolation of cells from lineages of interest.

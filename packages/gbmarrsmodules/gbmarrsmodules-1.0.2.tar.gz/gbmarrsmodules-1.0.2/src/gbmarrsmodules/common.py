import re
import os

from rdflib import Namespace

from .util import getDataRoot 


def getDownDir(dataset, dataBuild):
    dataroot = getDataRoot("data", dataBuild) # this is the location where the data should be stored from the downloaded input and output of the ETLs
    downloaddir = os.path.join (dataroot, dataset, "download/")
    return downloaddir

def getRDFDir(dataset, dataBuild):
    dataroot = getDataRoot("data", dataBuild)
    rdfdir = os.path.join (dataroot, dataset, "rdf/")
    return rdfdir

def getSQLDir(dataset, dataBuild):
    dataroot = getDataRoot("data", dataBuild)
    sqldir = os.path.join (dataroot, dataset, "sql/")
    return sqldir

def getWorkDir(dataset, dataBuild):
    dataroot = getDataRoot("data", dataBuild)
    workdir = os.path.join (dataroot, dataset, "work/")
    return workdir



# Public dataset graphs
#chembl
CHEMBL_DATA = Namespace ("http://generalbioinformatics.com/data/chembl#")
CHEMBL_VOC = Namespace ("http://generalbioinformatics.com/ontologies/chembl#")
#clinvar
CLINVAR_DATA = Namespace ("http://generalbioinformatics.com/data/clinvar#")
CLINVAR_VOC = Namespace ("http://generalbioinformatics.com/ontologies/clinvar#")
#intact
INTACT_DATA = Namespace ("http://generalbioinformatics.com/data/intact#")
INTACT_VOC = Namespace ("http://generalbioinformatics.com/ontologies/intact#")
#interpro
INTERPRO_DATA = Namespace ("http://generalbioinformatics.com/data/interpro#")
INTERPRO_VOC = Namespace ("http://generalbioinformatics.com/ontologies/interpro#")
#mgi
MGI_DATA = Namespace ("http://generalbioinformatics.com/data/mgi#")
MGI_VOC = Namespace ("http://generalbioinformatics.com/ontologies/mgi#")
#ncbigene
NCBIGENE_DATA = Namespace ("http://generalbioinformatics.com/data/ncbigene#")
NCBIGENE_VOC = Namespace ("http://generalbioinformatics.com/ontologies/ncbigene#")
#apo
APO_DATA = Namespace ("http://generalbioinformatics.com/data/apo#")
APO_VOC = Namespace ("http://generalbioinformatics.com/ontologies/apo#")
#chebi
CHEBI_DATA = Namespace ("http://generalbioinformatics.com/data/chebi#")
CHEBI_VOC = Namespace ("http://generalbioinformatics.com/ontologies/chebi#")
#dpo
DPO_DATA = Namespace ("http://generalbioinformatics.com/data/dpo#")
DPO_VOC = Namespace ("http://generalbioinformatics.com/ontologies/dpo#")
#go
GO_DATA = Namespace ("http://generalbioinformatics.com/data/go#")
GO_VOC = Namespace ("http://generalbioinformatics.com/ontologies/go#")
#reactome
REACTOME_DATA = Namespace ("http://generalbioinformatics.com/data/reactome#")
REACTOME_VOC = Namespace ("http://generalbioinformatics.com/ontologies/reactome#")
#taxon
TAXON_DATA = Namespace ("http://generalbioinformatics.com/data/taxon#")
TAXON_VOC = Namespace ("http://generalbioinformatics.com/ontologies/taxon#")
#wbphenotype
WBP_DATA = Namespace ("http://generalbioinformatics.com/data/wbphenotype#")
WBP_VOC = Namespace ("http://generalbioinformatics.com/ontologies/wbphenotype#")
#pdb
PDB_DATA = Namespace ("http://generalbioinformatics.com/data/pdb#")
PDB_VOC = Namespace ("http://generalbioinformatics.com/ontologies/pdb#")
#pfam
PFAM_DATA = Namespace ("http://generalbioinformatics.com/data/pfam#")
PFAM_VOC = Namespace ("http://generalbioinformatics.com/ontologies/pfam#")
#proteinAtlas
PROTEINATLAS_DATA = Namespace ("http://generalbioinformatics.com/data/proteinatlas#")
PROTEINATLAS_VOC = Namespace ("http://generalbioinformatics.com/ontologies/proteinatlas#")
#uniprot
UNIPROT_DATA = Namespace ("http://generalbioinformatics.com/data/uniprot#")
UNIPROT_VOC = Namespace ("http://generalbioinformatics.com/ontologies/uniprot#")

# Internal dataset graphs
CSIM_VOC = Namespace("http://generalbioinformatics.com/ontologies/crossSystemIdMapping#")
CSIM_DATA = Namespace("http://generalbioinformatics.com/data/crossSystemIdMapping#")

MAP_DATA = Namespace ("http://generalbioinformatics.com/data/idMapping#")
MAP_VOC = Namespace ("http://generalbioinformatics.com/ontologies/idMapping#")

PHENOTYPE_DATA = Namespace ("http://generalbioinformatics.com/data/phenotype#")
PHENOTYPE_VOC = Namespace ("http://generalbioinformatics.com/ontologies/phenotype#")

PROJECT_DATA = Namespace ("http://generalbioinformatics.com/data/project#")
PROJECT_VOC = Namespace ("http://generalbioinformatics.com/ontologies/project#")

RELATE_DATA = Namespace ("http://generalbioinformatics.com/data/relate#")
RELATE_VOC = Namespace ("http://generalbioinformatics.com/ontologies/relate#")


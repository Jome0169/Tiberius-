import os, getopt, sys
import shutil
from datetime import datetime


def TSVTableReader(Location):
    """TODO: Docstring for TSVTableReader.

    :Location: TODO
    :returns: TODO

    """
    Completedgene = []
    FracturedGenes = []
    with open(Location) as f:
        for line in f:
            if line.startswith('#'):
                pass
            else:
                newline = line.strip().split('\t')
                if newline[1] == "Missing":
                    pass
                elif newline[1] == "Complete":
                    Completedgene.append(newline)
                elif newline[1] == "Fragmented":
                    FracturedGenes.append(newline)
    
    return Completedgene, FracturedGenes





def FracturedListExtractor(tuplelist, AncestraFile):
    """TODO: Docstring for FracturedListExtractor.

    :tuplelist: TODO
    :DirectStrge: TODO
    :returns: TODO

    """

    try: 
        os.remove("FracturedGeneNames.txt") 
        os.remove("FracturedSeq.fasta")
    except:
        pass


            
    AncestralScaff = {}
    key = []
    with open(AncestraFile, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                NamedSeq = line.replace('>', '')
                key.append(NamedSeq)
                AncestralScaff[NamedSeq] = ""
            else:
                AncestralScaff[NamedSeq] += line

    Completed, Fractured = tuplelist #Loading in tuple list from tsv

    for item in Fractured:
        AncestralName = item[0]
        ScaffoldSeq = item[2]
        with open("FracturedGeneNames.txt", 'a+') as d:
            d.write(AncestralName)
            d.write('\t')
            d.write(ScaffoldSeq)
            d.write("\n")
     
     
    for item in Fractured:
        AncestralName = item[0]
        ScaffoldSeq = item[2]
        for key, value in AncestralScaff.iteritems():
            if AncestralName == key:
                with open("FracturedSeq.fasta", "a+") as z:
                    z.write(key)
                    z.write('\n')
                    z.write(value)
                    z.write("\n")
            else: 
                pass
            


def ListUnpacker(tuplelist, DirectStrge):
    """TODO: Docstring for ListUnpacker.

    :tuplelist: TODO
    :otherfiles: TODO
    :returns: TODO

    ['EOG09360LA3', 'Fragmented', '003370F|quiver', '34933', '40667', '194.2',
    '117']


    ['EOG09360LL8', 'Fragmented', '000767F|quiver', '43651', '47622', '242.7',
            '132']

    """
    Completed, Fractured = tuplelist
    
    FineStartComp = []
    NonStartListComp = []
    for item in Completed:
        NormalName = str(item[0])
        Buscogenename = str(item[0]) + '.faa'
        ScaffSeq = item[2]
        for file1 in DirectStrge:
            if Buscogenename in file1 and "SteepBUSCO_1e-10/single_copy_busco_sequences" in file1:
                with open(file1, 'r') as f:
                    for line in f:
                        if line.startswith('>'):
                            pass
                        elif line.startswith('M') != True:
                            NonStartListComp.append(file1)
                        else: FineStartComp.append(file1)
    return NonStartListComp, FineStartComp



   
def MoveFilesIntoBins(WrkignDir, TupleofFiles):
    """TODO: Docstring for MoveFilesIntoBins.

    :WrkignDir: TODO
    :TupleofFiles: TODO
    :returns: TODO

    """
    DirName1 = "Completed_CorrectStart"
    DirName2 = "Completed_NonStartSeq"
    MissingStart, CorrectFiles, = TupleofFiles
    if not os.path.exists(DirName1):
            os.makedirs(DirName1)
    if not os.path.exists(DirName2):
            os.makedirs(DirName2)

    for file1 in CorrectFiles:
        NuctFile1 = file1.replace(".faa", ".fna")
        shutil.copy(file1, DirName1)
        shutil.copy(NuctFile1, DirName1)



    for file2 in MissingStart:
        NuctFile2 = file2.replace(".faa", ".fna")
        shutil.copy(file2, DirName2)
        shutil.copy(NuctFile2, DirName2)







def Usage():
      print "\nThis is the usage function\n"
      print 'Usage: '+sys.argv[0]+' -d <file1> [Where the ancestral file name
      is fo the seq]'


def Main():

    global oflag
    DirectoryFile = None

    try:
        options, other_args = getopt.getopt(sys.argv[1:], "d:h:", ["help"])

    except getopt.GetoptError:
        print "There was a command parsing error"
        Usage()
        sys.exit(1)

    for option, value in options:
        if option == "-d":
            DirectoryFile = value
        elif option == "--help":
            Usage()
        else:
            print "Unhandeled options %s %s" % (options)

    if DirectoryFile == None:
        print "Need an AUGUSTUS output Directory"
        Usage()
        exit(-1)
    
    starttime = datetime.now()

    CurrentWrkDirectory = os.getcwd()
    FileDirectoryStorage = []
    for subdir, dirs, files in os.walk(CurrentWrkDirectory):
        for file in files:
            FileDirectoryStorage.append(os.path.join(subdir, file))

    
    for file1 in FileDirectoryStorage:
        if file1.endswith("/full_table_SteepBUSCO.tsv"):
            CompleteAndFract = TSVTableReader(file1)
    FileLists = ListUnpacker(CompleteAndFract, FileDirectoryStorage)
    MoveFilesIntoBins(CurrentWrkDirectory, FileLists)
    FracturedListExtractor(CompleteAndFract, DirectoryFile)

    



    print datetime.now() - starttime





if __name__ == '__main__':
    Main()











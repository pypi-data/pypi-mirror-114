
#Import Libraries
import sys
import os
import statistics
import gzip
import argparse
import time
import gc
import array
from optparse import OptionParser
from operator import itemgetter
import re
import json
import sqlite3
import json
import subprocess


def mintyper(args):
    i_illumina = args.i_illumina
    i_nanopore = args.i_nanopore
    paired_end = args.paired_end
    masking_scheme = args.masking_scheme
    prune_distance = args.prune_distance
    bc = args.bc
    ref_kma_database = args.ref_kma_database
    multi_threading = args.multi_threading
    reference = args.reference
    output_name = args.output_name
    exepath = args.exepath
    assemblies = args.i_assemblies
    insig_prune = args.insig_prune
    iqtree = args.iqtree
    FastTree = args.FastTree

    if i_illumina == [] and i_nanopore == [] and assemblies == []:
        sys.exit("No input was given.")

    if iqtree == True and FastTree == True:
        sys.exit("You selected both iqtree and fasttree - please choose only one or neither for CCphylo.")



    if assemblies != "":
        assembly_flag = True
        i_illumina = assemblies
    else:
        assembly_flag = False

    target_dir, logfile = checkOutputName(output_name)

    kma_database_path = ref_kma_database
    cmd = "mkdir " + target_dir + "DataFiles"
    os.system(cmd)

    kma_path = exepath + "kma/kma"


    startTime = time.time()
    print("# Running MINTyper 1.0.0 with following input conditions:", file=logfile)
    logfileConditionsResearch(logfile, masking_scheme, prune_distance, bc, ref_kma_database, multi_threading, reference, output_name, paired_end)

    i_illumina.sort()
    i_nanopore.sort()
    total_filenames = combine_input_files(i_illumina, i_nanopore)

    if 3 > len(i_nanopore) + len(i_illumina):
        sys.exit("You did not supply 2 or more input files. Please run the program again with correct input")


    best_template, templatename = findTemplateResearch(total_filenames, target_dir, kma_database_path, logfile, reference, kma_path)

    if i_illumina != []:
        if paired_end == True:
            illuminaMappingPE(i_illumina, best_template, target_dir, kma_database_path, logfile, multi_threading, reference, kma_path)
        else:
            illuminaMappingForward(i_illumina, best_template, target_dir, kma_database_path, logfile, multi_threading, reference, kma_path)
    if i_nanopore != []:
        nanoporeMapping(i_nanopore, best_template, target_dir, kma_database_path, logfile, multi_threading, bc, reference, kma_path)

    print ("calculating distance matrix")

    ccphylo_path = exepath + "ccphylo/ccphylo"

    checkAlignmentFiles(target_dir, total_filenames, paired_end)


    runCCphylo(iqtree, FastTree, ccphylo_path, target_dir, templatename, assembly_flag, insig_prune, prune_distance, masking_scheme, logfile, args.cluster_length)


    cleanUp(target_dir, i_illumina, i_nanopore, paired_end, reference)
    endTime = time.time()
    dTime = endTime - startTime
    print("MINTyper total runtime: " + str(dTime) + " seconds", file=logfile)
    logfile.close()
    print ("MINTyper has completed")

    cmd = "cat {}DataFiles/*.vcf.gz > {}combined.vcf.gz".format(target_dir, target_dir)
    os.system(cmd)

    varriansfileRenamer(total_filenames)

def findTemplateResearch(total_filenames, target_dir, kma_database_path, logfile, reference, kma_path):
    no_template_found = False
    best_template = ""
    best_template_score = 0.0
    templatename = ""
    if reference != "":
        #Check draftassembly
        proc = subprocess.Popen("wc -l {}".format(reference), shell=True, stdout=subprocess.PIPE)
        output = proc.communicate()[0]
        id = output.decode().rstrip()
        wc = id.split()[0]
        if int(wc) >= 2: #Draft
            # Concatenate contigs
            infile = open("{}".format(reference), 'r')
            newrefence = target_dir + "template_sequence.fasta"
            writefile = open("{}".format(newrefence), 'w')  # Adds all contigs to one sequence
            sequence = ""
            for line in infile:
                if line[0] != ">":
                    line = line.rstrip()
                    sequence += line
            print(">contatnateUserChosenDraftGenome", file=writefile)
            print(sequence, file=writefile)
            infile.close()
            writefile.close()
            best_template = newrefence
            print("# The reference given by the user was a draft genome, therfore is was concatnated.", file=logfile)
        else:
            best_template = reference
            print("# The reference given by the user was: " + best_template, file=logfile)
        print("#Making articial DB", file=logfile)
        cmd = "{} index -i {}  -o {}temdb.ATG -Sparse ATG".format(kma_path, best_template, target_dir)
        os.system(cmd)
        print("# Mapping reads to template", file=logfile)
        cmd = "{} -i {} -o {}template_kma_results -t_db {}temdb.ATG -Sparse -mp 20 -ss d".format(kma_path, total_filenames, target_dir, target_dir)
        os.system(cmd)

        try:
            infile_template = open(target_dir + "template_kma_results.spa", 'r')
            line = infile_template.readlines()[1]
            best_template = line.split("\t")[1]
            templatename = line.split("\t")[0]
            infile_template.close()
        except IndexError as error:
            print ("The template you have stated as a reference does not match the input reads to a good enough degree to make any type of analysis.")
            sys.exit()
        print("# Best template found was " + templatename, file=logfile)
        print("#Template number was: " + str(best_template), file=logfile)
        cmd = "{} seq2fasta -t_db {}temdb.ATG -seqs {} > {}template_sequence.fasta".format(kma_path, target_dir, str(best_template), target_dir)
        os.system(cmd)
        print("# Mapping reads to template", file=logfile)
        return best_template, templatename
    else:
        print("# Finding best template", file=logfile)
        cmd = "{} -i {} -o {}template_kma_results -ID 50 -t_db {} -Sparse -mp 20 -ss c".format(kma_path, total_filenames, target_dir, kma_database_path)
        os.system(cmd)
        try:
            infile_template = open(target_dir + "template_kma_results.spa", 'r')
            line = infile_template.readlines()[1]
            best_template = line.split("\t")[1]
            templatename = line.split("\t")[0]
            infile_template.close()
        except IndexError as error:
            sys.exit("Never found a template. Exiting. Check your SPA file.")
        print("# Best template found was " + templatename, file=logfile)
        print("# Template number was: " + str(best_template), file=logfile)
        cmd = "{} seq2fasta -t_db {} -seqs {} > {}template_sequence.fasta".format(kma_path, kma_database_path, str(best_template), target_dir)
        os.system(cmd)
        print("# Mapping reads to template", file=logfile)
        return best_template, templatename

def illuminaMappingForward(illumina_input, best_template, target_dir, kma_database_path, logfile, multi_threading, reference, kma_path):
    print("Single end illumina input was given")
    complete_path_illumina_input = illumina_input
    illumina_input = []
    for item in complete_path_illumina_input:
        illumina_input.append(item.split("/")[-1])
    if reference != "":
        kma_database_path = target_dir + "temdb.ATG"

    if illumina_input != "":
        for i in range(len(illumina_input)):
            cmd = "{} -i {} -o {}{}_mapping_results -t_db {} -ref_fsa -ca -dense -cge -vcf -bc90 -Mt1 {} -t {}".format(kma_path, complete_path_illumina_input[i], target_dir, illumina_input[i], kma_database_path, str(best_template), str(multi_threading))
            os.system(cmd)
        print ("# Illumina mapping completed succesfully", file=logfile)

def illuminaMappingPE(illumina_input, best_template, target_dir, kma_database_path, logfile, multi_threading, reference, kma_path):
    print("Paired end illumina input was given")
    complete_path_illumina_input = illumina_input
    illumina_input = []
    for item in complete_path_illumina_input:
        illumina_input.append(item.split("/")[-1])

    if reference != "":
        kma_database_path = target_dir + "temdb.ATG"

    if illumina_input != "":
        for i in range(0, len(illumina_input), 2):
            cmd = "{} -ipe {} {} -o {}{}_mapping_results -t_db {} -ref_fsa -ca -dense -cge -vcf -bc90 -Mt1 {} -t {}".format(kma_path, complete_path_illumina_input[i], complete_path_illumina_input[i+1], target_dir, illumina_input[i], kma_database_path, str(best_template), str(multi_threading))
            os.system(cmd)
        print ("# Illumina mapping completed succesfully", file=logfile)


def nanoporeMapping(nanopore_input, best_template, target_dir, kma_database_path, logfile, multi_threading, bc, reference, kma_path):
    complete_path_nanopore_input = nanopore_input
    nanopore_input = []
    for item in complete_path_nanopore_input:
        nanopore_input.append(item.split("/")[-1])


    if reference != "":
        kma_database_path = target_dir + "temdb.ATG"

    if nanopore_input != "":
        for i in range(0, len(nanopore_input)):
            cmd = "{} -i ".format(kma_path) + complete_path_nanopore_input[i] + " -o " + target_dir + nanopore_input[
                i] + "_mapping_results" + " -t_db " + kma_database_path + " -mp 20 -1t1 -dense -vcf -ref_fsa -ca -bcNano -Mt1 " + str(
                best_template) + " -t " + str(multi_threading) + " -bc " + str(bc)
            os.system(cmd)
        print ("# Nanopore mapping completed succesfully", file=logfile)

def cleanUp( target_dir, illumina_input, nanopore_input, paired_end, reference):
    complete_path_nanopore_input = nanopore_input
    nanopore_input = []
    for item in complete_path_nanopore_input:
        nanopore_input.append(item.split("/")[-1])

    complete_path_illumina_input = illumina_input
    illumina_input = []
    for item in complete_path_illumina_input:
        illumina_input.append(item.split("/")[-1])

    save_files_bool = True
    if save_files_bool == False:
        if illumina_input != "" and paired_end == False:
            for i in range(len(illumina_input)):
                cmd = "rm " + target_dir + illumina_input[i] + "_mapping_results.aln"
                os.system(cmd)
                cmd = "rm " + target_dir + illumina_input[i] + "_mapping_results.frag.gz"
                os.system(cmd)
                cmd = "rm " + target_dir + illumina_input[i] + "_mapping_results.res"
                os.system(cmd)
                cmd = "rm " + target_dir + illumina_input[i] + "_mapping_results.fsa"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.vcf.gz " + target_dir + "DataFiles"
                os.system(cmd)
        elif illumina_input != "" and paired_end == True:
            for i in range(0, len(illumina_input), 2):
                cmd = "rm " + target_dir + illumina_input[i] + "_mapping_results.aln"
                os.system(cmd)
                cmd = "rm " + target_dir + illumina_input[i] + "_mapping_results.frag.gz"
                os.system(cmd)
                cmd = "rm " + target_dir + illumina_input[i] + "_mapping_results.res"
                os.system(cmd)
                cmd = "rm " + target_dir + illumina_input[i] + "_mapping_results.fsa"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.vcf.gz " + target_dir + "DataFiles"
                os.system(cmd)
        if nanopore_input != "":
            for i in range(len(nanopore_input)):
                cmd = "rm " + target_dir + nanopore_input[i] + "_mapping_results.aln"
                os.system(cmd)
                cmd = "rm " + target_dir + nanopore_input[i] + "_mapping_results.frag.gz"
                os.system(cmd)
                cmd = "rm " + target_dir + nanopore_input[i] + "_mapping_results.res"
                os.system(cmd)
                cmd = "rm " + target_dir + nanopore_input[i] + "_mapping_results.fsa"
                os.system(cmd)
                cmd = "mv " + target_dir + nanopore_input[i] + "_mapping_results.vcf.gz " + target_dir + "DataFiles"
                os.system(cmd)
    elif save_files_bool == True:
        if illumina_input != "" and paired_end == False:
            for i in range(len(illumina_input)):
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.aln" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.frag.gz" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.res" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.fsa" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.vcf.gz " + target_dir + "DataFiles"
                os.system(cmd)
        elif illumina_input != "" and paired_end == True:
            for i in range(0, len(illumina_input), 2):
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.aln" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.frag.gz" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.res" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.fsa" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + illumina_input[i] + "_mapping_results.vcf.gz " + target_dir + "DataFiles"
                os.system(cmd)
        if nanopore_input != "":
            for i in range(len(nanopore_input)):
                cmd = "mv " + target_dir + nanopore_input[i] + "_mapping_results.aln" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + nanopore_input[i] + "_mapping_results.frag.gz" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + nanopore_input[i] + "_mapping_results.res" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + nanopore_input[i] + "_mapping_results.fsa" + " " + target_dir +"DataFiles"
                os.system(cmd)
                cmd = "mv " + target_dir + nanopore_input[i] + "_mapping_results.vcf.gz " + target_dir + "DataFiles"
                os.system(cmd)

    if reference != "":
        cmd = "rm " + target_dir + "temdb.ATG.comp.b"
        os.system(cmd)
        cmd = "rm " + target_dir + "temdb.ATG.length.b"
        os.system(cmd)
        cmd = "rm " + target_dir + "temdb.ATG.name"
        os.system(cmd)
        cmd = "rm " + target_dir + "temdb.ATG.seq.b"
        os.system(cmd)

def combine_input_files(i_illumina, i_nanopore):
    if i_illumina == []:
        total_input_files = i_nanopore
    elif i_nanopore == []:
        total_input_files = i_illumina
    else:
        total_input_files = i_illumina + i_nanopore
    total_input_files = " ".join(total_input_files)
    return total_input_files

def logfileConditionsResearch(logfile, masking_scheme, prune_distance, bc, ref_kma_database, multi_threading, reference, output_name, paired_end):
    logdict = {}
    if masking_scheme != "":
        logdict['masking_scheme'] = masking_scheme
    else:
        logdict['masking_scheme'] = ""
    if prune_distance != 10:
        logdict['prune_distance'] = prune_distance
    else:
        logdict['prune_distance'] = 10
    if bc != 0.7:
        logdict['bc'] = bc
    else:
        logdict['bc'] = 0.7
    if ref_kma_database != "":
        logdict['ref_kma_database'] = ref_kma_database
    else:
        logdict['ref_kma_database'] = ""
    if multi_threading != 1:
        logdict['multi_threading'] = multi_threading
    else:
        logdict['multi_threading'] = 1
    if reference != "":
        logdict['reference'] = reference
    else:
        logdict['reference'] = ""
    if output_name != "":
        logdict['output_name'] = output_name
    else:
        logdict['output_name'] = ""
    if paired_end != False:
        logdict['paired_end'] = str(paired_end)
    else:
        logdict['paired_end'] = str(False)
    print (logdict, file=logfile)
    if paired_end == True:
        print("# -pe", file=logfile)
    print("# -prune_distance: " + str(prune_distance), file=logfile)
    if bc != 0:
        print("# -bc: " + str(bc), file=logfile)
    if ref_kma_database != "":
        print("# -db: " + ref_kma_database, file=logfile)
    if multi_threading != 1:
        print("# -thread: " + str(multi_threading), file=logfile)
    if reference != "":
        print("# -ref: " + reference, file=logfile)
    print ("loading input")

def varriansfileRenamer(total_filenames):
    inputs = total_filenames.split(" ")
    sorted_input = []
    for i in range(len(inputs)):
        name = inputs[i].split("/")[-1]
        sorted_input.append(name)

def checkAlignmentFiles(target_dir, total_filenames, paired_end):
    total_filenames = total_filenames.split(" ")
    if paired_end == True:
        for i in range(0, len(total_filenames),2):
            if os.stat(target_dir + total_filenames[i].split("/")[-1] + "_mapping_results.fsa").st_size == 0:
                cmd = "rm {}{}".format(target_dir, total_filenames[i].split("/")[-1]  + "_mapping_results.fsa")
                os.system(cmd)
                # Skriv fejl i logfil
    else:
        for name in total_filenames:
            if os.stat(target_dir + name.split("/")[-1] + "_mapping_results.fsa").st_size == 0:
                cmd = "rm {}{}".format(target_dir, name.split("/")[-1] + "_mapping_results.fsa")
                os.system(cmd)
                #Skriv fejl i logfil

def checkOutputName(output_name):
    # if used on server and output path is provided:
    if output_name[0] == "/":
        target_dir = output_name + "/"
        cmd = "mkdir " + target_dir
        os.system(cmd)
        cmd = "chmod 775 " + target_dir
        os.system(cmd)
        cmd = "chmod 775 " + target_dir + "Datafiles/"
        os.system(cmd)
        logfilename = target_dir + "logfile"
        logfile = open(logfilename, 'w')
    else:
        current_path = os.getcwd()
        target_dir = current_path + "/" + output_name + "/"
        cmd = "mkdir " + output_name
        os.system(cmd)
        logfilename = target_dir + "logfile_" + output_name
        logfile = open(logfilename, 'w')

    return target_dir, logfile

def runCCphylo(iqtree, FastTree, ccphylo_path, target_dir, templatename, assembly_flag, insig_prune, prune_distance, masking_scheme, logfile, cluster_length):
    # Ccphylo
    if iqtree == False and FastTree == False:
        ccphyloflag = 1
        cmd = "{} dist -i {}*.fsa -o {}{} -r \"{}\" -mc 1 -nm 0".format(ccphylo_path, target_dir, target_dir,
                                                                        "distmatrix.txt", templatename)
        if assembly_flag == True:
            ccphyloflag += 8
        if insig_prune == True:
            ccphyloflag += 32
        if prune_distance != 0:
            cmd = cmd + " -pr {}".format(prune_distance)
        if masking_scheme != "":
            cmd = cmd + " -m {}".format(masking_scheme)

        cmd = cmd + " -f {}".format(ccphyloflag)
        cmd = cmd + " -nv {}nucleotideVarriance &>> {}distance_matrix_logfile".format(target_dir, target_dir)
        os.system(cmd)

        infile = open("{}distance_matrix_logfile".format(target_dir), 'r')
        for line in infile:
            line = line.rstrip()
            print(line, file=logfile)
        infile.close()

        cmd = "rm {}distance_matrix_logfile".format(target_dir)
        os.system(cmd)

        cmd = "{} tree -i {}{} -o {}outtree.newick".format(ccphylo_path, target_dir, "distmatrix.txt", target_dir)
        #print(cmd)
        #os.system(cmd)
        time.sleep(5) #Test
        cmd = cmd.split(" ")
        subprocess.run(cmd)

        if cluster_length > 0:
            cmd = "{} dbscan -d {} -i {}{} -o {}{}".format(ccphylo_path, cluster_length, target_dir,
                                                           "distmatrix.txt", target_dir, "cluster.dbscan")
            os.system(cmd)
    elif iqtree == True:
        ccphyloflag = 1
        cmd = "{} trim -i {}*.fsa -r \"{}\" > {}trimmedalign.fsa".format(ccphylo_path, target_dir, templatename,
                                                                         target_dir)
        if assembly_flag == True:
            ccphyloflag += 8
        if insig_prune == True:
            ccphyloflag += 32
        cmd = cmd + " -f {}".format(ccphyloflag)
        # Only include max flag value
        if prune_distance != 0:
            cmd = cmd + " -pr {}".format(prune_distance)
        if masking_scheme != "":
            cmd = cmd + " -m {}".format(masking_scheme)
        os.system(cmd)

        cmd = "iqtree -s {}trimmedalign.fsa > {}iqtree".format(target_dir, target_dir)
        os.system(cmd)

    elif FastTree == True:
        ccphyloflag = 1
        cmd = "{} trim -i {}*.fsa -r \"{}\" > {}trimmedalign.fsa".format(ccphylo_path, target_dir, templatename,
                                                                         target_dir)
        if assembly_flag == True:
            ccphyloflag += 8
        if insig_prune == True:
            ccphyloflag += 32
        cmd = cmd + " -f {}".format(ccphyloflag)
        if prune_distance != 0:
            cmd = cmd + " -pr {}".format(prune_distance)
        if masking_scheme != "":
            cmd = cmd + " -m {}".format(masking_scheme)
        os.system(cmd)

        cmd = "FastTree -nt -gtr {}trimmedalign.fsa > {}fasttree".format(target_dir, target_dir)
        os.system(cmd)










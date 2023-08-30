from Bio.SeqUtils.ProtParam import ProteinAnalysis
from datetime import date
from Bio import Entrez, Medline
import pyperclip
import sys

def prot_param(prot):
    
    protein = ProteinAnalysis(prot)

    epsilon = protein.molar_extinction_coefficient()
    mw = protein.molecular_weight()

    print("Number of residues: ", sum(protein.count_amino_acids().values()))
    print("Mw: ""%0.2f" % mw)
    print("IP: ""%0.2f" % protein.isoelectric_point())
    if epsilon[0] == 0:
        print("No Trp resiudes, can't compute Extinction coefficient")
    else:
        print("Extinction coefficient:", epsilon[0], "(reduced), ", epsilon[1], "(oxidized)", "\nAbs280nm (1g/l):", epsilon[0]/mw, " // ")#, 1/(epsilon[0]/mw))
    print("Copied to clipboard!\n")
    # pyperclip.copy("Mw: ""%0.2f" % mw, "\nIP: ""%0.2f" % protein.isoelectric_point(), "\nExtinction coefficient:", epsilon[0], "(reduced), ", epsilon[1], "(oxidized)", "\nAbs280nm (1g/l):", epsilon[0]/mw, " // ", 1/(epsilon[0]/mw))
    pyperclip.copy("Mw: ""%0.2f" % mw + "\nIP: " + str(protein.isoelectric_point()))
    
    return

def pubmed_search(query, n):
    Entrez.email = "aromeroc93@gmail.com"
    Entrez.api_key = "510d2439a3c3615a6f94e14430a9e33a1c08"

    handle = Entrez.esearch(db="pubmed", term=query, reldate=n)
    record = Entrez.read(handle)
    handle.close()
    idlist = record["IdList"]

    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode="text")
    records = Medline.parse(handle)
    
    today = date.today()
    today = today.strftime("%Y%m%d")

    i = 1
    file = open("pubmed_searches.md", "a")
    file.write("## " + today + "\n\nFound " + str(len(idlist)) + " papers from query " + query + " in the last " + str(n) + " days.\n\n")
    doi_list = []

    # Add some way to check how many results are already in the outpu file/check the last entry, and only consider the new entries.
    
    for record in records:
        title = record.get("TI", "?")
        authors = record.get("AU", "?")
        journal = record.get("SO", "?")
        doi = record.get("LID", "?")
        file.write("Result #" + str(i) + "\nTitle:" + title + "\nJournal:" + journal + "\nAuthors:")
        for author in authors:
            file.write(author + ",")
        file.write("\n\n")
        print("Result #", i, "\nTitle:", title, "\nAuthors:", authors, "\n")
        doi_list.append(doi)
        i += 1

    file.close()

    k = int(input("DOI to copy: "))
    while (k > len(doi_list)) or (k < 1):
        k = int(input("Invalid, try again: "))
    
    print("Here is your DOI:", doi_list[k - 1])
    pyperclip.copy(doi_list[k - 1])
    print("Copied to clipboard!\n")
    
    return

def show_menu():
    x = input("What script do you want to launch?\n 1 - prot-param\n 2 - pubmed-search\n 3 - Exit\n")
    return x
    
def main():
    
    x = '0'
    while (x!='1' and x!='2' and x!='3'):
        print("Not an option!\n")
        x = show_menu()
        
    if (x == '1'):
        prot = input("Insert protein sequence: ")
        prot_param(prot)
        x = show_menu()
    elif (x == '2'):
        query = input("Query: ")
        n = int(input("How many days back to search? "))
        pubmed_search(query, n)
        x = show_menu()
    elif (x == '3'):
        sys.exit(1)
    
    
if __name__ == "__main__":
    main()
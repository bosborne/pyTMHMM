import hashlib
import subprocess
import unittest
import sys
import os
import re
testdir = os.path.dirname(__file__)
srcdir = '../pyTMHMM'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))
import pyTMHMM


class TestTMHMM(unittest.TestCase):
    '''
    Run tmhmm and check the *annotation file and results
    '''

    annotation = 'B9DFX7|1B|HMA8_ARATH.annotation'
    plot = 'B9DFX7|1B|HMA8_ARATH.plot'
    summary = 'B9DFX7|1B|HMA8_ARATH.summary'
    seq = 'MASNLLRFPLPPPSSLHIRPSKFLVNRCFPRLRRSRIRRHCSRPFFLVSNSVEISTQSFESTESSIESVKSITSDTPIL\
LDVSGMMCGGCVARVKSVLMSDDRVASAVVNMLTETAAVKFKPEVEVTADTAESLAKRLTESGFEAKRRVSGMGVAENV\
KKWKEMVSKKEDLLVKSRNRVAFAWTLVALCCGSHTSHILHSLGIHIAHGGIWDLLHNSYVKGGLAVGALLGPGRELLF\
DGIKAFGKRSPNMNSLVGLGSMAAFSISLISLVNPELEWDASFFDEPVMLLGFVLLGRSLEERAKLQASTDMNELLSLI\
STQSRLVITSSDNNTPVDSVLSSDSICINVSVDDIRVGDSLLVLPGETFPVDGSVLAGRSVVDESMLTGESLPVFKEEG\
CSVSAGTINWDGPLRIKASSTGSNSTISKIVRMVEDAQGNAAPVQRLADAIAGPFVYTIMSLSAMTFAFWYYVGSHIFP\
DVLLNDIAGPDGDALALSLKLAVDVLVVSCPCALGLATPTAILIGTSLGAKRGYLIRGGDVLERLASIDCVALDKTGTL\
TEGRPVVSGVASLGYEEQEVLKMAAAVEKTATHPIAKAIVNEAESLNLKTPETRGQLTEPGFGTLAEIDGRFVAVGSLE\
WVSDRFLKKNDSSDMVKLESLLDHKLSNTSSTSRYSKTVVYVGREGEGIIGAIAISDCLRQDAEFTVARLQEKGIKTVL\
LSGDREGAVATVAKNVGIKSESTNYSLSPEKKFEFISNLQSSGHRVAMVGDGINDAPSLAQADVGIALKIEAQENAASN\
AASVILVRNKLSHVVDALSLAQATMSKVYQNLAWAIAYNVISIPIAAGVLLPQYDFAMTPSLSGGLMALSSIFVVSNSL\
LLQLHKSETSKNSL'

    def test_fasta1(self):
        # Fasta file with id and description
        fastafile = os.path.join(testdir, 'test1.fa')
        try:
            subprocess.run(['pyTMHMM',
                            '-f',
                            fastafile],
                           check=True)
        except (subprocess.CalledProcessError) as exception:
            print(
                "Error running pyTMHMM -f {0}: {1}".format(fastafile, str(exception)))
        with open(self.annotation) as infile:
            checksum = hashlib.md5(infile.read().encode()).hexdigest()
        self.remove_files()
        self.assertEqual(
            checksum, 'fc4ec46d73f9ab28b5623bded3d6f629', "Correct 128-bit checksum")

    def test_fasta2(self):
        # Fasta file with just id
        fastafile = os.path.join(testdir, 'test2.fa')
        try:
            subprocess.run(['pyTMHMM',
                            '-f',
                            fastafile],
                           check=True)
        except (subprocess.CalledProcessError) as exception:
            print(
                "Error running pyTMHMM -f {0}: {1}".format(fastafile, str(exception)))
        with open(self.annotation) as infile:
            checksum = hashlib.md5(infile.read().encode()).hexdigest()
        self.remove_files()
        self.assertEqual(
            checksum, '43826e2c876aaae1237df4296fd4ad28', "Correct 128-bit checksum")

    def test_annotation(self):
        annotation = pyTMHMM.predict(self.seq, compute_posterior=False)
        self.assertEqual(annotation.count('M'), 64,
                         "Correct number of TM amino acids")
        self.assertEqual(annotation.count('O'), 445,
                         "Correct number of external amino acids")
        self.assertEqual(annotation.count('i'), 365,
                         "Correct number of internal amino acids")
        self.assertEqual(len(re.findall(r'M+', annotation)),
                         3, "Correct number of TMs")

    def test_posterior(self):
        _, posterior = pyTMHMM.predict(self.seq)
        self.assertEqual(len(posterior), 883,
                         "Correct number of aa's in posterior")

    def remove_files(self):
        os.remove(self.annotation)
        os.remove(self.plot)
        os.remove(self.summary)


if __name__ == '__main__':
    unittest.main()

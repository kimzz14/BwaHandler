from lib.Process.Process import PROC
import os

class BwaHandler:
    def __init__(self):
        self.version = None

    def check_bwa(self):
        process = PROC('bwa')
        process.run()
        process.wait()

        for line in process.stderr.split('\n'):
            if line.startswith('Version') == True:
                self.version = line.replace('Version:', '').strip()

        if self.version == None:
            print('There is no BWA!!')
        else:
            print(self.version)

    def check_index(self, fastaFile):
        if os.path.exists(fastaFile + '.sa') == False:
            return False
        else:
            return True
        
    def makeDir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
            os.makedirs(dir + '/tmp')
            return True
        else:
            return False

    def run_index(self, fastaFile):
        process = PROC('bwa index ' + fastaFile)
        process.run()
        process.wait()

    def run_aln(self, threadN, maxMisN, refFile, outputDir):
        if self.makeDir(outputDir) == False:
            return False

        command  = ['bwa aln']
        command += ['-t ' + str(threadN)]
        command += ['-N -i 30 -d 30 -m 200000000 -l 100']
        command += ['-n ' + str(maxMisN)]
        command += [refFile]
        command += [outputDir + '/tmp/' + 'primer.fastq']
        command += ['1> ' + outputDir + '/tmp/' + 'primer.sai']
        command += ['2> ' + outputDir + '/tmp/' + 'primer.aln_log']

        process = PROC(' '.join(command))
        process.run()
        process.wait()

        command  = ['bwa samse -n 300000000']
        command += [refFile]
        command += [outputDir + '/tmp/' + 'primer.sai']
        command += [outputDir + '/tmp/' + 'primer.fastq']
        command += ['1> ' + outputDir + '/tmp/' + 'primer.sam']
        command += ['2> ' + outputDir + '/tmp/' + 'primer.samse_log']
        #command += ['| gzip > ' + outputDir + '/tmp/' + 'primer.sam.gz']

        process = PROC(' '.join(command))
        process.run()
        process.wait()

        return True

if __name__ == '__main__':
    bwaHandler = BwaHandler()
    #bwaHandler.check_bwa()
    #print(bwaHandler.check_index('Fxananassa_675_v1.0.fa'))
    #bwaHandler.run_index('genome.fa')
    bwaHandler.run_aln(128, 5, 'genome.fa', 'test')
    
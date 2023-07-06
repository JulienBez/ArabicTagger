import glob
import subprocess
from tqdm import tqdm

def docToDocx():
    for doc in tqdm(list(glob.iglob("data/doc/*.doc"))):
        subprocess.call(['soffice', '--headless', '--convert-to', 'docx', '--outdir', 'data/doc/',  doc])
        subprocess.call(['rm',doc])

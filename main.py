import argparse, os
import shutil
from progress.bar import Bar

def main():
    def get_cid(path):
        return os.popen(f'ipfs add -n -Q {path}', 'r').read()

    def my_full_path(string):
        script_dir = os.path.dirname(__file__)
        return  os.path.normpath(os.path.join(script_dir, string))


    parser = argparse.ArgumentParser(description='Copy file in a directory and rename them with their IPFS CIDv0.')
    parser.add_argument('--fromDir', required=True, type=my_full_path)
    parser.add_argument('--outputDir', required=True, type=my_full_path)

    args = parser.parse_args()

    if not os.path.exists(args.outputDir):
        os.mkdir(args.outputDir) 
    else:
        exit('Output directory already exists.')

    files = os.listdir(args.fromDir)


    progressBar = Bar('Processing', max=len(files))

    for file in files:        

        extension_file = os.path.splitext(file)[1]

        input_path = os.path.join(args.fromDir, file)
        hash = get_cid(input_path)

        output_filename = hash.strip() + extension_file
        output_path = os.path.join(args.outputDir, output_filename)
        
        shutil.copyfile(input_path, output_path)
        progressBar.next()

    progressBar.finish()
    print('Done.')

if __name__ == '__main__':
    main()
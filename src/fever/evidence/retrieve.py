import argparse
import json
from multiprocessing.pool import ThreadPool
from fever.reader import FEVERDocumentDatabase
from tqdm import tqdm

from fever.evidence.retrieval_methods.top_docs import TopNDocsTopNSents


def process_line(method,line, args):
    sents = method.get_sentences_for_claim(line["claim"])
    pages = list(set(map(lambda sent:sent[0],sents)))
    line["predicted_pages"] = pages
    line["predicted_sentences"] = sents
    return line


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_map_function(parallel):
    return p.imap if parallel else map


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str, help='/path/to/saved/db.db')
    parser.add_argument('--index', type=str, help='/path/to/saved/db.db')
    parser.add_argument('--in-file', type=str, help='/path/to/saved/db.db')
    parser.add_argument('--out-file', type=str, help='/path/to/saved/db.db')
    parser.add_argument('--max-page',type=int)
    parser.add_argument('--max-sent',type=int)
    parser.add_argument('--cuda-device',type=int,default=-1)
    parser.add_argument('--parallel',type=str2bool,default=True)
    parser.add_argument('--threads', type=int, default=None)

    args = parser.parse_args()

    database = FEVERDocumentDatabase(args.database)
    method = TopNDocsTopNSents(database, args.index, args.max_page, args.max_sent)

    processed = dict()
    with open(args.in_file,"r") as in_file, open(args.out_file, "w+") as out_file:
        lines = []
        for line in in_file:
            lines.append(json.loads(line))

        with ThreadPool(args.threads) as p:
            for line in tqdm(get_map_function(args.parallel)(lambda line: process_line(method,line, args),lines), total=len(lines)):
                out_file.write(json.dumps(line) + "\n")

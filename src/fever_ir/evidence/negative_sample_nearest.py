import argparse
import json
from tqdm import tqdm
from drqa import retriever


def process(ranker, query, k=1):
    doc_names, doc_scores = ranker.closest_docs(query, k)

    return doc_names



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--in-file', type=str)
    parser.add_argument('--out-file', type=str)
    parser.add_argument('--index', type=str)
    parser.add_argument('--count',type=int, default=1)
    args = parser.parse_args()

    k = args.count
    ranker = retriever.get_class('tfidf')(tfidf_path=args.index)

    with open(args.in_file) as f:
        with open(args.out_file,"w+") as f2:
            for line in tqdm(f.readlines()):
                line = json.loads(line)

                if line["label"] == "NOT ENOUGH INFO":
                    pages = process(ranker, line['claim'], k=k)
                    pp = list(pages)

                    for idx,evidence_group in enumerate(line['evidence']):
                        for evidence in evidence_group:
                            if idx<len(pp):
                                evidence[2] = pp[idx]
                                evidence[3] = -1


                f2.write(json.dumps(line) + "\n")


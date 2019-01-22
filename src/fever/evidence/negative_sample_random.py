import argparse
import json
import random
from fever.reader import FEVERDocumentDatabase


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--database', type=str)
    parser.add_argument('--in-file', type=str)
    parser.add_argument('--out-file', type=str)

    args = parser.parse_args()



    docdb = FEVERDocumentDatabase(args.database)

    idx = docdb.get_non_empty_doc_ids()

    r = random.Random(123)
    r.seed(123)

    with open(args.out_file, "w+") as f:
        for line in open(args.in_file):
            line = json.loads(line)

            if line["label"] == "NOT ENOUGH INFO":

                for evidence_group in line['evidence']:
                    for evidence in evidence_group:
                        evidence[2] = idx[r.next_rand(0, len(idx))]
                        evidence[3] = -1

            f.write(json.dumps(line)+"\n")
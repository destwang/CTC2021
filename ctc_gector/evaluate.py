import argparse
import traceback

def read_data(filename):
    '''
    读取数据
    :param filename:
    :return:
    '''
    det_set, cor_set = set(), set()
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            terms = line.strip().split(',')
            terms = [t.strip() for t in terms]
            pid = terms[0]
            if len(terms) == 2 and terms[-1] == '-1':
                continue
            elif (len(terms)-2) % 4 == 0:
                error_num = int((len(terms)-2) / 4)
                for i in range(error_num):
                    loc, typ, wrong, correct = terms[i*4+1: (i+1)*4+1]
                    det_set.add((pid, int(loc), wrong))
                    cor_set.add((pid, int(loc), wrong, correct))
            else:
                raise Exception('check your data format: {}'.format(line))
    return det_set, cor_set


def cal_f1(ref_set, pred_set):
    ref_num = len(ref_set)
    pred_num = len(pred_set)
    right_num = len(ref_set & pred_set)
    precision = float(right_num) / pred_num
    recall = float(right_num) / ref_num
    if precision + recall < 1e-6:
        return 0.0
    f1 = 2 * precision * recall / (precision + recall)
    return f1 * 100


def evaluate(ref_file, pred_file):
    ref_det_set, ref_cor_set = read_data(ref_file)
    pred_det_set, pred_cor_set = read_data(pred_file)
    detect_f1 = cal_f1(ref_det_set, pred_det_set)
    correct_f1 = cal_f1(ref_cor_set, pred_cor_set)
    final_score = 0.8 * detect_f1 + 0.2 * correct_f1
    print("detect_f1: {}".format(detect_f1))
    print("correct_f1: {}".format(correct_f1))
    print("final_score: {}".format(final_score))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--ref_file',
                        help='Path to the reference file',
                        required=True)
    parser.add_argument('-p', '--pred_file',
                        help='Path to the predict file',
                        required=True)
    args = parser.parse_args()
    try:
        evaluate(args.ref_file, args.pred_file)
    except:
        traceback.print_exc()

from typing import List
import csv


def __levenshtein(a: List, 
                  b: List) -> int:
    """Calculates the Levenshtein distance between a and b.
    """
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = list(range(n + 1))
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]


def word_error_rate(hypotheses: List[str], 
                    references: List[str],
                    use_cer = False) -> float:
    """
    Computes Average Word Error rate between two texts represented as
    corresponding lists of string. Hypotheses and references must have same length.

    Args:
        hypotheses: list of hypotheses
        references: list of references

    Returns:
        (float) average word error rate
    """
    scores = 0
    words = 0
    len_diff = len(references) - len(hypotheses) 
    if len_diff > 0:
        raise ValueError("In word error rate calculation, hypotheses and reference"
                         " lists must have the same number of elements. But I got:"
                         "{0} and {1} correspondingly".format(len(hypotheses), len(references)))
    elif len_diff < 0:
        hypotheses = hypotheses[:len_diff]
    
    for h, r in zip(hypotheses, references):
        if use_cer:
            # h = h.replace(' ', '')
            # r = r.replace(' ', '')
            h_list = list(h)
            r_list = list(r)
        else:
            h_list = h.split()
            r_list = r.split()

        words += len(r_list)
        scores += __levenshtein(h_list, r_list)

    if use_cer:
        print(f"==========>>>>>>Evaluation CER_WORDS: {words}")
        print(f"==========>>>>>>Evaluation CER_SCORES: {scores}")
    else:
        print(f"==========>>>>>>Evaluation WER_WORDS: {words}")
        print(f"==========>>>>>>Evaluation WER_SCORES: {scores}")

    with open("output.csv", 'w', encoding='utf-8-sig', newline='') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(['hypothesis', 'reference', 'CER_SCORES', 'CER_WORDS', 'CER', 'WER_SCORES', 'WER_WORDS', 'WER'])

        for h, r in zip(hypotheses, references):
            h_cer_list = list(h)
            r_cer_list = list(r)

            h_wer_list = h.split()
            r_wer_list = r.split()

            cer_words = len(r_cer_list)
            cer_scores = __levenshtein(h_cer_list, r_cer_list)

            wer_words = len(r_wer_list)
            wer_scores = __levenshtein(h_wer_list, r_wer_list)

            writer.writerow([h, r, cer_scores, cer_words, round(1.0*cer_scores/cer_words, 4) * 100, wer_scores, wer_words, round(1.0*wer_scores/wer_words, 4) * 100])

    if words!=0:
        wer = 1.0*scores/words
    else:
        wer = float('inf')

    # TODO CER 15%이상, WER 35% 이상 저장하기, 파일명은 그냥 절대값으로 주고
    return wer, scores, words
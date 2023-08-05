import random
import math
import itertools
from collections import defaultdict


def pattern_count(text, pattern):
    """[finds all occurences of a pattern in a text of bases]

    Args:
        text ([string]): [input string]
        pattern ([string]): [pattern to search for in string]

    Returns:
        [int]: [running tally of how many occurrences of pattern were found in text]
    """
    Count = 0
    PatternLength = len(pattern)
    TextLength = len(text)
    for i in range((TextLength - PatternLength)+1):  # i represents a kmer
        if text[i:i+PatternLength] == pattern:
            Count += 1
    return Count


def frequency_map(text, k):
    """[computes the frequency map of a given string text and integer k, returns a dictionary of each supplied k-mer value]

    Args:
        text ([string]): [input string]
        k ([int]): [determine length of kmer]

    Returns:
        [dict]: [for every length of kmer specified by k(keys), returns how many times it occurs in text(values)]
    """
    Freq = {}
    TextLength = len(text)
    for i in range(TextLength-k+1):  # range over all possible kmer combinations
        Pattern = text[i:i+k]
        Freq[Pattern] = 0
        for j in range(TextLength-k+1):
            if text[j:j+k] == Pattern:
                Freq[Pattern] += 1
    return Freq


def frequent_words(text, k):
    """[list of all keys that have value in frequency map == k]

    Dependancies:
        frequency map

    Args:
        text ([string]): [input string]
        k ([int]): [standard for values returned by frequency map; equal valued kmers are sought out]

    Returns:
        [list]: [when kmer from frequency map (the key's value) occurs as many times as specified k in this function, 
        it is appended to the returned list]
    """
    Words = []
    Freq = frequency_map(text, k)
    MaxFreqKey = max(Freq.values())
    for kmer in Freq:
        if Freq[kmer] == MaxFreqKey:
            pattern = kmer
            Words.append(pattern)
    return Words


def reverse(pattern):
    """[reverses a string]

    Args:
        pattern ([string]): [string to be reversed]

    Returns:
        [string]: [reversed version of inputted string "pattern"]
    """
    return ''.join(reversed(pattern))
    # OR return pattern[::-1]


def compliment(pattern):
    """[finds the complimentary strand of DNA "pattern"]

    Args:
        pattern ([string]): [DNA strand of which compliment is found]

    Returns:
        [string]: [compliment of DNA pattern: A -> T, G -> C, T -> A, C -> G]
    """
    Basepairs = {"A": "T", "G": "C", "T": "A", "C": "G"}
    Complement = ""
    for base in pattern:
        # Get returns a key's value. eg: if base = "A", get will find the key "A" and return its value, "T"
        Complement += Basepairs.get(base)
    return Complement


def reverse_compliment(pattern):
    """[finds the complement strand of a DNA strand]

    Dependancies:
        reverse, compliment
    Args:
        pattern ([string]): [string of DNA to be used to find the reverse compliment]

    Returns:
        [string]: [pattern has been reversed and the complimentary base replaces the current one in string pattern]
    """
    pattern = reverse(pattern)  # reverse all letters in a string
    pattern = compliment(pattern)  # compliment each letter in a string
    return pattern
    # OR return(pattern[::-1].replace("A","t").replace("T","a").replace("G","c").replace("C","g").upper())


def pattern_matching(pattern, genome):
    """[find all occurrences of a pattern in a string]

    Args:
        pattern ([string]): [input string]
        genome ([string]): [text to be parsed, locating all occurrences of "pattern"]

    Returns:
        [list]: [returns location where text "pattern" is found in text "genome"]
    """
    Positions = []
    GenomeLength = len(genome)
    PatternLength = len(pattern)
    for i in range(GenomeLength - PatternLength + 1):
        if pattern == genome[i:i+PatternLength]:
            Positions.append(i)
    return Positions

# -------------------------------------------------------------------------

# def SymbolArray(genome, symbol):
#     array = {}
#     n = len(genome)
#     Extendedgenome = genome + genome[0:n//2]
#     for i in range(n):  # i-th element is the number of occurrences of the symbol in window length len(genome)//2 starting at pos i of Extended genome
#         array[i] = pattern_count(symbol, Extendedgenome[i:i+(n//2)])
#     return array


# FasterSymbol array - takes genome and symbol but computes it quicker by using a better for loop
# uses pattern_count


def symbol_array(genome, symbol):
    """[helps to count the number of C in a window of Extended genome, along with pattern count]

    Dependancies:
        pattern_count

    Args:
        genome ([string]): [string to be parsed]
        symbol ([string]): [whichever nucleotide base to be searched for, ATGC]

    Returns:
        [dict]: [symbol array of genome corresponding to symbol.  the i-th element of the symbol array is the number of
        occurrences of symbol in window length len(genome)//2 starting as pos i of Extendedgenome]
    """
    SymbolArray = {}
    GenomeLength = len(genome)
    Extendedgenome = genome + genome[0:GenomeLength//2]  # copied to the end of the genome string

    # look at the first half of genome to compute first array value
    SymbolArray[0] = pattern_count(symbol, genome[0:GenomeLength//2])

    for i in range(1, GenomeLength):
        # start by setting the current array value equal to the previous array value
        SymbolArray[i] = SymbolArray[i-1]

        # the current array value can differ from the previous array value by at most 1
        if Extendedgenome[i-1] == symbol:
            SymbolArray[i] = SymbolArray[i]-1
        if Extendedgenome[i+(GenomeLength//2)-1] == symbol:
            SymbolArray[i] = SymbolArray[i]+1
    return SymbolArray


def skew_array(genome):
    """[keeps track of total no of occurrences of C and G encountered so far in genome]

    Args:
        genome ([string]): [string to be parsed]

    Returns:
        [list]: [tracks how many times nucleotide bases C and G appear in genome]
    """
    Skew = [0]
    for i in range(len(genome)):
        if genome[i] == 'C':
            Skew.append(Skew[i] - 1)
        elif genome[i] == 'G':
            Skew.append(Skew[i] + 1)
        else:
            Skew.append(Skew[i])
    return Skew


def minimum_skew(genome):
    """[location where skew diagram obtains a minimum(location of ori)]

    Dependancies:
        skew_array

    Args:
        genome ([string]): [string to be parsed]

    Returns:
        [list]: [. All integers i minimizing Skew[i] among all values of i from 0 to len(genome)
        wherever skew diagram obtains a minimum, it is appended to the list]
    """
    Positions = []
    SkewArray = skew_array(genome)
    count = 0
    MinArray = min(SkewArray)
    for i in SkewArray:
        if i == MinArray:
            Positions.append(count)
        count += 1
    return Positions


def hamming_distance(p, q):
    """[Total no. of mismatches bt strings p and q, pos i in kmers p and q is a mismatch
        if the symbols at pos i of the 2 strings are not the same. NOTE: MUST BE EQUAL LENGTH STRINGS.
        IF NOT EQUAL LENGTH, USE LEVENSHTEIN DISTANCE]

    Args:
        p ([string]): [first reference string]
        q ([string]): [second reference string]

    Returns:
        [int]: [number of mismatches at every point along strings p[i] and q[i]]
    """
    Count = 0
    for x, y in zip(p, q):
        if x != y:
            Count += 1
    return Count


def approx_pattern_match(text, pattern, d):
    """[find all approximate occurrences of a pattern in a string with at most d mismatches]

    Dependancies:
        hamming_distance

    Args:
        text ([string]): [input string to be searched]
        pattern ([string]): [string that is searched for in text]
        d ([int]): [how many mismatches are permitted]

    Returns:
        [list]: [positions that pattern are located in text with at most d mismatches in that relationship]
    """
    Positions = []
    for i in range(len(text)-len(pattern)+1):
        if hamming_distance(text[i:i+len(pattern)], pattern) <= d:
            Positions.append(i)
    return Positions


def approx_pattern_count(pattern, text, d):
    """[find DnaA boxes by identifying frequent kmers, with d possible mismatches]

    Args:
        text ([string]): [input string to be searched]
        pattern ([string]): [string that is searched for in text]
        d ([int]): [how many mismatches are permitted]

    Returns:
        [int]: [frequent kmers with at most d mismatches indicating the likely presence of a DnaA box to initiate
        Dna replication]
    """
    Count = 0  # initialize Count variable
    for i in range(len(text)-len(pattern)+1):
        if hamming_distance(pattern, text[i:i+len(pattern)]) <= d:
            Count += 1
    return Count

# -------------------------------------------------------------------------


def count(Motifs):
    """[creates a dictionary with all the nucleotides and how much they are present in the j-th column of the Motif matrix]

    Args:
        Motifs ([string matrix]): [holds several DNA strings as kmers - motifs]

    Returns:
        [dict]: [lists of int with nucleotids as keys]
    """
    CountArray = {}
    MotifLength = len(Motifs[0])
    for symbol in 'ACGT':
        CountArray[symbol] = []
        for j in range(MotifLength):
            CountArray[symbol].append(0)
    t = len(Motifs)
    for i in range(t):
        for j in range(MotifLength):
            symbol = Motifs[i][j]
            CountArray[symbol][j] += 1
    return CountArray


def profile(Motifs):
    """[frequency of i-th nucleotide in the j-th column of the Motif matrix]

    Dependancies:
        count

    Args:
        Motifs ([string matrix]): [holds several DNA strings as kmers - motifs]

    Returns:
        [dict]: [all elements of count matrix divided by the number of rows in motifs]
    """
    ProfileArray = count(Motifs)
    MotifLength = len(Motifs)
    for letter, values in ProfileArray.items():
        new_vals = [v / MotifLength for v in values]
        ProfileArray[letter] = new_vals
    return ProfileArray


def consensus(Motifs):
    """[string formed from the most frequent nucleotide per row in Motif matrix]

    Dependancies:
        count

    Args:
        Motifs ([string matrix]): [holds several DNA strings as kmers - motifs]

    Returns:
        [string]: [most popular nucleotides in each column of motif matrix. If Motifs seen correctly from collection of upstream regions, consensus provides a candidate regulatory motif for these regions]
    """
    MotifLength = len(Motifs[0])
    Count = count(Motifs)
    Consensus = ""
    for j in range(MotifLength):
        MostPopular = 0  # Initialize the most popular nucleotide base as a reference
        FrequentSymbols = ""
        for symbol in "ACGT":
            if Count[symbol][j] > MostPopular:
                MostPopular = Count[symbol][j]
                FrequentSymbols = symbol
        Consensus += FrequentSymbols
    return Consensus


def score(Motifs):
    """[summing the number of symbols in the j-th column of Motifs that do not match the symbol in position j of the consensus string]

    Dependancies:
        consensus, count

    Args:
        Motifs ([string matrix]): [holds several DNA strings as kmers - motifs]

    Returns:
        [int]: [number of unpopular letters in motif matrix, minimizing this score results in the most conservative matrix]
    """
    Count = count(Motifs)
    Consensus = consensus(Motifs)
    Letters = {'A', 'C', 'T', 'G'}
    running_sum = 0
    for i, letter in enumerate(Consensus):
        UnpopularLetter = Letters - set(letter)
        for RemainingLetter in UnpopularLetter:
            running_sum += Count[RemainingLetter][i]
    return running_sum


def probability_kmer(text, profile):
    """[Probability of finding a chosen kmer given the profile matrix]

    Args:
        text ([string]): [string to be searched against]
        profile ([dict]): [contains the probability of finding each nucleotide]

    Returns:
        [int]: [multiplication of the probability of each nucleotide's position in text against the listed probability in profile]
    """
    p = 1
    k = len(text)
    for i in range(k):
        char = text[i]
        p *= profile[char][i]
    return p


def profile_most_probable_kmer(text, k, profile):
    """[ a kmer that was most likely to have been generated by profile among all kmers in text]

    Dependancies:
        probability_kmer

    Args:
        text ([string]): [string to be searched against]
        k ([int]): [determines length of kmer]
        profile ([dict]): [contains the probability of finding each nucleotide]

    Returns:
        [string]: [kmer that has the highest probability of being generated]
    """
    TextLength = len(text)
    CurrentProbability = 0
    x = text[1:k]
    for i in range(TextLength-k+1):
        Pattern = text[i:i+k]
        MostProbableKmer = probability_kmer(text, profile)
        if MostProbableKmer > CurrentProbability:
            CurrentProbability = MostProbableKmer
            x = Pattern
    return x


def entropy(nucleotide, probability):
    """[Measure of the uncertainty of a probability distribution]

    Args:
        nucleotide ([string]): [the 4 nucleotides ATGC]
        probability ([int]): [probability of each of the 4 nucleotides in a column]

    Returns
        [int]: [represents conservation of the column. lower entropy is better as it means probability distribution is most likely to occur]
    """
    ProbabilityDistribution = zip(nucleotide, probability)
    H = 0
    for j in ProbabilityDistribution:
        for i in j:
            H = H + i*(math.log(i, 2))

    return(-H)

# -------------------------------------------------------------------------


def count_with_pseudocounts(Motifs):
    """[Takes a list of strings Motifs as input and returns the count matrix of Motifs with pseudocounts as a dict of lists]

    Args:
        Motifs ([list]): [list of strings, motifs]

    Returns:
        [dict]: [count matrix of Motifs with pseudocounts as a dict of lists]
    """
    Count = {}
    MotifLength = len(Motifs[0])
    for symbol in "ACGT":
        Count[symbol] = []
        for j in range(MotifLength):
            Count[symbol].append(1)
    FullMotifLength = len(Motifs)
    for i in range(FullMotifLength):
        for j in range(MotifLength):
            symbol = Motifs[i][j]
            Count[symbol][j] += 1
    return Count


def profile_with_pseudocounts(Motifs):
    """[Takes a list of strings Motifs as input and returns the profile matrix of Motifs with pseudocount as a dict of lists]

    Args:
        Motifs ([list]): [list of strings, motifs]

    Returns:
        [dict]: [profile matrix of Motifs with pseudocount as a dict of lists]
    """
    #MotifLength = len(Motifs[0])
    Profile = {}
    Count = count_with_pseudocounts(Motifs)
    total = 0
    for symbol in "ACGT":
        total += Count[symbol][0]
        for k, v in Count.items():
            Profile[k] = [x/total for x in v]
    return Profile


def greedy_motif_with_pseudocounts(Dna, k, t):
    """[Generates each profile matrix with pseudocounts]

    Dependancies:
         score,consensus,count,Pr,profile_most_probable_kmer, profile_with_pseudocounts, count_with_pseudocounts

    Args:
        Dna ([string]): [reference sequence to be searched]
        k ([int]): [determines length of kmer]
        t ([int]): [total length parameter (range)]

    Returns:
        [list]: [A collection of strings BestMotifs resulting from running greedy_motif_search(Dna, k, t) with
                pseudocounts. If at any step you find more than one Profile-most probable k-mer in a given string,
                use the one occurring first.]
    """
    BestMotifs = []
    for i in range(t):
        BestMotifs.append(Dna[i][:k])
    DnaLengthInitial = len(Dna[0])
    for _ in range(DnaLengthInitial-k+1):
        Motifs = []
        Motifs.append(Dna[0][i:i+k])
        for j in range(1, t):
            P = profile_with_pseudocounts(Motifs[0:j])
            Motifs.append(profile_most_probable_kmer(Dna[j], k, P))
        if score(Motifs) < score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs


def motifs(profile, Dna):
    """[takes a profile Matrix profile corresponding to a list of strings Dna as input and returns a list of the profile most probable k-mers in each string from Dna]

    Dependancies:
        profile_most_probable_kmer

    Args:
        profile ([string]): [reference sequence to be searched]
        Dna ([string]): [profile Matrix profile corresponding to a list of strings]

    Returns:
        [type]: [description]
    """
    Motifs = []
    DnaLength = len(Dna)
    k = 4
    for i in range(DnaLength):
        motif = profile_most_probable_kmer(Dna[i], k, profile)
        Motifs.append(motif)
    return motifs


def random_motifs(Dna, k, t):
    """[choose a random kmer from each of t different strings Dna and returns a list of t strings which continuously iterates for as long as the score of the constructed motifs keep improving]

    Args:
        Dna ([string]): [reference sequence to be searched]
        k ([int]): [determines length of kmer]
        t ([int]): [total length parameter (range)]

    Returns:
        [list]: [lowest scoring motifs which would represent the most conservative ones.]
    """
    DnaLength = len(Dna)
    DnaLengthInitial = len(Dna[0])
    RandomMotif = []
    for i in range(DnaLength):
        RandomKmer = random.randint(0, DnaLengthInitial-k)
        RandomMotif.append(Dna[i][RandomKmer:RandomKmer+k])
    return RandomMotif


def random_motif_search(Dna, k, t):
    """[starts by generating a collection of random motifs using the random_motifs function which we set as the best scoring collection of motifs. It continuously runs until motif score stops improving.]

    Dependancies:
        random_motifs, profile_with_pseudocounts, Motifs, score

    Args:
        Dna ([string]): [reference sequence to be searched]
        k ([int]): [determines length of kmer]
        t ([int]): [total length parameter (range)]

    Returns:
        [list]: [best scoring motifs representing the most conservative ones from a RANDOM MOTIF SELECTION]
    """
    M = random_motifs(Dna, k, t)
    BestMotifs = M

    while True:
        Profile = profile_with_pseudocounts(M)
        M = motifs(Profile, Dna)
        if score(M) < score(BestMotifs):
            BestMotifs = M
        else:
            return BestMotifs


def repeated_random_motif_search(Dna, k, t):
    """[finds best scoring motif]

    Dependancies:
        uses randommotif, profile_with_pseudocounts,count_with_pseudocounts,score,consensus,count,motifs,Pr,random_motif_search

    Args:
        Dna ([string]): [reference sequence to be searched]
        k ([int]): [determines length of kmer]
        t ([int]): [total length parameter (range)]

    Returns:
        [list]: [The best scoring motif in Dna]
    """
    Bestscore = float('inf')
    BestMotifs = []
    for i in range(len(Dna)):
        Motifs = random_motif_search(Dna, k, t)
        Currscore = score(Motifs)
        if Currscore < Bestscore:
            Bestscore = Currscore
            BestMotifs = Motifs
    return BestMotifs


def normalize(Probabilities):
    """[rescale a collection of probabilities so that they sum to 1. It takes a dict Probabilities whose keys are kmers values are probabilities of these kmers. It then divides each value in Probabilities by the sum of all values in Probabilities,returning the resulting dict.]

    Args:
        Probabilities ([dict]): [keys are kmers and values of probabilities of these kmers to occur]

    Returns:
        [dict]: [original keys with values rescaled so they sum to 1]
    """
    SumKmerProbability = sum(Probabilities.values())
    for key in Probabilities.keys():
        Probabilities[key] /= SumKmerProbability
    return Probabilities


def weighted_die(Probabilities):
    """[takes a dict Probabilities whose keys are kmers and values are Prob of these Kmers]

    Args:
        Probabilities ([dict]): [keys are kmers and values of probabilities of these kmers to occur]

    Returns:
        [string]: [most probable kmer with respect to values in probabilities]
    """
    kmer = ''  # output variable
    num = random.uniform(0, 1)
    SumKmerProbability = 0
    for key in Probabilities.keys():
        SumKmerProbability += Probabilities[key]
        if num < SumKmerProbability:
            kmer = key
            break
    return kmer


def profile_generated_string(text, profile, k):
    """[returns a randomly generated kmer from text whose probabilities are generated from profile]

    Dependancies:
        normalize, weighted_die, profile_most_probable_kmer

    Args:
        Dna ([string]): [reference sequence to be searched]
        k ([int]): [determines length of kmer]
        t ([int]): [total length parameter (range)]

    Returns:
        [string]: [randomly generated kmer from text whose probabilities are generated from profile]
    """
    TextLength = len(text)
    probabilities = {}
    for i in range(TextLength-k+1):
        probabilities[text[i:i+k]] = probability_kmer(text[i:i+k], profile)
    probabilities = normalize(probabilities)
    return weighted_die(probabilities)


def gibbs_sampler(Dna, k, t, N):
    """[ discards a single kmer from the current set of motifs at each iteration and decides to either keep or replace one
# continuously to generate a suboptimal solution particularly for different search problems with elusive motifs (local optimum)]

    Dependancies:
        randommotifs, count_with_pseudocounts,profile_with_pseudocounts,profilegeneratingstring,normalize,weighteddie, pr,score,consensus,count

    Args:
        Dna ([string]): [reference sequence to be searched]
        k ([int]): [determines length of kmer]
        t ([int]): [total length parameter (range)]
        N ([int]): [iterator]

    Returns:
        [list]: [GibbsSampler(Dna, k, t, N)]
    """
    BestMotifs = []
    Motifs = random_motifs(Dna, k, t)
    BestMotifs = Motifs
    for _ in range(N):
        i = random.randint(0, t-1)
        NewMotif = []
        for k1 in range(t):
            if k1 != i:
                NewMotif.append(Motifs[k1])
        profile = profile_with_pseudocounts(NewMotif)
        motif_i = profile_generated_string(Dna[i], profile, k)
        Motifs[i] = motif_i
        if score(Motifs) < score(BestMotifs):
            BestMotifs = Motifs
    return BestMotifs

# ------------------------------------------------------------------------------------------------------


def list_to_string(mylist):
    """[ A simple function to convert a list of values to a string of values with no separators
]

    Args:
        s ([list]): [list of values]

    Returns:
        [string]: [joint values from list]
    """
    return ' '.join(str(word) for word in mylist)


def find_clumps(genome, k, L, t):
    """[ Returns all distinct k-mers forming (L, t)-clumps in Genome]

    Dependancies:
        pattern_count
    Args:
        genome ([string]): [genome / nucleotide sequence to be parsed]
        k ([int]): [length of k-mer / DnaA box]
        L ([int]): [length of ori]
        t ([int]): [occurrence expected in genome - clump expected to be found at least 't' times]
    """
    # k is len of k-mer/DnaA box, L is length of genome, t is occurence
    Count = {}
    for i in range(L):
        pattern = genome[i:i+k]
        if (pattern_count(genome, pattern) == t):
            Count[pattern] = pattern_count(genome, pattern)
    print(" ".join(Count.keys()))
    return Count


def permute_motif_once(motif, alphabet={"A", "C", "G", "T"}):
    """
    Gets all strings within hamming distance 1 of motif and returns it as a
    list.
    """
    #online solution
    return list(set(itertools.chain.from_iterable([[
        motif[:pos] + nucleotide + motif[pos + 1:] for
        nucleotide in alphabet] for
        pos in range(len(motif))])))


def permute_motif_distance_times(motif, d):
    WorkingSet = {motif}
    for _ in range(d):
        WorkingSet = set(itertools.chain.from_iterable(map(permute_motif_once, WorkingSet)))
    return list(WorkingSet)


def freq_words_mismatch(Genome, k, d):
    """[A most frequent k-mer with up to d mismatches in Text is
        simply a string Pattern maximizing Countd(Text, Pattern) among all k-mersary]

    Dependancies:
        permute_motif_once, permute_motif_distance_times

    Args:
        Genome ([string]): [string to be parsed]
        k ([int]): [determines length of kmer]
        d ([int]): [mismatch allowance]

    Returns:
        [list]: [most frequent kmers]
    """
    ApproxFreqWords = []
    Freqs = defaultdict(lambda: 0)
    # all existent kmers with d mismatches of current kmer in genome
    for index in range(len(Genome) - k + 1):
        CurrentKmerAndNeighbor = permute_motif_distance_times(Genome[index: index + k], d)
        for kmer in CurrentKmerAndNeighbor:
            Freqs[kmer] += 1

    for kmer in Freqs:
        if Freqs[kmer] == max(Freqs.values()):
            ApproxFreqWords.append(kmer)
    return ApproxFreqWords


def pattern_matching_with_mismatch(text, pat, d):
    Count = 0
    for i in range(0, len(text)):
        p = text[i:i+len(pat)]
        if len(p) != len(pat):
            break
        if hamming_distance(p, pat) <= d:
            Count = Count+1
    return Count


def pattern_to_number(pattern):
    if len(pattern) == 0:
        return
    SymbolToNumber = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    if len(pattern) == 1:
        return SymbolToNumber[pattern]
    PatternLength = len(pattern)
    symbol = pattern[PatternLength-1]
    prefix = pattern[:PatternLength-1]
    return (4*pattern_to_number(prefix)+SymbolToNumber[symbol])


def number_to_pattern(index, k):
    NumberToSymbol = {0: 'A', 1: 'C', 2: 'G', 3: 'T'}
    if k == 1:
        return NumberToSymbol[index]
    prefix_index = index//4
    r = index % 4
    symbol = NumberToSymbol[r]
    return number_to_pattern(prefix_index, k-1)+symbol


def mismatches_and_reverse_compliment(text, k, d):
    """[account for both mismatches and reverse complements.
        Recall that Patternrc refers to the reverse complement of Pattern.]

    Dependancies:
        pattern_to_number,number_to_pattern,pattern_matching,hamming_distance,reverse_compliment


    Args:
        text ([string]): [string to be parsed]
        k ([int]): [determines length of kmer]
        d ([int]): [mistmatch allowance]

    Returns:
        [dict]: [performs pattern matching accounting for both reverse compliments of regular and mismatches]
    """
    FrequencyArray = {}
    RevComp = reverse_compliment(text)
    for i in range(0, 4**k):
        FrequencyArray[i] = 0
    for i in FrequencyArray:
        Count, RevCount = 0, 0
        Count = pattern_matching_with_mismatch(text, number_to_pattern(i, k), d)
        RevCount = pattern_matching_with_mismatch(RevComp, number_to_pattern(i, k), d)
        FrequencyArray[i] = Count+RevCount
    return FrequencyArray


def neighbors(Pattern, d):
    """[Our idea for generating neighbors(Pattern, d) is as follows. If we remove the first symbol of Pattern
        then we will obtain a (k − 1)-mer sequence denoted SuffixNeighbors. Find all possible combinations for each base and each SuffixNeighbor
        k-neighbors of any k-mer is an easy way of generating all kmers.]

    Args:
        Pattern ([string]): [string to be parsed]
        d ([int]): [mismatch allowance]

    Returns:
        [list]: [all suffixes in d-neighborhood]
    """
    if d == 0:
        return Pattern
    if len(Pattern) == 1:
        return {"A", "C", "G", "T"}
    Neighborhood = []
    Suffixneighbors = neighbors(Pattern[1:], d)
    for Text in Suffixneighbors:
        if hamming_distance(Pattern[1:], Text) < d:
            for x in {"A", "C", "G", "T"}:
                Neighborhood.append(x + Text)
        else:
            Neighborhood.append(Pattern[0] + Text)
    return Neighborhood

# ---------------------------------------------------------------------------------------


def suffix(Pattern):
    """
    return every symbol in pattern except the first
    """
    if len(Pattern) == 1:
        return ""
    Sufx = Pattern[1:]
    return Sufx


def first_symbol(Pattern):
    """
    return first symbol of pattern
    """
    x = Pattern[0]
    return x


def motif_enumeration(Dna, k, d):
    """[A kmer is a k,d motif if it appears in every string
       from Dna with at most d mismatches]

    Dependancies:
        neighbours,suffix,first_symbol,hamming_distance

    Args:
        Dna ([string]): [space separated string sequences of nucleotides]
        k ([int]): [determines length of kmer]
        d ([int]): [mismatch allowance]

    Returns:
        [string]: [Returns all (k,d)-motifs in Dna]
    """
    Patterns = set()
    DnaLength = len(Dna)
    AllKmers = []
    for j in range(DnaLength):
        a = Dna[j]
        kmers = []
        DnaLength_1 = len(a)
        for i in range(DnaLength_1 - k + 1):
            kmers.append(a[i:i+k])
        Neighbors = []
        for i in range(len(kmers)):
            l = neighbors(kmers[i], d)
            for val in l:
                Neighbors.append(val)
        AllKmers.append(Neighbors)
    x1 = set(AllKmers[0])
    x2 = set(AllKmers[1])
    Patterns = x1 and x2
    for y in range(2, len(AllKmers)):
        Patterns = Patterns and set(AllKmers[y])
    Patterns = list(Patterns)
    string = ""
    for i in Patterns:
        string = string + i + " "
    return string


def median_string(Dna, k):
    """[a fast algorithm for generating Motifs(Pattern,Dna), a collection of Motifs(Pattern,Dna) as a collection
        of kmers that minimize d(Pattern,Motifs) where d is the hamming distance]
        **NB: fails as long as a single sequence does not have the transcription factor binding sight.
        Runtime: len(dna) * (k+ k**d) * len(dna) * k

    Dependancies
        neighbors, hamming_distance, suffix

    Args:
        Dna ([string]): [space separated string sequences of nucleotides]
        Pattern ([string]): [pattern to search for in Dna string]
        k ([int]): [determines length of kmer]

    Returns
        [string]: [kmer pattern minimizing d(Pattern,Dna) among all possible choices of kmer]
    """

    def get_distance(Pattern, Text):
        TextLength = len(Text)
        PatternLength = len(Pattern)
        min_distance = hamming_distance(Text[:PatternLength], Pattern)
        for i in range(TextLength - PatternLength + 1):
            distance = hamming_distance(Text[i:i + PatternLength], Pattern)
            if distance < min_distance:
                min_distance = distance
        return min_distance

    def get_total_distance(Pattern, Dna):
        TotalDistance = 0
        for text in Dna:
            Distance = get_distance(Pattern, text)
            TotalDistance += Distance
        return TotalDistance

    min_pattern = first_symbol(Dna)
    MinTotalDistance = get_total_distance(min_pattern, Dna)
    for pattern in suffix(Dna):
        TotalDistance = get_total_distance(pattern, Dna)
        if TotalDistance < MinTotalDistance:
            min_pattern = pattern
            MinTotalDistance = TotalDistance

    return min_pattern


def distance_between_pattern_and_string(Pattern, Dna):
    """[the sum of distances between Pattern and each string in Dna = {Dna1, ..., Dnat}]

    Dependancies:
        hamming_distance

    Args:
        Pattern ([string]): [k-mer pattern reference to be searched for in Dna]
        Dna ([string]): [space separated string sequences of nucleotides]

    Returns:
        [int]: [the distance between Pattern and Dna - score]
    """
    PatternLength = len(Pattern)
    d = 0
    for text in Dna:
        d_temp = float('Inf')
        for i in range(len(text) - PatternLength + 1):
            if d_temp > hamming_distance(Pattern, text[i:i+PatternLength]):
                d_temp = hamming_distance(Pattern, text[i:i+PatternLength])
        d += d_temp
    return d


def profile_most_probable_kmer_noPR(text, k, profile):
    """[a kmer that was most likely to have been generated by profile among all kmers in text]

    Dependancies:
        probability_kmer

    Args:
        text ([string]): [string to be searched against]
        k ([int]): [determines length of kmer]
        profile ([dict]): [contains the probability of finding each nucleotide]

    Returns:
        [string]: [kmer that has the highest probability of being generated]
    """
    Probability = []
    for i in range(len(text)-k+1):
        compute = 1
        for j in range(k):
            compute = compute*(profile[text[i+j]][j])
        Probability.append(compute)
    idx = Probability.index(max(Probability))
    return text[idx:idx+k]


def greedy_motif_search(Dna, k, t):
    """[selects the most attractive candidate from the profile using profile_most_probable_kmer]

    Dependancies:
        score,profile,profilemostprobablekmer

    Args:
        Dna ([string]): [reference sequence to be searched]
        k ([int]): [determines length of kmer]
        t ([int]): [total length parameter (range)]

    Returns:
        [list]: [A collection of strings BestMotifs]
    """
    BestMotifs = [string[:k]for string in Dna]
    for j in range(len(Dna[0])-k+1):
        motifs = [Dna[0][j:j+k]]
        for i in range(1, t):
            motifs += [profile_most_probable_kmer_noPR(Dna[i], k, profile(motifs))]
        if score(motifs) < score(BestMotifs):
            BestMotifs = motifs
    return BestMotifs

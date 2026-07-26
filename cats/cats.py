"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> choose(ps, s, 0)
    'hi'
    >>> choose(ps, s, 1)
    'fine'
    >>> choose(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    taget_para_list=[x for x in paragraphs if select(x)]
    if k>=len(taget_para_list):
        return ""
    return taget_para_list[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def contains_words_in_topic(paragraph):
        paragraph=lower(paragraph)
        paragraph=remove_punctuation(paragraph)
        list_of_paragraph=split(paragraph)
        for i in topic:
            for j in list_of_paragraph:
                if i==j:
                    return True
        return False
    return contains_words_in_topic
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    Arguments:
        typed: a string that may contain typos
        reference: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    count=0
    if len(typed_words)==0 and len(reference_words)!=0:
        return 0.0
    if len(typed_words)==0 and len(reference_words)==0:
        return 100.0
    min_len=min(len(typed_words),len(reference_words))
    i=0
    while i<=min_len-1:
        if typed_words[i]==reference_words[i]:
           count+=1
        i+=1
    return (count/len(typed_words))*100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return (len(typed)/5)/(elapsed/60)
    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing reference words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    ideal_obj=word_list[0]
    diff=diff_function(typed_word,word_list[0],limit)
    for i in word_list:
        if typed_word==i:
            return typed_word
        if diff_function(typed_word,i,limit)<diff:
            diff=diff_function(typed_word,i,limit)
            ideal_obj=i
    if diff>limit:
        return typed_word
    return ideal_obj
    # END PROBLEM 5


def sphinx_swaps(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths and returns the result.

    Arguments:
        start: a starting word
        goal: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> sphinx_swaps("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> sphinx_swaps("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> sphinx_swaps("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> sphinx_swaps("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> sphinx_swaps("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    def count_diff(start,goal,i,change_num):
        if change_num>limit:
            return limit+1
        if i>=min(len(start),len(goal)):
            return 0
        return count_diff(start,goal,i+1,change_num+int(start[i]!=goal[i]))+int(start[i]!=goal[i])
    count=count_diff(start,goal,0,0)
    if count==limit+1:
        return count
    count+=abs(len(start)-len(goal))
    return count#避免深度递归
    # END PROBLEM 6


def minimum_mewtations(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.

    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    if start==goal:
        return 0
    if limit<0:
        return limit+1
    if len(start)==0 or len(goal)==0:
        return max(len(start),len(goal))
    if abs(len(start)-len(goal))>limit:
        return limit+1
    else:
        add =1+minimum_mewtations(start,goal[1:],limit-1) if start[0]!=goal[0] else minimum_mewtations(start[1:],goal[1:],limit)
        remove=1+minimum_mewtations(start[1:],goal,limit-1) if start[0]!=goal[0] else minimum_mewtations(start[1:],goal[1:],limit)
        substitute = 1+minimum_mewtations(start[1:],goal[1:],limit-1) if start[0]!=goal[0] else minimum_mewtations(start[1:],goal[1:],limit)
        return min(add,remove,substitute)



def final_diff(start, goal, limit):
    """A diff function that takes in a string START, a string GOAL, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(sofar, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        sofar: a list of the words input so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> sofar = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(sofar, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    len_of_prompt=len(prompt)
    match_num=0
    i=0
    while i<len(sofar):
        if sofar[i]!=prompt[i]:
            break
        match_num+=1
        i+=1
    ratio=match_num/len_of_prompt
    upload({'id':user_id,'progress':ratio})
    return ratio
    # END PROBLEM 8


def time_per_word(words, times_per_player):
    """Given timing data, return a match dictionary, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> match["words"]
    ['collar', 'plush', 'blush', 'repute']
    >>> match["times"]
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    times=[]
    i=0
    while i<len(times_per_player):
        times_of_player_i=times_of_eachplayer(times_per_player,i)
        times+=[times_of_player_i]
        i+=1
    return match(words,times)
def times_of_eachplayer(times_per_player,user_id):
    times_of_player=[]
    i=0
    while i<len(times_per_player[user_id])-1:
        times_of_player+=[times_per_player[user_id][i+1]-times_per_player[user_id][i]]
        i+=1
    return times_of_player

def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match dictionary as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(match["times"]))
    word_indices = range(len(match["words"]))
    final_result=[]
    i=0
    while i<len(player_indices):
        final_result+=[[]]
        i+=1
    j=0
    while j<len(word_indices):
        start_time=time(match,0,j)
        tag=0
        k=1
        while k<len(player_indices):
            if time(match,k,j)<start_time:
                start_time=time(match,k,j)
                tag=k
            k+=1
        final_result[tag]+=[word_at(match,j)]
        j+=1
    return final_result
def match(words, times):
    """A dictionary containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def word_at(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(match["words"]), "word_index out of range of words"
    return match["words"][word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(match["words"]), "word_index out of range of words"
    assert player_num < len(match["times"]), "player_num out of range of players"
    return match["times"][player_num][word_index]


def match_string(match):
    """A helper function that takes in a match dictionary and returns a string representation of it"""
    return f"match({match['words']}, {match['times']})"


enable_multiplayer = True  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)


def tree(label,branches=[]):
    if not branches:
        return [label]
    else:
        return ['(',label]+sum(branches,start=[])+[')']

def label(tree):
    if len(tree)==1:
        return tree[0]
    else:
        assert tree[0]=='(', tree
        return tree[1]

def branches(tree):
    if len(tree)==1:
        return []
    opened=1
    assert tree[0]=='(',tree
    current_branch=[]
    all_branches=[]
    for tokens in tree[2:]:
        current_branch.append(tokens)
        if tokens =='(':
            opened+=1
        elif tokens==')':
            opened-=1
        if opened==1:
            all_branches.append(current_branch)
            current_branch=[]
    assert opened==0
    return all_branches
def is_leaf(tree):
    return not branches(tree)

def leaves(t):
    if is_leaf(t):
        return [label(t)]
    else:
        return sum([leaves(b) for b in branches(t)],[])
example=tree('ROOT',
             [tree('FRAG',
                   [tree('NP',
                         [tree('DT',[tree('a')]),
                          tree('JJ',[tree('little')]),
                          tree('NN',[tree('bug')])]),
                    tree('.',[tree('.')])])])
from string import punctuation
contractions=["n't","'s","'re","'ve"]
def words(t):
    s=''
    for w in leaves(t):
        no_space=(w in punctuation and w!='$') or w in contractions
        if not s or no_space:
            s=s+w
        else:
            s=s+' '+w
    return s
def replace(t,s,w):
    if label(t)==s:
        return tree(s,[tree(w)])
    else:
        return tree(label(t),[replace(b,s,w) for b in branches(t)])
def parse_word_files(SE,dir_vk,dir_wp,print_crucial,print_debug):

    word_set = []
    word_pair_set = []
    v_keyword_set = {}

    with open(dir_vk,'r') as f:
        for line in f.readlines():
            if(line.strip() and line[0]!='#'):
                words = line.strip().split()
                v_keyword_set[words[0]]=[]
                for w in words:
                    word_set.append(w)
                    v_keyword_set[words[0]].append(w)

    with open(dir_wp,'r') as f:
        newwordpair=True
        lastw = ""
        for line in f.readlines():
            if(line.strip() and line[0]!='#'):
                words = line.strip().split()
                word_set.append(words[0])
                word_set.append(words[1])
                word_pair_set.append((words[0],words[1]))

    isFound = False
    
    for w in word_set:
        if not SE.ifSingleWord(w):
            if(print_crucial):
                print(w,"is not a single token.")
            isFound = True

    if isFound == False:
        if(print_crucial):
            print("All word pairs are single token.")
    else:
        assert()
        
    if(print_debug):
        print()
        print(word_set)
        print()
        print(word_pair_set)
        print()
        print(v_keyword_set)
        
    return word_set, word_pair_set, v_keyword_set
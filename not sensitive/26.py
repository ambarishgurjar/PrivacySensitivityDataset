    def encode(self, x: str) -> str:

        assert not x.startswith(' ')
        assert not x.endswith(' ')
        if INSERT_OR_REPLACE == 1:
            temp = []   
            word = ''                     
            for ch in x:
                if ch == ' ':
                    if word:
                        temp.append(word)
                        word = ''
                    temp.append('<s>')
                else:
                    word += ch
            if word:
                temp.append(word)

            for i in range(len(temp)):
                if temp[i] != '<s>':
                    temp[i] = ' '.join(map(str, self.bpe.encode(temp[i])))
                        
            return ' '.join(temp)
        elif INSERT_OR_REPLACE == 0:
            temp = []   
            word = ''                     
            for ch in x:
                if ch == ' ':
                    if word:
                        temp.append(word)
                        word = ' '
                    temp.append('<s>')
                else:
                    word += ch
            if word:
                temp.append(word)

            for i in range(len(temp)):
                if temp[i] != '<s>':
                    temp[i] = ' '.join(map(str, self.bpe.encode(temp[i])))
            
            return ' '.join(temp)    
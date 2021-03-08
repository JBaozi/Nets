import socket
import random

class C_Ham:
    def __init__(self, length_w = 85, length_h = 92):
        self.length_word = length_w
        self.length_code = length_h
        self.w_without_m = 0
        self.w_with_m = 0
        self.message = ''
    
    def binary(self, letter):
        return bin(letter)[2:].zfill(8)
    
    def toBinary(self, text):
        text = text.encode('UTF-8')
        subtext = ''
        for i in text: subtext += self.binary(i)
        return subtext;
    
    def toChar(self, num):
        return int(num, 2);
    
    def toText(self, binary):
        text = []
        for i in range(0, len(binary), 8):
            text.append(self.toChar(binary[i:i+8]))
        return bytes(text).decode('UTF-8')
    
    def extra(self, w):
        i = 0;
        while(2 ** i < len(w)):
            w.insert(2 ** i - 1, 0)
            i += 1
        return w
    
    def mCode(self, cur, m = 0):
        k = 1
        while k < len(cur):
            for i in range(k - 1, len(cur), k*2):
                for j in range(i, min(i+k, len(cur)), 1):
                    cur[k-1] ^= cur[j]
            k *= 2
        
        if m == 1:
            k = random.randrange(len(cur))
            cur[k] ^= 1
        
        if m == 2:
            for i in range(len(cur)):
                if (random.randrange(10) == 0):
                    cur[i] ^= 1
        
        return cur
    
    def coder(self, s, m = 0):
        j = [int(s[i]) for i in range(len(s))]
        arr = []
        for k in range(0, len(j), self.length_word):            
            cur = j[k : k + self.length_word]
            cur = self.extra(cur)
            cur = self.mCode(cur, m)
            arr += cur
        f_arr = ''
        for i in arr:
            f_arr += str(i)
        return f_arr
    
    def decoder(self, s):
        j = [int(s[i]) for i in range(len(s))]
        h = j.copy()
        res = ''
        
        for k in range(0, len(j), self.length_code):
            cur = j[k : k + self.length_code]
            count_m = 0
            while True:
                ch = h[k : k + self.length_code]
                cp = 0
                while 2 ** cp < len(cur):
                    cur[2 ** cp - 1] = 0
                    cp += 1
                cur = self.mCode(cur)
                s_mist = 0
                cp = 0
                while 2 ** cp < len(cur):
                    if cur[2 ** cp - 1] != ch[2 ** cp - 1]:
                        s_mist += 2 ** cp
                    cp += 1
                
                cp = 0
                if s_mist == 0:
                    break
                
                flag = True
                while 2 ** cp < len(cur):                
                    if s_mist == 2 ** cp:
                        flag = False
                        break
                    cp += 1
                
                if flag == False:
                    break
                
                count_m += 1
                if (s_mist >= len(cur)):
                    break
                
                cur[s_mist - 1] ^= 1
                
            if count_m > 0:
                self.w_with_m += 1
            else:
                self.w_without_m += 1
                
            print('Кол-во ошибок - ', count_m)
            self.message += 'Кол-во ошибок - ' + str(count_m) + '\n'
            cursumbit = 0
            for i in range(len(cur)):
                if (i == cursumbit):
                    cursumbit = (cursumbit + 1) * 2 - 1
                else:
                    res += str(cur[i])
        self.message += 'Кол-во слов БЕЗ ошибки - ' + str(self.w_without_m) + '\n'
        self.message += 'Кол-во слов С ошибкой - ' + str(self.w_with_m) + '\n'
        print('Кол-во слов БЕЗ ошибки - ', self.w_without_m)
        print('Кол-во слов С ошибкой - ', self.w_with_m)
        return res



s1 = socket.socket()
s1.bind(('', 5000))
s1.listen(1)
conn, addr = s1.accept()

print ('Соединение:', addr)

cur = ''
while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    cur += data
    
ham = C_Ham(85, 92)   
print(cur)
cur = ham.decoder(cur)
cur = ham.toText(cur)
conn.close()


print(cur)
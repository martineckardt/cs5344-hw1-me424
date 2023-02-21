from wonderwords import RandomSentence
from signature import MTSignature

s = RandomSentence()

S1 = MTSignature(10, 2)
S1.KeyGen(2023)
signature = S1.Sign("This is a test message")

print(signature)
forged_signature = ""

while signature != forged_signature:
    sentence = s.bare_bone_sentence()
    forged_signature = S1.Sign(sentence)

print(sentence)
print(forged_signature)


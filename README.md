# shuparts
It's a flashcard tool for testing musical piece memorization at the command line.

Feed shuparts.py a list of part names, like

    shuparts.py A B C D

or give it a file from MuseScore Studio, like 

    shuparts.py 3-Gymnopedies.Erik-Satie.mscz

shuparts parses `mscz` files for rehearsal marks, tempo text, titles, and
section breaks.  If shuparts finds multiple sections, it'll ask the user to
type the number of the section to practice, or you can just hit enter to
practice parts across all the sections.

shuparts shuffles all the parts selected for practice and presents them one at
a time.  Hit enter to proceed to the next one.  Once the list is exhausted,
shuparts exits.

# Examples

## shuparts.py example execution

    $ shuparts.py 3-Gymnopedies.Erik-Satie.mscz
    Available parts:

    1: Gymnopédie no. 1 (♩ = 69 Lent et douloureux)
      A1 A'1 B1 C1 D1 A2 A'2 B2 C2 D2'

    2: Gymnopédie no. 2 (♩ = 69 Lent et triste)
      A1[Basis] A1.2[Basis].2 B1[Statement] B'1[Re-statement] A1.3[Basis]2 C1[Concern] D1[Concern].2 E1[Minor-basis] F1[Minor-basis].2 C2'[Concern]2 D2'[Concern]2.2 E2'[Minor-basis]2 A3[Basis]3 B3'[Statement]2 B'3'[Re-statement]2 A3.2[Basis]4 C3[Concern]3 D3''[Concern]3.2 E3''[Minor-basis]3 F3[Minor-basis]3.2 F'3[Minor-basis]3.3

    3: Gymnopédie no. 3 (♩ = 69 Lent et grave)
      A1 B1 C1 D1 E1 A2' B2 C2' D2 E2 A3' F


    Enter section # to choose from, or hit enter to practice all: 2
    Selecting from parts:
      A1[Basis] A1.2[Basis].2 B1[Statement] B'1[Re-statement] A1.3[Basis]2 C1[Concern] D1[Concern].2 E1[Minor-basis] F1[Minor-basis].2 C2'[Concern]2 D2'[Concern]2.2 E2'[Minor-basis]2 A3[Basis]3 B3'[Statement]2 B'3'[Re-statement]2 A3.2[Basis]4 C3[Concern]3 D3''[Concern]3.2 E3''[Minor-basis]3 F3[Minor-basis]3.2 F'3[Minor-basis]3.3

    <hit enter to pick the next part, or ctrl-C to exit early>
    -->  E2'[Minor-basis]2    <--
    -->  F3[Minor-basis]3.2   <--
    -->  A1.2[Basis].2        <--
    -->  F1[Minor-basis].2    <--
    -->  E3''[Minor-basis]3   <--
    -->  C1[Concern]          <--^C
    <exiting early due to ctrl-C>
    $

## MuseScore Studio music snippet from page 5 of 3-Gymnopedies.Erik-Satie.mscz

![Snippet from the score of Satie's Gymnopedies](assets/example_score.png)

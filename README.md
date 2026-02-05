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

### shuparts.py example execution

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

### MuseScore Studio music snippet

This is from page 5 of 3-Gymnopedies.Erik-Satie.mscz used in the above command line execution example:

![Snippet from the score of Satie's Gymnopedies](assets/example_score.png)

# MuseScore Studio .mscz file details

- shuparts only looks at the topmost staff, so only add markings there&mdash;marks in the lower staves are ignored.
- Rehearsal marks are the fundamental practice unit.  They can be inserted easily be selecting a note or rest in the top staff and hitting `ctrl-m`.  Space them at comfortable intervals for flashcard practice.
- Staff text of the format `[description]` (words enclosed in square brackets) are pulled from the same measure containing a Rehearsal mark and are associated with that mark.  See the A1 mark with the `[basis]` description in the score snippet above.  Use this to provide mnemonics to the parts you want to practice.  Add staff text by selecting a note or rest in the top staff and hitting `ctrl-t`.
- If a Rehearsal mark doesn't have a `[description]` staff text in the same measure, shuparts will apply the description from the closest mark that does.  In this case, the description will be suffixed with a `.` and the number corresponding to the number of marks this is past the last one with a `[description]`.  For example, see the `A1.2[Basis].2` part name in the shuparts.py execution example above.
- If a `[description]` with the same text occurs again with a later Rehearsal mark, the number of times this has happened is suffixed to the `[description]` in the part name, prior to any `.N` from the above point.  For example, see the `F3[Minor-basis]3.2` part name in the exection above.  This means the description `[Minor-basis]` has been applied to 2 prior marks, and the `F3` mark does not have a `[description]`, but the prior mark did.
- Sections are separated by Section breaks.  Insert a section break in MuseScore Studio by selecting the measure you want the break to occur after and selecting the *Section break* icon from the *Layout* palette - it looks like `]]`.
- To name a section, it needs a Title text.  Insert one by selecting the first measure of the section (the one right after the section break), and using the menu item *Add -> Frames -> Insert vertical frame*.  Then select the frame and use *Add -> Text -> Title*.
- To add a performance tempo description (e.g. shown as `♩ = 69 Lent et triste` in the example), select the first measure of the section and choose a tempo marking from the *Tempo* palette.  If you want to change the tempor or add additional expression guidance text to the tempo marking, select the tempo marking you added to the score and click into it again to set the insert cursor so you can type. 

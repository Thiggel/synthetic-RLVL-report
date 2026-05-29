# OOD Generation Examples

Logic root: `/home/atuin/c107fa/c107fa12/synthetic-RLVL/lm_eval_results/ood_large_2026-05-25/sft_hfsa_depth_scaling_logic_train1to25_10k_seed3407`
NL root: `/home/atuin/c107fa/c107fa12/synthetic-RLVL/lm_eval_results/ood_large_2026-05-25/sft_hfsa_depth_scaling_nl_exact_train1to25_10k_seed3407`

Examples are paired by `doc_id`. GSM8K metric is exact match after tag/numeric extraction; HotpotQA, 2WikiMultiHopQA, and MuSiQue metric shown here is token F1 after strict answer-tag extraction.

## gsm8k

### doc_id 386

Question: To have the car for the weekend, Wilson's report card needs to show that he received 80 or higher in his math class. His math grade is calculated by the average of 5 test scores. On those tests, he received: 65, 94, 81, 86 and 74. What is his current math grade?

Gold: 80

Logic explicit extraction: `80`; EM=1.000; tag_found=1.000

Logic generation:

```text
<formal>
<constants>
<constants>
Wilson = Wilson
</constants>
<predicates>
<predicates>
Ax: x is the average of 5 test scores
Bx: x is 80 or higher
Cx: x is 65
Dx: x is 94
Ex: x is 81
Fx: x is 86
Gx: x is 74
Hx: x is 5
Ix: x is 80
Jx: x is 81
Kx: x is 86
Lx: x is 74
Mx: x is 65
Nx: x is 94
Ox: x is 5
Px: x is 80
Qx: x is 81
Rx: x is 86
Sx: x is 74
Tx: x is 65
Ux: x is 94
Vx: x is 5
Wx: x is 80
Xx: x is 81
Yx: x is 86
Zx: x is 74
</predicates>
<premises>
Ax
Bx
Cx
Dx
Ex
Fx
Gx
Hx
Ix
Jx
Kx
Lx
Mx
Nx
Ox
Px
Qx
Rx
Sx
Zx
</premises>
<proof>
Ax ; R
Bx ; R
</proof>
<conclusion>
Bx
</conclusion>
</formal>
<answer>
80
```

NL explicit extraction: `74`; EM=0.000; tag_found=1.000

NL generation:

```text
<think>
<premises>
a = 65
b = 94
c = 81
d = 86
e = 74
</premises>
<proof>
a = 65
b = 94
c = 81
d =  is not a variable
e = 74
</proof>
<conclusion>
Wilson's math grade is 74.
</conclusion>
</think>
<answer>
74
```

### doc_id 3

Question: James decides to run 3 sprints 3 times a week. He runs 60 meters each sprint. How many total meters does he run a week?

Gold: 540

Logic explicit extraction: ``; EM=0.000; tag_found=0.000

Logic generation:

```text
<formal>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<consta
...[truncated]...
ants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants
```

NL explicit extraction: `540`; EM=1.000; tag_found=1.000

NL generation:

```text
<think>
<premises>
a = 3
b = 3
c = 60
</premises>
<proof>
a = 3
b = 3
c = 60
total = a * b * c
total = 3 * 3 * 60
total = 540
</proof>
<conclusion>
James runs a total of 540 meters a week.
</conclusion>
</think>
<answer>
540
```

### doc_id 0

Question: Janet’s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?

Gold: 18

Logic explicit extraction: ``; EM=0.000; tag_found=0.000

Logic generation:

```text
<formal>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<consta
...[truncated]...
ants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants>
<constants
```

NL explicit extraction: `2`; EM=0.000; tag_found=1.000

NL generation:

```text
<think>
<premises>
a = 16
b = 3
c = 4
d = 2
</premises>
<proof>
a = 16
b = 3
c = 4
d = 2
</proof>
<conclusion>
Janet makes $2 every day at the farmers' market.
</conclusion>
</think>
<answer>
2
```

### doc_id 1

Question: A robe takes 2 bolts of blue fiber and half that much white fiber. How many bolts in total does it take?

Gold: 3

Logic explicit extraction: `Qa`; EM=0.000; tag_found=1.000

Logic generation:

```text
<formal>
<constants>
a = 2
b = 1
</constants>
<predicates>
Ax: x is white
Bx: x is blue
Cx: x is a robe
Dx: x is a bolt
Ex: x is half
Fx: x is a fiber
Gx: x is a total
Hx: x is a number
Ix: x is a sum
Jx: x is a product
Kx: x is a difference
Lx: x is a quotient
Mx: x is a variable
Nx: x is a constant
Ox: x is a coefficient
Px: x is a value
Qx: x is a quantity
Rx: x is a ratio
Sx: x is a term
Tx: x is a unit
Ux: x is a measure
Vx: x is a factor
Wx: x is a part
Xx: x is a component
Yx: x is a component
Zx: x is a component
</predicates>
<premises>
Ba
Eb
Ca
Da
Ia
Ja
Ka
La
Ma
Na
Oa
Pa
Qa
Ra
Sa
Ta
Ua
Va
Wa
Xa
Ya
Za
</premises>
<proof>
Ba ; R
Eb ; R
Ca ; ->E
Da ; ->E
Ia ; ->E
Ja ; ->E
Ka ; ->E
La ; ->E
Ma ; ->E
Na ; ->E
Oa ; ->E
Pa ; ->E
Qa ; ->E
Ra ; ->E
Sa ; ->E
Ta ; ->E
Ua ; ->E
Va ; ->E
Wa ; ->E
Xa ; ->E
Ya ; ->E
Za ; ->E
</proof>
<conclusion>
Qa
</conclusion>
</formal>
<answer>
Qa
```

NL explicit extraction: `2 bolts of blue fiber and half that much white fiber.`; EM=0.000; tag_found=1.000

NL generation:

```text
<think>
<premises>
a takes 2 bolts of blue fiber and half that much white fiber.
</premises>
<proof>
a takes 2 bolts of blue fiber and half that much white fiber.
</proof>
<conclusion>
a takes 2 bolts of blue fiber and half that much white fiber.
</conclusion>
</think>
<answer>
2 bolts of blue fiber and half that much white fiber.
```

## hotpotqa

### doc_id 9

Question: Question: For which band, was the female member of Fitz and The Tantrums, the front woman for ten years ?

Gold: The Rebirth

Logic explicit extraction: `The Rebirth`; F1=1.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
The Rebirth
```

NL explicit extraction: ``; F1=0.000; tag_found=0.000

NL generation:

```text
<think>
<premises>
aikido
aikido is a Japanese martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a marti
...[truncated]...
o is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is a martial art
aikido is
```

### doc_id 72

Question: Question: What was the Roud Folk Song Index of the nursery rhyme inspiring What Are Little Girls Made Of?

Gold: 821

Logic explicit extraction: `16150`; F1=0.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
16150
```

NL explicit extraction: `821`; F1=1.000; tag_found=1.000

NL generation:

```text
<answer>
821
```

### doc_id 2

Question: Question: Prior to playing for Michigan State, Keith Nichol played football for a school located in what city?

Gold: Norman

Logic explicit extraction: `Lowell`; F1=0.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Lowell
```

NL explicit extraction: ``; F1=0.000; tag_found=0.000

NL generation:

```text
<think>
<premises>
aikman was a quarterback for the Dallas Cowboys.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XXVII.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XXVIII.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XXIX.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XXX.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XXXI.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XXXII.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XXXIII.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl X
...[truncated]...
an was the starting quarterback for the Dallas Cowboys in Super Bowl XLVII.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XLVIII.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl XLIX.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl L.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl LI.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl LII.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl LIII.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl LIV.
aikman was the starting quarterback for the Dallas Cowboys in Super Bowl LV.
```

### doc_id 0

Question: Question: Which case was brought to court first Miller v. California or Gates v. Collier ?

Gold: Miller v. California

Logic explicit extraction: `Gates v. Collier`; F1=0.333; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Gates v. Collier
```

NL explicit extraction: `Gates v. Collier`; F1=0.333; tag_found=1.000

NL generation:

```text
<answer>
Gates v. Collier
```

## 2wikimqa

### doc_id 3

Question: Question: Do both Beauty And The Bad Man and Wild Child (Film) films have the directors from the same country?

Gold: no

Logic explicit extraction: `no`; F1=1.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
no
```

NL explicit extraction: ``; F1=0.000; tag_found=0.000

NL generation:

```text
<think>
<premises>
aikido is a martial art.
aikido is a Japanese martial art.
aikido is a martial art that is practiced worldwide.
aikido is a martial art that is practiced in the United States.
aikido is a martial art that is practiced in the United Kingdom.
aikido is a martial art that is practiced in Canada.
aikido is a martial art that is practiced in Australia.
aikido is a martial art that is practiced in New Zealand.
aikido is a martial art that is practiced in South Africa.
aikido is a martial art that is practiced in India.
aikido is a martial art that is practiced in Pakistan.
aikido is a martial art that is practiced in Bangladesh.
aikido is a martial art that is practiced in Sri L
...[truncated]...
at is practiced in Australia.
aikido is a martial art that is practiced in New Zealand.
aikido is a martial art that is practiced in South Africa.
aikido is a martial art that is practiced in India.
aikido is a martial art that is practiced in Pakistan.
aikido is a martial art that is practiced in Bangladesh.
aikido is a martial art that is practiced in Sri Lanka.
aikido is a martial art that is practiced in Nepal.
aikido is a martial art that is practiced in Bhutan.
aikido is a martial art that is practiced in the Maldives.
aikido is a martial art that is practiced in the Philippines.
aikido is a martial art that is practiced in Thailand.
aikido is a martial art that is practiced in Vietnam
```

### doc_id 11

Question: Question: Who is the paternal grandmother of Marie Of Brabant, Queen Of France?

Gold: Marie of Hohenstaufen

Logic explicit extraction: `Henry III, Duke of Brabant`; F1=0.250; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Henry III, Duke of Brabant
```

NL explicit extraction: `Marie of Brabant`; F1=0.667; tag_found=1.000

NL generation:

```text
<answer>
Marie of Brabant
```

### doc_id 1

Question: Question: Who is Sobe (Sister Of Saint Anne)'s grandchild?

Gold: John the Baptist

Logic explicit extraction: `Elizabeth`; F1=0.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Elizabeth
```

NL explicit extraction: `Elizabeth`; F1=0.000; tag_found=1.000

NL generation:

```text
<answer>
Elizabeth
```

### doc_id 0

Question: Question: Where was the wife of Francis I Rákóczi born?

Gold: Ozalj

Logic explicit extraction: `Ozalj`; F1=1.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Ozalj
```

NL explicit extraction: `Ozalj`; F1=1.000; tag_found=1.000

NL generation:

```text
<answer>
Ozalj
```

## musique

### doc_id 0

Question: Question: Who plays the wife of the producer of Here Comes the Boom in Grown Ups?

Gold: Maria Bello

Logic explicit extraction: `Maria Bello`; F1=1.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Maria Bello
```

NL explicit extraction: ``; F1=0.000; tag_found=0.000

NL generation:

```text
<think>
<premises>
aikido is a martial art.
aikido is a Japanese martial art.
aikido is a martial art that is practiced by people of all ages.
aikido is a martial art that is practiced by people of all genders.
aikido is a martial art that is practiced by people of all nationalities.
aikido is a martial art that is practiced by people of all religions.
aikido is a martial art that is practiced by people of all socioeconomic statuses.
aikido is a martial art that is practiced by people of all physical abilities.
aikido is a martial art that is practiced by people of all levels of experience.
aikido is a martial art that is practiced by people of all levels of fitness.
aikido is a martial art
...[truncated]...
eople of all levels of patience.
aikido is a martial art that is practiced by people of all levels of perseverance.
aikido is a martial art that is practiced by people of all levels of courage.
aikido is a martial art that is practiced by people of all levels of confidence.
aikido is a martial art that is practiced by people of all levels of self-esteem.
aikido is a martial art that is practiced by people of all levels of self-awareness.
aikido is a martial art that is practiced by people of all levels of self-control.
aikido is a martial art that is practiced by people of all levels of self-discipline.
aikido is a martial art that is practiced by people of all levels of self-motivation.
aik
```

### doc_id 13

Question: Question: Who is the spouse of the person who voices Jarvis in Iron Man?

Gold: Jennifer Connelly

Logic explicit extraction: `Elizabeth Olsen`; F1=0.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Elizabeth Olsen
```

NL explicit extraction: `a beautiful mind is the original soundtrack album on the decca records label of the 2001 film a beautiful mind starring russell crowe, jennifer connelly (who won the academy award for best supporting actress for her role as "alicia nash"), christopher plummer and paul bettany. the original score and songs were composed and conducted by james horner. the album garnered nominations for the golden globe award for best original score and the academy award for best original score. music critics felt that the musical`; F1=0.053; tag_found=1.000

NL generation:

```text
<think>
<premises>
a beautiful mind is the original soundtrack album on the decca records label of the 2001 film a beautiful mind starring russell crowe, jennifer connelly (who won the academy award for best supporting actress for her role as "alicia nash"), christopher plummer and paul bettany.
the original score and songs were composed and conducted by james horner.
the album garnered nominations for the golden globe award for best original score and the academy award for best original score. music critics felt that the musical score fit the film well, but believed it to be similar to several of horner's previous films.
</premises>
<proof>
a beautiful mind is the original soundtrack album
...[truncated]...
award for best original score. music critics felt that the musical score fit the film well, but believed it to be similar to several of horner's previous films.
</conclusion>
<answer>
a beautiful mind is the original soundtrack album on the decca records label of the 2001 film a beautiful mind starring russell crowe, jennifer connelly (who won the academy award for best supporting actress for her role as "alicia nash"), christopher plummer and paul bettany.
the original score and songs were composed and conducted by james horner.
the album garnered nominations for the golden globe award for best original score and the academy award for best original score. music critics felt that the musical
```

### doc_id 1

Question: Question: What was the person who provided evidence to suggest the existence of the neutron a participant of?

Gold: Manhattan Project

Logic explicit extraction: `Cavendish Laboratory`; F1=0.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Cavendish Laboratory
```

NL explicit extraction: `Chadwick`; F1=0.000; tag_found=1.000

NL generation:

```text
<answer>
Chadwick
```

### doc_id 2

Question: Question: In which borough was Callum McManaman born?

Gold: Knowsley, Metropolitan Borough of Knowsley

Logic explicit extraction: `Whiston`; F1=0.000; tag_found=1.000

Logic generation:

```text
<formal>
<answer>
Whiston
```

NL explicit extraction: `Whiston`; F1=0.000; tag_found=1.000

NL generation:

```text
<answer>
Whiston
```

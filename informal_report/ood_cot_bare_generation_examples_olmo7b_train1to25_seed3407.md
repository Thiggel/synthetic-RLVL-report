# Bare-Format OOD Generation Examples

## gsm8k doc_id 3

Question: James decides to run 3 sprints 3 times a week. He runs 60 meters each sprint. How many total meters does he run a week?

Gold: 540

Logic extracted: ``; metric=0.000

```text
<formal>
<constants>
a = 3
b = 60
</constants>
<predicates>
Ax: x is a sprint
Bx: x is a week
Cx: x is a meter
Dx: x is a run
Ex: x is a time
Fx: x is a distance
Gx: x is a number
Hx: x is a total
Ix: x is a run time
Jx: x is a sprint time
Kx: x is a sprint
Lx: x is a week time
Mx: x is a distance run
Nx: x is a sprint distance
Ox: x is a run distance
Px: x is a sprint distance run
Qx: x is a run distance run
Rx: x is a sprint distance run
Sx: x
...[truncated]...
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
Ja
Ka
La
Ma
```

NL extracted: `540`; metric=1.000

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
James runs 540 meters a week.
</conclusion>
</think>
<answer>
540
```

## hotpotqa doc_id 0

Question: Question: Which case was brought to court first Miller v. California or Gates v. Collier ?

Gold: Miller v. California

Logic extracted: `Gates v. Collier`; metric=0.333

```text
<answer>
Gates v. Collier
```

NL extracted: ``; metric=0.000

```text
<think>
<premises>
austrian supplier Gasser and Italian distributor MISAT entered into a contract together for the supply of children's clothes. In the contract, they included a choice-of-court agreement, stipulating that an Austrian court have jurisdiction in case of conflict. However, when a dispute arose between the two parties, MISAT seised an Italian court to declare that the contract had been terminated, contrary to the choice-of-court clau
...[truncated]...
ending the choice-of-court agreement experience substantive disadvantages in the other Member State, as the court situated there might declare the agreement invalid, the party may also be exposed to procedural disadvantages, caused by judicial system which is not chosen.: 573  This in turn can make the jurisdiction agreement ineffective altogether, going against the principle of party autonomy. Taking a formalistic and literal approach, the Court
```

## 2wikimqa doc_id 0

Question: Question: Where was the wife of Francis I Rákóczi born?

Gold: Ozalj

Logic extracted: `Ozalj`; metric=1.000

```text
<answer>
Ozalj
```

NL extracted: `Ozalj`; metric=1.000

```text
<answer>
Ozalj
```

## musique doc_id 0

Question: Question: Who plays the wife of the producer of Here Comes the Boom in Grown Ups?

Gold: Maria Bello

Logic extracted: `Maria Bello`; metric=1.000

```text
<answer>
Maria Bello
```

NL extracted: ``; metric=0.000

```text
<think>
<premises>
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aiki
...[truncated]...
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
aikido
a
```

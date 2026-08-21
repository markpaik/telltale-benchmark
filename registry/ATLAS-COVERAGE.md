# Atlas coverage audit

Checked 433 figure names from the Silva Rhetoricae index against the `atlas.*` registry family (69 entries).

Audited 2026-08-21 against registry v4, content hash `c11d41efebf3`. Maintained by hand: an atlas entry added or renamed should be reflected here in the same commit.

| verdict | names | share |
| --- | --- | --- |
| in-atlas | 121 | 28% |
| deferred-semantic | 182 | 42% |
| not-measurable | 130 | 30% |

The three verdicts mean different things and only one of them is a gap. **in-atlas** is
measured today. **deferred-semantic** is a figure worth measuring that no regex or
statistic can isolate without a reader deciding what a passage means — metaphor, irony,
understatement; a pattern for one of these would be a pattern for its most obvious
special case, and would report that special case as the figure. **not-measurable** is
different again: nothing is being given up, because the figure has no countable surface
in this corpus at all — a metrical elision, a unit of clause length, a move that spans a
whole argument.

Many Silva names are synonyms of one another (antistrophe and epistrophe, commutatio and
antimetabole), and several atlas entries therefore answer to more than one name. The
atlas is also wider than this list on one side: the metadiscourse entries come from
Hyland's interpersonal model, which is not a figure taxonomy at all.

Sources checked, for names and coverage only — every definition, pattern, and
example in the registry is original:

- Silva Rhetoricae, *Flowers* index (Brigham Young University), <http://rhetoric.byu.edu/Figures/flowers.htm>, fetched 2026-08-21.
- Hyland's interpersonal model of metadiscourse as tabulated in an open-access review: *English Language Teaching* 3(4), December 2010, ERIC EJ1081977, <https://files.eric.ed.gov/fulltext/EJ1081977.pdf>. Ten categories: transitions, frame markers, endophoric markers, evidentials, code glosses (interactive); hedges, boosters, attitude markers, self-mention, engagement markers (interactional). All ten are measured.

## What the atlas holds

| category | entries |
| --- | --- |
| lexical | 26 |
| punctuation | 5 |
| statistical | 1 |
| structural | 2 |
| syntactic | 35 |
| **total** | **69** |

By detection method: 53 regex, 16 statistic. No judge entries: the atlas is deterministic, so adding it to a run costs nothing but CPU.

## Where coverage is partial

Five entries measure part of a figure and are named here so nobody reads them as the
whole of it. `atlas.antimetabole` catches chiasmus only when the words themselves return
(A B ... B A); grammatical chiasmus without word repetition is deferred.
`atlas.isocolon` measures length parallelism and not grammatical parallelism, so it
reads high. `atlas.assonance` and `atlas.homoioteleuton` are orthographic approximations
of phonetic figures — spelling stands in for sound, which mismatches in both directions.
`atlas.interrogative` counts every question, rhetorical or not; only the stock forms are
separated out, in `atlas.rhetorical-question-stock`. `atlas.epimone` counts repeated
trigrams, which catches a refrain and also catches ordinary terminology.

## Atlas entries with no Silva counterpart

These are measured but do not answer to a classical name — the metadiscourse categories,
the two markdown-shaped structural figures, and a few surface counts kept for profiling.

- `atlas.anaphora-paragraph` — anaphora (paragraph level)
- `atlas.bullet-anaphora` — bullet-list anaphora
- `atlas.colon-rate` — colon
- `atlas.md-attitude` — metadiscourse: attitude markers
- `atlas.md-boosters` — metadiscourse: boosters
- `atlas.md-code-glosses` — metadiscourse: code glosses
- `atlas.md-endophoric` — metadiscourse: endophoric markers
- `atlas.md-engagement-directives` — metadiscourse: engagement directives
- `atlas.md-engagement-pronoun` — metadiscourse: reader pronouns
- `atlas.md-evidentials` — metadiscourse: evidentials
- `atlas.md-frame-goal` — metadiscourse: goal announcers
- `atlas.md-hedges` — metadiscourse: hedges
- `atlas.md-self-mention` — metadiscourse: self mention
- `atlas.md-transitions-additive` — metadiscourse: additive transitions
- `atlas.md-transitions-consequential` — metadiscourse: consequential transitions
- `atlas.md-transitions-contrastive` — metadiscourse: contrastive transitions
- `atlas.sentence-initial-conjunction` — sentence-initial conjunction

## Full verdict table

| figure (Silva name) | verdict | atlas id / reason |
| --- | --- | --- |
| abating | not-measurable | operates over a whole passage or argument; there is no span to count |
| abbaser | not-measurable | operates over a whole passage or argument; there is no span to count |
| abcisio | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| abecedarian | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| ablatio | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| abode | not-measurable | operates over a whole passage or argument; there is no span to count |
| abominatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| abuse | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| abusio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| abusion | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| accismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| accumulatio | in-atlas | `atlas.congeries` |
| accusatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| accusatio adversa | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| acervatio | in-atlas | `atlas.congeries` |
| acoloutha | not-measurable | operates over a whole passage or argument; there is no span to count |
| acrostic | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| acyrologia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| acyron | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| adage | in-atlas | `atlas.proverb-frame` |
| adagium | in-atlas | `atlas.proverb-frame` |
| addubitatio | in-atlas | `atlas.aporia` |
| adhortatio | in-atlas | `atlas.adhortatio` |
| adianoeta | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| adjectio | not-measurable | a unit of clause length rather than a device |
| adjournment | not-measurable | operates over a whole passage or argument; there is no span to count |
| adjudicatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| adjunct | not-measurable | a unit of clause length rather than a device |
| adjunctio | not-measurable | a unit of clause length rather than a device |
| admonitio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| adnexio | not-measurable | a unit of clause length rather than a device |
| adnominatio | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| adynata | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| adynaton | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| aeschrologia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| aetiologia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| affirmatio | not-measurable | operates over a whole passage or argument; there is no span to count |
| affirmation | not-measurable | operates over a whole passage or argument; there is no span to count |
| aganactesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| agnominatio | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| agnomination | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| aischrologia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| allegory | deferred-semantic | sustained across a whole text |
| alleotheta | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| alliteration | in-atlas | `atlas.alliteration` |
| amara irrisio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| ambage | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| ambiguitas | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| ambiguous | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| amphibologia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| ampliatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| anacephalaeosis | in-atlas | `atlas.md-frame-sequencers` |
| anacoenosis | in-atlas | `atlas.deliberative-question` |
| anacoloutha | not-measurable | operates over a whole passage or argument; there is no span to count |
| anacoluthon | deferred-semantic | an abandoned construction; needs a parse to see the break |
| anadiplosis | in-atlas | `atlas.anadiplosis` |
| anamnesis | not-measurable | operates over a whole passage or argument; there is no span to count |
| anangeon | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| anaphora | in-atlas | `atlas.anaphora` |
| anapodoton | not-measurable | operates over a whole passage or argument; there is no span to count |
| anastrophe | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| anemographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| anesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| antanaclasis | deferred-semantic | the same word in two senses; the senses are the figure |
| antanagoge | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| antenantiosis | in-atlas | `atlas.litotes` |
| anthimeria | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| anthropopatheia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| anthypophora | in-atlas | `atlas.hypophora-frame` |
| anticategoria | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| anticipation | in-atlas | `atlas.procatalepsis` |
| antilogy | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| antimetabole | in-atlas | `atlas.antimetabole` |
| antimetathesis | in-atlas | `atlas.antimetabole` |
| antipersonification | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| antiphrasis | in-atlas | `atlas.irony-marker` |
| antiprosopopoeia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| antiptosis | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| antirrhesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| antisagoge | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| antistasis | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| antisthecon | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| antistrophe | in-atlas | `atlas.epistrophe` |
| antithesis | in-atlas | `atlas.antithesis-frame` |
| antitheton | in-atlas | `atlas.antithesis-frame` |
| antonomasia | deferred-semantic | an epithet standing in for a name |
| apagoresis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| aphaeresis | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| aphorismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| apocarteresis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| apocope | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| apodioxis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| apodixis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| apologue | not-measurable | operates over a whole passage or argument; there is no span to count |
| apophasis | in-atlas | `atlas.praeteritio` |
| apoplanesis | not-measurable | operates over a whole passage or argument; there is no span to count |
| aporia | in-atlas | `atlas.aporia` |
| aposiopesis | in-atlas | `atlas.aposiopesis` |
| apostrophe | deferred-semantic | address to someone absent; needs the referent |
| apothegm | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| apparent refusal | in-atlas | `atlas.praeteritio` |
| appositio | in-atlas | `atlas.appositive` |
| apposition | in-atlas | `atlas.appositive` |
| ara | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| articulus | in-atlas | `atlas.congeries` |
| aschematismus | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| aschematiston | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| asphalia | in-atlas | `atlas.emphatic-negation` |
| assonance | in-atlas | `atlas.assonance` |
| assumptio | not-measurable | operates over a whole passage or argument; there is no span to count |
| assumption | not-measurable | operates over a whole passage or argument; there is no span to count |
| asteismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| astrothesia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| asyndeton | in-atlas | `atlas.asyndeton` |
| auxesis | in-atlas | `atlas.superlative` |
| avancer | not-measurable | operates over a whole passage or argument; there is no span to count |
| aversio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| barbarism | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| battologia | in-atlas | `atlas.epizeuxis` |
| bdelygmia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| benedictio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| bomphiologia | in-atlas | `atlas.hyperbole-marker` |
| brachiepia | in-atlas | `atlas.asyndeton` |
| brachylogia | in-atlas | `atlas.asyndeton` |
| broad floute | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| cacemphaton | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| cacophonia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| cacosyntheton | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| cacozelia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| casus pro casu | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| catachresis | deferred-semantic | a misapplied word; the misapplication is semantic |
| catacosmesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| cataphasis | in-atlas | `atlas.praeteritio` |
| cataplexis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| categoria | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| cause shown | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| change of name | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| characterismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| charientismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| chiasmus | in-atlas | `atlas.antimetabole` |
| chorographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| chreia | in-atlas | `atlas.exemplum-frame` |
| chronographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| circumlocutio | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| civille jest | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| clause | not-measurable | a unit of clause length rather than a device |
| climax | deferred-semantic | escalation, which is a judgement about weight |
| coenotes | in-atlas | `atlas.ploce-intensive` |
| colon | not-measurable | a unit of clause length rather than a device |
| combined repetition | in-atlas | `atlas.symploce` |
| comma | not-measurable | a unit of clause length rather than a device |
| common cause | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| commoratio | in-atlas | `atlas.epimone` |
| communicatio | in-atlas | `atlas.deliberative-question` |
| commutatio | in-atlas | `atlas.antimetabole` |
| comparatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| compensatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| complexio | in-atlas | `atlas.symploce` |
| compositum ex contrariis | in-atlas | `atlas.antithesis-frame` |
| comprobatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| conceit | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| concessio | in-atlas | `atlas.paromologia` |
| conciliatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| conclusio | not-measurable | operates over a whole passage or argument; there is no span to count |
| condescensio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| condescension | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| conduplicatio | deferred-semantic | a key word carried across clauses; the key is the point |
| congeries | in-atlas | `atlas.congeries` |
| conjunctio | not-measurable | a unit of clause length rather than a device |
| consonance | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| contencion | in-atlas | `atlas.antithesis-frame` |
| contentio | in-atlas | `atlas.antithesis-frame` |
| continued metaphor | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| contractio | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| contrarium | in-atlas | `atlas.antithesis-frame` |
| contrast | in-atlas | `atlas.antithesis-frame` |
| conversio | in-atlas | `atlas.epistrophe` |
| correctio | in-atlas | `atlas.correctio` |
| counter turne | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| counterchange | in-atlas | `atlas.antimetabole` |
| counterfait in personation | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| counterfait place | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| counterfeit time | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| cutted comma | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| cutting from the end | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| deesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| dehortatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| dendrographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| deprecatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| descriptio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| diacope | in-atlas | `atlas.diacope` |
| diaeresis | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| dialogismus | in-atlas | `atlas.quotation` |
| dialysis | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| dialyton | in-atlas | `atlas.asyndeton` |
| dianoea | not-measurable | operates over a whole passage or argument; there is no span to count |
| diaphora | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| diaporesis | in-atlas | `atlas.aporia` |
| diaskeue | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| diastole | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| diasyrmus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| diazeugma | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| dicaeologia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| digressio | not-measurable | operates over a whole passage or argument; there is no span to count |
| dilemma | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| dirimens copulatio | in-atlas | `atlas.not-only-but-also` |
| distinctio | in-atlas | `atlas.distinctio` |
| distributio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| doubtfull | in-atlas | `atlas.aporia` |
| ecphonesis | in-atlas | `atlas.exclamation` |
| ecphrasis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| ecthlipsis | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| effictio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| elenchus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| ellipsis | deferred-semantic | grammatical omission; what is missing cannot be matched |
| emphasis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| enallage | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| enantiosis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| enargia | deferred-semantic | as hypotyposis |
| encomium | not-measurable | operates over a whole passage or argument; there is no span to count |
| energia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| enigma | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| ennoia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| enthymeme | deferred-semantic | a suppressed premise; nothing on the surface marks it |
| enumeratio | in-atlas | `atlas.numbered-preview` |
| epanalepsis | in-atlas | `atlas.epanalepsis` |
| epanodos | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| epanorthosis | in-atlas | `atlas.correctio` |
| epenthesis | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| epergesis | in-atlas | `atlas.appositive` |
| epexegesis | in-atlas | `atlas.appositive` |
| epicrisis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| epilogus | not-measurable | operates over a whole passage or argument; there is no span to count |
| epimone | in-atlas | `atlas.epimone` |
| epiphonema | not-measurable | operates over a whole passage or argument; there is no span to count |
| epiplexis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| epistrophe | in-atlas | `atlas.epistrophe` |
| episynaloephe | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| epitasis | not-measurable | operates over a whole passage or argument; there is no span to count |
| epitheton | deferred-semantic | as epithet |
| epitrochasmus | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| epitrope | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| epizeugma | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| epizeuxis | in-atlas | `atlas.epizeuxis` |
| erotema | in-atlas | `atlas.interrogative` |
| ethopoeia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| eucharistia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| euche | in-atlas | `atlas.optatio` |
| eulogia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| euphemismus | deferred-semantic | a softened substitution the reader has to recognize as one |
| eustathia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| eutrepismus | in-atlas | `atlas.numbered-preview` |
| example | in-atlas | `atlas.exemplum-frame` |
| excitatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| exclamatio | in-atlas | `atlas.exclamation` |
| excursus | not-measurable | operates over a whole passage or argument; there is no span to count |
| exergasia | not-measurable | operates over a whole passage or argument; there is no span to count |
| exouthenismos | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| expeditio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| expolitio | not-measurable | operates over a whole passage or argument; there is no span to count |
| exuscitatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| frequentatio | in-atlas | `atlas.congeries` |
| geographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| gnome | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| graecismus | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| hendiadys | deferred-semantic | one idea split across two coordinated nouns; coordination alone does not distinguish it from a list |
| heterogenium | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| homiologia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| homoeoprophoron | in-atlas | `atlas.alliteration` |
| homoeosis | in-atlas | `atlas.simile-marker` |
| homoioptoton | in-atlas | `atlas.homoioteleuton` |
| homoioteleuton | in-atlas | `atlas.homoioteleuton` |
| horismus | in-atlas | `atlas.distinctio` |
| hydrographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| hypallage | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| hyperbaton | deferred-semantic | needs a syntactic parse to call the order marked |
| hyperbole | in-atlas | `atlas.hyperbole-marker` |
| hypophora | in-atlas | `atlas.hypophora` |
| hypotyposis | deferred-semantic | vivid description; the vividness is the figure |
| hypozeugma | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| hypozeuxis | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| hysterologia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| hysteron proteron | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| icon | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| indignatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| inopinaturm | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| insinuatio | not-measurable | operates over a whole passage or argument; there is no span to count |
| inter se pugnantia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| interrogatio | in-atlas | `atlas.interrogative` |
| intimation | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| irony | deferred-semantic | meaning inverted against the words; the words look ordinary |
| isocolon | in-atlas | `atlas.isocolon` |
| litotes | in-atlas | `atlas.litotes` |
| macrologia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| martyria | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| maxim | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| medela | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| meiosis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| membrum | not-measurable | a unit of clause length rather than a device |
| mempsis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| merismus | in-atlas | `atlas.merism` |
| mesarchia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| mesodiplosis | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| mesozeugma | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| metabasis | in-atlas | `atlas.md-frame-topic-shift` |
| metalepsis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| metallage | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| metaphor | deferred-semantic | the figure is the transfer of sense, not a word |
| metaplasm | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| metastasis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| metathesis | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| metonymy | deferred-semantic | as metaphor |
| mimesis | in-atlas | `atlas.quotation` |
| mycterismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| noema | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| oeonismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| ominatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| onedismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| onomatopoeia | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| optatio | in-atlas | `atlas.optatio` |
| orcos | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| oxymoron | deferred-semantic | a contradiction between two senses |
| paenismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| palilogia | in-atlas | `atlas.diacope` |
| parabola | in-atlas | `atlas.simile-marker` |
| paradiastole | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| paradiegesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| paradigma | in-atlas | `atlas.exemplum-frame` |
| paradox | deferred-semantic | a contradiction across a whole claim |
| paraenesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| paragoge | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| paralipsis | in-atlas | `atlas.praeteritio` |
| parallelism | in-atlas | `atlas.isocolon` |
| paramythia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| parathesis | not-measurable | a unit of clause length rather than a device |
| parecbasis | not-measurable | operates over a whole passage or argument; there is no span to count |
| paregmenon | deferred-semantic | needs stemming, like polyptoton |
| parelcon | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| parembole | in-atlas | `atlas.parenthesis` |
| parenthesis | in-atlas | `atlas.parenthesis` |
| pareuresis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| paroemia | in-atlas | `atlas.proverb-frame` |
| paroemion | in-atlas | `atlas.alliteration` |
| paromoiosis | in-atlas | `atlas.isocolon` |
| paromologia | in-atlas | `atlas.paromologia` |
| paronomasia | deferred-semantic | a pun is a sound coincidence the reader has to hear |
| parrhesia | in-atlas | `atlas.parrhesia` |
| pathopoeia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| perclusio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| periergia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| period | not-measurable | a unit of clause length rather than a device |
| periphrasis | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| perissologia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| peristasis | not-measurable | operates over a whole passage or argument; there is no span to count |
| permutatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| personification | deferred-semantic | attribution of a human trait; the trait is semantic |
| philophronesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| pleonasm | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| ploce | in-atlas | `atlas.ploce-intensive` |
| polyptoton | deferred-semantic | needs stemming: one root in two forms is not a repeated string |
| polysyndeton | in-atlas | `atlas.polysyndeton` |
| pragmatographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| procatalepsis | in-atlas | `atlas.procatalepsis` |
| proclees | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| prodiorthosis | not-measurable | operates over a whole passage or argument; there is no span to count |
| proecthesis | not-measurable | operates over a whole passage or argument; there is no span to count |
| prolepsis | in-atlas | `atlas.procatalepsis` |
| prosapodosis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| proslepsis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| prosonomasia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| prosopographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| prosopopoeia | deferred-semantic | as personification |
| prosphonesis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| protherapeia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| prothesis | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| protrope | in-atlas | `atlas.adhortatio` |
| proverb | in-atlas | `atlas.proverb-frame` |
| prozeugma | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| pysma | in-atlas | `atlas.pysma` |
| ratiocinatio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| repetitio | in-atlas | `atlas.epimone` |
| repotia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| restrictio | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| rhetorical question | in-atlas | `atlas.rhetorical-question-stock` |
| sarcasmus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| scesis onomaton | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| schematismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| scheme | not-measurable | a unit of clause length rather than a device |
| scurra | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| sententia | deferred-semantic | an aphorism has no marker, only a shape a reader recognizes |
| sermocinatio | deferred-semantic | invented speech; quotation marks do not say who spoke |
| simile | in-atlas | `atlas.simile-marker` |
| skotison | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| solecismus | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| soraismus | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| sorites | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| subjectio | in-atlas | `atlas.hypophora-frame` |
| sustentatio | not-measurable | operates over a whole passage or argument; there is no span to count |
| syllepsis | deferred-semantic | one governing word across mismatched objects; needs a parse |
| syllogismus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| symperasma | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| symploce | in-atlas | `atlas.symploce` |
| synaeresis | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| synaloepha | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| synathroesmus | in-atlas | `atlas.congeries` |
| syncatabasis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| syncategorema | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| synchoresis | in-atlas | `atlas.paromologia` |
| synchysis | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| syncope | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| syncrisis | in-atlas | `atlas.antithesis-frame` |
| synecdoche | deferred-semantic | as metaphor |
| synoeciosis | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| synonymia | deferred-semantic | near-synonyms in series; needs a thesaurus and a judgement |
| synthesis | not-measurable | a unit of clause length rather than a device |
| syntheton | not-measurable | a unit of clause length rather than a device |
| synzeugma | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| systole | not-measurable | sound-change figure: alters a word's form for meter; no occurrence in modern prose that is not a typo |
| systrophe | not-measurable | operates over a whole passage or argument; there is no span to count |
| tapinosis | deferred-semantic | belittling by word choice; needs the referent |
| tasis | not-measurable | a unit of clause length rather than a device |
| tautologia | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| taxis | not-measurable | a unit of clause length rather than a device |
| thaumasmus | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| tmesis | deferred-semantic | word split by an insertion; vanishingly rare outside verse |
| topographia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| topothesia | deferred-semantic | needs a reader's judgement of meaning, intent, or tone; no surface form to count |
| traductio | in-atlas | `atlas.diacope` |
| transitio | in-atlas | `atlas.md-frame-topic-shift` |
| transplacement | in-atlas | `atlas.diacope` |
| tricolon | in-atlas | `atlas.tricolon-series` |
| verborum bombus | not-measurable | needs a syntactic parse; word order alone does not isolate it |
| zeugma | deferred-semantic | as syllepsis |

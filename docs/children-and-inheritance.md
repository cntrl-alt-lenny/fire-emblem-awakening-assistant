# Children and inheritance

Sources: `inheritance`, `inheritance_1`, `character_growths`, `class_sets`, `recruitment`. This document contains future-system spoilers.

Child personal growth = floor((mother personal growth + father personal growth + child absolute growth)/3). Add the child's current class growth to obtain actual growth; Aptitude is an equipped skill bonus, not part of parental personal growth. `inheritance.py child` calculates growths and caps only from two supplied, resolved parents.

Child cap modifiers = mother modifier + father modifier +1 in each non-HP stat. If Robin marries a child-generation character, Morgan omits the extra+1. Asset/flaw-dependent Robin values must be resolved first. HP is not part of ordinary inherited cap modifiers.

Recruitment bases depend on normalized parent current stats and absolute child bases. Absolute bases in `characters.json` are **not actual recruited stats**. Recruitment autolevel treatment, parent equipment normalization and exact rounding across those operations remain insufficiently audited, so no recruitment-stat calculator is provided. Use actual recruited stats.

Children inherit class access with gender substitutions and exceptions. Source replacement table includes: Vaike daughters Fighter/Barbarian→Knight/Mercenary; Gaius Fighter→Pegasus Knight; Donnel daughters Villager/Fighter→Pegasus Knight/Troubadour; Gregor/Henry Barbarian→Troubadour. Lissa sons Pegasus Knight/Troubadour→Myrmidon/Barbarian; Miriel Troubadour→Barbarian; Maribelle Pegasus Knight/Troubadour→Cavalier/Priest; Olivia Dancer/Pegasus Knight→Mercenary/Barbarian; Panne Wyvern Rider→Barbarian; Cherche Troubadour→Fighter. Robin has broad gender-compatible ordinary access; unique classes are exceptions. Full legal inherited class-set resolution is not implemented.

Inherited skills normally use the last active equipped slot of each parent upon entering the recruitment map. DLC skills and Special Dance are excluded. Chrom always passes Aether to daughters and Rightful King to sons regardless of current acquisition/equipping. These facts do not mean every starting skill listed for a child is fixed for every parent. Record the actual recruited skill set.

Fixed parents and child paralogue unlock/access conditions are captured in recruitment and retained factual tables. Full father-choice legality, dynamic siblings and Morgan exceptional starting class/inventory need context. Never invent a child's parents from a generic recommendation.

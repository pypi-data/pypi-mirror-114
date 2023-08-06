import random


class Adjective:
    def __init__(self, word, starts_with_vowel_sound = None):
        self.word = word
        self.starts_with_vowel_sound = starts_with_vowel_sound
        if starts_with_vowel_sound == None:
            self.starts_with_vowel_sound = word[0] in "aeiou"


class Noun:
    def __init__(self, word, plural = None):
        self.singular = word
        self.plural = plural
        if plural == None:
            if word[-1] == "s":
                self.plural = word + "es"
            else:
                self.plural = word + "s"


class QuoteGenerator:
    def __init__(self):
        self.intros = [
            "Just biject it to a",
            "Just view the problem as a",
        ]

        self.adjectives = [
            Adjective("abelian"),
            Adjective("associative"),
            Adjective("computable"),
            Adjective("Lebesgue-measurable"),
            Adjective("semi-decidable"),
            Adjective("simple"),
            Adjective("combinatorial"),
            Adjective("structure-preserving"),
            Adjective("diagonalizable"),
            Adjective("nonsingular"),
            Adjective("orientable"),
            Adjective("twice-differentiable"),
            Adjective("thrice-differentiable"),
            Adjective("countable"),
            Adjective("prime"),
            Adjective("complete"),
            Adjective("continuous"),
            Adjective("trivial"),
            Adjective("3-connected"),
            Adjective("bipartite"),
            Adjective("planar"),
            Adjective("finite"),
            Adjective("nondeterministic"),
            Adjective("alternating"),
            Adjective("convex"),
            Adjective("undecidable"),
            Adjective("dihedral"),
            Adjective("context-free"),
            Adjective("rational"),
            Adjective("regular"),
            Adjective("Noetherian"),
            Adjective("Cauchy"),
            Adjective("open"),
            Adjective("closed"),
            Adjective("compact"),
            Adjective("clopen"),
            Adjective("pointless"),
            Adjective("perfect"),
            Adjective("non-degenerate"),
            Adjective("degenerate"),
            Adjective("skew-symmetric"),
            Adjective("sesquilinear"),
            Adjective("fundamental"),
            Adjective("smooth"),
            Adjective("connected"),
            Adjective("simplicial"),
            Adjective("universal", starts_with_vowel_sound = False),
            Adjective("greedy"),
            Adjective("normal"),
            Adjective("total"),
            Adjective("left invertible"),
            Adjective("exact"),
            Adjective("empty"),
        ]

        self.set_nouns = [
            Noun("multiset"),
            Noun("metric space"),
            Noun("group"),
            Noun("monoid"),
            Noun("semigroup"),
            Noun("ring"),
            Noun("field"),
            Noun("module"),
            Noun("topological space"),
            Noun("Hilbert space"),
            Noun("manifold"),
            Noun("hypergraph"),
            Noun("DAG"),
            Noun("residue class"),
            Noun("logistic system"),
            Noun("complexity class"),
            Noun("language"),
            Noun("poset"),
            Noun("algebra"),
            Noun("Lie algebra"),
            Noun("Dynkin system"),
            Noun("sigma-algebra"),
            Noun("ultrafilter"),
            Noun("Cayley graph"),
            Noun("variety", plural = "varieties"),
            Noun("orbit"),
        ]

        self.all_nouns = self.set_nouns + [
            # Mathematical objects that can't contain elements (unless you're a
            # set theorist).
            Noun("integer"),
            Noun("Turing machine"),
            Noun("automorphism"),
            Noun("bijection"),
            Noun("generating function"),
            Noun("taylor series", plural = "taylor series"),
            Noun("linear transformation"),
            Noun("pushdown automaton", plural = "pushdown automata"),
            Noun("combinatorial game"),
            Noun("equivalence relation"),
            Noun("tournament"),
            Noun("random variable"),
            Noun("triangulation"),
            Noun("unbounded-fan-in circuit"),
            Noun("log-space reduction"),
            Noun("Markov chain"),
            Noun("4-form"),
            Noun("7-chain"),
            Noun("operator"),
            Noun("homeomorphism"),
            Noun("color"),
            Noun("Betti number"),
            Noun("Radon-Nikodym derivative"),
        ]

    def create(self):
        first_adjective = random.choice(self.adjectives)
        intro_suffix = "n" if first_adjective.starts_with_vowel_sound else ""

        output = []
        
        output.append("The proof is trivial! " + random.choice(self.intros) + intro_suffix)
        output.append(first_adjective.word)
        output.append(random.choice(self.set_nouns).singular)
        output.append("whose elements are")
        output.append(random.choice(self.adjectives).word)
        output.append(random.choice(self.all_nouns).plural)

        return output
